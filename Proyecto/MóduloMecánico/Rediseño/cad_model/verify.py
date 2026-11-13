import math
from collections import Counter
from itertools import combinations

from .geometry import V, box, cylinder
from .model import door_position

BOX_EPS = 1e-5
VOLUME_EPS = 0.05


def boxes_overlap(a, b):
    return all((
        min(a.xmax, b.xmax) - max(a.xmin, b.xmin) > BOX_EPS,
        min(a.ymax, b.ymax) - max(a.ymin, b.ymin) > BOX_EPS,
        min(a.zmax, b.zmax) - max(a.zmin, b.zmin) > BOX_EPS,
    ))


def positive_overlap(a, b):
    if not boxes_overlap(a.BoundingBox(), b.BoundingBox()):
        return 0.0
    return sum(abs(solid.Volume()) for solid in a.intersect(b).Solids())


def part_errors(items):
    errors = []
    for item in items:
        solids = item.shape.Solids()
        if not item.shape.isValid() or (item.method in ("FDM", "laser") and len(solids) != 1):
            errors.append(item.key)
    return errors


def check_pairs(pairs):
    collisions, issues = [], []
    bounds = {}
    for first, second in pairs:
        try:
            for item in (first, second):
                if item.key not in bounds:
                    bounds[item.key] = item.shape.BoundingBox()
            if not boxes_overlap(bounds[first.key], bounds[second.key]):
                continue
            volume = sum(abs(solid.Volume()) for solid in first.shape.intersect(second.shape).Solids())
            if volume > VOLUME_EPS:
                collisions.append({"a": first.key, "b": second.key, "mm3": round(volume, 4)})
        except (RuntimeError, ValueError) as exc:
            issues.append({"a": first.key, "b": second.key, "error": str(exc)})
    return collisions, issues


def check_plate(p, open_items, scale_height):
    radius = p.dish_diameter / 2
    z = p.panel + scale_height + p.carrier_thickness
    height, destination = p.dish_rim_height, p.center_y
    approach = -radius - 35
    start = cylinder(radius, height, (0, approach, z))
    finish = cylinder(radius, height, (0, destination, z))
    bridge = box(-radius, approach, z, radius, destination, z + height)
    swept = start.fuse(bridge, finish).clean()
    conflicts = []
    for item in open_items:
        if item.shape.Solids():
            volume = positive_overlap(swept, item.shape)
            if volume > VOLUME_EPS:
                conflicts.append({"pieza": item.key, "mm3": round(volume, 4)})
    return {
        "diametro_plato_mm": p.dish_diameter,
        "altura_envolvente_mm": height,
        "z_superficie_portante_mm": round(z, 2),
        "holgura_por_lado_vano_mm": round((p.aperture - p.dish_diameter) / 2, 2),
        "holgura_fondo_interior_mm": round(p.inside_rear - destination - radius, 2),
        "interferencias_barrido": conflicts,
    }


def check_door(p, items):
    angles = sorted({0, 0.5, 1, 2, 5, *range(10, int(p.door_angle), 10), p.door_angle})
    samples = {}
    for angle in angles:
        posed = door_position(items, p, angle, unlocked=True)
        mobile = [item for item in posed if item.door]
        fixed = [item for item in posed if not item.door and item.shape.Solids()]
        clashes, issues = check_pairs((a, b) for a in mobile for b in fixed)
        if clashes or issues:
            samples[str(angle)] = {"interferencias": clashes, "errores": issues}
    return {"angulos_grados": angles, "muestras_con_observaciones": samples}


def check_fasteners(items):
    # Compare the center and axis of each fastener to its nut through the
    # installed geometry. Closed-state B-Rep intersections check panel bores.
    instances = {item.key: item for item in items}
    axes, errors = [], []
    for key, screw in instances.items():
        if not key.endswith("_screw"):
            continue
        nut = instances[key.removesuffix("_screw") + "_nut"]
        cyl = max((f for f in screw.shape.Faces() if f.geomType() == "CYLINDER"), key=lambda face: face.Area())
        surface = cyl._geomAdaptor().Cylinder()
        direction = V(surface.Axis().Direction().XYZ())
        point = V(surface.Location().XYZ())
        radial_error = (nut.shape.Center() - point).cross(direction).Length
        axes.append(radial_error)
        if radial_error > 0.05:
            errors.append(key)
    return {"pares": len(axes), "desalineacion_radial_max_mm": round(max(axes, default=0), 5), "observaciones": errors}


def verify(p, items, open_items):
    solid_items = [item for item in items if item.shape.Solids()]
    clashes, boolean_errors = check_pairs(combinations(solid_items, 2))
    # The OEM threaded insert uses its minor bore in the solid model. The
    # nominal full-diameter screw represents material in the thread engagement.
    thread_contacts = [
        pair for pair in clashes
        if pair["a"] == "E03" and pair["b"].startswith("LCD") and pair["mm3"] <= 1
    ]
    openings = p.optical_hole / 2 - (p.lens_z + p.lens_adjust - p.shelf) * math.tan(math.radians(60))
    carrier = next(item for item in items if item.key == "P10")
    nearest_fixed = [
        carrier.shape.distance(item.shape) for item in solid_items
        if item.key != "P10" and item.system in {"Pesaje", "Carcasa", "Fijaciones"}
    ]
    return {
        "umbral_volumen_mm3": VOLUME_EPS,
        "instancias": len(items),
        "solidos": sum(len(item.shape.Solids()) for item in items),
        "por_metodo": dict(Counter(item.method for item in items)),
        "piezas_brep_invalidas": part_errors(items),
        "interferencias_cerrado": [pair for pair in clashes if pair not in thread_contacts],
        "contactos_nominales_rosca_oled": thread_contacts,
        "fijaciones": check_fasteners(items),
        "errores_booleanos": boolean_errors,
        "puerta": check_door(p, items),
        "plato": check_plate(p, open_items, p.scale_height),
        "plato_con_altura_alternativa_bmh_mm_36_4": check_plate(p, open_items, 36.4),
        "pesaje": {
            "separacion_min_portante_a_geometria_fija_modelada_mm": round(min(nearest_fixed), 4),
            "nota": "Excluye geometría no publicada de base, celda, arnés y placa móvil. La coincidencia de la cara de apoyo es intencional.",
        },
        "optica": {
            "distancia_lente_a_borde_plato_mm": round(p.lens_z-p.dish_z-p.dish_rim_height, 2),
            "holgura_radial_teorica_en_vano_mm": round(openings, 2),
            "nota": "Cono simetrico hipotetico de 120 grados. Faltan intrinsecos, enfoque, refraccion y ensayo de vapor.",
        },
    }

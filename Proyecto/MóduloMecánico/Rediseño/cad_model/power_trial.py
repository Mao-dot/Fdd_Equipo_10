"""Generate the optional P09a test panel with the stock P09 interface."""

import json
from pathlib import Path

import cadquery as cq

from .geometry import ROOT, box, compound, cylinder, orient, translate
from .integration import asset, electronics
from .parameters import Design
from .structure import wood_panels


JACK_X = -17.0
SWITCH_X = 3.0
FUSE_X = 20.5
TRIAL_PATH = ROOT / "commercial" / "auxiliary" / "power" / "P09a_trial"


def panel(p):
    """Cut the published interfaces on the original removable blank."""
    blank = next(item for item in electronics(p) if item.key == "P09")
    thickness = blank.native.BoundingBox().zlen
    if not 1.5 <= thickness <= 3.5:
        raise ValueError("El espesor de P09 queda fuera del rango del conector Tensility")
    jack = cylinder(13.9 / 2, thickness + 0.2, (JACK_X, 0, -0.1)).intersect(
        box(JACK_X - 8, -6.4, -0.1, JACK_X + 8, 6.4, thickness + 0.1)
    )
    # The 25 mm length of the rocker opening runs vertically on P09a.
    switch = box(SWITCH_X - 7.7, -12.5, -0.1, SWITCH_X + 7.7, 12.5, thickness + 0.1)
    fuse = cylinder(13.0 / 2, thickness + 0.2, (FUSE_X, 0, -0.1))
    return blank.native.cut(jack, switch, fuse).clean(), (jack, switch, fuse)


def connector_at_panel(thickness):
    """Orient the OEM solids and seat the separate hardware on the rear."""
    original = asset("auxiliary/power/tensility_54-00406_original.step")
    seating_face = 4.471998
    washer_front = 4.67146
    parts = []
    for solid in original.Solids():
        bounds = solid.BoundingBox()
        # Identify the supplied washer and nut by original file extent.
        if bounds.ylen > 18.0 and 4.6 < bounds.xmin < 7.6:
            solid = translate(solid, x=seating_face + thickness - washer_front)
        parts.append(solid)
    center = (0.27078333, 0.81509262)
    return orient(compound(parts), (JACK_X - center[0], -center[1], -seating_face),
                  (0, 0, 1), (0, 1, 0))


def trial_parts(thickness):
    """Create protected fit volumes for candidates without validated 3D data."""
    # NKK JWMW product drawing B45: flange 30 x 18, body width 15.0,
    # body length 22.6 and depth to terminal 22.2 behind the nominal seating face.
    rocker = box(SWITCH_X - 9.0, -15.0, -7.2, SWITCH_X + 9.0, 15.0, 0)
    rocker = rocker.fuse(box(SWITCH_X - 7.5, -11.3, 0, SWITCH_X + 7.5, 11.3, 22.2)).clean()
    # FPG2 3101.0120 slotted IP67, SW14 nut, Ø11.1 body and 41.5 mm total.
    fuse = cylinder(16.1 / 2, 4, (FUSE_X, 0, -4))
    fuse = fuse.fuse(cylinder(12.5 / 2, 12.9, (FUSE_X, 0, 0)))
    fuse = fuse.fuse(cylinder(11.1 / 2, 24.6, (FUSE_X, 0, 12.9))).clean()
    return {
        "Tensility_54-00406_STEP_OEM": connector_at_panel(thickness),
        "NKK_JWMW11RAA_espacio_de_montaje": rocker,
        "Schurter_FPG2_3101.0120_espacio_de_montaje": fuse,
    }


def export(output=TRIAL_PATH):
    p = Design()
    cut_plate, cutouts = panel(p)
    thickness = cut_plate.BoundingBox().zlen
    assert cut_plate.isValid() and len(cut_plate.Solids()) == 1
    fit_parts = trial_parts(thickness)

    service_center = (106.5, p.depth + thickness, 350.5)
    rear = next(item.shape for item in wood_panels(p) if item.key == "P04")

    def world(shape):
        return orient(shape, service_center, (1, 0, 0), (0, -1, 0))

    clearances = {}
    for label, candidate in fit_parts.items():
        assert candidate.isValid()
        clearances[label] = {
            "interseccion_placa_mm3": round(candidate.intersect(cut_plate).Volume(), 6),
            "interseccion_panel_posterior_mm3": round(world(candidate).intersect(rear).Volume(), 6),
        }
    pairs = list(fit_parts.items())
    overlaps = {
        f"{first_name} / {second_name}": round(first.intersect(second).Volume(), 6)
        for index, (first_name, first) in enumerate(pairs)
        for second_name, second in pairs[index + 1:]
    }
    minimum_cutout_clearance = min(world(shape).distance(rear) for shape in cutouts)
    if max(value for overlaps_by_part in clearances.values() for value in overlaps_by_part.values()) > 0.01:
        raise ValueError(f"Interferencia con panel P09a o P04: {clearances}")
    if max(overlaps.values()) > 0.01:
        raise ValueError(f"Interferencia entre componentes del panel P09a: {overlaps}")

    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    name = "P09a_panel_alimentacion_prueba"
    cq.exporters.export(cut_plate, str(output / f"{name}.step"))
    lower_face = min(cut_plate.Faces(), key=lambda face: face.Center().z)
    cq.exporters.exportDXF(lower_face.Wires(), str(output / f"{name}.dxf"))
    trial = cq.Assembly(cut_plate, name="P09a_referencia_de_ajuste")
    for label, candidate in fit_parts.items():
        trial.add(candidate, name=label)
    trial.export(str(output / "P09a_referencia_de_ajuste.step"))
    report = {
        "unidad": "mm",
        "uso": "Prueba de montaje. Disposición eléctrica y portafusible pendientes de validación física.",
        "interferencias": clearances,
        "interferencias_entre_componentes_mm3": overlaps,
        "distancia_minima_de_corte_a_ventana_P04_mm": round(minimum_cutout_clearance, 3),
        "centros_locales_x": {"conector": JACK_X, "interruptor": SWITCH_X, "portafusible": FUSE_X},
    }
    (output / "P09a_verificacion.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                                                 encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(export(), indent=2, ensure_ascii=False))

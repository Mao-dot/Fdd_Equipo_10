import argparse
import json
import struct
from collections import Counter, defaultdict
from pathlib import Path

import cadquery as cq
import ezdxf

from .geometry import ROOT, translate
from .model import build, door_position, reference_objects, to_assembly
from .parameters import Design
from .verify import verify


def planar_dxf(shape, target):
    faces = [face for face in shape.Faces() if face.geomType() == "PLANE" and face.normalAt().z > 0.99999]
    face = max(faces, key=lambda face: face.Area())
    top = face.Center().z
    wires = [translate(wire, z=-top) for wire in face.Wires()]
    if not all(wire.IsClosed() for wire in wires):
        raise ValueError(f"Hay contornos abiertos en {target.name}")
    cq.exporters.exportDXF(cq.Workplane("XY").newObject(wires), str(target))
    drawing = ezdxf.readfile(target)
    drawing.units = 4
    drawing.saveas(target)
    entities = Counter(entity.dxftype() for entity in drawing.modelspace())
    if not entities or drawing.audit().errors:
        raise ValueError(f"DXF inválido: {target.name}")
    return {"contornos_cerrados_brep": len(wires), "entidades": dict(entities), "unidades": "mm"}


def mesh_stl(shape, target):
    shape.exportStl(str(target), tolerance=0.05, angularTolerance=0.12, ascii=False)
    data = target.read_bytes()
    count = struct.unpack_from("<I", data, 80)[0]
    if not count or len(data) != 84 + 50 * count:
        raise ValueError(f"STL inválido: {target.name}")
    edges = Counter()
    for triangle in struct.iter_unpack("<12fH", memoryview(data)[84:]):
        points = [tuple(round(x, 4) for x in triangle[i:i+3]) for i in (3, 6, 9)]
        for a, b in zip(points, points[1:] + points[:1]):
            edges[tuple(sorted((a, b)))] += 1
    unmatched = sum(n != 2 for n in edges.values())
    if unmatched:
        raise ValueError(f"{target.name} tiene {unmatched} aristas de malla sin dos triángulos")
    return {"triangulos": count, "aristas_sin_dos_triangulos": unmatched, "unidades_del_modelo": "mm"}


def fabrication(items, output):
    report = {}
    for item in items:
        if item.native is None or item.part_id in report:
            continue
        if item.method == "laser":
            target = output / "dxf" / f"{item.part_id}.dxf"
            entry = planar_dxf(item.native, target)
        else:
            target = output / "stl" / f"{item.part_id}.stl"
            entry = mesh_stl(item.native, target)
        bounds = item.native.BoundingBox()
        entry["caja_xyz_mm"] = [round(length, 3) for length in (bounds.xlen, bounds.ylen, bounds.zlen)]
        report[item.part_id] = entry
    return report


def write_bom(items, path):
    grouped = defaultdict(list)
    for item in items:
        if item.key.startswith("BMH_"):
            key = ("BMH12M205", "Best Modules BMH12M205, conjunto 5 kg", "Pesaje")
        else:
            label = item.label.split(" · ")[0] if item.system == "Fijaciones" else item.label
            key = (item.part_id or "—", label, item.system)
        grouped[key].append(item)
    lines = [
        "# Lista de materiales",
        "",
        "Cantidades por equipo en revisión. La tabla agrupa las instancias del CAD.",
        "",
        "| ID | Descripción | Cant. | Sistema | Material o proceso | Estado |",
        "|---|---|---:|---|---|---|",
    ]
    for (ident, label, system), instances in sorted(grouped.items(), key=lambda row: (row[0][2],row[0][0],row[0][1])):
        item = instances[0]
        quantity = 1 if ident == "BMH12M205" else len(instances)
        lines.append(f"| {ident} | {label} | {quantity} | {system} | {item.material or item.method} | {item.state} |")
    lines.extend([
        "",
        "## Elementos sin geometría de montaje aprobada",
        "",
        "| Elemento | Cant. | Estado |",
        "|---|---:|---|",
        "| KLUŚ HS-11 B17208F_1, difusor opal de 220 mm | 4 | Medir encastre en perfil. Se incluye archivo de sección de referencia. |",
        "| Terminales, cableado, pasacables y fijación de perfiles | Según arnés | Se reserva espacio. Medir las salidas y validar la temperatura y la adhesión. |",
        "| Fuente externa 5 V / 4,8 A, entrada, interruptor y fusible | 1 conjunto | Propuesta eléctrica pendiente. La versión base lleva placa de servicio ciega. |",
        "| PCB auxiliar de control | 1 | Volumen reservado. Sustituir por STEP de EasyEDA al definir el circuito. |",
        "| Plato del usuario Ø270 mm máx. de referencia | 1 | Envolvente de verificación. El equipo incluye el disco portante P10. |",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Genera los CAD y las verificaciones de FoodScan")
    parser.add_argument("--output", type=Path, default=ROOT / "exports")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    output = args.output
    for folder in ("step","stl","dxf","validacion"):
        (output / folder).mkdir(parents=True, exist_ok=True)

    p = Design()
    items = build(p)
    open_items = door_position(items, p, p.door_angle, unlocked=True)
    if not args.verify_only:
        for label, instances in [("cerrado",items),("abierto",open_items)]:
            name = f"FoodScan_{label}"
            print(f"STEP {name}", flush=True)
            to_assembly(instances, name).export(str(output / "step" / f"{name}.step"), exportType="STEP")
        refs = cq.Assembly(name="Referencias dimensionales provisionales")
        for name, shape in reference_objects(p).items():
            refs.add(shape, name=name, color=cq.Color(0.26,0.66,0.64,0.25))
        refs.export(str(output / "step" / "FoodScan_referencias.step"), exportType="STEP")
        print("DXF y STL", flush=True)
        fab = fabrication(items, output)
        (output / "validacion" / "fabricacion.json").write_text(
            json.dumps(fab, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        write_bom(items, output / "BOM.md")

    print("Verificación geométrica", flush=True)
    results = verify(p, items, open_items)
    (output / "validacion" / "geometria.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Instancias: {results['instancias']}; colisiones en cerrado: {len(results['interferencias_cerrado'])}")
    print(f"Muestras de apertura con observaciones: {len(results['puerta']['muestras_con_observaciones'])}")
    print(f"Colisiones de entrada del plato: {len(results['plato']['interferencias_barrido'])}")


if __name__ == "__main__":
    main()

"""Mechanical exchange variant of the Waveshare SKU 25742."""

import argparse
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import cadquery as cq
from OCP.BRepCheck import BRepCheck_Analyzer

from .geometry import ROOT, V, box, compound, cylinder, read_step
from .integration import OLED_STEP, asset, oled_placement
from .model import build, door_position, to_assembly
from .parameters import Design
from .verify import boxes_overlap, positive_overlap

OEM_SHA256 = "531897681ff3d66d813d84e7f8c6f8272270ad2d5c56287f63813bcfe4822190"
MOUNT_CENTERS = [(x, y) for x in (3.0, 58.5) for y in (3.5, 36.0)]
SUPPORT_Z = -3.41148
BOARD_BACK_Z = -0.41148
SHOULDER_HEIGHT = 1.2


def is_exactly_valid(solid):
    return BRepCheck_Analyzer(solid.wrapped, True, False, True).IsValid()


def bounds(shape):
    b = shape.BoundingBox()
    return (b.xmin, b.ymin, b.zmin, b.xmax, b.ymax, b.zmax)


def mounting_boss(x, y):
    """Keep the measured OEM support faces and use a smooth M2.5 bore."""
    shank_top = BOARD_BACK_Z + SHOULDER_HEIGHT
    outer = cylinder(2, 3, (x, y, SUPPORT_Z)).fuse(
        cylinder(1.45, SHOULDER_HEIGHT, (x, y, BOARD_BACK_Z))
    )
    bore = cylinder(1.25, shank_top - SUPPORT_Z + 0.2, (x, y, SUPPORT_Z - 0.1))
    # The entry mouths on the OEM model are Ø2.80. The simplified through
    # bore uses the nominal M2.5 diameter and 0.15 mm chamfers.
    entry = cq.Solid.makeCone(1.4, 1.25, 0.15, V(x, y, SUPPORT_Z))
    exit = cq.Solid.makeCone(1.4, 1.25, 0.15, V(x, y, shank_top), V(0, 0, -1))
    return outer.cut(bore, entry, exit).clean()


def repair_connectors(solids):
    # The strict check localizes the bad curves to the rounded lower lip
    # of the flex latch and two tiny fillets inside the side socket.
    latch = solids[21].cut(
        *(box(x - 0.0015, 28.19, -2.652, x + 0.0025, 28.51, -2.34)
          for x in (22.699944, 38.799944))
    ).clean()
    socket = solids[160].cut(
        *(box(6.995, y - 0.027, -1.813, 7.205, y + 0.027, -1.759)
          for y in (14.5, 26.0))
    ).clean()
    return [latch, socket]


def make_oled():
    source = ROOT / "commercial" / OLED_STEP
    if hashlib.sha256(source.read_bytes()).hexdigest() != OEM_SHA256:
        raise ValueError("Cambió el STEP Waveshare. Revisar los índices y cotas de los sólidos.")

    original = asset(OLED_STEP)
    solids = original.Solids()
    invalid = {index for index, solid in enumerate(solids) if not is_exactly_valid(solid)}
    known = {21, 160, 161, 162, 163, 164}
    details = invalid - known
    if len(solids) != 165 or not known <= invalid or any(solids[i].Volume() > 1e-5 for i in details):
        raise ValueError("Cambió el diagnóstico topológico del STEP original del OLED.")
    retained = [solid for index, solid in enumerate(solids) if index not in invalid]
    connectors = repair_connectors(solids)
    for index, repaired in zip((21, 160), connectors, strict=True):
        if len(repaired.Solids()) != 1 or abs(repaired.Volume() - solids[index].Volume()) > 0.001:
            raise ValueError(f"El recorte del sólido {index} excede la reparación prevista.")
    bosses = [mounting_boss(x, y) for x, y in MOUNT_CENTERS]
    mechanical = compound([*retained, *connectors, *bosses])
    if max(abs(a - b) for a, b in zip(bounds(original), bounds(mechanical), strict=True)) > 0.002:
        raise ValueError("La envolvente de montaje del OLED se desplazó.")
    return mechanical, len(retained), len(details)


def exact_roundtrip(step, expected_solids):
    solids = read_step(step).Solids()
    invalid = sum(not is_exactly_valid(solid) for solid in solids)
    if invalid or len(solids) != expected_solids:
        raise ValueError(f"{step.name}: {len(solids)} sólidos, {invalid} inválidos.")
    return len(solids)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "exports" / "step")
    args = parser.parse_args()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    design = Design()
    items = build(design)
    native, retained, details = make_oled()
    # The standalone file is already in assembly coordinates for reuse as
    # an exchange component at the document origin.
    installed = oled_placement(native, design)
    original_oled = next(item for item in items if item.key == "E03")
    replacement = replace(original_oled, shape=installed)
    items = [replacement if item.key == "E03" else item for item in items]
    oled_bounds = installed.BoundingBox()
    oled_solids = [(solid, solid.BoundingBox()) for solid in installed.Solids()]
    interfering = {}
    for item in items:
        if item.key == "E03" or not item.shape.Solids():
            continue
        item_bounds = item.shape.BoundingBox()
        if not boxes_overlap(oled_bounds, item_bounds):
            continue
        volume = sum(positive_overlap(solid, item.shape) for solid, bounds in oled_solids
                     if boxes_overlap(bounds, item_bounds))
        if volume > 0.05:
            interfering[item.key] = volume
    if interfering:
        raise ValueError(f"Interferencias del OLED con el montaje: {interfering}")

    oled_file = out / "E03_Waveshare_25742_mecanico.step"
    installed.exportStep(str(oled_file))
    count = exact_roundtrip(oled_file, len(installed.Solids()))
    variants = (
        ("FoodScan_cerrado_Onshape", items),
        ("FoodScan_abierto_Onshape", door_position(items, design, design.door_angle, unlocked=True)),
    )
    for name, instances in variants:
        print(f"STEP {name}", flush=True)
        path = out / f"{name}.step"
        to_assembly(instances, name).export(str(path), exportType="STEP")
    report_dir = out.parent / "validacion"
    report_dir.mkdir(exist_ok=True)
    report = {
        "fuente_oem": OLED_STEP,
        "sha256_oem": OEM_SHA256,
        "solidos_oem_conservados": retained,
        "microrrelieves_omitidos": details,
        "conectores_oem_con_reparacion_local": 2,
        "separadores_con_rosca_visual_simplificada": 4,
        "solidos_validos_al_reimportar_oled": count,
        "limites_oled_en_montaje_mm": [round(x, 5) for x in bounds(installed)],
        "interferencias_externas_oled_mm3_umbral_0_05": interfering,
    }
    (report_dir / "OLED_Onshape.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

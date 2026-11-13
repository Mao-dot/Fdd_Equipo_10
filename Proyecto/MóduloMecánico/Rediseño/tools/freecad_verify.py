"""Reimportar STEP con FreeCAD, verificar B-Rep y guardar copias FCStd."""

import argparse
import hashlib
import itertools
import json
from math import dist, isclose
import os
from pathlib import Path
import tempfile

import FreeCAD as App
import Part


def _world_shape(obj):
    shape = obj.Shape.copy()
    parent_placement = obj.getGlobalPlacement().multiply(obj.Placement.inverse())
    shape.Placement = parent_placement.multiply(shape.Placement)
    return shape


def _bounding_box(box):
    return [round(value, 6) for value in (box.XMin, box.YMin, box.ZMin, box.XMax, box.YMax, box.ZMax)]


def _repair_step_labels(document):
    changed = 0
    for obj in document.Objects:
        original = obj.Label
        try:
            label = original.encode("latin-1").decode("utf-8")
        except UnicodeError:
            label = original
        label = "".join("_" if 0x7F <= ord(character) <= 0x9F else character for character in label)
        if label != original:
            obj.Label = label
            changed += 1
    return changed


def _group_path(obj):
    groups = []
    while parent := obj.getParentGeoFeatureGroup():
        groups.append(parent.Label)
        obj = parent
    return groups[::-1]


def _read_parts(document):
    records = []
    solids = []
    for obj in document.Objects:
        if not obj.isDerivedFrom("Part::Feature"):
            continue
        shape = _world_shape(obj)
        has_shape = not shape.isNull()
        record = {
            "object": obj.Name,
            "label": obj.Label,
            "group_path": _group_path(obj),
            "valid": has_shape and shape.isValid(),
        }
        if has_shape:
            shape_solids = shape.Solids
            record.update(
                shape_type=shape.ShapeType,
                solids=len(shape_solids),
                faces=len(shape.Faces),
                bounds_mm=_bounding_box(shape.BoundBox),
                area_mm2=round(shape.Area, 6),
                solid_volume_mm3=round(sum(abs(solid.Volume) for solid in shape_solids), 6),
            )
            if shape_solids:
                geometry = shape_solids[0] if len(shape_solids) == 1 else Part.makeCompound(shape_solids)
                solids.append((record, geometry, geometry.BoundBox))
        records.append(record)
    return records, solids


def _boxes_overlap(first, second):
    return all(
        min(first_max, second_max) - max(first_min, second_min) > 1e-6
        for first_min, first_max, second_min, second_max in (
            (first.XMin, first.XMax, second.XMin, second.XMax),
            (first.YMin, first.YMax, second.YMin, second.YMax),
            (first.ZMin, first.ZMax, second.ZMin, second.ZMax),
        )
    )


def _check_overlaps(solids, tolerance):
    tested = 0
    overlaps = []
    errors = []
    for first, second in itertools.combinations(solids, 2):
        part_a, shape_a, box_a = first
        part_b, shape_b, box_b = second
        if not _boxes_overlap(box_a, box_b):
            continue
        tested += 1
        pair = [part_a["label"], part_b["label"]]
        object_ids = [part_a["object"], part_b["object"]]
        try:
            overlap = shape_a.common(shape_b)
            volume = sum(abs(solid.Volume) for solid in overlap.Solids)
            if volume > tolerance:
                overlaps.append({"pair": pair, "object_ids": object_ids, "volume_mm3": round(volume, 6)})
        except (RuntimeError, Part.OCCError) as error:
            errors.append({"pair": pair, "object_ids": object_ids, "message": str(error)})
    return {
        "broad_phase_candidates": tested,
        "threshold_mm3": tolerance,
        "positive_volume": sorted(overlaps, key=lambda item: item["volume_mm3"], reverse=True),
        "boolean_errors": errors,
    }


def _sha256(path):
    with path.open("rb") as file:
        return hashlib.file_digest(file, "sha256").hexdigest()


def _model_bounds(records):
    boxes = [entry["bounds_mm"] for entry in records if "bounds_mm" in entry]
    if not boxes:
        raise RuntimeError("El documento importado no contiene geometría medible.")
    return [min(box[i] for box in boxes) for i in range(3)] + [max(box[i] for box in boxes) for i in range(3, 6)]


def _same_record(first, second):
    if first is None or second is None or first.keys() != second.keys():
        return False
    measures = ("bounds_mm", "area_mm2", "solid_volume_mm3")
    for key in first:
        if key == "bounds_mm":
            if not all(isclose(a, b, abs_tol=0.002) for a, b in zip(first[key], second[key], strict=True)):
                return False
        elif key in measures:
            if not isclose(first[key], second[key], rel_tol=1e-6, abs_tol=0.005):
                return False
        elif first[key] != second[key]:
            return False
    return True


def _set_opening_view(gui, bounds):
    from pivy import coin

    lower, upper = bounds[:3], bounds[3:]
    diagonal = max(1, dist(lower, upper))
    center = App.Vector(*[(a + b) / 2 for a, b in zip(lower, upper)])
    vertical = App.Vector(0, 0, 1)
    back = App.Vector(1, -1.4, 0.75).normalize()
    right = vertical.cross(back).normalize()
    rotation = App.Rotation(right, back.cross(right), back, "ZXY")
    position = center + back * (2 * diagonal)
    view = gui.activeDocument().activeView()
    if view.getCameraType() != "Orthographic":
        view.setCameraType("Orthographic")
    camera = view.getCameraNode()
    camera.position.setValue(position.x, position.y, position.z)
    camera.orientation.setValue(coin.SbRotation(*rotation.Q))
    camera.nearDistance.setValue(diagonal)
    camera.farDistance.setValue(3 * diagonal)
    camera.focalDistance.setValue(2 * diagonal)
    camera.height.setValue(1.05 * diagonal)


def verify_step(path, native_dir, report_dir, importer, gui, tolerance, skip_overlaps):
    native_file = native_dir / path.with_suffix(".FCStd").name
    report_file = report_dir / f"{path.stem}_freecad.json"
    native_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    document = App.newDocument(path.stem)
    try:
        importer.insert(str(path), document.Name, merge=False, useLinkGroup=False)
        repaired_labels = _repair_step_labels(document)
        document.recompute()
        tree = [obj.Label for obj in document.RootObjects]
        records, solids = _read_parts(document)
        if not records:
            raise RuntimeError(f"El importador no generó piezas para {path.name}.")
        bounds = _model_bounds(records)
        collisions = None if skip_overlaps else _check_overlaps(solids, tolerance)
        if gui:
            _set_opening_view(gui, bounds)

        with tempfile.TemporaryDirectory(dir=native_dir) as temporary:
            staged = Path(temporary) / native_file.name
            document.saveAs(str(staged))
            App.closeDocument(document.Name)
            document = None
            document = App.openDocument(str(staged))
            reopened, _ = _read_parts(document)
            reopened_tree = [obj.Label for obj in document.RootObjects]
            records_by_id = {entry["object"]: entry for entry in records}
            reopened_by_id = {entry["object"]: entry for entry in reopened}
            changes = sorted(obj_id for obj_id in records_by_id.keys() | reopened_by_id.keys()
                             if not _same_record(reopened_by_id.get(obj_id), records_by_id.get(obj_id)))
            matches = not changes and reopened_tree == tree
            App.closeDocument(document.Name)
            document = None
            staged.replace(native_file)
    finally:
        if document is not None:
            App.closeDocument(document.Name)

    invalid = [entry["label"] for entry in records if not entry["valid"]]
    passed = matches and not invalid and not (collisions and collisions["boolean_errors"])
    report = {
        "freecad_version": ".".join(App.Version()[:3]),
        "source_step": path.name,
        "source_sha256": _sha256(path),
        "native_file": native_file.name,
        "native_sha256": _sha256(native_file),
        "root_labels": tree,
        "step_labels_repaired_on_import": repaired_labels,
        "features": len(records),
        "features_with_solids": len(solids),
        "surface_or_wire_features": len(records) - len(solids),
        "model_bounds_mm": bounds,
        "invalid_features": invalid,
        "native_reopen_matches_step_import": matches,
        "native_reopen_changed_object_ids": changes,
        "import_and_boolean_checks_passed": passed,
        "overlap_free_over_threshold": None if skip_overlaps else not collisions["positive_volume"] and not collisions["boolean_errors"],
        "features_mm": records,
        "overlaps": collisions,
    }
    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    overlap_count = "omitidos" if skip_overlaps else len(collisions["positive_volume"])
    print(f"{path.name}: {len(records)} piezas, {len(solids)} con sólidos, "
          f"{len(invalid)} B-Rep inválidas, solapes volumétricos {overlap_count}, "
          f"reapertura FCStd {'correcta' if matches else 'con diferencias'}.")
    return passed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", nargs="+", type=Path, help="Archivos STEP de entrada")
    parser.add_argument("--fcstd-dir", type=Path, help="Carpeta de salida FCStd (por defecto, la carpeta de cada STEP)")
    parser.add_argument("--report-dir", type=Path, help="Carpeta de los informes JSON")
    parser.add_argument("--overlap-threshold-mm3", type=float, default=0.01)
    parser.add_argument("--skip-overlaps", action="store_true", help="Omitir intersecciones por pares")
    parser.add_argument("--geometry-only", action="store_true", help="Importar mediante FreeCAD sin inicializar Qt")
    args = parser.parse_args()
    if args.overlap_threshold_mm3 < 0:
        parser.error("El umbral de solape debe ser no negativo.")
    for step in args.step:
        if not step.is_file():
            parser.error(f"No se encuentra {step}.")

    gui = None
    if args.geometry_only:
        import Import as importer
    else:
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        import FreeCADGui as gui

        gui.showMainWindow()
        import ImportGui as importer

    results = []
    for step in args.step:
        step = step.resolve()
        native_dir = (args.fcstd_dir or step.parent).resolve()
        report_dir = (args.report_dir or step.parent.parent / "validacion").resolve()
        results.append(verify_step(step, native_dir, report_dir, importer, gui,
                                   args.overlap_threshold_mm3, args.skip_overlaps))
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Construye la PCB auxiliar desde la matriz y las huellas KiCad 10."""

import argparse
import csv
import heapq
import math
import shutil
from collections import defaultdict
from pathlib import Path

import numpy as np
import sexpdata as sexp


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = (80, 70)
WIDTH, HEIGHT, GRID = 60, 65, 0.25
CLEARANCE = 0.23
VIA_DIAMETER, VIA_DRILL = 0.70, 0.35
GRID_SHAPE = (2, 1 + round(HEIGHT / GRID), 1 + round(WIDTH / GRID))
S = sexp.Symbol

TERM2 = "TerminalBlock_Phoenix:TerminalBlock_Phoenix_PT-1,5-2-5.0-H_1x02_P5.00mm_Horizontal"
TERM4 = "TerminalBlock_Phoenix:TerminalBlock_Phoenix_PT-1,5-4-5.0-H_1x04_P5.00mm_Horizontal"
RES = "Resistor_SMD:R_0603_1608Metric"
CAP = "Capacitor_SMD:C_0603_1608Metric"
POL = "Capacitor_THT:CP_Radial_D8.0mm_P3.50mm"
FET = "Package_TO_SOT_SMD:SOT-23"
BUCK = "FoodScan:RECOM_R-78K-1.0"
HOLE = "FoodScan:NPTH_3.4mm_M3"


def jst(pins):
    return f"Connector_JST:JST_XH_B{pins}B-XH-A_1x{pins:02}_P2.50mm_Vertical"


# Component coordinates are measured from the top-left board corner.
PLACEMENT = {
    "J1": (TERM2, 6, 33, 270), "J2": (TERM4, 10.5, 55, 0), "J3": (TERM4, 35, 55, 0),
    "J4": (jst(4), 10.5, 9, 0), "J5": (jst(2), 24, 9, 0),
    "J6": (jst(6), 9, 25, 0), "J7": (jst(7), 34, 9, 0),
    "J8": (jst(6), 36.5, 18, 0), "J9": (jst(3), 10.5, 17, 0),
    "J10": (jst(2), 48, 29, 0), "J11": (jst(3), 41, 40, 0),
    "J12": (jst(2), 31, 37, 0), "U2": (BUCK, 30, 29, 0),
    "C1": (POL, 14, 42, 0), "C2": (CAP, 23, 32, 0),
    "C3": (CAP, 40.5, 26, 0), "C4": (CAP, 40.5, 23.5, 0), "C5": (CAP, 54, 35, 0),
    "Q1": (FET, 24, 48.25, 0), "Q2": (FET, 46, 48.25, 0),
    "R1": (RES, 23, 44, 0), "R2": (RES, 43, 45.5, 0),
    "R3": (RES, 20, 48.25, 0), "R4": (RES, 42, 48.25, 0),
    "R5": (RES, 45, 24, 0), "R6": (RES, 48, 35, 90),
    "R7": (RES, 52, 39, 0), "R8": (RES, 26, 35, 90), "R10": (RES, 26, 39, 90),
    "H1": (HOLE, 4, 4, 0), "H2": (HOLE, 56, 4, 0),
    "H3": (HOLE, 4, 61, 0), "H4": (HOLE, 56, 61, 0),
}
LEGENDS = {
    "J1 5V IN": (3, 44), "J2 COB 1/2": (10, 62), "J3 COB 3/4": (36, 62),
    "J4 PESO": (8, 5), "J5 CAM 3V3": (21, 5), "J6 ESP PWR/IO": (9, 21.4),
    "J7 OLED": (34, 5), "J8 ESP SPI": (36, 14), "J9 ESP UART": (10, 13.4),
    "J10 PUERTA": (45.5, 25), "J11 BOTONES": (39, 36.2), "J12 ESP BOT": (28, 33.5),
    "U2": (30, 32.3), "C1": (14, 36.8), "Q1": (25, 45.5), "Q2": (48, 46.1),
}
TRACK_WIDTHS = {"5V_SW": 1.8, "LED_RET_A": 0.8, "LED_RET_B": 0.8,
                "GND": 0.35, "3V3_AUX": 0.6}


def fields(node, name):
    return [item for item in node if isinstance(item, list) and item[0] == S(name)]


def field(node, name):
    return next(iter(fields(node, name)), None)


def number(value):
    return round(float(value), 5)


def absolute(point):
    return [number(o + p) for o, p in zip(ORIGIN, point)]


def rotate(x, y, angle):
    radians = math.radians(angle)
    return number(x * math.cos(radians) + y * math.sin(radians)), number(-x * math.sin(radians) + y * math.cos(radians))


def hole_footprint():
    return sexp.loads("""(footprint "NPTH_3.4mm_M3" (layer "F.Cu")
      (attr exclude_from_pos_files exclude_from_bom board_only)
      (fp_circle (center 0 0) (end 3.05 0) (stroke (width 0.05) (type solid)) (fill none) (layer "F.CrtYd"))
      (pad "" np_thru_hole circle (at 0 0) (size 3.4 3.4) (drill 3.4) (layers "*.Cu" "*.Mask")))""")


def regulator_footprint():
    # RECOM R-78K-1.0 Rev. 6-2025 dimensional drawing; pitch 2.54 mm.
    return sexp.loads("""(footprint "RECOM_R-78K-1.0" (layer "F.Cu") (attr through_hole)
      (descr "RECOM R-78K-1.0 SIP3, OEM drawing")
      (fp_rect (start -3.21 -5.55) (end 8.29 2.0) (stroke (width 0.1) (type solid)) (fill none) (layer "F.Fab"))
      (fp_rect (start -3.34 -5.68) (end 8.42 2.13) (stroke (width 0.12) (type solid)) (fill none) (layer "F.SilkS"))
      (fp_rect (start -3.46 -5.8) (end 8.54 2.25) (stroke (width 0.05) (type solid)) (fill none) (layer "F.CrtYd"))
      (pad "1" thru_hole rect (at 0 0) (size 1.85 1.85) (drill 1) (layers "*.Cu" "*.Mask"))
      (pad "2" thru_hole circle (at 2.54 0) (size 1.85 1.85) (drill 1) (layers "*.Cu" "*.Mask"))
      (pad "3" thru_hole circle (at 5.08 0) (size 1.85 1.85) (drill 1) (layers "*.Cu" "*.Mask"))
      (model "${KIPRJMOD}/../fuentes/RECOM-R-78K-1.0-original.STEP"
        (offset (xyz 2.54 2.325 0)) (scale (xyz 1 1 1)) (rotate (xyz 180 0 0))))""")


def load_footprint(library, key):
    if key == HOLE:
        return hole_footprint()
    if key == BUCK:
        return regulator_footprint()
    folder, name = key.split(":")
    return sexp.loads((library / f"{folder}.pretty" / f"{name}.kicad_mod").read_text(encoding="utf-8"))


def localize_model(footprint, model_dir, output):
    model = field(footprint, "model")
    if not model or "KICAD10_3DMODEL_DIR" not in model[1]:
        return
    source = model_dir / model[1].split("/", 1)[1]
    if not source.is_file():
        raise FileNotFoundError(source)
    destination = output / "modelos" / source.name
    destination.parent.mkdir(exist_ok=True)
    if not destination.exists():
        shutil.copyfile(source, destination)
    model[1] = "${KIPRJMOD}/modelos/" + source.name


def text_node(ref, value, x, y, layer, hidden=False, size=0.8):
    return sexp.loads(f"""(property {sexp.dumps(ref)} {sexp.dumps(value)} (at {x} {y} 0)
        (layer "{layer}") {'(hide yes)' if hidden else ''}
        (effects (font (size {size} {size}) (thickness 0.13))))""")


def make_parts(library, models, output, assignments, net_ids):
    footprints, pads = [], []
    for ref, (key, x, y, angle) in PLACEMENT.items():
        original = load_footprint(library, key)
        localize_model(original, models, output)
        lib, name = key.split(":")
        pretty = output / (lib + ".pretty")
        pretty.mkdir(exist_ok=True)
        (pretty / (name + ".kicad_mod")).write_text(sexp.dumps(original) + "\n", encoding="utf-8")
        footprint = original[:]
        footprint[1] = key
        footprint[:] = [item for item in footprint if not isinstance(item, list) or
                        item[0] not in map(S, ("version", "generator", "property"))]
        footprint.insert(3, [S("at"), *absolute((x, y)), angle])
        value = assignments[ref][0]["model"] if ref in assignments else "NPTH 3.4 mm"
        footprint.extend((text_node("Reference", ref, 0, -2, "F.Fab", ref.startswith("H")),
                          text_node("Value", value, 0, 0, "F.Fab", True)))
        physical = {pad[1] for pad in fields(footprint, "pad") if pad[1]}
        expected = {row["pin"]: row["net"] for row in assignments.get(ref, [])}
        if physical != expected.keys():
            raise ValueError(f"{ref}: huella {sorted(physical)}, esquema {sorted(expected)}")
        for pad in fields(footprint, "pad"):
            pin = pad[1]
            net = expected.get(pin, "")
            if net:
                pad.append([S("net"), net_ids[net], net])
            lx, ly, *local_angle = field(pad, "at")[1:]
            dx, dy = rotate(lx, ly, angle)
            sx, sy = field(pad, "size")[1:]
            total_angle = angle + (local_angle[0] if local_angle else 0)
            field(pad, "at")[3:] = [total_angle % 360] if total_angle % 360 else []
            if total_angle % 180 == 90:
                sx, sy = sy, sx
            layers = (0,) if pad[2] == S("smd") else (0, 1)
            pads.append((ref, pin, net, (number(x + dx), number(y + dy)), (sx, sy), layers))
        footprints.append(footprint)
    return footprints, pads


def rectangular_mask(array, cx, cy, rx, ry, layers):
    x0, x1 = max(0, math.ceil((cx - rx) / GRID)), min(GRID_SHAPE[2] - 1, math.floor((cx + rx) / GRID))
    y0, y1 = max(0, math.ceil((cy - ry) / GRID)), min(GRID_SHAPE[1] - 1, math.floor((cy + ry) / GRID))
    for layer in layers:
        array[layer, y0:y1 + 1, x0:x1 + 1] = True


def segment_mask(array, a, b, margin, layer):
    x0, y0 = a
    x1, y1 = b
    left, right = max(0, math.ceil((min(x0, x1) - margin) / GRID)), min(GRID_SHAPE[2] - 1, math.floor((max(x0, x1) + margin) / GRID))
    top, bottom = max(0, math.ceil((min(y0, y1) - margin) / GRID)), min(GRID_SHAPE[1] - 1, math.floor((max(y0, y1) + margin) / GRID))
    xx = np.arange(left, right + 1) * GRID - x0
    yy = np.arange(top, bottom + 1)[:, None] * GRID - y0
    vx, vy = x1 - x0, y1 - y0
    norm = vx * vx + vy * vy
    t = np.clip((xx * vx + yy * vy) / norm, 0, 1) if norm else 0
    array[layer, top:bottom + 1, left:right + 1] |= ((xx - t * vx) ** 2 + (yy - t * vy) ** 2 <= margin ** 2)


def make_masks(net, pads, tracks, vias, width, *, via=False):
    result = np.zeros(GRID_SHAPE, dtype=bool)
    edge = math.ceil((0.5 + width / 2) / GRID)
    result[:, :edge, :] = result[:, -edge:, :] = True
    result[:, :, :edge] = result[:, :, -edge:] = True
    gap = CLEARANCE + width / 2
    for _, _, other, (x, y), (sx, sy), layers in pads:
        if other != net or via:
            pad_gap = gap if not via else max(gap, 0.30 + VIA_DRILL / 2 + width / 2)
            rectangular_mask(result, x, y, sx / 2 + pad_gap, sy / 2 + pad_gap, layers)
    for other, layer, a, b, w in tracks:
        if other != net:
            segment_mask(result, a, b, gap + w / 2, layer)
    for other, point in vias:
        if other != net or via:
            for layer in (0, 1):
                segment_mask(result, point, point, gap + VIA_DIAMETER / 2, layer)
    return result


def node_at(point, layer):
    return layer, round(point[1] / GRID), round(point[0] / GRID)


def point_at(node):
    return node[2] * GRID, node[1] * GRID


DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1))


def find_route(starts, goals, mask, via_mask):
    gy0, gy1 = min(g[1] for g in goals), max(g[1] for g in goals)
    gx0, gx1 = min(g[2] for g in goals), max(g[2] for g in goals)

    def estimate(node):
        _, y, x = node
        dy = max(gy0 - y, y - gy1, 0)
        dx = max(gx0 - x, x - gx1, 0)
        return 10 * max(dx, dy) + 4 * min(dx, dy)

    values = {node: 0 for node in starts if not mask[node]}
    queue = [(estimate(node), 0, node) for node in values]
    heapq.heapify(queue)
    parent = {}
    while queue:
        _, distance, node = heapq.heappop(queue)
        if distance != values[node]:
            continue
        if node in goals:
            path = [node]
            while path[-1] in parent:
                path.append(parent[path[-1]])
            return path[::-1]
        layer, y, x = node
        next_nodes = []
        for dy, dx in DIRECTIONS:
            yy, xx = y + dy, x + dx
            if not (0 <= yy < GRID_SHAPE[1] and 0 <= xx < GRID_SHAPE[2]):
                continue
            if dy and dx and (mask[layer, y, xx] or mask[layer, yy, x]):
                continue
            next_nodes.append(((layer, yy, xx), 14 if dx and dy else 10))
        if not via_mask[0, y, x] and not via_mask[1, y, x]:
            next_nodes.append(((1 - layer, y, x), 60))
        for candidate, cost in next_nodes:
            new_distance = distance + cost
            if mask[candidate] or new_distance >= values.get(candidate, math.inf):
                continue
            values[candidate] = new_distance
            parent[candidate] = node
            heapq.heappush(queue, (new_distance + estimate(candidate), new_distance, candidate))
    raise ValueError("No existe ruta libre")


def add_path(net, width, path, tracks, vias):
    start = path[0]
    previous = start
    direction = None
    for node in path[1:]:
        new_direction = tuple(b - a for a, b in zip(previous, node))
        if direction != new_direction and start != previous:
            tracks.append((net, start[0], point_at(start), point_at(previous), width))
            start = previous
        if node[0] != previous[0]:
            vias.append((net, point_at(node)))
            start = node
        direction, previous = new_direction, node
    if start != previous:
        tracks.append((net, start[0], point_at(start), point_at(previous), width))


def route_board(pads):
    groups = defaultdict(list)
    for pad in pads:
        if pad[2]:
            groups[pad[2]].append(pad)
    tracks, vias = [], []
    order = ("5V_SW", "LED_RET_A", "LED_RET_B", "3V3_AUX", "LED_GATE_A", "LED_GATE_B")
    nets = list(order) + [name for name in groups if name not in order and name != "GND"] + ["GND"]
    for net in nets:
        pending = groups[net][:]
        width = TRACK_WIDTHS.get(net, 0.25)
        _, _, _, first, _, layers = pending.pop(0)
        connected = {node_at(first, layer) for layer in layers}
        for layer in layers:
            point = point_at(node_at(first, layer))
            if first != point:
                tracks.append((net, layer, first, point, width))
        while pending:
            closest = min(pending, key=lambda p: (
                net == "5V_SW" and len(p[5]) == 1,
                min(abs(p[3][0] - point_at(n)[0]) + abs(p[3][1] - point_at(n)[1])
                    for n in connected),
            ))
            pending.remove(closest)
            ref, pin, _, position, _, pad_layers = closest
            if net == "5V_SW":
                width = 0.3 if len(pad_layers) == 1 else 1.8
            starts = [node_at(position, layer) for layer in pad_layers]
            mask = make_masks(net, pads, tracks, vias, width)
            via_mask = make_masks(net, pads, tracks, vias, VIA_DIAMETER, via=True)
            if net == "5V_SW" and len(pad_layers) == 2:
                via_mask[:] = True
                mask[0, :, :] = True
                for node in starts + list(connected):
                    if node[0] == 0:
                        mask[node] = False
            try:
                path = find_route(starts, connected, mask, via_mask)
            except ValueError as error:
                raise ValueError(f"{net} → {ref}.{pin}: {error}") from error
            point = point_at(path[0])
            if position != point:
                tracks.append((net, path[0][0], position, point, width))
            add_path(net, width, path, tracks, vias)
            connected.update(path)
            connected.update(starts)
    return tracks, vias


def write_board(target, footprints, tracks, vias, net_ids):
    board = sexp.loads("""(kicad_pcb (version 20240108) (generator "pcbnew")
      (general (thickness 1.6)) (paper "A4")
      (title_block (title "FoodScan - Placa auxiliar") (rev "A"))
      (layers (0 "F.Cu" signal) (31 "B.Cu" signal) (32 "B.Adhes" user "B.Adhesive")
       (33 "F.Adhes" user "F.Adhesive") (34 "B.Paste" user) (35 "F.Paste" user)
       (36 "B.SilkS" user "B.Silkscreen") (37 "F.SilkS" user "F.Silkscreen")
       (38 "B.Mask" user) (39 "F.Mask" user) (40 "Dwgs.User" user "User.Drawings")
       (44 "Edge.Cuts" user) (46 "B.CrtYd" user "B.Courtyard") (47 "F.CrtYd" user "F.Courtyard")
       (48 "B.Fab" user) (49 "F.Fab" user))
      (setup (pad_to_mask_clearance 0)))""")
    board.extend([[S("net"), n, name] for name, n in net_ids.items()])
    board.extend(footprints)
    outline = [(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)]
    for a, b in zip(outline, outline[1:] + outline[:1]):
        board.append([S("gr_line"), [S("start"), *absolute(a)], [S("end"), *absolute(b)],
                      [S("stroke"), [S("width"), 0.05], [S("type"), S("solid")]],
                      [S("layer"), "Edge.Cuts"]])
    for net, layer, a, b, width in tracks:
        board.append([S("segment"), [S("start"), *absolute(a)], [S("end"), *absolute(b)],
                      [S("width"), width], [S("layer"), ("F.Cu", "B.Cu")[layer]], [S("net"), net_ids[net]]])
    for net, point in vias:
        board.append([S("via"), [S("at"), *absolute(point)], [S("size"), VIA_DIAMETER],
                      [S("drill"), VIA_DRILL], [S("layers"), "F.Cu", "B.Cu"], [S("net"), net_ids[net]]])
    for caption, (x, y) in LEGENDS.items():
        board.append(sexp.loads(f"""(gr_text "{caption}" (at {ORIGIN[0]+x} {ORIGIN[1]+y})
            (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.14)) (justify left)))"""))
    board.append(sexp.loads("""(gr_text "FOODSCAN AUX A" (at 110 133.5) (layer "F.SilkS")
        (effects (font (size 1.15 1.15) (thickness 0.18))))"""))
    for layer in ("F.Cu", "B.Cu"):
        vertices = " ".join(f"(xy {x} {y})" for x, y in [absolute(p) for p in outline])
        board.append(sexp.loads(f"""(zone (net {net_ids['GND']}) (net_name "GND") (layer "{layer}")
          (hatch edge 0.5) (connect_pads (clearance 0.25)) (min_thickness 0.25)
          (fill yes (thermal_gap 0.28) (thermal_bridge_width 0.35))
          (polygon (pts {vertices})))"""))
    target.write_text("(kicad_pcb\n" + "\n".join(sexp.dumps(item) for item in board[1:]) + ")\n", encoding="utf-8")
    lib_entries = " ".join(f'(lib (name "{p.stem}") (type "KiCad") (uri "${{KIPRJMOD}}/{p.name}") (options "") (descr ""))'
                           for p in sorted(target.parent.glob("*.pretty")))
    (target.parent / "fp-lib-table").write_text(f"(fp_lib_table (version 7) {lib_entries})\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kicad_share", type=Path, help="Directorio share/kicad de KiCad 10")
    args = parser.parse_args()
    output = ROOT / "pcb"
    assignments = defaultdict(list)
    with (ROOT / "Matriz_conexiones.csv").open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            if row["section"].startswith("01 "):
                assignments[row["ref"]].append(row)
    nets = sorted({row["net"] for rows in assignments.values() for row in rows if row["net"]})
    net_ids = {name: index for index, name in enumerate(nets, 1)}
    footprints, pads = make_parts(args.kicad_share / "footprints", args.kicad_share / "3dmodels",
                                  output, assignments, net_ids)
    tracks, vias = route_board(pads)
    write_board(output / "FoodScan_Auxiliar.kicad_pcb", footprints, tracks, vias, net_ids)
    print(f"{len(assignments)} componentes, {len(net_ids)} redes, {len(tracks)} pistas, {len(vias)} vías")


if __name__ == "__main__":
    main()

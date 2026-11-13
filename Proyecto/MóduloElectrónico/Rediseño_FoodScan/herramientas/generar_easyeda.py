"""Build and independently check the editable EasyEDA Pro V3 schematic archive."""

import argparse
from collections import Counter, defaultdict
import csv
from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
TITLE = "FoodScan - Rediseño electrónico"
CLIENT = "foodscan"
VERSION = "1794531600000"
BLUE = "#244566"
GRAY = "#516070"
ATTR_FIELDS = {
    "rotation": 0, "color": None, "fillColor": None, "fontFamily": None,
    "fontSize": None, "strikeout": False, "underline": False, "italic": False,
    "fontWeight": False, "align": "LEFT_BOTTOM", "version": "2.0",
}
JST_CODES = {
    "B2B-XH-A": "C158012", "B3B-XH-A": "C144394", "B4B-XH-A": "C144395",
    "B5B-XH-A": "C157991", "B6B-XH-A": "C144397", "B7B-XH-A": "C144398",
}
WRONG_LIBRARY_PITCH = {"C157991", "C3817931"}
PHOENIX_CODES = {"1935161": "C3819953", "1935187": "C3817931"}
PIN_TYPES = {
    "In": "IN", "Input": "IN", "Out": "OUT", "Output": "OUT",
    "I/O": "IO", "IO": "IO", "Power": "POWER", "Power in": "POWER",
    "Passive": "Undefined", "Undefined": "Undefined",
}


def id_for(*parts):
    return hashlib.sha256(("FoodScan:" + ":".join(parts)).encode()).hexdigest()[:16]


def turn(x, y, rotation):
    return {0: (x, y), 90: (-y, x), 180: (-x, -y), 270: (y, -x)}[rotation % 360]


def json_text(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


@dataclass
class Doc:
    kind: str
    uuid: str
    rows: list

    def add(self, kind, data, key=None):
        key = key or f"e{len(self.rows) + 1}"
        self.rows.append((kind, key, data))
        return key

    def meta(self, data):
        self.add("META", data, "META")

    def canvas(self):
        self.add("CANVAS", {"originX": 0, "originY": 0}, "CANVAS")

    def body(self, kind, part="", **props):
        return self.add(kind, {
            "partId": part, "groupId": "", "locked": False,
            "zIndex": len(self.rows) + 1, **props,
        })

    def attr(self, parent, name, value, *, x=None, y=None, visible=False, part="", **style):
        return self.body("ATTR", part, **{
            **ATTR_FIELDS, "parentId": parent, "key": name, "value": value,
            "keyVisible": False, "valueVisible": visible, "x": x, "y": y, **style,
        })

    def rect(self, x1, y1, x2, y2, *, part="", color=BLUE):
        self.body("RECT", part, dotX1=x1, dotY1=y1, dotX2=x2, dotY2=y2,
                  radiusX=0, radiusY=0, rotation=0, strokeColor=color,
                  strokeWidth=1, strokeStyle="SOLID", fillColor=None, fillStyle="NONE")

    def text(self, x, y, value, size, *, bold=False, color=BLUE, align="LEFT_BOTTOM"):
        self.body("TEXT", **{**ATTR_FIELDS, "x": x, "y": y, "value": value,
                             "fontSize": size, "color": color, "fontWeight": bold,
                             "align": align})


def parse_archive(path):
    decoder = json.JSONDecoder()
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError(f"CRC incorrecto: {path}")
        config = json.loads(archive.read("project2.json"))
        files = [name for name in archive.namelist() if name.endswith(".epru")]
        if len(files) != 1:
            raise ValueError(f"Se esperaba un único log de proyecto: {path}")
        documents = []
        for line in archive.read(files[0]).decode("utf-8").split("\n"):
            if not line.strip():
                continue
            head, cursor = decoder.raw_decode(line)
            body, end = decoder.raw_decode(line, cursor + 2)
            if line[cursor:cursor + 2] != "||" or line[end:].strip() not in {"", "|"}:
                raise ValueError(f"Registro EasyEDA inválido: {head!r} {line[end:end + 40]!r}")
            if head["type"] == "DOCHEAD":
                documents.append(Doc(body["docType"], body["uuid"], []))
            else:
                documents[-1].rows.append((head["type"], head.get("id", ""), body))
    return config, documents


def write_archive(path, documents):
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    ticket = 0
    for doc in documents:
        head = {"docType": doc.kind, "client": CLIENT, "uuid": doc.uuid,
                "updateTime": int(VERSION), "version": VERSION}
        lines.append(json_text({"type": "DOCHEAD"}) + "||" + json_text(head) + "|\n")
        for kind, key, data in doc.rows:
            ticket += 1
            meta = {"type": kind, "ticket": ticket}
            if key:
                meta["id"] = key
            lines.append(json_text(meta) + "||" + json_text(data) + "|\n")
    config = {"uuid": id_for(TITLE), "title": TITLE, "cbb_project": False,
              "editorVersion": "3.2.209", "description": ""}
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("FoodScan.epru", "".join(lines))
        archive.writestr("project2.json", json_text(config))


def convert(converter, source, decoder, target_dir, encoder="easyeda-pro-2"):
    extension = ".epro2" if encoder == "easyeda-pro-2" else ".epro"
    output = target_dir / (source.stem + "-converted" + extension)
    params = {
        "decodingOptions": {"decodingType": decoder, "decodingFilePath": str(source)},
        "encodingOptions": {"encodingType": encoder, "savingDirPath": str(target_dir),
                            "savingFileName": output.stem},
    }
    config = target_dir / (source.stem + "-convert-options.json")
    config.write_text(json_text(params), encoding="utf-8")
    process = subprocess.run(["node", str(converter), "--cmd", "conversion",
                              "--params-path", str(config)], capture_output=True,
                             text=True, encoding="utf-8", errors="replace", timeout=75)
    if process.returncode or "success: true" not in process.stdout or not output.is_file():
        raise RuntimeError(process.stdout + process.stderr)
    return output


def load_matrix(path):
    by_section = defaultdict(dict)
    seen = set()
    with path.open(encoding="utf-8-sig", newline="") as stream:
        for raw in csv.DictReader(stream):
            row = {key: (value or "").strip() for key, value in raw.items()}
            ref, pin, section = row["ref"], row["pin"], row["section"]
            if not ref or not pin or not section or (ref, pin) in seen:
                raise ValueError(f"Fila incompleta o pin repetido: {row}")
            seen.add((ref, pin))
            by_section[section].setdefault(ref, []).append(row)
    return by_section


def collect_pins(symbol):
    ids = {body["parentId"]: body["value"] for kind, _, body in symbol.rows
           if kind == "ATTR" and body["key"] in {"Pin Number", "NUMBER"}}
    pins = {ids[key]: (key, body) for kind, key, body in symbol.rows if kind == "PIN"}
    if len(pins) != len(ids):
        raise ValueError(f"Numeración de pin ambigua: {symbol.uuid}")
    return pins


def downloaded_part(rows, source_dir, converter, work, *, external):
    row = rows[0]
    model, ref = row["model"], row["ref"]
    library_key = row.get("library_mpn") or JST_CODES.get(model.split("(")[0], "")
    library_key = library_key or next((code for pn, code in PHOENIX_CODES.items()
                                      if pn in model), "")
    if not library_key:
        match = re.search(r"\bC\d{4,}\b", model)
        library_key = match.group() if match else ""
    if "DevKitC" in model:
        filename = source_dir / "EasyEDA-DevKitC-community-source.json"
    else:
        filename = source_dir / f"EasyEDA-{library_key}-original.json"
    if not filename.is_file():
        return None
    raw = json.loads(filename.read_bytes())["result"]
    source = work / f"{ref}-library.zip"
    with zipfile.ZipFile(source, "w", zipfile.ZIP_DEFLATED) as archive:
        # The installed converter reads a Node buffer's backing allocation.
        # A ZIP over 4 KiB avoids its small-buffer offset bug.
        archive.comment = b" " * 4096
        archive.writestr("symbol.json", json_text(raw["dataStr"]))
        if (not external and library_key not in WRONG_LIBRARY_PITCH
                and raw.get("packageDetail", {}).get("dataStr")):
            archive.writestr("footprint.json", json_text(raw["packageDetail"]["dataStr"]))
    _, converted = parse_archive(convert(converter, source, "easyeda", work))
    symbol = next(doc for doc in converted if doc.kind == "SYMBOL")
    device = next(doc for doc in converted if doc.kind == "DEVICE")
    footprint = next((doc for doc in converted if doc.kind == "FOOTPRINT"), None)
    symbol.uuid = id_for(ref, "symbol")
    device.uuid = id_for(ref, "device")
    if footprint:
        footprint.uuid = id_for(ref, "footprint")
    pin_map = collect_pins(symbol)
    if "DevKitC" in model and {pin["pin"] for pin in rows} != set(pin_map):
        pin_map = {f"J1.{num}": pin_map[str(num)] for num in range(1, 23)} | {
            f"J3.{num}": pin_map[str(45 - num)] for num in range(1, 23)
        }
    actual = {row["pin"] for row in rows}
    if actual != set(pin_map):
        raise ValueError(f"{ref} {model}: biblioteca {sorted(pin_map)}, matriz {sorted(actual)}")
    types = {pin_map[r["pin"]][0]: PIN_TYPES.get(r.get("pin_type", ""), "")
             for r in rows}
    for kind, _, body in symbol.rows:
        if kind == "ATTR" and body["key"] == "Pin Type" and types.get(body["parentId"]):
            body["value"] = types[body["parentId"]]
        if kind == "ATTR" and body["key"] in ("Pin Name", "Pin Number") and len(rows) > 12:
            body["fontSize"] = min(body["fontSize"] or 8, 7)
        if kind == "TEXT" and "DevKitC" in model and "DevKitC" in body["value"]:
            body.update(x=0, y=0, rotation=90, align="CENTER_MIDDLE", fontSize=10)
    meta = device.rows[0][2]
    meta["source"] = f"https://easyeda.com/api/components/{raw['uuid']}"
    meta["attributes"].update({
        "Symbol": symbol.uuid, "Footprint": footprint.uuid if footprint else "",
        "Convert to PCB": "no" if external else "yes",
    })
    license_text = raw["dataStr"]["head"].get("license")
    if license_text:
        meta["attributes"]["Library License"] = license_text
    symbol.rows[0][2]["source"] = meta["source"]
    if footprint:
        footprint.rows[0][2]["source"] = f"https://easyeda.com/api/components/{raw['packageDetail']['uuid']}"
        if set(pin_map) != {p["num"] for kind, _, p in footprint.rows if kind == "PAD" and p["num"]}:
            raise ValueError(f"{ref}: los pines y pads de biblioteca no coinciden")
    return symbol, device, footprint, pin_map, filename.name


def interface_part(rows, *, external):
    ref, model = rows[0]["ref"], rows[0]["model"]
    symbol = Doc("SYMBOL", id_for(ref, "symbol"), [])
    device = Doc("DEVICE", id_for(ref, "device"), [])
    part = "part"
    per_side = math.ceil(len(rows) / 2) if len(rows) > 12 else len(rows)
    top = per_side * 10 + 5
    width = max(65, math.ceil((10 + max(len(row["pin_name"]) for row in rows) * 4) / 5) * 5)
    designator = re.sub(r"\d.*", "?", ref)
    symbol.meta({"title": model, "description": "Interfaz según matriz", "tags": [],
                 "docType": 2, "source": ""})
    symbol.canvas()
    symbol.add("PART", {"title": model, "BBOX": [-width, top, width, -top]}, part)
    symbol.rect(-width, -top, width, top, part=part)
    symbol.attr("", "Designator", designator, part=part)
    for index, row in enumerate(rows):
        side = -1 if index < per_side else 1
        y = (per_side - 1) * 10 - (index % per_side) * 20
        endpoint = side * (width + 15)
        pin = symbol.body("PIN", part, x=endpoint, y=y, length=15,
                          rotation=0 if side == -1 else 180, display=True,
                          color=None, pinShape="NONE")
        symbol.attr(pin, "Pin Name", row["pin_name"], x=side * (width - 5),
                    y=y + 1, visible=True, part=part, fontSize=9, color=BLUE,
                    align="LEFT_MIDDLE" if side == -1 else "RIGHT_MIDDLE")
        symbol.attr(pin, "Pin Number", row["pin"], x=side * (width + 2),
                    y=y + 2, visible=True, part=part, fontSize=7,
                    align="RIGHT_BOTTOM" if side == -1 else "LEFT_BOTTOM")
        symbol.attr(pin, "Pin Type", PIN_TYPES.get(row.get("pin_type"), "Undefined"), part=part)
    device.meta({"title": model, "tags": [], "source": "", "images": [],
                 "attributes": {"Symbol": symbol.uuid, "Footprint": "", "Name": model,
                                "Designator": designator,
                                "Convert to PCB": "no" if external else "yes",
                                "Add into BOM": "yes"}})
    return symbol, device, None, collect_pins(symbol), "Interfaz trazada de la matriz"


def camera_part(rows, source_dir):
    """Adapt Adafruit's downloaded Fritzing symbol to the physical JP2 pin numbers."""
    source = source_dir / "Adafruit-OV5640-Camera-Breakout.fzpz"
    with zipfile.ZipFile(source) as archive:
        filename = next(name for name in archive.namelist() if name.startswith("svg.schematic."))
        drawing = ET.fromstring(archive.read(filename))
    symbol, device, _, _, _ = interface_part(rows, external=True)
    # Fritzing connector IDs 46–63 correspond to the numbered JP2 contacts.
    terminals = {element.get("id"): element.attrib for element in drawing.iter()
                 if (element.get("id") or "").endswith("terminal")}
    body = next(element for element in drawing.iter() if element.tag.endswith("}rect")
                and element.get("stroke") == "#000000")
    x0 = float(body.get("x"))
    y0 = float(body.get("y"))
    width = float(body.get("width"))
    height = float(body.get("height"))
    scale = 2
    center_x, center_y = x0 + width / 2, y0 + height / 2
    rect = next(data for kind, _, data in symbol.rows if kind == "RECT")
    rect.update({"dotX1": -width, "dotX2": width, "dotY1": -height, "dotY2": height})
    symbol.rows[2][2]["BBOX"] = [-width, height, width, -height]
    attrs = defaultdict(dict)
    for kind, _, data in symbol.rows:
        if kind == "ATTR":
            attrs[data["parentId"]][data["key"]] = data
    for number, (pin_id, pin) in collect_pins(symbol).items():
        terminal = terminals[f"connector{45 + int(number)}terminal"]
        labels = attrs[pin_id]
        if "points" in terminal:
            coordinates = [tuple(map(float, point.split(","))) for point in terminal["points"].split()]
            tx = (min(x for x, _ in coordinates) + max(x for x, _ in coordinates)) / 2
            ty = coordinates[0][1]
            top = ty < y0
            endpoint_x = round((tx - center_x) * scale / 5) * 5
            endpoint_y = round((center_y - ty) * scale / 5) * 5
            inward = -1 if top else 1
            pin.update(x=endpoint_x, y=endpoint_y, length=round(abs(endpoint_y) - height, 2),
                       rotation=90 if top else 270)
            labels["Pin Name"].update(x=endpoint_x, y=(height - 9) * -inward,
                                      align="CENTER_MIDDLE")
            labels["Pin Number"].update(x=endpoint_x + 5, y=endpoint_y + inward * 12,
                                        align="LEFT_MIDDLE")
        else:
            tx = float(terminal["x"])
            ty = float(terminal["y"]) + float(terminal["height"]) / 2
            endpoint_x = round((tx - center_x) * scale / 5) * 5
            endpoint_y = round((center_y - ty) * scale / 5) * 5
            left = tx < x0
            inward = 1 if left else -1
            pin.update(x=endpoint_x, y=endpoint_y, length=round(abs(endpoint_x) - width, 2),
                       rotation=0 if left else 180)
            labels["Pin Name"].update(x=-inward * (width - 4), y=endpoint_y,
                                      align="LEFT_MIDDLE" if left else "RIGHT_MIDDLE")
            labels["Pin Number"].update(x=endpoint_x + inward * 10, y=endpoint_y + 1,
                                        align="LEFT_BOTTOM" if left else "RIGHT_BOTTOM")
    model_url = "https://learn.adafruit.com/adafruit-ov5640-camera-breakout/downloads"
    symbol.rows[0][2].update(source=model_url, description="Símbolo Fritzing adaptado a JP2")
    device.rows[0][2].update(source=model_url)
    device.rows[0][2]["attributes"]["Source"] = source.name
    return symbol, device, None, collect_pins(symbol), source.name + " · adaptación a JP2"


def stamp_component(doc, rows, part, x, y):
    symbol, device, footprint, pins, _ = part
    row = rows[0]
    ref, model = row["ref"], row["model"]
    part_id = next(key for kind, key, _ in symbol.rows if kind == "PART")
    unique_id = id_for(ref, "instance")
    # Turn library symbols with vertical pins to keep dense labels in separate rows.
    rotation = 90 if all(p["rotation"] % 180 for _, p in pins.values()) else 0
    component = doc.body("COMPONENT", part_id, x=x, y=y, rotation=rotation,
                         isMirror=False, attrs={"Unique ID": unique_id})
    doc.attr(component, "Device", device.uuid)
    doc.attr(component, "Symbol", symbol.uuid)
    doc.attr(component, "Unique ID", unique_id)
    if footprint:
        doc.attr(component, "Footprint", footprint.uuid)
    body_top = max(turn(pin["x"], pin["y"], -rotation)[1] for _, pin in pins.values())
    vertical_stub = any((pin["rotation"] + rotation) % 360 == 90 for _, pin in pins.values())
    label_y = y + body_top + (64 if vertical_stub else 32)
    doc.attr(component, "Designator", ref, x=x, y=label_y + 12, visible=True,
             fontSize=12, fontWeight=True, color=BLUE, align="CENTER_BOTTOM")
    doc.attr(component, "Name", model, x=x, y=label_y, visible=True,
             fontSize=9, color=GRAY, align="CENTER_BOTTOM")
    if row.get("note"):
        doc.text(x, label_y - 12, row["note"], 8, color=GRAY, align="CENTER_BOTTOM")
    for row in rows:
        pin_id, pin = pins[row["pin"]]
        dx0, dy0 = turn(pin["x"], pin["y"], -rotation)
        pin_x, pin_y = x + dx0, y + dy0
        angle = math.radians((pin["rotation"] + rotation) % 360)
        dx, dy = -round(math.cos(angle)), round(math.sin(angle))
        if not row["net"]:
            doc.attr(component + "-" + pin_id, "NO_CONNECT", "yes", x=pin_x, y=pin_y)
            continue
        end_x, end_y = pin_x + dx * 35, pin_y + dy * 25
        wire = doc.body("WIRE")
        doc.add("LINE", {"lineGroup": wire, "startX": pin_x, "startY": pin_y,
                         "endX": end_x, "endY": end_y, "strokeColor": None,
                         "strokeStyle": None, "fillColor": None, "strokeWidth": None,
                         "fillStyle": None})
        align = "RIGHT_BOTTOM" if dx < 0 else "LEFT_BOTTOM"
        doc.attr(wire, "NET", row["net"], x=end_x, y=end_y + 2, visible=True,
                 color="#2e5649", fontSize=8, align=align)


def build(matrix, converter, work):
    sections = load_matrix(matrix)
    board = Doc("BOARD", id_for("board"), [])
    sch = Doc("SCH", id_for("schematic"), [])
    config = Doc("CONFIG", "CONFIG", [])
    board.meta({"title": "FoodScan", "zIndex": -1})
    sch.meta({"title": "FoodScan", "source": "", "board": board.uuid, "zIndex": -1})
    config.add("UNIVERSAL", {
        "allowLibRename": True, "defaultNetName": True, "wireMultipleNet": False,
        "netFlagCrossLayerConnection": True, "netLabelCrossPageConnection": True,
        "busGenerateNetClass": True, "relevanceDisplayRow": "SINGLE",
        "relevanceBelongSchPage": "NAME", "relevanceLocation": "ZONE",
    }, "UNIVERSAL")
    pages, library = [], []
    report = {}
    for index, (section, components) in enumerate(sections.items(), start=1):
        page = Doc("SCH_PAGE", id_for("sheet", section), [])
        page.meta({"title": section, "schematic": sch.uuid, "source": "", "zIndex": index})
        page.canvas()
        pages.append(page)
        external = not section.startswith("01")
        page.text(35, -40, "FoodScan | " + section, 23, bold=True)
        page.text(35, -58, "Mismo nombre de red = conexión eléctrica entre hojas.", 10, color=GRAY)
        page.text(35, -74, "JLCEDA/EasyEDA Official Library · https://lceda.cn/ · https://easyeda.com", 8, color=GRAY)
        if external:
            page.text(35, -90, "Módulos y arneses externos. Referencias excluidas de la PCB auxiliar.", 8, color=GRAY)
        y = -185
        parts = list(components.values())
        for start in range(0, len(parts), 3):
            batch = parts[start:start + 3]
            bodies = []
            for col, rows in enumerate(batch):
                ref = rows[0]["ref"]
                part = downloaded_part(rows, matrix.parent / "fuentes", converter, work,
                                       external=external)
                if part is None:
                    part = (camera_part(rows, matrix.parent / "fuentes") if ref == "CAM1"
                            else interface_part(rows, external=external))
                library.extend(doc for doc in part[:3] if doc is not None)
                bodies.append(part)
                report[ref] = {"symbol_source": part[4], "pins": len(part[3]),
                               "footprint": part[2].uuid if part[2] else None}
            height = max(max(abs(p["y"]) for _, p in part[3].values()) for part in bodies)
            height = max(math.ceil(height / 5) * 5, 40)
            for col, (rows, part) in enumerate(zip(batch, bodies)):
                stamp_component(page, rows, part, 255 + col * 470, y - height + 40)
            y -= height * 2 + 120
        page.rect(15, y + 55, 470 * min(3, len(parts)) - 10, -16, color="#9eaab6")
    config.meta({"defaultSheet": pages[0].uuid})
    return [config, *library, board, sch, *pages], report


def kicad_converter_input(source, work):
    """Map KiCad 10 named net records to the indexed form EasyEDA imports."""
    text = source.read_text(encoding="utf-8")
    named = r'(\([ \t]*(pad|segment|arc|via|zone)\b[^\n]*\n)|^([ \t]*)\(net ("(?:\\.|[^"\\])*")\)[ \t]*$'
    names = sorted({match.group(4) for match in re.finditer(named, text, re.MULTILINE)
                    if match.group(4) and match.group(4) != '""'})
    if not names:
        return source
    indices = {name: i for i, name in enumerate(names, start=1)} | {'""': 0}
    context = ""

    def replace(match):
        nonlocal context
        if match.group(1):
            context = match.group(2)
            return match.group(0)
        indent, name = match.group(3), match.group(4)
        idx = indices[name]
        if context == "zone":
            return f"{indent}(net {idx})\n{indent}(net_name {name})"
        if context in ("segment", "arc", "via"):
            return f"{indent}(net {idx})"
        return f"{indent}(net {idx} {name})"

    text = re.sub(named, replace, text, flags=re.MULTILINE)
    definitions = "\n".join(f"\t(net {idx} {name})"
                            for name, idx in sorted(indices.items(), key=lambda item: item[1]))
    text = re.sub(r"(?m)^(?=[ \t]*\(footprint )", definitions + "\n", text, count=1)
    path = work / "Auxiliar-compatible.kicad_pcb"
    path.write_text(text, encoding="utf-8")
    return path


def integrate_pcb(documents, matrix, converter, source, work, report):
    """Use the vendor converter's PCB geometry and link it to the schematic by reference."""
    conversion_input = kicad_converter_input(source, work)
    _, pcb_docs = parse_archive(convert(converter, conversion_input, "kicad", work))
    pcb = next(doc for doc in pcb_docs if doc.kind == "PCB")
    devices = {doc.uuid: doc for doc in pcb_docs if doc.kind == "DEVICE"}
    footprints = {doc.uuid: doc for doc in pcb_docs if doc.kind == "FOOTPRINT"}
    board = next(doc for doc in documents if doc.kind == "BOARD")
    pcb.rows[0][2].update({"title": "Placa auxiliar", "board": board.uuid})
    page = next(doc for doc in documents if doc.kind == "SCH_PAGE")
    onboard = next(iter(load_matrix(matrix).values()))
    pcb_attrs = defaultdict(dict)
    sch_attrs = defaultdict(dict)
    pcb_pads = defaultdict(dict)
    for kind, key, data in pcb.rows:
        if kind == "ATTR" and data["parentId"]:
            pcb_attrs[data["parentId"]][data["key"]] = data
        if kind == "PAD_NET":
            _, component, number, _ = json.loads(key)
            pcb_pads[component][number] = data["padNet"]
    for kind, _, data in page.rows:
        if kind == "ATTR":
            sch_attrs[data["parentId"]][data["key"]] = data
    pcb_refs = {data["value"]: parent for parent, attrs in pcb_attrs.items()
                if (data := attrs.get("Designator"))}
    sch_refs = {data["value"]: parent for parent, attrs in sch_attrs.items()
                if (data := attrs.get("Designator"))}
    missing = set(onboard) - set(pcb_refs)
    if missing:
        raise ValueError(f"La PCB no contiene estas referencias: {sorted(missing)}")
    sources = {doc.uuid: doc for doc in documents}
    replaced, added = set(), {}
    for ref, parent in pcb_refs.items():
        attrs = pcb_attrs[parent]
        pcb_dev = devices[attrs["Device"]["value"]]
        pcb_footprint = footprints[pcb_dev.rows[0][2]["attributes"]["Footprint"]]
        added[pcb_footprint.uuid] = pcb_footprint
        if ref not in onboard:
            if any(pcb_pads[parent].values()):
                raise ValueError(f"{ref}: referencia eléctrica de la PCB ausente del esquema")
            added[pcb_dev.uuid] = pcb_dev
            continue
        expected = {row["pin"]: row["net"] for row in onboard[ref]}
        physical_pads = {p["num"] for kind, _, p in pcb_footprint.rows if kind == "PAD" and p["num"]}
        if expected.keys() != physical_pads:
            raise ValueError(f"{ref}: la numeración de los pads de la PCB difiere del esquema")
        found = {pin: pcb_pads[parent].get(pin, "") for pin in physical_pads}
        if expected != found:
            raise ValueError(f"{ref}: redes de la PCB {found} y esquema {expected} diferentes")
        sch_parent = sch_refs[ref]
        sch_dev = sources[sch_attrs[sch_parent]["Device"]["value"]]
        sch_dev_attrs = sch_dev.rows[0][2]["attributes"]
        if old_footprint := sch_dev_attrs.get("Footprint"):
            replaced.add(old_footprint)
        sch_dev_attrs["Footprint"] = pcb_footprint.uuid
        if "Footprint" in sch_attrs[sch_parent]:
            sch_attrs[sch_parent]["Footprint"]["value"] = pcb_footprint.uuid
        else:
            page.attr(sch_parent, "Footprint", pcb_footprint.uuid)
        attrs["Device"]["value"] = sch_dev.uuid
        if "Footprint" in attrs:
            attrs["Footprint"]["value"] = pcb_footprint.uuid
        instance = next(data for kind, key, data in pcb.rows
                        if kind == "COMPONENT" and key == parent)
        instance["attrs"]["Unique ID"] = id_for(ref, "instance")
        report[ref]["footprint"] = pcb_footprint.uuid
        report[ref]["footprint_source"] = pcb_footprint.rows[0][2]["title"]
    documents = [doc for doc in documents if doc.uuid not in replaced]
    documents[1:1] = added.values()
    documents.append(pcb)
    return documents


def validate(path, matrix):
    _, docs = parse_archive(path)
    by_id = {doc.uuid: doc for doc in docs}
    expected = load_matrix(matrix)
    found = {}
    for doc in docs:
        if doc.kind != "SCH_PAGE":
            continue
        attrs = defaultdict(dict)
        locations = {}
        for kind, key, data in doc.rows:
            if kind == "ATTR":
                attrs[data["parentId"]][data["key"]] = data["value"]
            if kind == "LINE":
                location = (data["startX"], data["startY"])
                if location in locations:
                    raise ValueError(f"Dos cables con el mismo origen: {location}")
                locations[location] = data["lineGroup"]
        for kind, key, data in doc.rows:
            if kind != "COMPONENT":
                continue
            comp = attrs[key]
            ref = comp.get("Designator")
            if not ref:
                continue
            model_pins = collect_pins(by_id[comp["Symbol"]])
            found[ref] = {}
            for num, (pin_id, pin) in model_pins.items():
                x, y = turn(pin["x"], pin["y"], -data["rotation"])
                point = (data["x"] + x, data["y"] + y)
                wire = locations.get(point)
                nc = attrs.get(key + "-" + pin_id, {}).get("NO_CONNECT") == "yes"
                if (wire is None) != nc:
                    raise ValueError(f"{ref}.{num}: requiere un único cable o marca NC")
                found[ref][num] = attrs[wire]["NET"] if wire else ""
    nets = Counter()
    for section in expected.values():
        for ref, pins in section.items():
            pin_values = {r["pin"]: r["net"] for r in pins}
            if set(pin_values) != set(found[ref]) and all(p.startswith(("J1.", "J3.")) for p in pin_values):
                pin_values = {str(int(k[3:]) if k.startswith("J1.") else 45 - int(k[3:])): v
                              for k, v in pin_values.items()}
            if pin_values != found[ref]:
                raise ValueError(f"{ref}: redes diferentes\n{pin_values}\n{found[ref]}")
            nets.update(value for value in pin_values.values() if value)
    if len(found) != sum(len(section) for section in expected.values()):
        raise ValueError("Hay componentes adicionales en el esquemático")
    return {"components": len(found), "pages": sum(d.kind == "SCH_PAGE" for d in docs),
            "connected_pins": sum(nets.values()), "nets": len(nets),
            "explicit_nc": sum(len(pins) for pins in found.values()) - sum(nets.values())}


def inspect_pcb(board):
    dimensions = []
    power_tracks = Counter()
    pours = []
    for kind, _, data in board.rows:
        if kind == "POLY" and data.get("polyType") == "BOARD_OUTLINE":
            points = [value for value in data["path"] if isinstance(value, (int, float))]
            dimensions.append([round((max(axis) - min(axis)) * 0.0254, 3)
                               for axis in (points[::2], points[1::2])])
        elif kind == "LINE" and data["netName"] in {"5V_SW", "3V3_AUX", "LED_RET_A", "LED_RET_B"}:
            power_tracks[(data["netName"], round(data["width"] * 0.0254, 3))] += 1
        elif kind == "POUR":
            pours.append({field: data[field] for field in ("netName", "layerId", "path")})
    return {"outline_mm": dimensions,
            "power_tracks": [{"net": net, "width_mm": width, "segments": count}
                             for (net, width), count in sorted(power_tracks.items())],
            "pours": sorted(pours, key=lambda pour: pour["layerId"])}


def export_svg(converter, project, target, docs, work):
    options = work / "svg-options.json"
    options.write_text(json_text({
        "decodingOptions": {"decodingType": "easyeda-pro-2", "decodingFilePath": str(project)},
        "encodingOptions": {"encodingType": "svg", "savingDirPath": str(work),
                            "savingFileName": "preview"},
    }), encoding="utf-8")
    converted = subprocess.run(["node", str(converter), "--cmd", "conversion",
                                "--params-path", str(options)], capture_output=True,
                               text=True, encoding="utf-8", errors="replace", timeout=75)
    if converted.returncode or "success: true" not in converted.stdout:
        raise RuntimeError(converted.stdout[-2500:] + converted.stderr[-2500:])
    svg_namespace = "http://www.w3.org/2000/svg"
    ET.register_namespace("", svg_namespace)
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    pages = {doc.uuid: doc for doc in docs if doc.kind == "SCH_PAGE"}
    target.mkdir(parents=True, exist_ok=True)
    result = []
    with zipfile.ZipFile(work / "preview.zip") as archive:
        for name in archive.namelist():
            if not name.startswith("schematics/") or not name.endswith(".svg"):
                continue
            drawing = ET.fromstring(archive.read(name))
            page = pages[drawing.get("id")]
            canvas = next(child for child in drawing if child.get("id") == "canvas")
            # The converter draws the Y-up schematic coordinates directly in SVG.
            # Invert geometry as a group, then counter-invert every text around its anchor.
            canvas.set("transform", "scale(1 -1)")
            instances = {key: data for kind, key, data in page.rows if kind == "COMPONENT"}
            for group in canvas:
                instance = instances.get(group.get("id"))
                if not instance:
                    continue
                element = group.find(f"{{{svg_namespace}}}use")
                if element is not None:
                    x, y = instance["x"], instance["y"]
                    symbol_id = element.get("{http://www.w3.org/1999/xlink}href", "")[1:]
                    svg_symbol = next(child for child in canvas if child.get("id") == symbol_id)
                    local_x, local_y, _, _ = map(float, svg_symbol.get("viewBox").split())
                    element.set("x", f"{x + local_x:g}")
                    element.set("y", f"{y + local_y:g}")
                    element.attrib.pop("transform-origin", None)
                    element.set("transform", f"rotate({-instance['rotation']} {x:g} {y:g})")
            for element in canvas.iter(f"{{{svg_namespace}}}text"):
                x, y = float(element.get("x", "0")), float(element.get("y", "0"))
                transform = element.get("transform", "")
                element.set("transform", f"translate({x:g},{y:g}) scale(1,-1) "
                            f"translate({-x:g},{-y:g}) {transform}")
                if element.get("text-anchor") == "center":
                    element.set("text-anchor", "middle")
                if element.get("font-weight") == "7px":
                    element.attrib.pop("font-weight")
            border = next(data for kind, _, data in reversed(page.rows)
                          if kind == "RECT" and data.get("strokeColor") == "#9eaab6")
            xmin, ymin, xmax, ymax = (border[k] for k in ("dotX1", "dotY1", "dotX2", "dotY2"))
            width, height = xmax - xmin + 24, ymax - ymin + 24
            drawing.attrib.pop("style", None)
            drawing.set("viewBox", f"{xmin - 12:g} {-ymax - 12:g} {width:g} {height:g}")
            drawing.set("width", str(width))
            drawing.set("height", str(height))
            filename = target / Path(name).name
            ET.ElementTree(drawing).write(filename, encoding="utf-8", xml_declaration=True)
            result.append(filename.name)
    if len(result) != len(pages):
        raise ValueError("El conversor no produjo todas las vistas SVG")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=ROOT / "Matriz_conexiones.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "easyeda" / "FoodScan.epro2")
    parser.add_argument("--converter", type=Path)
    parser.add_argument("--pcb", type=Path, help="Placa KiCad que vincular al esquemático")
    parser.add_argument("--svg", type=Path, help="Directorio de vistas del esquemático")
    args = parser.parse_args()
    converter = args.converter
    if converter is None:
        base = Path(os.environ.get("ProgramFiles", "C:/Program Files"))
        converter = next((base / "easyeda-pro" / "resources" / "app" / "assets" /
                          "chameleon").rglob("convert-node-server.js"), None)
    if converter is None:
        parser.error("Indica la ruta a convert-node-server.js con --converter")
    matrix = args.matrix.resolve()
    output = args.output.resolve()
    with tempfile.TemporaryDirectory(prefix="foodscan-easyeda-") as temp:
        work = Path(temp)
        docs, report = build(matrix, converter, work)
        if args.pcb:
            docs = integrate_pcb(docs, matrix, converter, args.pcb.resolve(), work, report)
        write_archive(output, docs)
        validation = validate(output, matrix)
        # The official converter reopens the native log with a distinct implementation.
        roundtrip = convert(converter, output, "easyeda-pro-2", work)
        _, reopened = parse_archive(roundtrip)
        counts = Counter(doc.kind for doc in reopened)
        components = sum(kind == "COMPONENT" for doc in reopened if doc.kind == "SCH_PAGE"
                         for kind, _, _ in doc.rows)
        if counts["SCH_PAGE"] != validation["pages"] or components != validation["components"]:
            raise ValueError(f"El conversor de EasyEDA perdió elementos: {counts}, {components}")
        validation["vendor_converter"] = {"pages": counts["SCH_PAGE"], "components": components,
                                          "symbols": counts["SYMBOL"], "footprints": counts["FOOTPRINT"]}
        if args.pcb:
            board = next(doc for doc in docs if doc.kind == "PCB")
            reopened_pcb = next((doc for doc in reopened if doc.kind == "PCB"), None)
            if reopened_pcb is None:
                raise ValueError("El conversor no recuperó la PCB")
            wanted = ("COMPONENT", "PAD_NET", "LINE", "VIA", "POUR")
            original_counts = Counter(kind for kind, _, _ in board.rows if kind in wanted)
            reopened_counts = Counter(kind for kind, _, _ in reopened_pcb.rows if kind in wanted)
            if original_counts != reopened_counts:
                raise ValueError(f"La PCB perdió elementos al reabrir: {original_counts} → {reopened_counts}")
            validation["pcb_vendor_converter"] = dict(reopened_counts)
            geometry = inspect_pcb(board)
            if geometry != inspect_pcb(reopened_pcb):
                raise ValueError("El contorno, pistas de potencia o planos cambiaron al reabrir")
            validation["pcb_geometry"] = geometry
        if args.svg:
            validation["svg"] = export_svg(converter, output, args.svg.resolve(), docs, work)
    validation["library_sources"] = report
    output.with_name("Verificacion_EasyEDA.json").write_text(
        json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(validation, ensure_ascii=True))


if __name__ == "__main__":
    main()

"""Generate millimetre STEP solids from the original camera and DevKitC CAD."""

from math import hypot, radians, tan
from pathlib import Path
from xml.etree import ElementTree

import cadquery as cq


DIRECTORY = Path(__file__).resolve().parent
ORIGINALS = DIRECTORY / "originals"

# Local camera datums: x centred, y=0 at the straight pin-header edge.
# z=0 at the lens-side PCB face. +z is the nominal optical axis.
CAMERA_PCB_THICKNESS = 1.57  # Eagle stack design values; confirm on sample.
CAMERA_OPTICAL_XY = (0.20, 30.65)  # Photo registration, confirm on sample.
CAMERA_HOLE_CENTRES = ((-8.89, 33.02), (8.89, 33.02))
CAMERA_FOCUS_HEIGHT = 5.10  # FD5640 drawing, regular focus position.

# Local DevKit datums: x=0 at the left PCB edge (UART port side),
# y=0 at the connector end, z=0 at the lower face of the PCB.
ESP_PCB_THICKNESS = 1.60  # Third-party nominal; confirm on the board.
ESP_USB_PORT_CENTRES_X = (6.0, 19.4)


def camera_board(thickness=CAMERA_PCB_THICKNESS):
    """Build the board outline, mounting bores and header holes from Eagle."""
    board = ElementTree.parse(ORIGINALS / "Adafruit-OV5640-Breakout.brd").find(".//board")
    outline = board.findall("./plain/wire[@layer='20']")
    offset = max(float(edge.get("x2")) for edge in outline) / 2
    profile = cq.Workplane("XY").moveTo(offset - float(outline[0].get("x1")), 0)
    for edge in outline:
        x1, y1, x2, y2 = (
            float(edge.get(key)) for key in ("x1", "y1", "x2", "y2")
        )
        x1 = offset - x1
        x2 = offset - x2
        angle = -float(edge.get("curve", 0))
        if angle:
            # The lens-side view mirrors the source board, reversing the arc angle.
            sagitta_ratio = -tan(radians(angle) / 4) / 2
            midpoint = (
                (x1 + x2) / 2 - (y2 - y1) * sagitta_ratio,
                (y1 + y2) / 2 + (x2 - x1) * sagitta_ratio,
            )
            profile = profile.threePointArc(midpoint, (x2, y2))
        else:
            profile = profile.lineTo(x2, y2)

    pcb = profile.close().extrude(-thickness)
    for name in ("U$1", "U$17", "JP1", "JP2"):
        element = board.find(f"./elements/element[@name='{name}']")
        x, y = (float(element.get(key)) for key in ("x", "y"))
        library = board.find(f"./libraries/library[@name='{element.get('library')}']")
        package = library.find(f"./packages/package[@name='{element.get('package')}']")
        if element.get("rot") != "MR0":
            raise ValueError(f"Unexpected rotation on Eagle element {name}")
        for pad in package.findall("pad"):
            # Reflect Eagle top-view x once more for the lens-side convention.
            local_x = offset - x + float(pad.get("x"))
            local_y = y + float(pad.get("y"))
            drill = float(pad.get("drill"))
            pcb = pcb.cut(
                cq.Solid.makeCylinder(
                    drill / 2, thickness, cq.Vector(local_x, local_y, -thickness)
                )
            )
    return pcb.val()


def camera_optical_envelope(
    optical_xy=CAMERA_OPTICAL_XY, focus_height=CAMERA_FOCUS_HEIGHT
):
    """FD5640 external envelope from its drawing, with provisional board registration."""
    body_width = 8.50
    backing_length = 8.70
    backing_thickness = 0.20
    x, y = optical_xy
    body = (
        cq.Workplane("XY")
        .box(
            body_width,
            body_width,
            focus_height - backing_thickness,
            centered=(True, True, False),
        )
        .edges("|Z")
        .fillet(0.5)
        .translate((x, y, backing_thickness))
        .val()
    )
    backing = (
        cq.Workplane("XY")
        .box(body_width, backing_length, backing_thickness, centered=(True, True, False))
        .edges("|Z")
        .fillet(0.5)
        .translate((x, y + (backing_length - body_width) / 2, 0))
        .val()
    )
    return cq.Compound.makeCompound([body, backing])


def camera_model(
    optical_xy=CAMERA_OPTICAL_XY,
    focus_height=CAMERA_FOCUS_HEIGHT,
    thickness=CAMERA_PCB_THICKNESS,
):
    """Camera PCB and FD5640 envelope. The folded flex and fitted header are pending."""
    return cq.Compound.makeCompound(
        [camera_board(thickness), camera_optical_envelope(optical_xy, focus_height)]
    )


def dxf_entities():
    """Read 2D polyline vertices in the official DevKitC-1 v1.1 CAD."""
    source = ORIGINALS / "ESP32-S3-DevKitC-1-v1.1.dxf"
    fields = source.read_text(encoding="gbk", errors="replace").splitlines()
    codes = list(zip(map(str.strip, fields[::2]), map(str.strip, fields[1::2])))
    start = codes.index(("2", "ENTITIES")) + 1
    fields = []
    for code, value in codes[start:]:
        if code == "0":
            if fields and fields[0][1] == "LWPOLYLINE":
                properties = dict(fields)
                xs = [float(v) for k, v in fields if k == "10"]
                ys = [float(v) for k, v in fields if k == "20"]
                yield properties["8"], int(properties["70"]), tuple(zip(xs, ys))
            if value == "ENDSEC":
                break
            fields = []
        fields.append((code, value))


def esp32_board(thickness=ESP_PCB_THICKNESS):
    """Build the ESP32 DevKitC PCB outline and GPIO bores from Espressif DXF."""
    entities = list(dxf_entities())
    profile = {
        point
        for layer, closed, vertices in entities
        if layer == "BOARD_OUTLINE" and not closed
        for point in vertices
    }
    width = max(x for x, y in profile)
    length = max(y for x, y in profile)
    radius = min(x for x, y in profile if x > 0)
    pcb = (
        cq.Workplane("XY")
        .box(width, length, thickness, centered=(False, False, False))
        .edges("|Z")
        .fillet(radius)
    )

    drills = {
        tuple(sorted(vertices[:2]))
        for layer, _, vertices in entities
        if layer == "TOOL_BOT"
        and len(vertices) == 3
        and vertices[0] == vertices[-1]
        and abs(vertices[0][1] - vertices[1][1]) < 1e-8
    }
    if len(drills) != 44:
        raise ValueError(f"Expected 44 GPIO holes, extracted {len(drills)}")
    for (x1, y1), (x2, y2) in drills:
        pcb = pcb.cut(
            cq.Solid.makeCylinder(
                hypot(x2 - x1, y2 - y1) / 2,
                thickness,
                cq.Vector((x1 + x2) / 2, y1, 0),
            )
        )
    return pcb.val()


def esp32_module(thickness=ESP_PCB_THICKNESS):
    """Place the unmodified manufacturer STEP for the ESP32-S3-WROOM-1 package."""
    module = cq.importers.importStep(str(ORIGINALS / "Espressif-ESP32-S3-WROOM-1.step"))
    return module.val().translate((3.75, 69.14 - 25.50, thickness))


def esp32_model(thickness=ESP_PCB_THICKNESS):
    """DXF-derived DevKitC PCB with the original WROOM-1 manufacturer package."""
    return cq.Compound.makeCompound([esp32_board(thickness), esp32_module(thickness)])


def export_step_models():
    for filename, model in (
        ("Adafruit-5838-referencia-parcial.step", camera_model()),
        ("ESP32-S3-DevKitC-1-v1.1-referencia-parcial.step", esp32_model()),
    ):
        if not model.isValid():
            raise ValueError(f"Invalid geometry: {filename}")
        path = DIRECTORY / filename
        cq.exporters.export(model, str(path))
        imported = cq.importers.importStep(str(path)).val()
        if not imported.isValid() or len(imported.Solids()) != len(model.Solids()):
            raise ValueError(f"STEP round-trip failed: {filename}")
        bounds = imported.BoundingBox()
        size = (bounds.xlen, bounds.ylen, bounds.zlen)
        print(f"{filename}: {len(imported.Solids())} solids, " + " × ".join(f"{v:.3f}" for v in size))


if __name__ == "__main__":
    export_step_models()

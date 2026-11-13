from dataclasses import dataclass
from pathlib import Path

import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]
V = cq.Vector


@dataclass(frozen=True)
class Item:
    key: str
    label: str
    system: str
    shape: cq.Shape
    color: tuple
    material: str = ""
    method: str = "compra"
    native: cq.Shape | None = None
    part_id: str = ""
    state: str = "diseno"
    door: bool = False


def box(x0, y0, z0, x1, y1, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def cylinder(radius, length, xyz, direction=(0, 0, 1)):
    return cq.Solid.makeCylinder(radius, length, V(*xyz), V(*direction))


def cut_holes(shape, points, diameter, depth, start_z=-0.1):
    for x, y in points:
        shape = shape.cut(cylinder(diameter / 2, depth + 0.2, (x, y, start_z)))
    return shape


def xy_panel(bounds, thickness, holes=(), windows=(), diameter=3.4):
    x0, y0, x1, y1 = bounds
    shape = box(x0, y0, 0, x1, y1, thickness)
    for l, b, r, t in windows:
        shape = shape.cut(box(l, b, -0.1, r, t, thickness + 0.1))
    return cut_holes(shape, holes, diameter, thickness).clean()


def translate(shape, x=0, y=0, z=0):
    return shape.translate(V(x, y, z))


def orient(shape, origin, x_direction, normal):
    return shape.moved(cq.Plane(origin, xDir=x_direction, normal=normal).location)


def compound(shapes):
    return cq.Compound.makeCompound(list(shapes))


def read_step(path):
    data = cq.importers.importStep(str(path))
    return compound(data.vals())


def standard_screw(length, diameter=3.0):
    """ISO 4762 nominal fit envelope, plain shank and socket clearance."""
    head_diameter, head_height, across = (5.5, 3.0, 2.5) if diameter == 3.0 else (4.5, 2.5, 2.0)
    shank = cylinder(diameter / 2, length, (0, 0, 0))
    head = cylinder(head_diameter / 2, head_height, (0, 0, -head_height))
    socket = (cq.Workplane("XY").workplane(offset=-head_height - 0.01)
              .polygon(6, across / 0.866025403784).extrude(head_height * 0.6).val())
    return shank.fuse(head.cut(socket)).clean()


def m3_nut():
    blank = cq.Workplane("XY").polygon(6, 5.5 / 0.866025403784).extrude(2.4).val()
    return blank.cut(cylinder(1.5, 2.6, (0, 0, -0.1))).clean()

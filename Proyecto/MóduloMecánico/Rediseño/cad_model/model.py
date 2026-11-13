from dataclasses import replace
import unicodedata

import cadquery as cq

from .geometry import V, box, cylinder
from .integration import camera_mount, detector, display, electronics, leds, weighing
from .parameters import Design
from .structure import structure


def build(p=Design()):
    p.check()
    items = [
        *structure(p), *weighing(p), *camera_mount(p), *leds(p),
        *display(p), *electronics(p), *detector(p),
    ]
    keys = [item.key for item in items]
    if len(keys) != len(set(keys)):
        raise ValueError("Las claves de instancia deben ser únicas")
    return items


def door_position(items, p, angle, unlocked=False):
    hinge = V(p.hinge_x, p.hinge_y, 0)
    latch = V(p.latch_x, p.door_outer_y, 151)
    positioned = []
    for item in items:
        if item.door:
            shape = item.shape.rotate(hinge, hinge + V(0, 0, 1), -angle)
        elif unlocked and item.key == "P25":
            shape = item.shape.rotate(latch, latch + V(0, 1, 0), 180)
        else:
            positioned.append(item)
            continue
        positioned.append(replace(item, shape=shape))
    return positioned


def to_assembly(items, name):
    assembly = cq.Assembly(name=name)
    groups = {}
    for item in items:
        group = groups.setdefault(item.system, cq.Assembly(name=item.system))
        # Keep part numbers in the exported product names for Onshape and FreeCAD.
        label = f"{item.key} - {item.label.split(' · ')[0]}".replace("Ø", "dia ").replace("×", "x")
        label = unicodedata.normalize("NFKD", label).encode("ascii", "ignore").decode()
        group.add(item.shape, name=label, color=cq.Color(*item.color))
    for group in groups.values():
        assembly.add(group)
    return assembly


def reference_objects(p):
    return {
        "Plato maximo - envolvente de insercion": cylinder(
            p.dish_diameter / 2, p.dish_rim_height, (0, p.center_y, p.dish_z)
        ),
        "PCB auxiliar sin definir - volumen reservado": box(
            69, 223, p.shelf + p.panel + 3, 134, 296, p.lid_z - 7
        ),
        "Pesaje - volumen maximo reservado": box(
            -p.scale_size / 2, p.center_y - p.scale_size / 2, p.panel,
            p.scale_size / 2, p.center_y + p.scale_size / 2, p.panel + p.scale_reserve_height
        ),
        "USB - reserva para conector y extraccion": box(
            -110, 290, p.shelf + p.panel + 5, -75, p.inside_rear, p.lid_z - 8
        ),
        "Camara - zona de cabeceras a confirmar": box(
            -15, p.center_y + 23, p.shelf + p.panel + 8, 15, p.center_y + 48, p.lid_z - 5
        ),
    }

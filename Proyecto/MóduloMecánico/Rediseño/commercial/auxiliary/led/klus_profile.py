"""Build a cut length from the end section of the original KLUŚ OBJ.

The extrusion is a faceted conversion of the manufacturer's mesh in mm.
The installed cross-section occupies X=0..16 and Y=0..16. Its light points
toward (-1,-1,0). The mounting faces lie on X=16 and Y=16.
"""

from collections import Counter, defaultdict
from math import sqrt
from pathlib import Path

import cadquery as cq


SOURCE = Path(__file__).with_name("klus_A08504_original.obj")


def corner_datum(point):
    """Convert section coordinates in mm from the optical to mounting axes."""
    side, depth = point
    return (5 + (side + depth) / sqrt(2), 5 + (depth - side) / sqrt(2))


def manufacturer_section():
    """Walk the boundary of the triangulated planar end at native Z=0."""
    vertices = []
    triangles = []
    for line in SOURCE.read_text(encoding="utf-8").splitlines():
        fields = line.split()
        if fields and fields[0] == "v":
            vertices.append(tuple(map(float, fields[1:4])))
        if fields and fields[0] == "f":
            triangles.append(tuple(int(field.split("/")[0]) - 1 for field in fields[1:]))

    edges = Counter()
    for triangle in triangles:
        points = [vertices[index] for index in triangle]
        if any(point[2] != 0 for point in points):
            continue
        for start, end in zip(points, points[1:] + points[:1]):
            if start != end:
                edges[tuple(sorted((start[:2], end[:2])))] += 1

    neighbors = defaultdict(list)
    for (start, end), uses in edges.items():
        if uses == 1:
            neighbors[start].append(end)
            neighbors[end].append(start)
    if not neighbors or any(len(items) != 2 for items in neighbors.values()):
        raise ValueError("La sección del OBJ de KLUŚ no forma un contorno cerrado")

    first = min(neighbors)
    current = first
    previous = None
    section = []
    while current not in section:
        section.append(current)
        previous, current = current, next(point for point in neighbors[current] if point != previous)
    if current != first or len(section) != len(neighbors):
        raise ValueError("La sección del OBJ de KLUŚ contiene más de un contorno")

    return [corner_datum((100 * side, 100 * depth)) for side, depth in section]


def extrusion(length):
    """Return one solid of KLUŚ 45-16 cut to length along +Z."""
    return cq.Workplane("XY").polyline(manufacturer_section()).close().extrude(length).val()


def nominal_diffuser(length, front_depth=0):
    """Reconstruct the unstrained B17208 cover from the dimensioned drawing.

    12.5 mm width and 4 mm depth are published. The 2.1 mm base and the
    0.7 mm lips are measured from the drawing image. The nominal outline
    is a reference for the purchased part and does not model snap deflection.
    """
    half_width = 12.5 / 2
    inside = half_width - 0.7
    section = [
        (-half_width, 0),
        (half_width, 0),
        (half_width, 4),
        (inside, 4),
        (inside, 2.1),
        (-inside, 2.1),
        (-inside, 4),
        (-half_width, 4),
    ]
    section = [corner_datum((side, depth + front_depth)) for side, depth in section]
    return cq.Workplane("XY").polyline(section).close().extrude(length).val()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("length", type=float, help="longitud de corte en mm")
    parser.add_argument("output", type=Path, help="archivo STEP de salida")
    parser.add_argument("--diffuser", action="store_true", help="geometría de referencia de la tapa")
    args = parser.parse_args()
    profile = nominal_diffuser(args.length) if args.diffuser else extrusion(args.length)
    assert profile.isValid() and len(profile.Solids()) == 1
    cq.exporters.export(profile, str(args.output))

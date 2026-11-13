"""Referencias mecánicas del kit Best Modules BMH12M205, en milímetros."""

from pathlib import Path

import cadquery as cq


PLAN_X_MM = 120.0
PLAN_Y_MM = 120.0
MANUAL_HEIGHT_MM = 30.7
CATALOG_HEIGHT_MM = 36.4
INSTALLATION_HEIGHT_MM = 37.0


def _interface_face(z_mm: float) -> cq.Face:
    outline = cq.Workplane("XY", origin=(0, 0, z_mm)).rect(PLAN_X_MM, PLAN_Y_MM).val()
    return cq.Face.makeFromWires(outline)


def build_weighing_components(height_mm: float = MANUAL_HEIGHT_MM) -> dict[str, cq.Shape]:
    """Return projected plan faces at the support and unloaded platform datums.

    Both are reference surfaces. The lower face reserves the support footprint
    for the manufacturer's feet; the upper face locates the top of the moving
    plate. After measuring the received kit, pass its unloaded overall height.
    The actual plates, feet, load cell and harness require physical data.
    """
    return {
        "BMH12M205_Base_Fija_Interfaz": _interface_face(0.0),
        "BMH12M205_Plataforma_Movil_Interfaz": _interface_face(height_mm),
    }


def build_weighing_clearance() -> cq.Solid:
    """Return the hard-component keep-out including the disputed overall height."""
    lower_corner = cq.Vector(-PLAN_X_MM / 2, -PLAN_Y_MM / 2, 0)
    return cq.Solid.makeBox(PLAN_X_MM, PLAN_Y_MM, INSTALLATION_HEIGHT_MM, lower_corner)


def export_interface_step(path: Path) -> None:
    """Write just the reference faces as a named STEP assembly."""
    assembly = cq.Assembly(name="Best_Modules_BMH12M205_Interfaces_de_Referencia")
    for name, face in build_weighing_components().items():
        assembly.add(face, name=name)
    assembly.export(str(path))


if __name__ == "__main__":
    export_interface_step(Path(__file__).with_name("BMH12M205_interfaces_referencia.step"))

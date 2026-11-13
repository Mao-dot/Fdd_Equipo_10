"""Render the door-open assembly from the nominal CAD geometry."""

import vtk

from .geometry import ROOT
from .model import build, door_position, reference_objects
from .parameters import Design


def actor_for(shape, color, opacity=1):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(shape.toVtkPolyData(tolerance=0.005, angularTolerance=0.2, normals=True))
    mapper.ScalarVisibilityOff()
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    style = actor.GetProperty()
    style.SetColor(*color)
    style.SetOpacity(opacity)
    style.SetAmbient(0.38)
    style.SetDiffuse(0.68)
    style.SetSpecular(0.10)
    style.SetSpecularPower(15)
    return actor


def main():
    design = Design()
    items = door_position(build(design), design, design.door_angle, unlocked=True)
    scene = vtk.vtkRenderer()
    scene.SetBackground(0.97, 0.98, 0.985)
    scene.UseFXAAOn()
    for item in items:
        scene.AddActor(actor_for(item.shape, item.color, opacity=0.40 if item.key == "W01" else 1))
    plate = next(iter(reference_objects(design).values()))
    scene.AddActor(actor_for(plate, (0.23, 0.59, 0.65), opacity=0.42))
    window = vtk.vtkRenderWindow()
    window.SetOffScreenRendering(1)
    window.SetMultiSamples(0)
    window.SetSize(1440, 1120)
    window.AddRenderer(scene)
    camera = scene.GetActiveCamera()
    camera.SetFocalPoint(-45, 25, 185)
    camera.SetPosition(720, -1240, 820)
    camera.SetViewUp(0, 0, 1)
    camera.ParallelProjectionOn()
    camera.SetParallelScale(339)
    scene.ResetCameraClippingRange()
    window.Render()
    capture = vtk.vtkWindowToImageFilter()
    capture.SetInput(window)
    capture.ReadFrontBufferOff()
    capture.Update()
    writer = vtk.vtkPNGWriter()
    writer.SetFileName(str(ROOT / "exports" / "FoodScan_vista_abierta.png"))
    writer.SetInputConnection(capture.GetOutputPort())
    writer.Write()
    window.Finalize()


if __name__ == "__main__":
    main()

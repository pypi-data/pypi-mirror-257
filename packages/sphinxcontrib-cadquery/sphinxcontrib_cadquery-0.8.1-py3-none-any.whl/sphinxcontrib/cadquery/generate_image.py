"""
From [voneiden/ocp-freecad-cam: CAM for CadQuery and Build123d by leveraging FreeCAD](https://github.com/voneiden/ocp-freecad-cam)

https://github.com/voneiden/ocp-freecad-cam/blob/4813dc9fdf90fef397a64a9f07a2ff9981b5faff/docs/examples/generate_image.py
"""
from pathlib import Path

import cadquery as cq
from OCP.AIS import AIS_DisplayMode, AIS_InteractiveContext, AIS_Shaded, AIS_Shape
from OCP.Aspect import Aspect_DisplayConnection, Aspect_TypeOfTriedronPosition
from OCP.Image import Image_AlienPixMap
from OCP.OpenGl import OpenGl_GraphicDriver
from OCP.Quantity import Quantity_Color
from OCP.TCollection import TCollection_AsciiString
from OCP.TopoDS import (
    TopoDS_Compound,
    TopoDS_Edge,
    TopoDS_Face,
    TopoDS_Solid,
    TopoDS_Vertex,
    TopoDS_Wire,
)
from OCP.V3d import V3d_Viewer
from OCP.Xw import Xw_Window


def extract_topods_shapes(shape_source, compound=False):
    if isinstance(shape_source, list):
        shapes = []
        for source in shape_source:
            shapes += extract_topods_shapes(source, compound=compound)
        return shapes

    valid_cq_shapes = (
        [cq.Compound, cq.Solid] if compound else [cq.Face, cq.Wire, cq.Edge, cq.Vertex]
    )
    if isinstance(shape_source, cq.Workplane):
        return [
            shape.wrapped
            for shape in shape_source.objects
            if type(shape) in valid_cq_shapes
        ]
    elif type(shape_source) in valid_cq_shapes:
        return [shape_source.wrapped]

    valid_topods_shapes = (
        [TopoDS_Compound, TopoDS_Solid]
        if compound
        else [TopoDS_Face, TopoDS_Wire, TopoDS_Edge, TopoDS_Vertex]
    )
    if type(shape_source) in valid_topods_shapes:
        return [shape_source]

    raise ValueError(f"Unknown shape source of type {type(shape_source)}")


def render(shapes, output_path):
    display_connection = Aspect_DisplayConnection()
    graphic_driver = OpenGl_GraphicDriver(display_connection)
    viewer = V3d_Viewer(graphic_driver)
    viewer.SetDefaultLights()
    viewer.SetLightOn()

    context = AIS_InteractiveContext(viewer)
    context.SetDisplayMode(AIS_DisplayMode.AIS_Shaded, True)
    context.DefaultDrawer().SetFaceBoundaryDraw(True)
    view = viewer.CreateView()
    view.TriedronDisplay(
        Aspect_TypeOfTriedronPosition.Aspect_TOTP_RIGHT_LOWER, Quantity_Color(), 0.1
    )
    params = view.ChangeRenderingParams()
    params.NbMsaaSamples = 8
    params.IsAntialiasingEnabled = True
    window = Xw_Window(display_connection, "", 0, 0, 660, 495)
    window.SetVirtual(True)
    view.SetWindow(window)
    view.MustBeResized()

    for shape in shapes:
        context.Display(shape, False)

    view.FitAll()
    view.Redraw()

    image = Image_AlienPixMap()
    view.ToPixMap(image, 660, 495)
    image.Save(TCollection_AsciiString(output_path))


# def render_file(file_path, display_object_names, output_path):
#     with open(file_path, "r") as f:
#         ast = compile(f.read(), file_path, "exec")
#
#     _locals = {}
#     exec(ast, _locals)
#
#     display_shapes = []
#     for name in display_object_names:
#         obj = _locals[name]
#         if isinstance(obj, Job):
#             display_shapes.append(obj.show())
#         else:
#             shapes = extract_topods_shapes(obj)
#             if not shapes:
#                 shapes = extract_topods_shapes(obj, compound=True)
#             if not shapes:
#                 raise ValueError("No shapes found)")
#             ais_shapes = []
#             for shape_ in shapes:
#                 ais_shape = AIS_Shape(shape_)
#                 ais_shape.SetHilightMode(AIS_Shaded)
#                 ais_shapes.append(ais_shape)
#
#             display_shapes += ais_shapes
#
#     render(display_shapes, output_path)


def render_workplane(workplane: cq.Workplane, output_path: Path) -> None:
    """Render CadQuery Workplane as PNG image."""

    shapes = extract_topods_shapes(workplane)

    if not shapes:
        shapes = extract_topods_shapes(workplane, compound=True)
    if not shapes:
        raise ValueError("No shapes found)")

    ais_shapes = []
    for shape_ in shapes:
        ais_shape = AIS_Shape(shape_)
        ais_shape.SetHilightMode(AIS_Shaded)
        ais_shapes.append(ais_shape)

    render(ais_shapes, output_path.as_posix())


if __name__ == "__main__":
    result = cq.Workplane().box(1, 1, 0.5)
    render_workplane(result, Path("box.png"))

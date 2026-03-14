from fabric import Application
from fabric.widgets.box import Box
from fabric.widgets.x11 import X11Window as Window

from bezier_morph_shape import AnimateShapeMorph


class Pill(Window):
    def __init__(self, **kwargs):
        super().__init__(
            name="pill",
            layer="top",
            geometry="center",
            type_hint="normal",
            margin=(0, 0, 0, 0),
            visible=True,
            size=(400,400),
            all_visible=True,
        )
        self.children = Box(
            name="container",
            h_expand=True,
            v_expand=True,
            children=[
                # BezierShapeMorph(),
                AnimateShapeMorph(),
            ],
        )


if __name__ == "__main__":
    window = Pill()

    app_kwargs = {
        "shape-win": window,
        "open_inspector": False,
    }

    app = Application("cairo-shapes", **app_kwargs)
    app.run()

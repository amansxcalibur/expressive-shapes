from fabric import Application
from fabric.widgets.box import Box
from fabric.widgets.x11 import X11Window as Window

from shapes import Square, Triangle, ShapeMorph, BezierShapeMorph, AnimateShapeMorph

from fabric.utils import get_relative_path, monitor_file


class Pill(Window):
    def __init__(self, **kwargs):
        super().__init__(
            name="pill",
            layer="top",
            geometry="center",
            type_hint="normal",
            margin=(0, 0, 0, 0),
            visible=True,
            all_visible=True,
        )
        self.children = Box(
            name="container",
            h_expand=True,
            v_expand=True,
            children=[
                Square(),
                Triangle(),
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

    def set_css(*args):
        app.set_stylesheet_from_file(
            get_relative_path("./main.css"),
        )

    app.style_monitor = monitor_file(get_relative_path("./main.css"))
    app.style_monitor.connect("changed", set_css)
    set_css()

    app.run()

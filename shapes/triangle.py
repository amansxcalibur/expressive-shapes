import cairo
from typing import Tuple

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Triangle(Gtk.DrawingArea):
    def __init__(
        self,
        size: Tuple[int, int] = (140, 140),
        color: Tuple[float, float, float] = (0.2, 0.7, 0.3),
    ):
        super().__init__()
        self.set_size_request(*size)
        self.color = color
        self.connect("draw", self.on_draw)
        self.vertices = [(0.5, 0.1), (0.9, 0.8), (0.1, 0.8)]
        self.show()

    def on_draw(self, widget, ctx: cairo.Context):
        width = self.get_allocated_width()
        height = self.get_allocated_height()

        ctx.scale(width, height)
        ctx.set_source_rgb(*self.color)
        ctx.move_to(*self.vertices[0])
        for vert in self.vertices[1:]:
            ctx.line_to(*vert)

        ctx.close_path()

        ctx.fill()

        return False

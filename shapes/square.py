import cairo
from typing import Tuple

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Square(Gtk.DrawingArea):
    def __init__(
        self,
        size: Tuple[int, int] = (140, 140),
        dark: bool = False,
        override_color: Tuple[float, float, float] | None = None,
    ):
        super().__init__()
        self.set_size_request(*size)
        self.dark = dark
        self._override_color = override_color or (0.2, 0.4, 0.9)

        self.path = [
            (0.1, 0.1),
            (0.9, 0.1),
            (0.9, 0.9),
            (0.1, 0.9),
        ]
        self.connect("draw", self.on_draw)
        self.show()

    def on_draw(self, widget, ctx: cairo.Context):
        width = self.get_allocated_width()
        height = self.get_allocated_height()

        scale_factor = min(width, height)
        offset_x = (width - scale_factor) / 2
        offset_y = (height - scale_factor) / 2

        ctx.translate(offset_x, offset_y)
        ctx.scale(scale_factor, scale_factor)

        ctx.set_source_rgb(*self._override_color)

        ctx.move_to(*self.path[0])
        for vert in self.path[1:]:
            ctx.line_to(*vert)

        ctx.close_path()
        ctx.fill()

        return False

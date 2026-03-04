import math
import cairo
from pathlib import Path

from geometry.rounded_polygon import RoundedPolygon
from shapes.shape_presets import (
    star,
    clover_flower,
    organic_blob,
    puffy_square,
    pill,
    shield,
    concave_rectangle,
    cookie_12,
    cookie_8,
    fan,
    apple,
    t_apple,
    t_fan
)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"


def draw_material_shape(unit_data, filename="shape.png", size=1000, margin=0):
    draw_area = size - (margin * 2)

    verts = []
    per_vertex = []
    for (ux, uy), rounding_preset in unit_data:
        sx = margin + (ux * draw_area)
        sy = margin + (uy * draw_area)
        verts.extend([sx, sy])
        per_vertex.append(rounding_preset)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(0, 0, 0)  # black BG
    ctx.paint()

    poly = RoundedPolygon.create(vertices=verts, per_vertex_rounding=per_vertex)

    curves = poly.get_all_curves()
    if curves:
        ctx.move_to(curves[0].p0.x, curves[0].p0.y)
        for c in curves:
            ctx.curve_to(c.p1.x, c.p1.y, c.p2.x, c.p2.y, c.p3.x, c.p3.y)
        ctx.close_path()

    ctx.set_source_rgb(1.0, 1.0, 1.0)  # Dark Surface
    # ctx.fill_preserve()
    ctx.set_line_width(1)
    # ctx.set_source_rgb(0.3, 0.3, 0.3)  # Subtle Stroke
    ctx.stroke()

    # --- debug dots ---
    dot_radius = 6
    for c in curves:
        # anchors (p0, p3), control points (p1, p2)
        pts = [(c.p0, True), (c.p1, False), (c.p2, False), (c.p3, True)]

        for pt, is_anchor in pts:
            if is_anchor:
                ctx.set_source_rgb(0.0, 0.4, 1.0)  # Deep Blue
                ctx.arc(pt.x, pt.y, dot_radius, 0, 2 * math.pi)
                ctx.fill()
            else:
                ctx.set_source_rgba(0.0, 0.8, 1.0, 0.7)  # Translucent Cyan
                ctx.arc(pt.x, pt.y, dot_radius, 0, 2 * math.pi)
                ctx.stroke()

        # draw lines connecting handles to anchors
        ctx.set_source_rgba(0.5, 0.5, 0.5, 0.5)
        ctx.set_line_width(2)
        ctx.move_to(c.p0.x, c.p0.y)
        ctx.line_to(c.p1.x, c.p1.y)
        ctx.move_to(c.p3.x, c.p3.y)
        ctx.line_to(c.p2.x, c.p2.y)
        ctx.stroke()

    ctx.set_source_rgb(1.0, 0.0, 0.5)  # Material Pink
    for i in range(0, len(verts), 2):
        vx, vy = verts[i], verts[i + 1]
        ctx.arc(vx, vy, dot_radius + 2, 0, 2 * math.pi)
        ctx.fill()

    output_path = OUTPUT_DIR / filename
    surface.write_to_png(str(output_path))
    print(f"Saved as {output_path}")


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    draw_material_shape(star, "star.png")
    draw_material_shape(clover_flower, "clover.png")
    draw_material_shape(organic_blob, "blob.png")
    draw_material_shape(puffy_square, "squircle.png")
    draw_material_shape(pill, "pill.png")
    draw_material_shape(shield, "shield.png")
    draw_material_shape(concave_rectangle, "concave_rectangle.png")
    draw_material_shape(cookie_12, "cookie_12.png")
    draw_material_shape(cookie_8, "cookie_8.png")
    draw_material_shape(fan, "fan.png")
    draw_material_shape(apple, "apple.png")
    draw_material_shape(t_fan, "t_fan.png")
    draw_material_shape(t_apple, "t_apple.png")

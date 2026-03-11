import math
from dataclasses import dataclass

from .bezier_geometry import Point, Cubic


@dataclass
class CornerRounding:
    radius: float = 0.0
    smoothing: float = 0.0

    @classmethod
    def UNROUNDED(cls):
        return cls(0.0, 0.0)


class RoundedCorner:
    """
    Computes the G2-continuous (curvature-continuous) rounding geometry
    for a single polygon corner defined by three points p0 -> p1 -> p2,
    where p1 is the sharp corner tip.

    The rounding consists of three cubic Bezier segments:
      1. Entry flanking curve  - eases from the straight edge into the arc.
      2. Circular arc segment  - a true circular arc at the corner.
      3. Exit flanking curve   - eases from the arc back onto the straight edge.

    Key distances (measured from the corner tip p1 along each edge):

        expected_round_cut  - distance to the tangent point of the
                              unsmoothed circular arc. The arc begins and
                              ends exactly here when smoothing == 0.
        expected_cut        - distance to where the flanking curve starts,
                              i.e. expected_round_cut x (1 + smoothing).
                              This is how much space the full rounding
                              consumes on each side of the corner.

    Attributes:
        p0, p1, p2:          Original skeleton vertices. p1 is the corner.
        rounding:            CornerRounding parameters (radius, smoothing).
        d1:                  Unit vector from p1 toward p0 (incoming direction).
        d2:                  Unit vector from p1 toward p2 (outgoing direction).
        smoothing:           Smoothing factor in [0, 1]. 0 = pure arc, 1 = maximum blend.
        cos_angle:           Cosine of the half-angle at the corner.
        sin_angle:           Sine of the half-angle at the corner.
        expected_round_cut:  Arc tangent cut distance (no smoothing).
        is_convex:           True if this corner is convex relative to the polygon interior.
        center:              Center of the rounding circle (set during get_cubics).
    """

    DISTANCE_EPSILON = 1e-3  # Threshold below which distances are treated as zero.

    def __init__(
        self,
        p0: Point,
        p1: Point,
        p2: Point,
        rounding: CornerRounding | None = None,
        clockwise_winding: bool = True,
    ):
        self.p0, self.p1, self.p2 = p0, p1, p2
        self.rounding = rounding

        v01 = p0 - p1  # vector from corner toward previous vertex
        v21 = p2 - p1  # vector from corner toward next vertex
        d01, d21 = v01.get_distance(), v21.get_distance()

        if d01 > 0 and d21 > 0:
            self.d1, self.d2 = v01 / d01, v21 / d21  # unit direction vectors
            self.corner_radius = rounding.radius if rounding else 0.0
            self.smoothing = rounding.smoothing if rounding else 0.0
            self.cos_angle = self.d1.dot_product(self.d2)
            self.sin_angle = math.sqrt(max(0.0, 1.0 - (self.cos_angle**2)))

            # 2D Cross Product (v_in x v_out) to find turn direction
            # v_in x v_out > 0 -> CW (concave)
            #              < 0 -> CCW (convex)
            v_in = p1 - p0
            v_out = p2 - p1
            cross = (v_in.x * v_out.y) - (v_in.y * v_out.x)

            self.is_convex = cross <= 0 if clockwise_winding else cross >= 0

            # Distance from the corner tip to the tangent point of the inscribed circle.
            # Derived from: tan(half_angle) = radius / expected_round_cut
            # which rearranges to: expected_round_cut = radius × cos(a) / sin(a) + radius / sin(a)
            #                                         = radius × (cos(a) + 1) / sin(a)
            if self.sin_angle > 1e-3:
                self.expected_round_cut = (
                    self.corner_radius * (self.cos_angle + 1) / self.sin_angle
                )
            else:
                self.expected_round_cut = 0.0
        else:
            # zero-length edge - treat as a point with no rounding.
            self.d1 = self.d2 = Point(0, 0)
            self.corner_radius = self.smoothing = self.cos_angle = self.sin_angle = 0.0
            self.expected_round_cut = self.is_convex = True

        self.center = Point(0, 0)

    @property
    def expected_cut(self) -> float:
        """Total cut distance from the corner tip, including the smoothing extension."""
        return (1 + self.smoothing) * self.expected_round_cut

    def get_cubics(self, allowed_cut_0: float, allowed_cut_1: float) -> list[Cubic]:
        """Generate the three cubic Bezier curves that form this rounded corner."""

        # for symmetry
        allowed_cut = min(allowed_cut_0, allowed_cut_1)

        # return if no space available or zero radius
        if (
            self.expected_round_cut < self.DISTANCE_EPSILON
            or allowed_cut < self.DISTANCE_EPSILON
            or self.corner_radius < self.DISTANCE_EPSILON
        ):
            self.center = self.p1
            # zero_seg = Cubic.straight_line(self.p1.x, self.p1.y, self.p1.x, self.p1.y)
            # return [zero_seg, zero_seg, zero_seg]
            return [Cubic.straight_line(self.p1.x, self.p1.y, self.p1.x, self.p1.y)]

        # Arc tangent cut distance
        actual_round_cut = min(allowed_cut, self.expected_round_cut)

        # Smoothing for each side based on space
        actual_smoothing0 = self._calculate_actual_smoothing(allowed_cut_0)
        actual_smoothing1 = self._calculate_actual_smoothing(allowed_cut_1)

        # Scale radius if we had to shrink the cut to fit
        actual_r = self.corner_radius * actual_round_cut / self.expected_round_cut

        # Calculate center of the rounding circle
        # The center lies along the angle bisector from p1
        center_dist = math.sqrt((actual_r**2) + (actual_round_cut**2))
        bisector_dir = (self.d1 + self.d2).get_direction()  # d1 and d2 are unit vectors
        self.center = self.p1 + bisector_dir * center_dist

        # Tangent points on either sides. Smoothening is done using this as base
        circle_inter0 = self.p1 + self.d1 * actual_round_cut
        circle_inter2 = self.p1 + self.d2 * actual_round_cut

        flanking0 = self._compute_flanking_curve(
            actual_round_cut,
            actual_smoothing0,
            self.p1,
            self.p0,
            circle_inter0,
            circle_inter2,
            self.center,
            actual_r,
        )
        flanking2 = self._compute_flanking_curve(
            actual_round_cut,
            actual_smoothing1,
            self.p1,
            self.p2,
            circle_inter2,
            circle_inter0,
            self.center,
            actual_r,
        ).reverse()

        return [
            flanking0,
            Cubic.circular_arc(
                self.center.x,
                self.center.y,
                flanking0.p3.x,
                flanking0.p3.y,
                flanking2.p0.x,
                flanking2.p0.y,
                is_convex=self.is_convex,
            ),
            flanking2,
        ]

    def _calculate_actual_smoothing(self, allowed_cut: float) -> float:
        if allowed_cut > self.expected_cut:
            return self.smoothing
        if allowed_cut > self.expected_round_cut:
            # Proportionally scale smoothing based on available space
            return (
                self.smoothing
                * (allowed_cut - self.expected_round_cut)
                / (self.expected_cut - self.expected_round_cut)
            )
        return 0.0

    def _compute_flanking_curve(
        self,
        actual_round_cut,
        smoothing,
        corner,
        side_start,
        circle_inter,
        other_inter,
        center,
        radius,
    ) -> Cubic:
        side_dir = (side_start - corner).get_direction()  # unit vector along the edge
        # Start the curve further back on the straight edge based on smoothing
        curve_start = corner + side_dir * actual_round_cut * (1 + smoothing)

        # Interpolate point on circle to determine where smoothing ends
        # Creates a point `p` that starts at the tangent point (circle_inter)
        # and moves to the arc midpoint based on `smoothing` value
        p = Point.interpolate(
            circle_inter, (circle_inter + other_inter) / 2.0, smoothing
        )
        curve_end = center + (p - center).get_direction() * radius

        # The end control point must be tangent to the circle at curve_end.
        # The tangent to a circle at a point is perpendicular to the radius there.
        circle_tangent = (curve_end - center).rotate_90()

        # Find where the straight edge (extended) meets the circle tangent line.
        # This intersection is the "anchor" that naturally blends both directions.
        anchor_end = (
            self._line_intersection(side_start, side_dir, curve_end, circle_tangent)
            or circle_inter
        )

        # Place the first control point 1/3 of the way from curve_start to anchor_end.
        # (Cubic Bezier: p1 at 1/3, p2 at anchor_end gives a smooth entry.)
        anchor_start = (curve_start + anchor_end * 2.0) / 3.0

        return Cubic(curve_start, anchor_start, anchor_end, curve_end)

    def _line_intersection(self, p0, d0, p1, d1) -> Point | None:
        """Returns the intersection of two infinite lines."""
        rotated_d1 = d1.rotate_90()
        den = d0.dot_product(rotated_d1)
        if abs(den) < self.DISTANCE_EPSILON:
            return None
        num = (p1 - p0).dot_product(rotated_d1)
        k = num / den
        return p0 + d0 * k

    def get_start_point(self, allowed_cut: float) -> Point:
        """Returns the point on the edge where the rounding sequence begins."""
        return self.p1 + self.d1 * allowed_cut

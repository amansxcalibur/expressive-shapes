import math
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    # This handles the case where the float is on the left side: 5.0 * point
    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        return Point(self.x / scalar, self.y / scalar)

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y

    def get_distance(self):
        return math.hypot(self.x, self.y)

    def get_distance_squared(self):
        return self.x * self.x + self.y * self.y

    def dist_to(self, other):
        return math.hypot((self.x - other.x), (self.y - other.y))

    def rotate_90(self):
        return Point(-self.y, self.x)

    def rotate_270(self):
        return Point(self.y, -self.x)

    def get_direction(self):
        d = self.get_distance()
        return self / d if d > 0 else Point(0, 0)

    @staticmethod
    def interpolate(p1, p2, t):
        return Point(p1.x + (p2.x - p1.x) * t, p1.y + (p2.y - p1.y) * t)


@dataclass
class Cubic:
    p0: Point  # start anchor point
    p1: Point  # first control point
    p2: Point  # second control point
    p3: Point  # end anchor point

    def reverse(self) -> "Cubic":
        return Cubic(p0=self.p3, p1=self.p2, p2=self.p1, p3=self.p0)

    @staticmethod
    def straight_line(x0, y0, x1, y1):
        p0 = Point(x0, y0)
        p3 = Point(x1, y1)
        # control points are same as endpoints for a straight line
        return Cubic(p0, p0, p3, p3)

    @staticmethod
    def circular_arc(
        cx: float,
        cy: float,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        is_convex: bool,
    ) -> "Cubic":
        """
        Approximate a circular arc with a single cubic Bezier curve.

        Uses the standard "kappa" approximation, which places the control
        points at a distance of (4/3) x tan(θ/4) x radius along the tangent
        at each endpoint, where θ is the arc's subtended angle.

        Args:
            cx, cy:    Center of the circle.
            x0, y0:    Arc start point (must lie on the circle).
            x1, y1:    Arc end point   (must lie on the circle).
            is_convex: True if this corner is convex (bends outward).
                       False for concave (bends inward). Controls which
                       90° rotation is applied to the radius vectors.

        Returns:
            A Cubic Bezier closely approximating the circular arc from
            (x0, y0) to (x1, y1).
        """
        p0 = Point(x0, y0)
        p3 = Point(x1, y1)
        center = Point(cx, cy)

        # Vectors from center to endpoints
        v0 = p0 - center
        v3 = p3 - center

        # Calculate the angle between the two points, basically angle subtended
        # by the arc. Use the dot product of normalized vectors
        d0 = v0.get_direction()
        d3 = v3.get_direction()
        dot = d0.dot_product(d3)

        # Clamp dot product to avoid math domain errors due to precision
        angle = math.acos(max(-1.0, min(1.0, dot)))

        # Kappa: optimal handle length for the cubic arc approximation.
        # Calculate the handles distance (kappa)
        kappa = (4.0 / 3.0) * math.tan(angle / 4.0)

        # Place control points tangent to the circle at each endpoint.
        # The tangent at any point on a circle is perpendicular to its radius.
        # For a convex corner the tangent rotates CCW (rotate_90);
        # for a concave corner it rotates CW (rotate_270) to keep the arc
        # on the correct side of the chord
        if is_convex:
            p1 = p0 + v0.rotate_90() * kappa
            p2 = p3 + v3.rotate_90() * -kappa
        else:
            p1 = p0 + v0.rotate_270() * kappa
            p2 = p3 + v3.rotate_270() * -kappa
        return Cubic(p0, p1, p2, p3)

    def split(self, t: float) -> tuple["Cubic", "Cubic"]:
        """
        Splits the cubic Bezier curve at parameter t into two cubic Bezier curves.
        Uses De Casteljau's algorithm to calculate the new control points.
        """
        # Level 1: Interpolate between the 4 original points
        p01 = Point.interpolate(self.p0, self.p1, t)
        p12 = Point.interpolate(self.p1, self.p2, t)
        p23 = Point.interpolate(self.p2, self.p3, t)

        # Level 2: Interpolate between the 3 points from Level 1
        p012 = Point.interpolate(p01, p12, t)
        p123 = Point.interpolate(p12, p23, t)

        # Level 3: The point on the curve at time t
        p0123 = Point.interpolate(p012, p123, t)

        left = Cubic(p0=self.p0, p1=p01, p2=p012, p3=p0123)

        right = Cubic(p0=p0123, p1=p123, p2=p23, p3=self.p3)

        return left, right

    def point_at(self, t: float) -> Point:
        """Returns the Point on the curve at parameter t (0 to 1)."""
        u = 1 - t
        tt = t * t
        uu = u * u
        uuu = uu * u
        ttt = tt * t

        # Cubic Bezier formula: (1-t)^3*P0 + 3(1-t)^2*t*P1 + 3(1-t)*t^2*P2 + t^3*P3
        p = (
            (self.p0 * uuu)
            + (self.p1 * 3 * uu * t)
            + (self.p2 * 3 * u * tt)
            + (self.p3 * ttt)
        )
        return p

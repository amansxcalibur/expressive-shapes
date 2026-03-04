import math
from pprint import pprint
from dataclasses import dataclass
from typing import List, Optional, Tuple

from .bezier_geometry import Point, Cubic
from .corner_rounding import CornerRounding, RoundedCorner


@dataclass
class Feature:
    """Represents a segment of the polygon (either a Corner or an Edge)"""

    curves: List[Cubic]
    type: str  # "corner" or "edge"
    is_convex: bool = True

    # to make it hashable for set()
    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self is other

class RoundedPolygon:
    def __init__(self, features: List[Feature], center_x: float, center_y: float):
        self.features = features
        self.center_x = center_x
        self.center_y = center_y

    @classmethod
    def create(
        cls,
        vertices: List[float],
        rounding: CornerRounding = CornerRounding.UNROUNDED(),
        per_vertex_rounding: Optional[List[CornerRounding]] = None,
        center_x: Optional[float] = None,
        center_y: Optional[float] = None,
    ) -> "RoundedPolygon":

        n_floats = len(vertices)
        if n_floats < 6 or n_floats % 2 != 0:
            raise ValueError("Vertices must be even and at least 6 (3 points).")

        n = n_floats // 2  # number of polygon vertices
        if per_vertex_rounding and len(per_vertex_rounding) != n:
            raise ValueError("per_vertex_rounding size must match number of vertices.")

        # determine global winding (True if clockwise)
        is_cw = cls._is_clockwise(vertices)

        # --- Build a RoundedCorner for each vertex ---
        rounded_corners = []
        for i in range(n):
            v_rounding = per_vertex_rounding[i] if per_vertex_rounding else rounding

            prev_idx = ((i + n - 1) % n) * 2
            curr_idx = i * 2
            next_idx = ((i + 1) % n) * 2

            corner = RoundedCorner(
                Point(vertices[prev_idx], vertices[prev_idx + 1]),
                Point(vertices[curr_idx], vertices[curr_idx + 1]),
                Point(vertices[next_idx], vertices[next_idx + 1]),
                v_rounding,
                clockwise_winding=is_cw,
            )
            rounded_corners.append(corner)

        print("--- rounded corners ---")
        for i in rounded_corners:
            pprint([i.p0, i.p1, i.p2, i.rounding])
        print()

        # --- Resolve overlapping cuts (tight-space adjustment) ---
        # For each edge, check whether the two flanking corners claim more
        # space than the edge length provides, and compute scaling ratios.
        #
        # cut_adjusts[i] is a (round_ratio, smooth_ratio) pair for the edge
        # between vertex i and vertex (i+1).
        #
        #   round_ratio  – how much to scale the circular-arc cut distance.
        #                  < 1.0 means the arc had to be shrunk to fit.
        #   smooth_ratio – how much to scale the smoothing extension beyond
        #                  the arc tangent point. Only < 1.0 when the arc
        #                  itself fits but the smoothing overshoot doesn't.
        cut_adjusts = []
        for i in range(n):
            c1: RoundedCorner = rounded_corners[i]
            c2: RoundedCorner = rounded_corners[(i + 1) % n]

            expected_round_cut = c1.expected_round_cut + c2.expected_round_cut
            expected_total_cut = c1.expected_cut + c2.expected_cut

            side_len = math.hypot(
                vertices[i * 2] - vertices[((i + 1) % n) * 2],
                vertices[i * 2 + 1] - vertices[((i + 1) % n) * 2 + 1],
            )

            if expected_round_cut > side_len:
                cut_adjusts.append((side_len / expected_round_cut, 0.0))
            elif expected_total_cut > side_len:
                smooth_ratio = (side_len - expected_round_cut) / (
                    expected_total_cut - expected_round_cut
                )
                cut_adjusts.append((1.0, smooth_ratio))
            else:
                cut_adjusts.append((1.0, 1.0))

        print("----- cut adjusts -----")
        pprint(cut_adjusts)
        print()

        # --- Generate Final Features ---
        # Generate a corner feature paired with a straight edge on each vertex
        features = []
        for i in range(n):
            # allowed cut on incoming side of corner
            # (the edge between vertex i-1 and vertex i).
            r0, s0 = cut_adjusts[(i + n - 1) % n]
            allowed0 = (
                rounded_corners[i].expected_round_cut * r0
                + (
                    rounded_corners[i].expected_cut
                    - rounded_corners[i].expected_round_cut
                )
                * s0
            )

            # allowed cut on outgoing side of corner
            # (the edge between vertex i and vertex i+1).
            r1, s1 = cut_adjusts[i]
            allowed1 = (
                rounded_corners[i].expected_round_cut * r1
                + (
                    rounded_corners[i].expected_cut
                    - rounded_corners[i].expected_round_cut
                )
                * s1
            )

            # build corner cubic bezier curve
            corner_cubics: Cubic = rounded_corners[i].get_cubics(allowed0, allowed1)
            features.append(
                Feature(
                    curves=corner_cubics,
                    type="corner",
                    is_convex=rounded_corners[i].is_convex,
                )
            )

            # build straight edge from bezier curve end
            # We need the start of the NEXT corner to draw the line to it
            next_r0, next_s0 = cut_adjusts[i]  # The side between i and i+1
            next_allowed0 = (
                rounded_corners[(i + 1) % n].expected_round_cut * next_r0
                + (
                    rounded_corners[(i + 1) % n].expected_cut
                    - rounded_corners[(i + 1) % n].expected_round_cut
                )
                * next_s0
            )

            next_corner_start = rounded_corners[(i + 1) % n].get_start_point(
                next_allowed0
            )

            edge_line = Cubic.straight_line(
                corner_cubics[-1].p3.x,
                corner_cubics[-1].p3.y,
                next_corner_start.x,
                next_corner_start.y,
            )
            features.append(Feature(curves=[edge_line], type="edge"))

        print("----features-----")
        pprint(features)
        print()

        if center_x is None or center_y is None:
            center_x, center_y = cls._calculate_center(vertices)

        return cls(features, center_x, center_y)

    @staticmethod
    def _is_clockwise(vertices: List[float]) -> bool:
        # uses Shoelace formula
        area = 0.0
        n = len(vertices) // 2
        for i in range(n):
            x1, y1 = vertices[i * 2], vertices[i * 2 + 1]
            x2, y2 = vertices[((i + 1) % n) * 2], vertices[((i + 1) % n) * 2 + 1]
            area += (x2 - x1) * (y2 + y1)
        return area > 0

    @staticmethod
    def _calculate_center(vertices: List[float]) -> Tuple[float, float]:
        # arithmetic mean of all vertices
        n = len(vertices) // 2
        return (sum(vertices[0::2]) / n, sum(vertices[1::2]) / n)

    def get_all_curves(self) -> List[Cubic]:
        return [curve for f in self.features for curve in f.curves]

    def get_all_features(self) -> List[Feature]:
        return self.features

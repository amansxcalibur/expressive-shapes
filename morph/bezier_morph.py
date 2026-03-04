from pprint import pprint
from typing import List, Tuple
from bisect import bisect_left
from dataclasses import dataclass

from .debugger import MorphDebugger
from geometry.bezier_geometry import Cubic, Point
from geometry.rounded_polygon import RoundedPolygon, Feature
from geometry.polygon_measure import (
    AngleEpsilon,
    DistanceEpsilon,
    DoubleMapper,
    MeasuredFeature,
    MeasuredPolygon,
    measure_features,
    progress_distance,
    progress_in_range,
)


# Identity mapping used when no valid feature pairs are found
_IdentityMapping = [(0.0, 0.0), (0.5, 0.5)]


@dataclass
class DistanceVertex:
    distance: float
    f1: MeasuredFeature
    f2: MeasuredFeature


class Morph:
    @staticmethod
    def balance_segments(curves: List[Cubic], target_count: int) -> List[Cubic]:
        result = curves

        if not result:
            result = list(curves)

        print("splitting, length and target:", len(result), target_count)
        pprint(result)

        # repeatedly find the longest cubic and split
        while len(result) < target_count:
            idx_to_split = 0
            max_score = -1.0
            for i, c in enumerate(result):
                score = c.p0.dist_to(c.p1) + c.p1.dist_to(c.p2) + c.p2.dist_to(c.p3)
                if score > max_score:
                    max_score = score
                    idx_to_split = i
                    print("==splitting index : ", idx_to_split, score)

            c1, c2 = result[idx_to_split].split(0.5)
            result[idx_to_split] = c1
            result.insert(idx_to_split + 1, c2)
        return result

    @staticmethod
    def map_curves(
        poly_start: RoundedPolygon, poly_end: RoundedPolygon
    ) -> Tuple[List[Cubic], List[Cubic]]:
        curves_a = poly_start.get_all_curves()
        curves_b = poly_end.get_all_curves()

        target_count = max(len(curves_a), len(curves_b))
        print(
            " -- getting target count -- ", target_count, len(curves_a), len(curves_b)
        )

        # filter out degenerate cubics
        result_a = [c for c in curves_a if c.p0.dist_to(c.p3) > 0.001]
        result_b = [c for c in curves_b if c.p0.dist_to(c.p3) > 0.001]

        target_count = max(len(result_a), len(result_b))

        print(
            " -- getting filtered target count -- ",
            target_count,
            len(result_a),
            len(result_b),
        )

        balanced_a = Morph.balance_segments(result_a, target_count)
        balanced_b = Morph.balance_segments(result_b, target_count)

        # find the rotation of shape B that minimizes distance between start points
        best_shift = 0
        min_dist = float("inf")
        for shift in range(len(balanced_b)):
            d = balanced_a[0].p0.dist_to(balanced_b[shift].p0)
            if d < min_dist:
                min_dist = d
                best_shift = shift

        balanced_b = balanced_b[best_shift:] + balanced_b[:best_shift]

        return balanced_a, balanced_b

    @staticmethod
    def interpolate(
        curves_a: List[Cubic], curves_b: List[Cubic], alpha: float
    ) -> List[Cubic]:
        morphed = []
        for c1, c2 in zip(curves_a, curves_b):
            p0 = Point.interpolate(c1.p0, c2.p0, alpha)
            p1 = Point.interpolate(c1.p1, c2.p1, alpha)
            p2 = Point.interpolate(c1.p2, c2.p2, alpha)
            p3 = Point.interpolate(c1.p3, c2.p3, alpha)
            morphed.append(Cubic(p0, p1, p2, p3))
        return morphed

    @staticmethod
    def map_features(
        poly_start: RoundedPolygon, poly_end: RoundedPolygon
    ) -> DoubleMapper:
        _, feats_a = measure_features(poly_start.features)
        _, feats_b = measure_features(poly_end.features)

        print("all feats : ", len(poly_start.features))
        corners_a: List[MeasuredFeature] = [
            c for c in feats_a if c.feature.type == "corner"
        ]
        corners_b: List[MeasuredFeature] = [
            c for c in feats_b if c.feature.type == "corner"
        ]
        print("all corners : ", len(corners_a))

        feature_progress_mapping = Morph.do_mapping(corners_a, corners_b)

        print(
            " | ".join(
                f"{src:.4f} -> {dst:.4f}" for src, dst in feature_progress_mapping
            )
        )

        dm = DoubleMapper(*feature_progress_mapping)

        N = 10
        map_values = [f"{dm.map(i / N):.4f}" for i in range(N + 1)]
        map_back_values = [f"{dm.map_back(i / N):.4f}" for i in range(N + 1)]

        print("Map :", " | ".join(map_values))
        print("Mb  :", " | ".join(map_back_values))

        return dm

    @staticmethod
    def do_mapping(
        features1: List[MeasuredFeature],
        features2: List[MeasuredFeature],
    ) -> List[Tuple[float, float]]:
        """
        Builds a list of (progress1, progress2) anchor pairs by greedily matching
        corner features from both shapes based on spatial proximity.
        """

        MorphDebugger.print_distance_matrix(features1, features2)

        distance_vertex_list: List[DistanceVertex] = []

        for f1 in features1:
            for f2 in features2:
                d = Morph.feature_dist_squared(f1, f2)
                if d != float("inf"):
                    distance_vertex_list.append(DistanceVertex(d, f1, f2))

        # sort by distance
        distance_vertex_list = sorted(distance_vertex_list, key=lambda x: x.distance)

        if not distance_vertex_list:
            return list(_IdentityMapping)

        # only one valid pair => adds an antipodal point
        if len(distance_vertex_list) == 1:
            dv = distance_vertex_list[0]
            f1_prog = dv.f1.progress
            f2_prog = dv.f2.progress
            return [(f1_prog, f2_prog), ((f1_prog + 0.5) % 1.0, (f2_prog + 0.5) % 1.0)]

        helper = MappingHelper()
        for f in distance_vertex_list:
            helper.add_mapping(f.f1, f.f2)

        MorphDebugger.print_mapping_decisions(distance_vertex_list, helper.mapping)

        return helper.mapping

    @staticmethod
    def feature_dist_squared(f1: MeasuredFeature, f2: MeasuredFeature) -> float:
        # prevent convex <-> concave matching
        if (
            f1.feature.type == "corner"
            and f2.feature.type == "corner"
            and f1.feature.is_convex != f2.feature.is_convex
        ):
            return float("inf")

        return (
            Morph.feature_representative_point(f1.feature)
            - Morph.feature_representative_point(f2.feature)
        ).get_distance_squared()

    @staticmethod
    def feature_representative_point(feature: Feature) -> Point:
        # midpoint of first anchor0 and last anchor1, matching Kotlin
        return (feature.curves[0].p0 + feature.curves[-1].p3) / 2.0

    @staticmethod
    def match(
        poly1: RoundedPolygon, poly2: RoundedPolygon
    ) -> List[Tuple[Cubic, Cubic]]:
        MorphDebugger.inspect_all(poly1, poly2)

        measured1: MeasuredPolygon = MeasuredPolygon.measure_polygon(poly1)
        measured2: MeasuredPolygon = MeasuredPolygon.measure_polygon(poly2)

        corners1 = []
        for i, f in enumerate(measured1.features):
            if f.feature.type == "corner":
                f.index = i  # for debugging
                corners1.append(f)

        corners2 = []
        for i, f in enumerate(measured2.features):
            if f.feature.type == "corner":
                f.index = i
                corners2.append(f)

        mapping_pairs: List[Tuple[float, float]] = Morph.do_mapping(corners1, corners2)
        MorphDebugger.print_mapping_results(measured1, measured2, mapping_pairs)

        double_mapper = DoubleMapper(*mapping_pairs)

        # Determine where Shape 2 should "start" to align with Shape 1's 0.0
        poly2_cut_point = double_mapper.map(0.0)

        print("\n[ ALIGNMENT ]")
        print(f"Shape 2 cut point: {poly2_cut_point:.4f} (mapping of 0.0 on Shape 1)")

        # Cut and shift Shape 2 so its index 0 aligns with Shape 1's index 0
        bs1: MeasuredPolygon = measured1
        bs2: MeasuredPolygon = measured2.cut_and_shift(poly2_cut_point)

        print(
            f"After cut_and_shift: bs1 has {len(bs1)} cubics, bs2 has {len(bs2)} cubics"
        )

        # Walks both polygons simultaneously, producing matched (Cubic, Cubic) pairs.
        # Whichever cubic ends sooner is consumed whole; the other is cut at the
        # corresponding point so their boundaries align.
        ret = []
        i1, i2 = 0, 0
        b1 = bs1.get_cubic(i1)
        i1 += 1
        b2 = bs2.get_cubic(i2)
        i2 += 1

        step = 0
        MorphDebugger.print_walking_header()

        while b1 is not None and b2 is not None:
            # Convert both cubics' end progress to Shape 1's space for comparison.
            # Last cubic on either side is forced to 1.0 to guarantee both finish together.
            b1a = 1.0 if i1 == bs1.size else b1.end_outline_progress
            b2a = (
                1.0
                if i2 == bs2.size
                # Undo shift to get original Shape 2 progress, then map_back to Shape 1 space
                else double_mapper.map_back(
                    (b2.end_outline_progress + poly2_cut_point) % 1.0
                )
            )

            # smaller cubics determines split boundary
            min_b = min(b1a, b2a)

            print(f"{step:<5} | b1a={b1a:<10.4f} | b2a={b2a:<12.4f} | min={min_b:.4f}")

            # cut whichever extends past min_b
            if b1a > min_b + AngleEpsilon:
                seg1, new_b1 = b1.cut_at_progress(min_b)
            else:
                seg1 = b1
                new_b1 = bs1.get_cubic(i1)
                i1 += 1

            if b2a > min_b + AngleEpsilon:
                # Convert min_b (Shape 1 space) -> Shape 2 original space -> bs2 local space
                # map(min_b) gives Shape 2 original, subtract poly2_cut_point gives local
                seg2, new_b2 = b2.cut_at_progress(
                    (double_mapper.map(min_b) - poly2_cut_point) % 1.0
                )
            else:
                seg2 = b2
                new_b2 = bs2.get_cubic(i2)
                i2 += 1

            ret.append((seg1.cubic, seg2.cubic))
            b1 = new_b1
            b2 = new_b2
            step += 1

        if b1 is not None or b2 is not None:
            print(
                f"WARNING: Walking ended with b1={b1 is not None}, b2={b2 is not None}"
            )
            print(f"  i1={i1}/{bs1.size}, i2={i2}/{bs2.size}")

        MorphDebugger.print_final_matched_pairs(ret)

        return ret

    @staticmethod
    def as_cubics(
        matched_pairs: List[Tuple[Cubic, Cubic]], progress: float
    ) -> List[Cubic]:
        result = []
        first_cubic = None
        last_cubic = None
        for c1, c2 in matched_pairs:
            p0 = Point.interpolate(c1.p0, c2.p0, progress)
            p1 = Point.interpolate(c1.p1, c2.p1, progress)
            p2 = Point.interpolate(c1.p2, c2.p2, progress)
            p3 = Point.interpolate(c1.p3, c2.p3, progress)
            cubic = Cubic(p0, p1, p2, p3)
            if first_cubic is None:
                first_cubic = cubic
            if last_cubic is not None:
                result.append(last_cubic)
            last_cubic = cubic

        # close the shape: last cubic's end point snaps to first cubic's start
        if last_cubic is not None and first_cubic is not None:
            result.append(
                Cubic(last_cubic.p0, last_cubic.p1, last_cubic.p2, first_cubic.p0)
            )
        return result


class MappingHelper:
    def __init__(self):
        self.mapping: list[tuple[float, float]] = []  # [(progress1, progress2), ...]
        self.used_f1: set[MeasuredFeature] = set()
        self.used_f2: set[MeasuredFeature] = set()

    def add_mapping(self, f1: MeasuredFeature, f2: MeasuredFeature):
        if f1 in self.used_f1 or f2 in self.used_f2:
            return

        # binary search by f1.progress
        progresses = [m[0] for m in self.mapping]
        insertion_index = bisect_left(progresses, f1.progress)

        # no duplicate progress
        if (
            insertion_index < len(self.mapping)
            and self.mapping[insertion_index][0] == f1.progress
        ):
            raise ValueError("There can't be two features with the same progress")

        n = len(self.mapping)

        if n >= 1:
            before1, before2 = self.mapping[(insertion_index + n - 1) % n]
            after1, after2 = self.mapping[insertion_index % n]

            # discard too-close features
            if (
                progress_distance(f1.progress, before1) < DistanceEpsilon
                or progress_distance(f1.progress, after1) < DistanceEpsilon
                or progress_distance(f2.progress, before2) < DistanceEpsilon
                or progress_distance(f2.progress, after2) < DistanceEpsilon
            ):
                return

            # ensure no crossings
            # one is fine (end <-> start crossing)
            if n > 1 and not progress_in_range(f2.progress, before2, after2):
                return

        self.mapping.insert(insertion_index, (f1.progress, f2.progress))
        self.used_f1.add(f1)
        self.used_f2.add(f2)

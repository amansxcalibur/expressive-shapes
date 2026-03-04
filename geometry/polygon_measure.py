from dataclasses import dataclass
from typing import List, Optional, Tuple

from .bezier_geometry import Cubic
from .rounded_polygon import Feature, RoundedPolygon


DistanceEpsilon = 1e-4
AngleEpsilon = 1e-6
MIN_SEGMENTS = 3


@dataclass
class MeasuredFeature:
    progress: float  # normalized [0,1)
    feature: "Feature"

    # to make it hashable for set()
    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self is other


class LengthMeasurer:
    @staticmethod
    def measure_cubic(c: Cubic) -> float:
        """Returns the approximate arc length of the cubic."""
        return LengthMeasurer._closest_progress_to(c, float("inf"))[1]

    @staticmethod
    def find_cubic_cut_point(c: Cubic, m: float) -> float:
        """Returns the parametric t value where arc length from start reaches m."""
        return LengthMeasurer._closest_progress_to(c, m)[0]

    @staticmethod
    def _closest_progress_to(cubic: Cubic, threshold: float) -> Tuple[float, float]:
        total = 0.0
        remainder = threshold
        prev = cubic.p0

        for i in range(1, MIN_SEGMENTS + 1):
            progress = i / MIN_SEGMENTS
            point = cubic.point_at(progress)
            segment = prev.dist_to(point)

            if segment >= remainder:
                progress_precise = progress - (1.0 - remainder / segment) / MIN_SEGMENTS
                return progress_precise, threshold

            remainder -= segment
            total += segment
            prev = point

        return 1.0, total


def measure_features(feature_list: List[Feature]):
    """
    Converts a list of Feature objects into measured data:
    - outline_progress: cumulative arc-length-normalized progress for each cubic boundary
    - list of MeasuredFeature: each corner feature assigned a progress value at the
      midpoint of its middle rounding cubic's progress range

    This gives each corner a single progress value representing where on the perimeter
    it lives, used as anchor points for the DoubleMapper.
    """

    cubics = []
    feature_to_cubic_index = []

    for feature in feature_list:
        for i, cubic in enumerate(feature.curves):
            if feature.type == "corner" and i == len(feature.curves) // 2:
                feature_to_cubic_index.append((feature, len(cubics)))
            cubics.append(cubic)

    measures = [0.0]
    for cubic in cubics:
        length = LengthMeasurer.measure_cubic(cubic)
        if length < 0:
            raise ValueError("Measured cubic must be >= 0")
        measures.append(measures[-1] + length)

    total_length = measures[-1]
    if total_length == 0:
        raise ValueError("Polygon has zero total length")

    outline_progress = [m / total_length for m in measures]

    measured_features = []
    for feature, cubic_index in feature_to_cubic_index:
        start_p = outline_progress[cubic_index]
        end_p = outline_progress[cubic_index + 1]
        midpoint = (start_p + end_p) / 2

        measured_features.append(
            MeasuredFeature(progress=(midpoint % 1.0), feature=feature)
        )

    return outline_progress, measured_features


class DoubleMapper:
    """
    Piecewise-linear circular mapping between two shapes' progress spaces.

    Anchored at corner-to-corner pairs (source, target), it linearly interpolates
    between anchor points to map any progress value from one shape to the other.
    The mapping wraps around — the segment between the last and first anchor pair
    crosses the 0.0/1.0 boundary.

    map(x):      Shape 1 progress -> Shape 2 progress
    map_back(x): Shape 2 progress -> Shape 1 progress
    """

    def __init__(self, *mappings):
        self.source = [m[0] for m in mappings] # progress positions of shape1
        self.target = [m[1] for m in mappings] # progress positions of shape2

        self._validate_progress(self.source)
        self._validate_progress(self.target)

    def map(self, x: float) -> float:
        """Maps a progress value from Shape 1's space to Shape 2's space."""
        return self._linear_map(self.source, self.target, x)

    def map_back(self, x: float) -> float:
        """Maps a progress value from Shape 2's space back to Shape 1's space."""
        return self._linear_map(self.target, self.source, x)

    def _linear_map(
        self, x_values: list[float], y_values: list[float], x: float
    ) -> float:
        """
        Piecewise-linear interpolation on a circular [0, 1) domain.
        Finds which segment (between two adjacent anchor points) contains x,
        computes the relative position within that segment, and linearly
        interpolates the corresponding y segment.
        """
        if not (0.0 <= x <= 1.0):
            raise ValueError(f"Invalid progress: {x}")

        n = len(x_values)

        # find segment where x lies
        segment_start_index = None
        for i in range(n):
            if progress_in_range(x, x_values[i], x_values[(i + 1) % n]):
                segment_start_index = i
                break

        if segment_start_index is None:
            raise ValueError("No valid segment found for x")

        segment_end_index = (segment_start_index + 1) % n

        # circular segment sizes
        segment_size_x = (
            x_values[segment_end_index] - x_values[segment_start_index]
        ) % 1.0

        segment_size_y = (
            y_values[segment_end_index] - y_values[segment_start_index]
        ) % 1.0

        # position within segment
        if segment_size_x < 0.001:
            position_in_segment = 0.5
        else:
            position_in_segment = (
                (x - x_values[segment_start_index]) % 1.0
            ) / segment_size_x

        return (
            y_values[segment_start_index] + segment_size_y * position_in_segment
        ) % 1.0

    def _validate_progress(self, p: list[float]) -> None:
        if not p:
            raise ValueError("Progress list cannot be empty")

        prev = p[-1]
        wraps = 0

        for curr in p:
            # range check
            if not (0.0 <= curr < 1.0):
                raise ValueError(f"FloatMapping - Progress outside of range: {p}")

            # no duplicate / too close
            if progress_distance(curr, prev) <= DistanceEpsilon:
                raise ValueError(f"FloatMapping - Progress repeats a value: {p}")

            # detect wrap
            if curr < prev:
                wraps += 1
                if wraps > 1:  # one wrap is fine, end <-> start
                    raise ValueError(
                        f"FloatMapping - Progress wraps more than once: {p}"
                    )

            prev = curr


def progress_distance(p1: float, p2: float) -> float:
    """Shortest circular distance between two progress values on [0, 1)."""
    diff = abs(p1 - p2)
    return min(diff, 1.0 - diff)


def progress_in_range(
    progress: float, progress_from: float, progress_to: float
) -> bool:
    if progress_to >= progress_from:
        return progress_from <= progress <= progress_to
    else:
        # wrapped interval
        return progress >= progress_from or progress <= progress_to


@dataclass
class MeasuredCubic:
    cubic: Cubic
    start_outline_progress: float
    end_outline_progress: float
    measured_size: float  # arc length (used for proportional cutting)

    def update_progress_range(
        self, start_outline_progress=None, end_outline_progress=None
    ):
        if start_outline_progress is not None:
            self.start_outline_progress = start_outline_progress
        if end_outline_progress is not None:
            self.end_outline_progress = end_outline_progress

    def cut_at_progress(
        self, cut_outline_progress: float
    ) -> Tuple["MeasuredCubic", "MeasuredCubic"]:
        bounded_cut = max(
            self.start_outline_progress,
            min(cut_outline_progress, self.end_outline_progress),
        )
        outline_progress_size = self.end_outline_progress - self.start_outline_progress
        progress_from_start = bounded_cut - self.start_outline_progress

        relative_progress = (
            progress_from_start / outline_progress_size
            if outline_progress_size > 0
            else 0
        )
        t = LengthMeasurer.find_cubic_cut_point(
            self.cubic, relative_progress * self.measured_size
        )

        c1, c2 = self.cubic.split(t)
        return (
            MeasuredCubic(
                c1,
                self.start_outline_progress,
                bounded_cut,
                self.measured_size * relative_progress,
            ),
            MeasuredCubic(
                c2,
                bounded_cut,
                self.end_outline_progress,
                self.measured_size * (1 - relative_progress),
            ),
        )


class MeasuredPolygon:
    def __init__(self, features: List[MeasuredFeature], cubics: List[MeasuredCubic]):
        self._features = features
        self._cubics = cubics

    @property
    def features(self) -> List[MeasuredFeature]:
        return self._features

    @property
    def size(self) -> int:
        return len(self._cubics)

    def __len__(self) -> int:
        return len(self._cubics)

    def __getitem__(self, index: int) -> MeasuredCubic:
        return self._cubics[index]

    def get_cubic(self, index: int) -> Optional[MeasuredCubic]:
        if 0 <= index < self.size:
            return self._cubics[index]
        return None

    def cut_and_shift(self, cutting_point: float) -> "MeasuredPolygon":
        """
        Cut polygon 2 at cutting_point and rotate cubics so it starts there.
        Constructs new MeasuredPolygon from rearranged cubics with adjusted
        outline progress. Does NOT re-measure.
        """
        if cutting_point < DistanceEpsilon:
            return self

        # Find the cubic that contains the cutting point
        target_index = -1
        for i, c in enumerate(self._cubics):
            if c.start_outline_progress <= cutting_point <= c.end_outline_progress:
                target_index = i
                break

        if target_index == -1:
            return self

        target = self._cubics[target_index]

        # Cut the target cubic at the cutting point
        b1, b2 = target.cut_at_progress(cutting_point)

        # Construct the reordered list of cubics:
        # b2 (second half of cut), all cubics after target wrapping around, b1 (first half of cut)
        ret_cubics_raw = [b2.cubic]
        for i in range(1, len(self._cubics)):
            ret_cubics_raw.append(
                self._cubics[(i + target_index) % len(self._cubics)].cubic
            )
        ret_cubics_raw.append(b1.cubic)

        # Construct outline progress array
        n = len(self._cubics)
        ret_outline_progress = []
        for index in range(n + 2):
            if index == 0:
                ret_outline_progress.append(0.0)
            elif index == n + 1:
                ret_outline_progress.append(1.0)
            else:
                cubic_index = (target_index + index - 1) % n
                ret_outline_progress.append(
                    (self._cubics[cubic_index].end_outline_progress - cutting_point)
                    % 1.0
                )

        measured_cubics = []
        start_progress = 0.0
        for i in range(len(ret_cubics_raw)):
            end_progress = ret_outline_progress[i + 1]
            if (end_progress - ret_outline_progress[i]) > DistanceEpsilon:
                mc = MeasuredCubic(
                    ret_cubics_raw[i],
                    start_progress,
                    end_progress,
                    LengthMeasurer.measure_cubic(ret_cubics_raw[i]),
                )
                measured_cubics.append(mc)
                start_progress = end_progress

        # ensure last cubic ends at 1.0
        if measured_cubics:
            measured_cubics[-1].update_progress_range(end_outline_progress=1.0)

        # shift feature progresses
        new_features = []
        for f in self._features:
            new_prog = (f.progress - cutting_point) % 1.0
            new_features.append(MeasuredFeature(new_prog, f.feature))

        return MeasuredPolygon(new_features, measured_cubics)

    @staticmethod
    def measure_polygon(polygon: "RoundedPolygon") -> "MeasuredPolygon":
        # Note: Each corner's progress is the midpoint of its middle rounding cubic's progress
        # range - this gives a single representative position along the perimeter.

        # Flatten all features' curves into a single list, tracking which cubic
        # index corresponds to each corner feature's middle curve
        cubics = []
        feature_to_cubic = []  # contains the main corner feature (flank + corner + flank = corner feature)

        for feature_index, feature in enumerate(polygon.features):
            for cubic_index, cubic in enumerate(feature.curves):
                # extract main corner features at the middle curve
                if feature.type == "corner" and cubic_index == len(feature.curves) // 2:
                    feature_to_cubic.append((feature, len(cubics)))
                cubics.append(cubic)

        if not cubics:
            return MeasuredPolygon([], [])

        # contains the cumulative measures of the cubic. [0.1, (0.1+0.3), ...]
        measures = [0.0]
        for cubic in cubics:
            size = LengthMeasurer.measure_cubic(cubic)
            assert size >= 0, "Measured cubic is expected to be >= 0"
            measures.append(measures[-1] + size)

        total_measure = measures[-1]
        if total_measure == 0:
            total_measure = 1.0

        # normalize to [0,1]
        outline_progress = [m / total_measure for m in measures]

        # brand features with progress val
        features = []
        for feature, ix in feature_to_cubic:
            if ix + 1 < len(outline_progress):
                prog = ((outline_progress[ix] + outline_progress[ix + 1]) / 2) % 1.0
                features.append(MeasuredFeature(prog, feature))

        # filter out empty cubics and chain start/end progress correctly
        filtered_cubics: List[Cubic] = []
        start_progress = 0.0
        for i in range(len(cubics)):
            progress_size = outline_progress[i + 1] - outline_progress[i]
            if progress_size > DistanceEpsilon:
                mc = MeasuredCubic(
                    cubics[i],
                    start_progress,
                    outline_progress[i + 1],
                    LengthMeasurer.measure_cubic(cubics[i]),
                )
                filtered_cubics.append(mc)
                # next cubic starts exactly where this one ends
                start_progress = outline_progress[i + 1]

        # ensure last cubic ends at 1.0
        if filtered_cubics:
            filtered_cubics[-1].update_progress_range(end_outline_progress=1.0)

        return MeasuredPolygon(features, filtered_cubics)

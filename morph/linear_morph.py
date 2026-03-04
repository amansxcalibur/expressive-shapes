import math
from typing import List
from pprint import pprint
from dataclasses import dataclass


@dataclass
class MorphPoint:
    progress: float
    x: float
    y: float

    def to_tuple(self):
        return (self.x, self.y)


class Morph:
    @staticmethod
    def _dist(a, b):
        return math.hypot(b[0] - a[0], b[1] - a[1])

    @staticmethod
    def get_winding_order(vertices):
        """Returns True if clockwise, False if counter-clockwise (Shoelace formula)."""
        area = 0
        for i in range(len(vertices)):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % len(vertices)]
            area += (p2[0] - p1[0]) * (p2[1] + p1[1])
        return area > 0

    @staticmethod
    def create_progress_points(points):
        """Converts [(x,y)...] to [MorphPoint...] based on perimeter distance."""
        distances = [
            Morph._dist(points[i], points[(i + 1) % len(points)])
            for i in range(len(points))
        ]
        total_perimeter = sum(distances)

        progress_points = []
        current_dist = 0.0
        for i in range(len(points)):
            prog = current_dist / total_perimeter if total_perimeter > 0 else 0
            progress_points.append(MorphPoint(prog, points[i][0], points[i][1]))
            current_dist += distances[i]

        return progress_points

    @staticmethod
    def balance_morph_points(
        v1_mp: List[MorphPoint], target_count: int
    ) -> List[MorphPoint]:
        """Adds points to v1 by splitting the longest edges until it matches target_count."""
        result = list(v1_mp)

        while len(result) < target_count:
            max_gap = -1.0
            insert_at = -1

            for i in range(len(result)):
                p1 = result[i]
                p2 = result[(i + 1) % len(result)]

                # Calculate progress gap (handling 1.0 -> 0.0 wrap-around)
                gap = (
                    (p2.progress - p1.progress)
                    if p2.progress > p1.progress
                    else (1.0 - p1.progress + p2.progress)
                )

                if gap > max_gap:
                    max_gap = gap
                    insert_at = i + 1

            # Interpolate new point at the midpoint of the longest gap
            start_node = result[insert_at - 1]
            end_node = result[insert_at % len(result)]

            mid_progress = (start_node.progress + (max_gap / 2)) % 1.0
            mid_x = (start_node.x + end_node.x) / 2
            mid_y = (start_node.y + end_node.y) / 2

            result.insert(insert_at, MorphPoint(mid_progress, mid_x, mid_y))

        return result

    @staticmethod
    def map_vertices_1_to_1(v1_mp, v2_mp):
        """Finds the rotation of v2 that minimizes the distance to v1[0]."""
        best_start_idx = 0
        min_dist = float("inf")

        # determine the "least twisted" starting point
        for shift in range(len(v2_mp)):
            d = Morph._dist(v1_mp[0].to_tuple(), v2_mp[shift].to_tuple())
            if d < min_dist:
                min_dist = d
                best_start_idx = shift

        mapping = []
        for i in range(len(v1_mp)):
            target_idx = (i + best_start_idx) % len(v2_mp)
            mapping.append((v1_mp[i], v2_mp[target_idx]))

        return mapping

    @staticmethod
    def map_vertices(v1: list, v2: list):
        print("\n" + "=" * 30)

        # align winding
        if Morph.get_winding_order(v1) != Morph.get_winding_order(v2):
            v2 = v2[::-1]

        swapped = False
        if len(v1) > len(v2):
            v1, v2 = v2, v1
            swapped = True

        # compute progress (per unit of the perimeter)
        v1_mp = Morph.create_progress_points(v1)
        v2_mp = Morph.create_progress_points(v2)

        print("\n--- Initial Points (V1) ---")
        pprint(v1_mp)
        print("\n--- Initial Points (V2) ---")
        pprint(v2_mp)

        # equalize vertex counts
        equalized_v1_mp = Morph.balance_morph_points(v1_mp, len(v2_mp))

        print(f"\n--- Equalized V1 (Now {len(equalized_v1_mp)} points) ---")
        pprint(equalized_v1_mp)

        # 1:1 mapping
        print("\n--- Mapping (V1 -> V2) ---")
        mapping = Morph.map_vertices_1_to_1(equalized_v1_mp, v2_mp)
        pprint(mapping)

        mapped_v1 = [p1.to_tuple() for p1, p2 in mapping]
        mapped_v2 = [p2.to_tuple() for p1, p2 in mapping]

        print("=" * 30 + "\n")
        return (mapped_v2, mapped_v1) if swapped else (mapped_v1, mapped_v2)

    @staticmethod
    def get_interpolated(v1, v2, alpha):
        morphed = [
            (p1[0] + (p2[0] - p1[0]) * alpha, p1[1] + (p2[1] - p1[1]) * alpha)
            for p1, p2 in zip(v1, v2)
        ]
        print(f"\n=== alpha: {alpha} ===")
        pprint(morphed)
        return morphed

        # so the old algo goes like this.
        # triangle ->square
        # cycle 1
        # 0->0
        # 0.33->0.5
        # 0.66->0.25
        # cycle 2
        # 0->0 good
        # 0.33->0.5 good
        # 0.66->0.25 bad

        # then the algo goes
        # prev=0.33->0.5
        # next=1.0->1.0 or 0.75
        # # map to the closest in square progress
        # 0.66->0.75

        # cycle3
        # square list check for unpaired.
        # find s2 0.25
        # prev = 0.0->triangle 0
        # next = 0.5->triangle 0.33
        # check mapping with triangle
        # put point between 0 and 0.33 = 0.16
        # this algo could be useful for maybe more dynamic interpolations...maybe

        # for vert in v1

        # map
        # v2_map_limit = 0
        # for point_v1 in v1_mp:
        #     vertex_1 = point_v1.to_tuple()

        #     candidates = []
        #     # cycle 2
        #     search_area = v2_mp[v2_map_limit:]

        #     for offset, point_v2 in enumerate(search_area):
        #         dist = Morph._dist(vertex_1, point_v2.to_tuple())
        #         # Store (distance, point, original_index)
        #         candidates.append((dist, point_v2, v2_map_limit + offset))

        #     if candidates:
        #         # Find the closest point
        #         best_match = min(candidates, key=lambda x: x[0])

        #         min_dist_point = best_match[1]
        #         chosen_index = best_match[2] # This is the index in v2_mp

        #         mapping.append((point_v1, min_dist_point))

        #         # Update the limit to the next index so we don't look back
        #         v2_map_limit = chosen_index + 1

        # print()
        # pprint(mapping)

        # # cycle 2
        # map_length = len(mapping)
        # for idx, pair in enumerate(mapping):
        #     if idx==0:
        #         prev=pair[1]
        #         next=mapping[idx+1][1]
        #     elif idx==map_length-1:
        #         prev=mapping[idx-1][1]
        #         next=pair[1]
        #     else:
        #         prev=mapping[idx-1][1]
        #         next=mapping[idx+1][1]

        #     print()
        #     pprint(pair)
        #     if prev.progress>next.progress:
        #         print("==bad==")
        #     else:
        #         print("==good==")

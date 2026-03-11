from __future__ import annotations

from ..geometry.polygon_measure import MeasuredPolygon


def _debug_enabled() -> bool:
    import expressive_shapes

    return expressive_shapes.DEBUG


class MorphDebugger:
    @staticmethod
    def inspect_all(poly1, poly2):
        if not _debug_enabled():
            return
        print(f"\n{'=' * 24} MORPH INSPECTION {'=' * 24}")
        m1 = MeasuredPolygon.measure_polygon(poly1)
        m2 = MeasuredPolygon.measure_polygon(poly2)

        MorphDebugger.print_poly_summary("POLYGON 1 (Source)", m1)
        MorphDebugger.print_poly_summary("POLYGON 2 (Target)", m2)

    @staticmethod
    def print_mapping_results(measured_poly1, measured_poly2, mapping_pairs):
        if not _debug_enabled():
            return
        print("\n[ FEATURE ALIGNMENT MAP ]")
        print(
            f"{'Src Idx':<8} | {'Tgt Idx':<8} | {'Src Progress':<12} | {'Tgt Progress':<12}"
        )
        print("-" * 60)

        # Helper to find index by progress
        def get_idx(poly, prog):
            for i, mf in enumerate(poly.features):
                if abs(mf.progress - prog) < 1e-6:
                    return i
            return "?"

        for p1, p2 in mapping_pairs:
            idx1 = get_idx(measured_poly1, p1)
            idx2 = get_idx(measured_poly2, p2)
            print(f"{idx1:<8} | {idx2:<8} | {p1:<12.4f} | {p2:<12.4f}")

    @staticmethod
    def print_distance_matrix(features1, features2):
        if not _debug_enabled():
            return
        # avoid circular dependency
        from .bezier_morph import Morph

        print("\n[ GEOMETRIC DISTANCE MATRIX (Squared) ]")
        header = "       " + "".join([f"T{i:<8}" for i in range(len(features2))])
        print(header)
        print("-" * len(header))

        for i, f1 in enumerate(features1):
            row = f"S{i:<3} | "
            for f2 in features2:
                dist = Morph.feature_dist_squared(f1, f2)
                if dist == float("inf"):
                    row += f"{'inf':<9}"
                else:
                    row += f"{dist:<9.3f}"
            print(row)

    @staticmethod
    def print_walking_header():
        if not _debug_enabled():
            return
        print("\n[ MORPH GENERATION: WALKING THE PATH ]")
        print(f"{'Step':<5} | {'P1 End':<10} | {'P2 (Mapped)':<12} | {'Action'}")
        print("-" * 55)

    @staticmethod
    def print_poly_summary(label, measured_poly):
        if not _debug_enabled():
            return
        from .bezier_morph import Morph  # Avoid circular import

        print(f"\n--- {label} ---")
        print(
            f"{'Idx':<4} | {'Type':<8} | {'Convex':<7} | {'Mid-Prog':<10} | {'Coordinates (X, Y)'}"
        )
        print("-" * 75)

        for i, mf in enumerate(measured_poly.features):
            is_convex = getattr(mf.feature, "is_convex", "N/A")
            conv_str = (
                "YES" if is_convex is True else "NO" if is_convex is False else "N/A"
            )

            # Get physical point
            pt = Morph.feature_representative_point(mf.feature)

            print(
                f"{i:<4} | {mf.feature.type:<8} | {conv_str:<7} | {mf.progress:<10.4f} | ({pt.x:>7.2f}, {pt.y:>7.2f})"
            )

        print(f"Total Path Length: 1.0 (across {len(measured_poly)} cubics)")

    @staticmethod
    def print_mapping_decisions(distance_vertex_list, final_mapping):
        if not _debug_enabled():
            return
        from .bezier_morph import Morph

        print("\n[ MAPPING DECISION LOG ]")
        print(
            f"{'S_Idx':<5} | {'T_Idx':<5} | {'Source (X,Y)':<18} | {'Target (X,Y)':<18} | {'Status'}"
        )
        print("-" * 75)

        final_set = set(final_mapping)

        for dv in distance_vertex_list:
            pair = (dv.f1.progress, dv.f2.progress)

            s_idx = getattr(dv.f1, "index", "?")
            t_idx = getattr(dv.f2, "index", "?")

            p1 = Morph.feature_representative_point(dv.f1.feature)
            p2 = Morph.feature_representative_point(dv.f2.feature)

            status = "[Y]" if pair in final_set else "[N]"
            print(
                f"{s_idx:<5} | {t_idx:<5} | ({p1.x:>5.1f},{p1.y:>5.1f}) | ({p2.x:>5.1f},{p2.y:>5.1f}) | {status}"
            )

    @staticmethod
    def print_final_matched_pairs(matched_pairs):
        if not _debug_enabled():
            return
        print("\n[ FINAL MATCHED SEGMENT LIST ]")
        print(f"{'Pair':<5} | {'Source Start':<18} | {'Target Start':<18} | {'Type'}")
        print("-" * 65)

        for i, (c1, c2) in enumerate(matched_pairs):
            p1 = c1.p0
            p2 = c2.p0

            is_line = "Line" if (getattr(c1, "is_linear", False)) else "Curve"

            s_coord = f"({p1.x:>5.1f}, {p1.y:>5.1f})"
            t_coord = f"({p2.x:>5.1f}, {p2.y:>5.1f})"

            print(f"{i:<5} | {s_coord:<18} | {t_coord:<18} | {is_line}")
        print(f"Total Segments for Morph: {len(matched_pairs)}")

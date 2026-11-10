"""closest_pair.py

Closest pair of points in 2D:
1. Brute force: O(n^2)
2. Divide and conquer: O(n log n)

Both functions accept an optional `stats` dict. When given, they record the
number of distance comparisons and a short trace the web interface animates.
"""

import math

TRACE_DEPTH = 3  # record the top recursion levels only (keeps the trace readable)


def euclidean_dist(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def closest_pair_brute_force(points, stats=None, record=False):
    """Compare every pair. Returns (min_distance, (point_a, point_b))."""
    best, pair = float("inf"), None
    count = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d = euclidean_dist(points[i], points[j])
            count += 1
            if d < best:
                best, pair = d, (points[i], points[j])
                if record and stats is not None:
                    stats.setdefault("improvements", []).append(
                        {"d": d, "pair": [list(points[i]), list(points[j])], "i": i}
                    )
    if stats is not None:
        stats["comparisons"] = stats.get("comparisons", 0) + count
    return best, pair


def closest_pair_divide_and_conquer(points, stats=None):
    """Sort by x once, split at the median, solve both halves, then check the
    strip around the dividing line. Returns (min_distance, (point_a, point_b))."""
    # Each point carries its rank in x-order, so duplicate points are handled safely.
    px = sorted(points)
    py = sorted(((p[1], p[0], r) for r, p in enumerate(px)))
    py = [(x, y, r) for y, x, r in py]  # (x, y, rank), sorted by y

    def solve(lo, hi, by_y, depth):
        if hi - lo <= 3:
            return closest_pair_brute_force([(x, y) for x, y, _ in by_y], stats)
        mid = (lo + hi) // 2
        mid_x = px[mid][0]

        step = None
        if stats is not None and depth <= TRACE_DEPTH:
            step = {"depth": depth, "size": hi - lo, "mid_x": mid_x}
            stats.setdefault("steps", []).append(step)  # pre-order: top levels first

        left = [p for p in by_y if p[2] < mid]
        right = [p for p in by_y if p[2] >= mid]
        d1, pair1 = solve(lo, mid, left, depth + 1)
        d2, pair2 = solve(mid, hi, right, depth + 1)
        delta, pair = (d1, pair1) if d1 < d2 else (d2, pair2)
        delta_before = delta

        strip = [p for p in by_y if abs(p[0] - mid_x) < delta]
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 8, len(strip))):
                d = euclidean_dist(strip[i], strip[j])
                if stats is not None:
                    stats["comparisons"] = stats.get("comparisons", 0) + 1
                if d < delta:
                    delta, pair = d, ((strip[i][0], strip[i][1]), (strip[j][0], strip[j][1]))

        if step is not None:
            step.update(delta_before=delta_before, delta=delta, strip_size=len(strip),
                        improved=delta < delta_before)
        return delta, pair

    return solve(0, len(px), py, 0)


def load_dataset(filepath):
    """File format: first line n, then n lines of 'x y'."""
    with open(filepath, "r", encoding="utf-8") as f:
        return parse_points(f.read())


def parse_points(text):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    n = int(lines[0])
    return [tuple(map(float, ln.split()[:2])) for ln in lines[1:n + 1]]


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    pts = load_dataset(os.path.join(here, "datasets", "cp_01.txt"))
    print(closest_pair_divide_and_conquer(pts))
    print(closest_pair_brute_force(pts))

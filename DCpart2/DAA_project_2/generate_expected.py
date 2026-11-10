"""generate_expected.py

Writes expected_results.txt: the reference ("manual") answer for every dataset,
computed with methods that do NOT use the divide-and-conquer code:
  - closest pair : plain nested loops over every pair (math.dist), with the
                   line numbers of the two points so you can check them by hand
  - multiplication: Python's built-in big-integer multiplication
"""

import math
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(ROOT, "datasets")
OUT = os.path.join(ROOT, "expected_results.txt")


def read_points(path):
    with open(path, encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    n = int(lines[0])
    return [tuple(map(float, ln.split()[:2])) for ln in lines[1:n + 1]]


def read_numbers(path):
    with open(path, encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    return lines[0], lines[1]


def reference_closest_pair(pts):
    best, bi, bj = float("inf"), -1, -1
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = math.dist(pts[i], pts[j])
            if d < best:
                best, bi, bj = d, i, j
    return best, bi, bj


def main():
    out = ["CS302 REFERENCE RESULTS (computed without divide-and-conquer)", "=" * 70, ""]
    names = sorted(f for f in os.listdir(DATASET_DIR) if f.endswith(".txt"))
    for name in names:
        path = os.path.join(DATASET_DIR, name)
        if name.startswith("cp_"):
            pts = read_points(path)
            d, i, j = reference_closest_pair(pts)
            out += [f"### {name}  (closest pair, n = {len(pts)})",
                    f"distance : {d!r}",
                    f"point A  : {pts[i][0]} {pts[i][1]}   (point #{i + 1}, file line {i + 2})",
                    f"point B  : {pts[j][0]} {pts[j][1]}   (point #{j + 1}, file line {j + 2})", ""]
        elif name.startswith("mul_"):
            x, y = read_numbers(path)
            out += [f"### {name}  (multiplication, {len(x)} digits each)",
                    f"X       : {x}",
                    f"Y       : {y}",
                    f"X * Y   : {int(x) * int(y)}", ""]
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"Wrote {OUT} ({len(names)} datasets)")


if __name__ == "__main__":
    import sys
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(50000)
    main()

"""verify_results.py

Runs the project's algorithms on every dataset and compares the output with the
reference answers stored in expected_results.txt (see generate_expected.py).
"""

import math
import os
import sys

from closest_pair import closest_pair_divide_and_conquer, closest_pair_brute_force, load_dataset as load_cp
from karatsuba import karatsuba_multiply, schoolbook_multiply, load_dataset as load_mul

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(50000)

ROOT = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(ROOT, "datasets")
EXPECTED = os.path.join(ROOT, "expected_results.txt")


def parse_expected():
    exp, cur = {}, None
    with open(EXPECTED, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("### "):
                cur = line[4:].split()[0]
                exp[cur] = {}
            elif cur and " : " in line:
                key, val = line.split(" : ", 1)
                exp[cur][key.strip()] = val.strip()
    return exp


def verify():
    if not os.path.exists(EXPECTED):
        from generate_expected import main as gen
        gen()
    exp = parse_expected()
    passed = failed = 0

    print(f"{'File':<12} {'Algorithm':<22} {'Result':<8} Detail")
    print("-" * 78)
    for name in sorted(exp):
        e = exp[name]
        path = os.path.join(DATASET_DIR, name)
        if name.startswith("cp_"):
            pts = load_cp(path)
            want = float(e["distance"])
            for label, fn in (("Divide & Conquer", closest_pair_divide_and_conquer),
                              ("Brute Force", closest_pair_brute_force)):
                got = fn(pts)[0]
                ok = math.isclose(got, want, rel_tol=1e-9)
                passed, failed = passed + ok, failed + (not ok)
                print(f"{name:<12} {label:<22} {'PASS' if ok else 'FAIL':<8} got {got:.6f} | expected {want:.6f}")
        else:
            x, y = load_mul(path)
            want = e["X * Y"]
            for label, fn in (("Karatsuba", karatsuba_multiply), ("Schoolbook", schoolbook_multiply)):
                got = fn(x, y)
                ok = got == want
                passed, failed = passed + ok, failed + (not ok)
                print(f"{name:<12} {label:<22} {'PASS' if ok else 'FAIL':<8} {len(got)}-digit product "
                      f"{'matches' if ok else 'DIFFERS from'} expected")
    print("-" * 78)
    print(f"{passed} passed, {failed} failed (out of {passed + failed} checks)")
    return failed == 0


if __name__ == "__main__":
    sys.exit(0 if verify() else 1)

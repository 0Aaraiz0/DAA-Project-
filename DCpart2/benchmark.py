"""benchmark.py

Runs all 20 benchmark datasets and prints cleanly formatted tables
of measured execution times for:
1. Closest Pair: Divide-and-Conquer vs. Brute-Force
2. Integer Multiplication: Karatsuba vs. Schoolbook

Results are also saved to benchmark_results.csv.
"""

import csv
import math
import os
import time

from closest_pair import closest_pair_divide_and_conquer, closest_pair_brute_force, load_dataset as load_cp
from karatsuba import karatsuba_multiply, schoolbook_multiply, load_dataset as load_mul

ROOT = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(ROOT, "datasets")


def collect_results():
    """Run every dataset; return {'cp': [rows], 'mul': [rows]}. Raises on any wrong answer."""
    cp_rows, mul_rows = [], []

    cp_files = sorted(f for f in os.listdir(DATASET_DIR) if f.startswith("cp_") and f.endswith(".txt"))
    for fname in cp_files:
        pts = load_cp(os.path.join(DATASET_DIR, fname))

        t0 = time.perf_counter()
        d_dc, _ = closest_pair_divide_and_conquer(pts)
        t_dc = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        d_bf, _ = closest_pair_brute_force(pts)
        t_bf = (time.perf_counter() - t0) * 1000

        assert math.isclose(d_dc, d_bf, rel_tol=1e-9), f"Mismatch in {fname}"
        cp_rows.append({"file": fname, "n": len(pts), "dc_ms": t_dc, "bf_ms": t_bf,
                        "speedup": t_bf / t_dc if t_dc > 0 else 1.0, "min_dist": d_dc, "check": "PASS"})

    mul_files = sorted(f for f in os.listdir(DATASET_DIR) if f.startswith("mul_") and f.endswith(".txt"))
    for fname in mul_files:
        x_val, y_val = load_mul(os.path.join(DATASET_DIR, fname))

        t0 = time.perf_counter()
        prod_kar = karatsuba_multiply(x_val, y_val)
        t_kar = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        prod_sb = schoolbook_multiply(x_val, y_val)
        t_sb = (time.perf_counter() - t0) * 1000

        expected = str(int(x_val) * int(y_val))
        assert prod_kar == expected and prod_sb == expected, f"Calculation mismatch in {fname}"
        mul_rows.append({"file": fname, "digits": len(x_val), "kar_ms": t_kar, "sb_ms": t_sb,
                         "speedup": t_sb / t_kar if t_kar > 0 else 1.0, "check": "PASS"})

    return {"cp": cp_rows, "mul": mul_rows}


def save_csv(results, path=os.path.join(ROOT, "benchmark_results.csv")):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["problem", "file", "size", "fast_ms", "slow_ms", "speedup", "check"])
        for r in results["cp"]:
            w.writerow(["closest_pair", r["file"], r["n"], f"{r['dc_ms']:.3f}", f"{r['bf_ms']:.3f}",
                        f"{r['speedup']:.2f}", r["check"]])
        for r in results["mul"]:
            w.writerow(["multiplication", r["file"], r["digits"], f"{r['kar_ms']:.3f}", f"{r['sb_ms']:.3f}",
                        f"{r['speedup']:.2f}", r["check"]])


def run_all_benchmarks():
    print("=" * 80)
    print("CS302 ALGORITHMS BENCHMARK EXECUTION (20 DATASETS)")
    print("=" * 80)
    res = collect_results()

    print("\n[PART 1] Closest Pair of Points (2D)")
    print("-" * 80)
    print(f"{'File':<12} {'Points (n)':<12} {'D&C (ms)':<15} {'Brute-Force (ms)':<18} {'Speedup':<10} {'Min Dist':<12}")
    print("-" * 80)
    for r in res["cp"]:
        print(f"{r['file']:<12} {r['n']:<12} {r['dc_ms']:<15.3f} {r['bf_ms']:<18.3f} "
              f"{r['speedup']:.2f}x{'':<5} {r['min_dist']:<12.4f}")

    print("\n\n[PART 2] Integer Multiplication (Manual String Operations)")
    print("-" * 80)
    print(f"{'File':<12} {'Digits (d)':<12} {'Karatsuba (ms)':<15} {'Schoolbook (ms)':<18} {'Speedup':<10} {'Check':<10}")
    print("-" * 80)
    for r in res["mul"]:
        print(f"{r['file']:<12} {r['digits']:<12} {r['kar_ms']:<15.3f} {r['sb_ms']:<18.3f} "
              f"{r['speedup']:.2f}x{'':<5} {r['check']:<10}")

    save_csv(res)
    print("=" * 80)
    print(f"All {len(res['cp']) + len(res['mul'])} benchmarks completed and verified against ground truth.")
    print("Saved to benchmark_results.csv")
    print("=" * 80)
    return res


if __name__ == "__main__":
    run_all_benchmarks()

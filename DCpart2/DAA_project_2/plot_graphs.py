"""plot_graphs.py

Measures both algorithms on all 20 datasets and saves comparison graphs to graphs/:
  1. closest_pair_runtime.png      D&C vs brute force, time against n
  2. multiplication_runtime.png    Karatsuba vs schoolbook, time against digits
  3. speedup.png                   how many times faster the divide-and-conquer version is
  4. operation_counts.png          machine-independent work done (log scale)

Needs matplotlib:  pip install matplotlib
Each timing is the best of 3 runs to reduce noise.
"""

import os
import sys
import time

import matplotlib
matplotlib.use("Agg")  # no window needed, just write PNG files
import matplotlib.pyplot as plt

from closest_pair import closest_pair_divide_and_conquer, closest_pair_brute_force, load_dataset as load_cp
from karatsuba import karatsuba_multiply, schoolbook_multiply, load_dataset as load_mul

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(50000)

ROOT = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(ROOT, "datasets")
GRAPH_DIR = os.path.join(ROOT, "graphs")
REPEATS = 3
BLUE, GREEN, ORANGE, RED = "#1a5fb4", "#26a269", "#e66100", "#c01c28"


def best_ms(fn, *args):
    best = float("inf")
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        fn(*args)
        best = min(best, (time.perf_counter() - t0) * 1000)
    return best


def measure():
    cp, mul = [], []
    for f in sorted(os.listdir(DATASET_DIR)):
        path = os.path.join(DATASET_DIR, f)
        if f.startswith("cp_") and f.endswith(".txt"):
            pts = load_cp(path)
            s_dc, s_bf = {}, {}
            closest_pair_divide_and_conquer(pts, s_dc)
            closest_pair_brute_force(pts, s_bf)
            cp.append({"n": len(pts), "dc": best_ms(closest_pair_divide_and_conquer, pts),
                       "bf": best_ms(closest_pair_brute_force, pts),
                       "dc_ops": s_dc["comparisons"], "bf_ops": s_bf["comparisons"]})
            print(f"  {f}: n={len(pts)}")
        elif f.startswith("mul_") and f.endswith(".txt"):
            x, y = load_mul(path)
            s_k, s_s = {}, {}
            karatsuba_multiply(x, y, s_k)
            schoolbook_multiply(x, y, s_s)
            mul.append({"d": len(x), "kar": best_ms(karatsuba_multiply, x, y),
                        "sb": best_ms(schoolbook_multiply, x, y),
                        "kar_ops": s_k["digit_mults"], "sb_ops": s_s["digit_mults"]})
            print(f"  {f}: digits={len(x)}")
    cp.sort(key=lambda r: r["n"])
    mul.sort(key=lambda r: r["d"])
    return cp, mul


def style(ax, xlabel, ylabel, title):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.legend()


def save(fig, name):
    fig.tight_layout()
    path = os.path.join(GRAPH_DIR, name)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print("  saved", path)


def main():
    os.makedirs(GRAPH_DIR, exist_ok=True)
    print("Measuring all 20 datasets (best of 3 runs each)...")
    cp, mul = measure()
    n = [r["n"] for r in cp]
    d = [r["d"] for r in mul]

    # 1. Closest pair runtime
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(n, [r["bf"] for r in cp], "o-", color=RED, label="Brute Force  O(n²)")
    ax.plot(n, [r["dc"] for r in cp], "s-", color=BLUE, label="Divide & Conquer  O(n log n)")
    style(ax, "Number of points (n)", "Runtime (ms)", "Closest Pair: Runtime vs Input Size")
    save(fig, "closest_pair_runtime.png")

    # 2. Multiplication runtime
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(d, [r["sb"] for r in mul], "o-", color=RED, label="Schoolbook  O(n²)")
    ax.plot(d, [r["kar"] for r in mul], "s-", color=GREEN, label="Karatsuba  O(n^1.585)")
    style(ax, "Number of digits", "Runtime (ms)", "Integer Multiplication: Runtime vs Input Size")
    save(fig, "multiplication_runtime.png")

    # 3. Speedup
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.5))
    a1.plot(n, [r["bf"] / r["dc"] for r in cp], "o-", color=BLUE, label="Brute Force time / D&C time")
    style(a1, "Number of points (n)", "Speedup (x times faster)", "Closest Pair Speedup")
    a2.plot(d, [r["sb"] / r["kar"] for r in mul], "o-", color=GREEN, label="Schoolbook time / Karatsuba time")
    style(a2, "Number of digits", "Speedup (x times faster)", "Multiplication Speedup")
    save(fig, "speedup.png")

    # 4. Operation counts (independent of the computer used)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.5))
    a1.plot(n, [r["bf_ops"] for r in cp], "o-", color=RED, label="Brute Force")
    a1.plot(n, [r["dc_ops"] for r in cp], "s-", color=BLUE, label="Divide & Conquer")
    a1.set_yscale("log")
    style(a1, "Number of points (n)", "Distance comparisons (log scale)", "Closest Pair: Work Done")
    a2.plot(d, [r["sb_ops"] for r in mul], "o-", color=RED, label="Schoolbook")
    a2.plot(d, [r["kar_ops"] for r in mul], "s-", color=GREEN, label="Karatsuba")
    a2.set_yscale("log")
    style(a2, "Number of digits", "Single-digit multiplications (log scale)", "Multiplication: Work Done")
    save(fig, "operation_counts.png")
    print("Done.")


if __name__ == "__main__":
    main()

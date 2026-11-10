"""karatsuba.py

Simple, clean implementation of Large Integer Multiplication:
1. Schoolbook: O(n * m) digit-by-digit grade-school multiplication.
2. Karatsuba: O(n^1.585) divide-and-conquer using 3 recursive subproducts.
3. String Addition and Subtraction (manual, no built-in big-int multiplication).
"""

import sys
import time

# Allow verification of large numbers with Python's built-in int
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(50000)


BASE_CASE_DIGITS = 32
TRACE_DEPTH = 2  # recursion levels written to the visual trace


def add_strings(a: str, b: str) -> str:
    """Adds two non-negative digit strings column by column."""
    i, j, carry = len(a) - 1, len(b) - 1, 0
    res = []
    while i >= 0 or j >= 0 or carry:
        d1 = ord(a[i]) - 48 if i >= 0 else 0
        d2 = ord(b[j]) - 48 if j >= 0 else 0
        s = d1 + d2 + carry
        carry = s // 10
        res.append(str(s % 10))
        i -= 1
        j -= 1
    return "".join(reversed(res))


def sub_strings(a: str, b: str) -> str:
    """Subtracts b from a (assuming a >= b >= 0) column by column."""
    i, j, borrow = len(a) - 1, len(b) - 1, 0
    res = []
    while i >= 0:
        d1 = ord(a[i]) - 48 - borrow
        d2 = ord(b[j]) - 48 if j >= 0 else 0
        if d1 < d2:
            d1 += 10
            borrow = 1
        else:
            borrow = 0
        res.append(str(d1 - d2))
        i -= 1
        j -= 1
    out = "".join(reversed(res)).lstrip("0")
    return out if out else "0"


def schoolbook_multiply(x: str, y: str, stats=None) -> str:
    """Grade-school multiplication on digit strings: O(n * m)."""
    if x == "0" or y == "0":
        return "0"

    n, m = len(x), len(y)
    if stats is not None:
        stats["digit_mults"] = stats.get("digit_mults", 0) + n * m
    result = [0] * (n + m)

    for i in range(n - 1, -1, -1):
        d1 = ord(x[i]) - 48
        carry = 0
        for j in range(m - 1, -1, -1):
            d2 = ord(y[j]) - 48
            total = d1 * d2 + result[i + j + 1] + carry
            carry = total // 10
            result[i + j + 1] = total % 10
        result[i] += carry

    out = "".join(str(d) for d in result).lstrip("0")
    return out if out else "0"


def karatsuba_multiply(x: str, y: str, stats=None, depth: int = 0) -> str:
    """Karatsuba multiplication on digit strings: O(n^1.585).

    Recurrence:
      X = 10^m * X1 + X0
      Y = 10^m * Y1 + Y0
      Z2 = X1 * Y1
      Z0 = X0 * Y0
      Z1 = (X1 + X0) * (Y1 + Y0) - Z2 - Z0
      Result = Z2 * 10^(2m) + Z1 * 10^m + Z0
    """
    x = x.lstrip("0") or "0"
    y = y.lstrip("0") or "0"

    if stats is not None:
        stats["calls"] = stats.get("calls", 0) + 1
        stats["max_depth"] = max(stats.get("max_depth", 0), depth)

    if x == "0" or y == "0":
        return "0"

    # Base case: below this size recursion overhead beats the savings
    if len(x) <= BASE_CASE_DIGITS or len(y) <= BASE_CASE_DIGITS:
        if stats is not None:
            stats["base_cases"] = stats.get("base_cases", 0) + 1
        return schoolbook_multiply(x, y, stats)

    # Pad with leading zeros to equalize lengths
    n = max(len(x), len(y))
    x_pad = x.zfill(n)
    y_pad = y.zfill(n)

    m = n // 2
    x_high, x_low = x_pad[:-m], x_pad[-m:]
    y_high, y_low = y_pad[:-m], y_pad[-m:]

    trace = stats.setdefault("trace", []) if stats is not None else None
    log_this = trace is not None and depth <= TRACE_DEPTH and len(trace) < 60
    if log_this:
        pad = "  " * depth
        trace.append(f"{pad}[depth {depth}] {len(x)}d x {len(y)}d -> pad to {n}, split m = {m}: "
                     f"X = X1(10^{m}) + X0, Y = Y1(10^{m}) + Y0")

    # 3 recursive multiplications
    z2 = karatsuba_multiply(x_high, y_high, stats, depth + 1)
    z0 = karatsuba_multiply(x_low, y_low, stats, depth + 1)

    sum_x = add_strings(x_high, x_low)
    sum_y = add_strings(y_high, y_low)
    z1_comb = karatsuba_multiply(sum_x, sum_y, stats, depth + 1)

    # Z1 = z1_comb - z2 - z0
    z1 = sub_strings(sub_strings(z1_comb, z2), z0)

    # Combine: Z2 * 10^(2m) + Z1 * 10^m + Z0
    term2 = z2 + ("0" * (2 * m)) if z2 != "0" else "0"
    term1 = z1 + ("0" * m) if z1 != "0" else "0"

    total = add_strings(add_strings(term2, term1), z0)
    if log_this:
        trace.append(f"{pad}[depth {depth}] combine: Z2 ({len(z2)}d) x 10^{2*m} + Z1 ({len(z1)}d) x 10^{m} + Z0 ({len(z0)}d)")
    return total.lstrip("0") or "0"


def load_dataset(filepath):
    """Loads two integers from file: line 1 = X, line 2 = Y."""
    with open(filepath, "r", encoding="utf-8") as f:
        return parse_integers(f.read())


def parse_integers(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines[0], lines[1]


if __name__ == "__main__":
    # Test on first dataset
    import os
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datasets", "mul_01.txt")
    x_val, y_val = load_dataset(path)
    print(f"Loaded X ({len(x_val)} digits) and Y ({len(y_val)} digits) from {path}")

    t0 = time.perf_counter()
    prod_kar = karatsuba_multiply(x_val, y_val)
    t_kar = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    prod_sb = schoolbook_multiply(x_val, y_val)
    t_sb = (time.perf_counter() - t0) * 1000

    # Verification using Python's built-in big int
    expected = str(int(x_val) * int(y_val))
    is_correct = (prod_kar == expected == prod_sb)

    print(f"Karatsuba:  {prod_kar[:25]}... (len {len(prod_kar)}) in {t_kar:.2f} ms")
    print(f"Schoolbook: {prod_sb[:25]}... (len {len(prod_sb)}) in {t_sb:.2f} ms")
    print(f"Verified against Python int: {is_correct}")
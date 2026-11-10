"""Q1 - Levitin, Exercise 5.1 (2), p. 200: divide-and-conquer MIN and MAX."""
import random

count = 0  # key comparisons made by the divide-and-conquer version


def min_max(a, lo, hi):
    """Return (min, max) of a[lo..hi]."""
    global count
    if lo == hi:                          # base case: 1 element, 0 comparisons
        return a[lo], a[lo]
    if hi == lo + 1:                      # base case: 2 elements, 1 comparison
        count += 1
        return (a[lo], a[hi]) if a[lo] < a[hi] else (a[hi], a[lo])
    mid = (lo + hi) // 2                  # divide
    mn1, mx1 = min_max(a, lo, mid)        # conquer both halves
    mn2, mx2 = min_max(a, mid + 1, hi)
    count += 2                            # combine: compare minima, compare maxima
    return (mn1 if mn1 < mn2 else mn2), (mx1 if mx1 > mx2 else mx2)


def find_min_max(a):
    """Validated wrapper. Returns (min, max, comparisons)."""
    global count
    if len(a) == 0 or not all(isinstance(x, (int, float)) for x in a):
        raise ValueError("need a non-empty list of numbers")
    count = 0
    mn, mx = min_max(a, 0, len(a) - 1)
    return mn, mx, count


def brute_force(a):
    """Scan once; compare every element with the current min and max: 2(n-1) comparisons."""
    mn = mx = a[0]
    comparisons = 0
    for x in a[1:]:
        comparisons += 2
        if x < mn:
            mn = x
        if x > mx:
            mx = x
    return mn, mx, comparisons


def tests():
    assert find_min_max([5])[:2] == (5, 5)
    assert find_min_max([9, 2])[:2] == (2, 9)
    assert find_min_max([3] * 11)[:2] == (3, 3)                       # duplicates, odd size
    assert find_min_max(list(range(15)))[:2] == (0, 14)               # sorted
    assert find_min_max(list(range(15, 0, -1)))[:2] == (1, 15)        # reverse sorted
    for k in range(1, 11):                                            # n = 2^k: exactly 3n/2 - 2
        n = 2 ** k
        assert find_min_max(random.sample(range(10 * n), n))[2] == 3 * n // 2 - 2
    for n in range(1, 100):                                           # any n: correct, never worse than brute force
        a = [random.randint(-9, 9) for _ in range(n)]
        mn, mx, c = find_min_max(a)
        assert (mn, mx) == (min(a), max(a)) and c <= 2 * n - 2
    for bad in ([], ["a", 1]):
        try:
            find_min_max(bad)
            assert False
        except ValueError:
            pass
    print("Q1 tests passed")


def run(n):
    a = [random.randint(-50, 99) for _ in range(n)]
    print("Q1 array:", a)
    mn, mx, c = find_min_max(a)
    bmn, bmx, bc = brute_force(a)
    print(f"Divide and conquer: min={mn} max={mx} comparisons={c}")
    print(f"Brute force       : min={bmn} max={bmx} comparisons={bc}")
    assert (mn, mx) == (bmn, bmx)


def ask_size():
    while True:
        s = input("Enter n (>= 10): ")
        if s.isdigit() and int(s) >= 10:
            return int(s)
        print("n must be an integer >= 10")


if __name__ == "__main__":
    tests()
    run(ask_size())

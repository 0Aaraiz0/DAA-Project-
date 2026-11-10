"""Q6 - Kleinberg & Tardos, Algorithm Design 1st ed., Solved Exercise 1, p. 242 (solution pp. 243-244):
finding the peak of a unimodal array of distinct numbers by reading O(log n) entries."""
import random

reads = 0  # number of array entries read


def read(a, i):
    global reads
    reads += 1
    return a[i]


def peak(a, lo, hi):
    """Index (0-based) of the peak, known to lie in a[lo..hi]."""
    if lo == hi:
        return lo
    mid = (lo + hi) // 2
    here, right = read(a, mid), read(a, mid + 1)
    left = read(a, mid - 1) if mid - 1 >= lo else float("-inf")
    if left < here > right:                 # larger than both neighbours: the peak
        return mid
    if here < right:                        # going up: peak is to the right
        return peak(a, mid + 1, hi)
    return peak(a, lo, mid - 1)             # going down: peak is to the left


def is_unimodal(a):
    i = 0
    while i + 1 < len(a) and a[i] < a[i + 1]:
        i += 1
    while i + 1 < len(a) and a[i] > a[i + 1]:
        i += 1
    return len(a) > 0 and len(set(a)) == len(a) and i == len(a) - 1


def find_peak(a):
    """Validated wrapper. Returns (index, reads)."""
    global reads
    if not is_unimodal(a):
        raise ValueError("array must be non-empty, distinct and unimodal")
    reads = 0
    return peak(a, 0, len(a) - 1), reads


def make_unimodal(n, p):
    """Random distinct unimodal list of length n with the peak at index p."""
    vals = random.sample(range(10 * n), n)
    top = max(vals)
    rest = [v for v in vals if v != top]
    random.shuffle(rest)
    return sorted(rest[:p]) + [top] + sorted(rest[p:], reverse=True)


def tests():
    assert find_peak([1, 4, 9, 12, 15, 11, 8, 5, 3, 2])[0] == 4
    assert find_peak(list(range(10)))[0] == 9                  # increasing only
    assert find_peak(list(range(10, 0, -1)))[0] == 0           # decreasing only
    assert find_peak([42])[0] == 0
    for n in range(1, 60):                                     # every peak position
        for p in range(n):
            a = make_unimodal(n, p)
            idx, r = find_peak(a)
            assert idx == p == a.index(max(a))
            assert r <= 3 * (n.bit_length() - 1)               # at most 3 reads per level, floor(log2 n) levels
    for bad in ([], [1, 2, 2, 1], [3, 1, 2]):
        try:
            find_peak(bad)
            assert False
        except ValueError:
            pass
    print("Q6 tests passed")


def run(n):
    p = random.randrange(n)
    a = make_unimodal(n, p)
    idx, r = find_peak(a)
    print("Q6 array:", a)
    print(f"Peak at position {idx + 1} (1-indexed), value {a[idx]}; entries read = {r} (linear scan reads {n})")


def ask_size():
    while True:
        s = input("Enter n (>= 10): ")
        if s.isdigit() and int(s) >= 10:
            return int(s)
        print("n must be an integer >= 10")


if __name__ == "__main__":
    tests()
    run(ask_size())

"""Q4 - Levitin, Section 5.2, p. 202: quicksort (Hoare partition, first element as pivot)
and its best/worst-case behaviour."""
import math
import random
import sys

sys.setrecursionlimit(20000)   # worst case (sorted input) recurses n levels deep
count = 0                      # key comparisons


def partition(a, l, r):
    """Partition a[l..r] around pivot a[l]; return the pivot's final index."""
    global count
    p = a[l]
    i, j = l, r + 1
    while True:
        i += 1
        while i <= r:                 # scan right while a[i] < p
            count += 1
            if a[i] < p:
                i += 1
            else:
                break
        j -= 1
        while True:                   # scan left while a[j] > p
            count += 1
            if a[j] > p:
                j -= 1
            else:
                break
        if i >= j:
            break
        a[i], a[j] = a[j], a[i]
    a[l], a[j] = a[j], a[l]
    return j


def quicksort(a, l, r):
    if l < r:
        s = partition(a, l, r)
        quicksort(a, l, s - 1)
        quicksort(a, s + 1, r)


def sort(a):
    """Return (sorted copy, key comparisons)."""
    global count
    if not all(isinstance(x, (int, float)) for x in a):
        raise ValueError("list of numbers required")
    b = list(a)
    count = 0
    quicksort(b, 0, len(b) - 1)
    return b, count


def tests():
    cases = [[5, 3, 1, 9, 8, 2, 4, 7], [12, -7, 33, 5, 5, 41, -7, 0, 29, 18, 5],   # 11 elements, duplicates
             list(range(20)), list(range(20, 0, -1)), [4] * 15, [], [1], [2, 1]]
    for a in cases:
        assert sort(a)[0] == sorted(a)
    for _ in range(300):
        a = [random.randint(-20, 20) for _ in range(random.randint(0, 60))]
        assert sort(a)[0] == sorted(a)
    for n in (10, 50, 300):                                  # worst case matches Levitin's formula exactly
        assert sort(list(range(n)))[1] == (n + 1) * (n + 2) // 2 - 3
    try:
        sort(["a", 1])
        assert False
    except ValueError:
        pass
    print("Q4 tests passed")


def run(n):
    a = [random.randint(-50, 99) for _ in range(n)]
    out, c = sort(a)
    print("Q4 input :", a)
    print("Sorted   :", out)
    m = min(n, 3000)
    _, c_rand = sort([random.random() for _ in range(m)])
    _, c_sorted = sort(list(range(m)))
    print(f"n={m}: random input -> {c_rand} comparisons (about 1.39 n log2 n = {int(1.39 * m * math.log2(m))})")
    print(f"n={m}: sorted input -> {c_sorted} comparisons (worst case (n+1)(n+2)/2-3 = {(m + 1) * (m + 2) // 2 - 3})")


def ask_size():
    while True:
        s = input("Enter n (>= 10): ")
        if s.isdigit() and int(s) >= 10:
            return int(s)
        print("n must be an integer >= 10")


if __name__ == "__main__":
    tests()
    run(ask_size())

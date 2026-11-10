"""Q5 - Levitin, Exercise 5.5 (1), p. 223: one-dimensional closest pair by divide and conquer."""
import random

INF = float("inf")


def closest(s, lo, hi):
    """Closest pair inside the SORTED list s[lo..hi]. Returns (distance, x, y)."""
    if hi - lo < 1:                                   # one element: no pair
        return (INF, None, None)
    if hi - lo == 1:                                  # two elements: the only pair
        return (s[hi] - s[lo], s[lo], s[hi])
    mid = (lo + hi) // 2                              # divide by position
    best = min(closest(s, lo, mid), closest(s, mid + 1, hi))   # conquer
    cross = (s[mid + 1] - s[mid], s[mid], s[mid + 1])          # combine: only pair that straddles the split
    return min(best, cross)


def closest_pair(a):
    """Input need NOT be sorted: we sort first (n log n), then divide and conquer."""
    if len(a) < 2 or not all(isinstance(x, (int, float)) for x in a):
        raise ValueError("need at least two numbers")
    s = sorted(a)
    return closest(s, 0, len(s) - 1)


def sort_and_scan(a):
    """Simple alternative: sort, then look at adjacent elements."""
    s = sorted(a)
    return min((s[i + 1] - s[i], s[i], s[i + 1]) for i in range(len(s) - 1))


def brute_force(a):
    n = len(a)
    return min((abs(a[i] - a[j]), min(a[i], a[j]), max(a[i], a[j])) for i in range(n) for j in range(i + 1, n))


def tests():
    a = [41, 7, 93, 15, 62, 28, 80, 49, 3, 70, 57, 36]               # 12 numbers
    assert closest_pair(a) == sort_and_scan(a) == brute_force(a) == (4, 3, 7)
    assert closest_pair([5, 5])[0] == 0
    assert closest_pair([9, 1, 9, 4, 6, 8, 2, 7, 3, 10])[0] == 0     # duplicates -> distance 0
    assert closest_pair(list(range(0, 110, 10)))[0] == 10            # sorted
    assert closest_pair(list(range(100, -1, -10)))[0] == 10          # reverse sorted
    for _ in range(500):
        a = [random.randint(-50, 50) for _ in range(random.randint(2, 40))]
        assert closest_pair(a)[0] == sort_and_scan(a)[0] == brute_force(a)[0]
    for bad in ([], [1], ["a", 2]):
        try:
            closest_pair(bad)
            assert False
        except ValueError:
            pass
    print("Q5 tests passed")


def run(n):
    a = [random.randint(0, 5000) for _ in range(n)]
    print("Q5 numbers:", a)
    print("Divide and conquer (distance, x, y):", closest_pair(a))
    print("Sort + adjacent scan               :", sort_and_scan(a))
    print("Brute force                        :", brute_force(a))
    d = [5, 17, 42, 17, 90, 3, 61, 28, 77, 54]
    print("Duplicates", d, "->", closest_pair(d))


def ask_size():
    while True:
        s = input("Enter n (>= 10): ")
        if s.isdigit() and int(s) >= 10:
            return int(s)
        print("n must be an integer >= 10")


if __name__ == "__main__":
    tests()
    run(ask_size())

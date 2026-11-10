"""Q3 - Levitin, Exercise 5.1 (9), p. 201: counting inversions with a modified merge sort."""
import random


def sort_and_count(a):
    """Return (sorted copy of a, number of inversions in a). Input is not modified."""
    if len(a) <= 1:                                   # base case: no pairs
        return list(a), 0
    mid = len(a) // 2
    left, c_left = sort_and_count(a[:mid])            # inversions inside the left half
    right, c_right = sort_and_count(a[mid:])          # inversions inside the right half
    merged, cross, i, j = [], 0, 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:                       # ties: take left first (equal is not an inversion)
            merged.append(left[i])
            i += 1
        else:                                         # right[j] is smaller than ALL remaining left elements
            merged.append(right[j])
            j += 1
            cross += len(left) - i
    merged += left[i:] + right[j:]
    return merged, c_left + c_right + cross


def count_inversions(a):
    if not all(isinstance(x, (int, float)) for x in a):
        raise ValueError("list of numbers required")
    return sort_and_count(a)[1]


def brute_force(a):
    n = len(a)
    return sum(1 for i in range(n) for j in range(i + 1, n) if a[i] > a[j])


def tests():
    assert count_inversions([]) == 0 and count_inversions([5]) == 0
    assert count_inversions([2, 4, 1, 3, 5]) == 3
    sample = [8, 4, 2, 1, 9, 7, 3, 6, 5, 10]
    assert count_inversions(sample) == brute_force(sample) == 19
    for n in (10, 11, 40):
        assert count_inversions(list(range(n))) == 0                       # already sorted
        assert count_inversions(list(range(n, 0, -1))) == n * (n - 1) // 2  # reverse sorted
        assert count_inversions([7] * n) == 0                              # all equal
    for _ in range(500):                                                   # random, with many duplicates
        a = [random.randint(0, 6) for _ in range(random.randint(0, 40))]
        assert count_inversions(a) == brute_force(a)
    try:
        count_inversions(["x", 1])
        assert False
    except ValueError:
        pass
    print("Q3 tests passed")


def run(n):
    a = [random.randint(0, 30) for _ in range(n)]
    print("Q3 array:", a)
    print("Merge-sort count :", count_inversions(a))
    print("Brute-force count:", brute_force(a))


def ask_size():
    while True:
        s = input("Enter n (>= 10): ")
        if s.isdigit() and int(s) >= 10:
            return int(s)
        print("n must be an integer >= 10")


if __name__ == "__main__":
    tests()
    run(ask_size())

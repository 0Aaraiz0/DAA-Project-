"""Q8(b) - Kleinberg & Tardos, Algorithm Design 1st ed., Exercise 2, p. 246:
count significant inversions (pairs i < j with a[i] > 2*a[j]) in O(n log n)."""
import random


def sort_and_count(a):
    """Return (sorted copy of a, number of significant inversions)."""
    if len(a) <= 1:
        return list(a), 0
    mid = len(a) // 2
    left, c_left = sort_and_count(a[:mid])
    right, c_right = sort_and_count(a[mid:])
    cross, p = 0, 0
    for y in right:                          # right is ascending, so 2*y never decreases
        while p < len(left) and left[p] <= 2 * y:
            p += 1
        cross += len(left) - p               # left[p:] are all > 2*y
    merged, i, j = [], 0, 0                  # ordinary merge so the caller gets a sorted list
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged += left[i:] + right[j:]
    return merged, c_left + c_right + cross


def count_significant(a):
    if not all(isinstance(x, (int, float)) for x in a):
        raise ValueError("list of numbers required")
    return sort_and_count(a)[1]


def brute_force(a):
    n = len(a)
    return sum(1 for i in range(n) for j in range(i + 1, n) if a[i] > 2 * a[j])


def tests():
    assert count_significant([10, 4, 3, 1]) == 5          # hand-checked
    assert count_significant([5, 3, 2]) == 1              # hand-checked: only (5, 2)
    assert count_significant([]) == 0 and count_significant([7]) == 0
    assert count_significant(list(range(1, 15))) == 0     # increasing
    a = [14, 3, 9, 20, 1, 7, 18, 2, 11, 5]                # 10 elements
    assert count_significant(a) == brute_force(a)
    for _ in range(500):                                  # negatives, zero and duplicates included
        a = [random.randint(-30, 30) for _ in range(random.randint(0, 40))]
        assert count_significant(a) == brute_force(a)
    try:
        count_significant(["x", 1])
        assert False
    except ValueError:
        pass
    print("Q8(b) tests passed")


def run(n):
    a = random.sample(range(1, 10 * n), n)
    print("Q8(b) sequence:", a)
    print("Significant inversions (merge sort):", count_significant(a))
    print("Significant inversions (brute force):", brute_force(a))


def ask_size():
    while True:
        s = input("Enter n (>= 10): ")
        if s.isdigit() and int(s) >= 10:
            return int(s)
        print("n must be an integer >= 10")


if __name__ == "__main__":
    tests()
    run(ask_size())

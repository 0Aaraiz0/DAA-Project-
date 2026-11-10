"""Q8(a) - Kleinberg & Tardos, Algorithm Design 1st ed., Exercise 1, p. 246:
median of two databases (n values each) using O(log n) queries.
A query asks one database for its k-th smallest value; the median is the n-th smallest of all 2n values."""
import random

queries = 0


def query(db, k):
    """The ONLY way the algorithm touches a database (db is a sorted list; k is 1-indexed)."""
    global queries
    queries += 1
    return db[k - 1]


def kth_of_two(db1, db2, k):
    """k-th smallest of the union of the two databases."""
    a_lo, la = 1, len(db1)        # part of db1 still in play: ranks a_lo .. a_lo+la-1
    b_lo, lb = 1, len(db2)
    while True:
        if la == 0:
            return query(db2, b_lo + k - 1)
        if lb == 0:
            return query(db1, a_lo + k - 1)
        if k == 1:
            return min(query(db1, a_lo), query(db2, b_lo))
        i, j = min(la, k // 2), min(lb, k // 2)
        x = query(db1, a_lo + i - 1)
        y = query(db2, b_lo + j - 1)
        if x < y:                 # the first i entries of db1's part are all below rank k: discard them
            a_lo, la, k = a_lo + i, la - i, k - i
        else:                     # otherwise discard the first j entries of db2's part
            b_lo, lb, k = b_lo + j, lb - j, k - j


def median(db1, db2):
    """Validated wrapper. Returns (median, queries used)."""
    global queries
    if len(db1) != len(db2) or len(db1) == 0:
        raise ValueError("both databases need the same number n >= 1 of values")
    queries = 0
    m = kth_of_two(db1, db2, len(db1))
    return m, queries


def tests():
    assert median([1, 3, 5], [2, 4, 6])[0] == 3
    assert median([1], [2])[0] == 1
    for n in range(1, 80):
        for layout in range(4):
            pool = sorted(random.sample(range(10 * n + 10), 2 * n))
            if layout == 0:
                a, b = pool[:n], pool[n:]              # db1 entirely below db2
            elif layout == 1:
                a, b = pool[n:], pool[:n]              # db2 entirely below db1
            elif layout == 2:
                a, b = pool[0::2], pool[1::2]          # interleaved
            else:
                random.shuffle(pool)
                a, b = sorted(pool[:n]), sorted(pool[n:])
            m, q = median(a, b)
            assert m == sorted(a + b)[n - 1]
            assert q <= 2 * (n - 1).bit_length() + 2   # 2*ceil(log2 n) + 2
    try:
        median([1, 2], [3])
        assert False
    except ValueError:
        pass
    print("Q8(a) tests passed")


def run(n):
    pool = random.sample(range(10 * n), 2 * n)
    a, b = sorted(pool[:n]), sorted(pool[n:])
    print("Q8(a) database 1:", a)
    print("Q8(a) database 2:", b)
    m, q = median(a, b)
    print(f"Median = {m}, queries used = {q} (reading everything would need {2 * n}); check: {sorted(a + b)[n - 1]}")


def ask_size():
    while True:
        s = input("Enter n (>= 10): ")
        if s.isdigit() and int(s) >= 10:
            return int(s)
        print("n must be an integer >= 10")


if __name__ == "__main__":
    tests()
    run(ask_size())

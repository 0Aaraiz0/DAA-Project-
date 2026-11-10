"""Q7 - Kleinberg & Tardos, Algorithm Design 1st ed., Solved Exercise 2, p. 244 (solution pp. 245-246):
best day to buy and sell a stock (buy on day i, sell on a later day j) in O(n log n)."""
import random


def best_trade(p, lo, hi):
    """Best (profit, i, j) with lo <= i < j <= hi and profit > 0, or None."""
    if lo >= hi:                                     # 0 or 1 day: nothing to do
        return None
    mid = (lo + hi) // 2
    left = best_trade(p, lo, mid)                    # both days in the first half
    right = best_trade(p, mid + 1, hi)               # both days in the second half
    i = min(range(lo, mid + 1), key=lambda k: p[k])      # cheapest day in first half  (O(n) scan)
    j = max(range(mid + 1, hi + 1), key=lambda k: p[k])  # dearest day in second half (O(n) scan)
    cross = (p[j] - p[i], i, j)
    options = [t for t in (left, right, cross) if t is not None and t[0] > 0]
    return max(options) if options else None


def find_trade(p):
    """Validated wrapper. Returns (buy_day, sell_day, profit_per_share) with 1-indexed days, or None."""
    if not all(isinstance(x, (int, float)) for x in p):
        raise ValueError("list of numbers required")
    t = best_trade(p, 0, len(p) - 1)
    return None if t is None else (t[1] + 1, t[2] + 1, t[0])


def brute_force(p):
    best = None
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[j] - p[i] > 0 and (best is None or p[j] - p[i] > best):
                best = p[j] - p[i]
    return best


def tests():
    assert find_trade([9, 1, 5]) == (2, 3, 4)                         # the book's example
    assert find_trade([3, 8, 1, 9, 2, 7, 4, 6, 5, 10]) == (3, 10, 9)  # 10 days
    assert find_trade(list(range(20, 8, -1))) is None                 # falling prices: no profit
    assert find_trade([7] * 10) is None                               # flat: no profit
    assert find_trade([5]) is None and find_trade([]) is None
    for _ in range(1000):
        p = [random.randint(1, 20) for _ in range(random.randint(0, 30))]
        t = find_trade(p)
        ref = brute_force(p)
        assert (t is None) == (ref is None)
        if t:
            assert t[2] == ref and t[0] < t[1] and p[t[1] - 1] - p[t[0] - 1] == ref
    try:
        find_trade(["a", 1])
        assert False
    except ValueError:
        pass
    print("Q7 tests passed")


def run(n):
    p = [random.randint(1, 100) for _ in range(n)]
    print("Q7 prices:", p)
    t = find_trade(p)
    if t:
        print(f"Buy on day {t[0]}, sell on day {t[1]}: profit {t[2]} per share ({t[2] * 1000} for 1000 shares)")
    else:
        print("No profitable trade exists")
    print("Brute-force best profit:", brute_force(p))
    print("Book example [9, 1, 5]:", find_trade([9, 1, 5]))


def ask_size():
    while True:
        s = input("Enter n (>= 10): ")
        if s.isdigit() and int(s) >= 10:
            return int(s)
        print("n must be an integer >= 10")


if __name__ == "__main__":
    tests()
    run(ask_size())

"""Q8(c) - Kleinberg & Tardos, Algorithm Design 1st ed., Exercise 3, pp. 246-247:
decide whether MORE THAN n/2 bank cards are equivalent (same account), using only an
equivalence tester on pairs of cards and O(n log n) tester calls."""
import random

calls = 0


def tester(ids, i, j):
    """The ONLY operation allowed on cards: are cards i and j equivalent? (ids are hidden account numbers)"""
    global calls
    calls += 1
    return ids[i] == ids[j]


def majority(ids, cards):
    """Return a card whose class holds MORE than half of `cards`, or None."""
    n = len(cards)
    if n == 1:
        return cards[0]
    mid = n // 2
    c1 = majority(ids, cards[:mid])               # candidate from the first half
    c2 = majority(ids, cards[mid:])               # candidate from the second half
    for c in (c1, c2):                            # a majority class must win in at least one half
        if c is None:
            continue
        count = 1 + sum(1 for x in cards if x != c and tester(ids, c, x))
        if 2 * count > n:
            return c
    return None


def find_majority(ids):
    """Validated wrapper. Returns (card index or None, tester calls)."""
    global calls
    if len(ids) == 0:
        raise ValueError("need at least one card")
    calls = 0
    return majority(ids, list(range(len(ids)))), calls


def tests():
    assert find_majority([1, 2, 1, 3, 1, 4, 1, 5, 1, 6])[0] is None      # n=10, exactly 5 equal: NOT more than half
    assert find_majority([1, 2, 1, 3, 1, 4, 1, 5, 1, 6, 1])[0] is not None  # n=11, 6 equal
    assert find_majority([7])[0] == 0
    for n in range(1, 100):
        for _ in range(10):
            ids = [random.randint(0, random.choice([1, 2, 5])) for _ in range(n)]
            card, c = find_majority(ids)
            top = max(ids.count(x) for x in set(ids))
            assert (card is not None) == (2 * top > n)
            if card is not None:
                assert 2 * ids.count(ids[card]) > n
            assert c <= 2 * n * max(1, (n - 1).bit_length())   # O(n log n)
    try:
        find_majority([])
        assert False
    except ValueError:
        pass
    print("Q8(c) tests passed")


def run(n):
    for label, size in (("more than n/2 equivalent", n // 2 + 1), ("exactly n/2 equivalent", n // 2)):
        ids = [0] * size + [random.randint(1, n) for _ in range(n - size)]
        random.shuffle(ids)
        card, c = find_majority(ids)
        top = max(ids.count(x) for x in set(ids))
        print(f"Q8(c) {label}: hidden accounts {ids}")
        print("   ->", "NO majority class" if card is None else f"YES, card {card} (account {ids[card]})",
              f"| tester calls = {c} | correct: {(card is not None) == (2 * top > n)}")


def ask_size():
    while True:
        s = input("Enter n (>= 10): ")
        if s.isdigit() and int(s) >= 10:
            return int(s)
        print("n must be an integer >= 10")


if __name__ == "__main__":
    tests()
    run(ask_size())

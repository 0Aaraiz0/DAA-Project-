"""Q2 - Levitin, Exercise 5.1 (3), p. 200: a^n by divide and conquer (exponentiation by squaring).
the project asked for a^n; the Levitin book prints 5.1(3) as the factorial problem,
so a small factorial version is included at the bottom."""
import math

count = 0  # multiplications made by the divide-and-conquer version


def power(a, n):
    """a^n for integer n >= 1."""
    global count
    if n == 1:                    # base case: 0 multiplications
        return a
    h = power(a, n // 2)          # a^(floor(n/2)), computed ONCE
    count += 1
    square = h * h                # (a^(n/2))^2
    if n % 2 == 0:
        return square
    count += 1
    return a * square             # odd n: one extra factor a


def find_power(a, n):
    """Validated wrapper. Returns (a^n, multiplications)."""
    global count
    if not isinstance(a, (int, float)) or not isinstance(n, int) or n < 1:
        raise ValueError("a must be a number and n a positive integer")
    count = 0
    result = power(a, n)
    return result, count


def brute_force(a, n):
    """Repeated multiplication: n-1 multiplications."""
    result = a
    for _ in range(n - 1):
        result *= a
    return result, n - 1


def factorial_dc(lo, hi):
    """Supplement: product lo..hi by halving the range (n-1 multiplications for 1..n)."""
    if lo == hi:
        return lo
    mid = (lo + hi) // 2
    return factorial_dc(lo, mid) * factorial_dc(mid + 1, hi)


def tests():
    assert find_power(2, 1) == (2, 0)
    assert find_power(2, 10)[0] == 1024
    assert find_power(-2, 5)[0] == -32 and find_power(-2, 6)[0] == 64
    assert find_power(7, 64)[0] == 7 ** 64
    for n in range(1, 500):
        a = (n % 9) + 1
        r, c = find_power(a, n)
        assert r == a ** n == brute_force(a, n)[0]
        assert c == (n.bit_length() - 1) + bin(n).count("1") - 1       # exact count
    for k in range(1, 15):
        assert find_power(1, 2 ** k)[1] == k                           # n = 2^k -> k multiplications
    for n in range(1, 30):
        assert factorial_dc(1, n) == math.factorial(n)
    for bad in ((2, 0), (2, -1), (2, 1.5), ("x", 2)):
        try:
            find_power(*bad)
            assert False
        except ValueError:
            pass
    print("Q2 tests passed")


def run(n):
    a = 3
    print(f"Q2 base a = {a}")
    print(f"{'n':>6} {'D&C mults':>10} {'brute mults':>12}  correct")
    for e in sorted({1, 2, 3, 5, 10, n}):
        r, c = find_power(a, e)
        br, bc = brute_force(a, e)
        print(f"{e:>6} {c:>10} {bc:>12}  {r == br == a ** e}")


def ask_size():
    while True:
        s = input("Enter n (>= 10): ")
        if s.isdigit() and int(s) >= 10:
            return int(s)
        print("n must be an integer >= 10")


if __name__ == "__main__":
    tests()
    run(ask_size())

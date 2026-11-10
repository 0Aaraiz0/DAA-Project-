"""Runs the Part 1 solutions.
    python main.py          ask n (>= 10), then run the tests and a demo of every question
    python main.py 3        only question 3          (also: "8(a)", "8(b)", "8(c)")
"""
import importlib
import random
import sys

QUESTIONS = ["1", "2", "3", "4", "5", "6", "7", "8(a)", "8(b)", "8(c)"]


def ask_size():
    while True:
        s = input("Enter n (>= 10): ")
        if s.isdigit() and int(s) >= 10:
            return int(s)
        print("n must be an integer >= 10")


if __name__ == "__main__":
    chosen = sys.argv[1:] or QUESTIONS
    for q in chosen:
        if q not in QUESTIONS:
            sys.exit(f"Unknown question {q!r}. Choose from {QUESTIONS}")
    n = ask_size()
    random.seed(2026)                       # reproducible demo output
    for q in chosen:
        module = importlib.import_module(q)   # loads 1.py, 8(a).py, ...
        print(f"\n===== Question {q} =====")
        module.tests()
        module.run(n)

# CS302 Divide & Conquer Project: Closest Pair and Large Integer Multiplication

Covers project **Part 2** (generate 10 + 10 datasets), **Part 3** (apply the algorithms) and
**Part 4** (web interface that shows both algorithms working).

| Problem | Divide & Conquer | Baseline |
|---|---|---|
| Closest pair of points (2D) | O(n log n) | Brute force, O(n²) |
| Large integer multiplication | Karatsuba, O(n^1.585) | Schoolbook, O(n²) |

Multiplication works on digit strings with hand-written addition, subtraction and multiplication.
Python's built-in integers are used only to check answers.

## Requirements

- Python 3.8 or newer. No packages are needed to run the project or the web interface.
- `matplotlib` only for the graphs: `pip install matplotlib`

## Quick start

```
python main.py            # starts the backend and opens the web interface
```

The page opens at http://localhost:8000 (the next free port is used if 8000 is busy).
Stop the server with Ctrl+C. If the datasets are missing, they are generated automatically.

## All commands

| Command | What it does |
|---|---|
| `python main.py` | Starts the backend and web interface |
| `python main.py gen` | Regenerates the 20 dataset files (seed 42) |
| `python main.py benchmark` | Runs all 20 datasets, prints tables, saves `benchmark_results.csv` |
| `python main.py expected` | Writes `expected_results.txt` (reference answers) |
| `python main.py verify` | Checks every algorithm against `expected_results.txt` (40 checks) |
| `python main.py graphs` | Saves comparison graphs into `graphs/` |
| `python main.py cp` / `mul` | Quick console demo of one algorithm |

Every script can also be run on its own, for example `python benchmark.py`.

## Project layout

```
main.py                backend server + command line entry point
closest_pair.py        brute force and divide & conquer closest pair
karatsuba.py           schoolbook and Karatsuba multiplication (string arithmetic)
generate_datasets.py   creates the 20 input files
benchmark.py           times all datasets, writes benchmark_results.csv
generate_expected.py   creates expected_results.txt (reference answers, no D&C code used)
verify_results.py      compares algorithm output with expected_results.txt
plot_graphs.py         creates the comparison graphs
web/index.html         the user interface
datasets/              cp_01..cp_10.txt and mul_01..mul_10.txt
graphs/                generated PNG graphs
```

## Datasets (Part 2)

Fixed random seed 42, so regenerating always gives identical files.

| Files | Size of each file |
|---|---|
| `cp_01` to `cp_10` | 120, 150, 200, 300, 500, 750, 1000, 1250, 1500, 2000 points |
| `mul_01` to `mul_10` | 120, 150, 200, 300, 500, 750, 1000, 1250, 1500, 2000 digits per number |

- **Closest pair file:** the first line is `n`, followed by `n` lines of `x y`. Coordinates are random in [-5000, 5000] with 4 decimal places.
- **Multiplication file:** two lines, `X` then `Y`. Each is a random number with no leading zero.

## Using the web interface (Part 4)

- **Closest Pair tab:** choose a dataset from the dropdown, or upload your own `.txt` file.
  Run Divide & Conquer to watch the median split line and the 2δ strip appear level by level.
  Run Brute Force to watch the best pair improve (orange line) while all pairs are scanned.
  The red line and circles mark the final closest pair.
- **Multiplication tab:** choose a dataset or upload a two-line file. You can also edit X and Y by hand.
  Run Karatsuba to see the recursion trace (splits and combines). Run Schoolbook to see its digit operation count.
  The result is verified against Python's own multiplication.
- **Benchmark tab:** one button runs all 20 datasets and fills both tables.

The page needs the Python backend. Opening `index.html` directly by double-click will not work.

### Backend endpoints (used by the page)

| Endpoint | Purpose |
|---|---|
| `GET /api/datasets` | lists dataset files |
| `GET /datasets/<name>` | returns a dataset file |
| `POST /api/closest_pair` | `{text, algo: "dc" or "bf"}` |
| `POST /api/multiply` | `{x, y, algo: "karatsuba" or "schoolbook"}` |
| `GET /api/benchmark` | runs all 20 datasets (result is cached until restart) |

## Results and verification (Part 3)

- `expected_results.txt` holds the reference answer for every input. For closest pair it gives the distance and
  the two points with their line numbers in the dataset file. For multiplication it gives X, Y and X × Y.
  These were computed with plain nested loops and Python integers, not the divide-and-conquer code.
- `python main.py verify` runs both algorithms on all 20 files and compares them with it. Expected output: `40 passed, 0 failed`.
- `benchmark_results.csv` and the benchmark tables contain measured times. These depend on your computer,
  so rerun `python main.py benchmark` on your own machine before using numbers in your report.

## Graphs

`python main.py graphs` writes four PNG files (150 dpi) to `graphs/`. Each timing is the best of 3 runs.

| File | Shows |
|---|---|
| `closest_pair_runtime.png` | D&C vs brute force runtime against n |
| `multiplication_runtime.png` | Karatsuba vs schoolbook runtime against digits |
| `speedup.png` | how many times faster the divide-and-conquer version is |
| `operation_counts.png` | comparisons / digit multiplications on a log scale (independent of the machine) |

## Notes

- Karatsuba switches to schoolbook below 32 digits (`BASE_CASE_DIGITS` in `karatsuba.py`). Because everything is
  pure Python string arithmetic, the Karatsuba speedup is modest (about 1x at 120 digits, about 4x at 2000 digits).
  It grows with size, as the theory predicts.
- The closest-pair strip check compares each point with the next 7 points in y-order, which is enough by the standard packing argument.
- If port 8000 is in use, check the terminal for the actual address printed.

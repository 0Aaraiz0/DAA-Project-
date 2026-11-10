"""main.py - CS302 project entrypoint.

    python main.py            -> starts the backend + web interface (default)
    python main.py benchmark  -> runs all 20 datasets in the terminal
    python main.py cp | mul   -> quick console demo of one algorithm
    python main.py gen        -> regenerates the 20 dataset files
    python main.py expected   -> writes expected_results.txt (reference answers)
    python main.py verify     -> checks every algorithm against expected_results.txt
    python main.py graphs     -> saves comparison graphs to graphs/ (needs matplotlib)

The web page (web/index.html) talks to this Python backend:
    GET  /api/datasets    list of dataset files
    GET  /datasets/<name> raw dataset file
    POST /api/closest_pair  {text, algo: "dc"|"bf"}
    POST /api/multiply      {x, y, algo: "karatsuba"|"schoolbook"}
    GET  /api/benchmark   runs all 20 datasets (Python timings)
"""

import json
import os
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Always work relative to this file, wherever the command is run from.
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
sys.setrecursionlimit(10000)

from closest_pair import (closest_pair_divide_and_conquer, closest_pair_brute_force,
                          load_dataset as load_cp, parse_points)
from karatsuba import karatsuba_multiply, schoolbook_multiply, load_dataset as load_mul
from generate_datasets import main as generate_all_datasets
from benchmark import run_all_benchmarks, collect_results, save_csv

DATASET_DIR = os.path.join(ROOT, "datasets")
WEB_DIR = os.path.join(ROOT, "web")
_bench_cache = None


def ensure_datasets():
    if not os.path.exists(os.path.join(DATASET_DIR, "cp_01.txt")):
        print("Datasets not found. Generating them now...")
        generate_all_datasets()


# ----------------------------------------------------------------- API logic
def list_datasets():
    out = {"cp": [], "mul": []}
    for f in sorted(os.listdir(DATASET_DIR)):
        if not f.endswith(".txt"):
            continue
        path = os.path.join(DATASET_DIR, f)
        if f.startswith("cp_"):
            out["cp"].append({"name": f, "size": len(load_cp(path))})
        elif f.startswith("mul_"):
            out["mul"].append({"name": f, "size": len(load_mul(path)[0])})
    return out


def api_closest_pair(body):
    from closest_pair import closest_pair_brute_force as bf, closest_pair_divide_and_conquer as dc
    pts = parse_points(body["text"])
    if len(pts) < 2:
        raise ValueError("Need at least 2 points.")
    algo = body.get("algo", "dc")
    fn = dc if algo == "dc" else bf

    t0 = time.perf_counter()
    d, pair = fn(pts)                       # clean timing pass (no instrumentation)
    ms = (time.perf_counter() - t0) * 1000

    stats = {}
    if algo == "dc":
        fn(pts, stats)
    else:
        fn(pts, stats, True)
    verified = None
    if len(pts) <= 2500:
        verified = abs(d - bf(pts)[0]) < 1e-9

    improvements = stats.get("improvements", [])[-200:]
    return {"algo": algo, "n": len(pts), "points": [list(p) for p in pts], "distance": d,
            "pair": [list(pair[0]), list(pair[1])], "time_ms": ms,
            "comparisons": stats.get("comparisons", 0), "steps": stats.get("steps", []),
            "improvements": improvements, "verified": verified}


def api_multiply(body):
    x, y = body["x"].strip(), body["y"].strip()
    if not (x.isdigit() and y.isdigit()):
        raise ValueError("X and Y must contain digits only (0-9).")
    algo = body.get("algo", "karatsuba")
    fn = karatsuba_multiply if algo == "karatsuba" else schoolbook_multiply

    t0 = time.perf_counter()
    prod = fn(x, y)
    ms = (time.perf_counter() - t0) * 1000

    stats = {}
    fn(x, y, stats)
    expected = str(int(x) * int(y))
    return {"algo": algo, "x_digits": len(x), "y_digits": len(y), "product": prod,
            "time_ms": ms, "verified": prod == expected, "calls": stats.get("calls"),
            "base_cases": stats.get("base_cases"), "max_depth": stats.get("max_depth"),
            "digit_mults": stats.get("digit_mults", 0), "trace": stats.get("trace", [])}


def api_benchmark():
    global _bench_cache
    if _bench_cache is None:
        _bench_cache = collect_results()
        save_csv(_bench_cache)
    return _bench_cache


# -------------------------------------------------------------- HTTP handler
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, code, payload, ctype="application/json"):
        data = payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?")[0]
        try:
            if path in ("/", "/index.html"):
                with open(os.path.join(WEB_DIR, "index.html"), "rb") as f:
                    self._send(200, f.read(), "text/html; charset=utf-8")
            elif path == "/api/datasets":
                self._send(200, list_datasets())
            elif path == "/api/benchmark":
                self._send(200, api_benchmark())
            elif path.startswith("/datasets/"):
                name = os.path.basename(path)  # basename blocks path traversal
                with open(os.path.join(DATASET_DIR, name), "rb") as f:
                    self._send(200, f.read(), "text/plain; charset=utf-8")
            else:
                self._send(404, {"error": "not found"})
        except FileNotFoundError:
            self._send(404, {"error": "not found"})
        except Exception as e:
            self._send(500, {"error": str(e)})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length) or b"{}")
            if self.path == "/api/closest_pair":
                self._send(200, api_closest_pair(body))
            elif self.path == "/api/multiply":
                self._send(200, api_multiply(body))
            else:
                self._send(404, {"error": "not found"})
        except (ValueError, KeyError, IndexError) as e:
            self._send(400, {"error": f"Invalid input: {e}"})
        except Exception as e:
            self._send(500, {"error": str(e)})


def launch_web_ui(port=8000):
    if not os.path.exists(os.path.join(WEB_DIR, "index.html")):
        print("Could not find web/index.html.")
        return
    httpd = None
    for p in range(port, port + 10):  # try the next ports if 8000 is busy
        try:
            httpd = ThreadingHTTPServer(("127.0.0.1", p), Handler)
            port = p
            break
        except OSError:
            continue
    if httpd is None:
        print("No free port found.")
        return
    url = f"http://localhost:{port}/"
    print(f"Interface running at {url}  (press Ctrl+C to stop)")
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        httpd.server_close()


# ------------------------------------------------------------- console demos
def demo_closest_pair():
    pts = load_cp("datasets/cp_01.txt")
    d_dc, _ = closest_pair_divide_and_conquer(pts)
    d_bf, _ = closest_pair_brute_force(pts)
    print(f"{len(pts)} points | D&C: {d_dc:.4f} | Brute force: {d_bf:.4f} | match: {abs(d_dc - d_bf) < 1e-9}")


def demo_karatsuba():
    x, y = load_mul("datasets/mul_01.txt")
    k, s = karatsuba_multiply(x, y), schoolbook_multiply(x, y)
    print(f"{len(x)} digits | Karatsuba == Schoolbook == Python int: {k == s == str(int(x) * int(y))}")


def run_expected():
    from generate_expected import main as gen_expected
    gen_expected()


def run_verify():
    from verify_results import verify
    verify()


def run_graphs():
    try:
        from plot_graphs import main as plot
    except ImportError:
        print("matplotlib is required for graphs:  pip install matplotlib")
        return
    plot()


def main():
    ensure_datasets()
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "web"
    actions = {
        "web": launch_web_ui, "ui": launch_web_ui, "serve": launch_web_ui,
        "bench": run_all_benchmarks, "benchmark": run_all_benchmarks,
        "cp": demo_closest_pair, "closest_pair": demo_closest_pair,
        "mul": demo_karatsuba, "karatsuba": demo_karatsuba,
        "gen": generate_all_datasets, "generate": generate_all_datasets,
        "expected": run_expected, "verify": run_verify, "graphs": run_graphs,
    }
    if cmd not in actions:
        print("Unknown option. Use: web | benchmark | cp | mul | gen | expected | verify | graphs")
        return
    actions[cmd]()


if __name__ == "__main__":
    main()

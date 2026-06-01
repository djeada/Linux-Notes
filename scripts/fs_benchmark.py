#!/usr/bin/env python3
"""
fs_benchmark.py – Measure and plot file-system read / write throughput
                               versus the number of parallel workers.
python fs_benchmark.py --directory /tmp --file-size 256 --max-workers 8
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import os
import pathlib
import random
import string
import sys
import time
from typing import Tuple, List, Dict

import matplotlib.pyplot as plt


# ───────────────────────────── helpers ──────────────────────────────


def _random_name(n: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=n))


def _write_file(path: pathlib.Path, size_mb: int, chunk_mb: int = 4) -> float:
    """Write *size_mb* MiB to *path* in *chunk_mb* MiB chunks.
    Returns elapsed seconds."""
    chunk = b"\0" * (chunk_mb * 1024 * 1024)
    chunks = size_mb // chunk_mb
    leftover = size_mb % chunk_mb

    start = time.perf_counter()
    with path.open("wb", buffering=0) as fh:
        for _ in range(chunks):
            fh.write(chunk)
        if leftover:
            fh.write(b"\0" * (leftover * 1024 * 1024))
        fh.flush()
        os.fsync(fh.fileno())       # force flush to the device
    return time.perf_counter() - start


def _read_file(path: pathlib.Path, chunk_mb: int = 4) -> float:
    """Read entire file using *chunk_mb* MiB blocks. Returns elapsed seconds."""
    bufsize = chunk_mb * 1024 * 1024
    start = time.perf_counter()
    with path.open("rb", buffering=bufsize) as fh:
        while fh.read(bufsize):
            pass
    return time.perf_counter() - start


def _worker(task: str, path: str, size_mb: int) -> Tuple[str, float]:
    p = pathlib.Path(path)
    if task == "write":
        t = _write_file(p, size_mb)
    elif task == "read":
        t = _read_file(p)
    else:  # pragma: no cover
        raise ValueError(task)
    return task, t


# ───────────────────────────── benchmark ──────────────────────────────


def run_benchmark(
    directory: pathlib.Path,
    file_size_mb: int,
    max_workers: int,
) -> Tuple[Dict[int, float], Dict[int, float]]:
    """
    Returns two dicts: {workers → aggregate MB/s} for writes and reads.
    """
    write_bw: Dict[int, float] = {}
    read_bw: Dict[int, float] = {}

    # Pre-generate file names once – each worker gets its own file
    filenames = [directory / f"{_random_name()}_{i}.dat" for i in range(max_workers)]

    # ── loop over 1 … max_workers ──────────────────────
    for n in range(1, max_workers + 1):
        # pick n files for this round
        files_n = filenames[:n]

        # WRITE test
        with cf.ProcessPoolExecutor(max_workers=n) as pool:
            futures = [
                pool.submit(_worker, "write", str(p), file_size_mb) for p in files_n
            ]
            elapsed = [f.result()[1] for f in cf.as_completed(futures)]
        # MB / s  = (n · size_MB) / mean(elapsed)
        write_bw[n] = (n * file_size_mb) / (sum(elapsed) / n)

        # READ test
        with cf.ProcessPoolExecutor(max_workers=n) as pool:
            futures = [pool.submit(_worker, "read", str(p), 0) for p in files_n]
            elapsed = [f.result()[1] for f in cf.as_completed(futures)]
        read_bw[n] = (n * file_size_mb) / (sum(elapsed) / n)

    # cleanup
    for p in filenames:
        try:
            p.unlink()
        except FileNotFoundError:
            pass

    return write_bw, read_bw


# ───────────────────────────── plotting ──────────────────────────────


def plot_results(write_bw: dict[int, float], read_bw: dict[int, float], out: pathlib.Path):
    workers = sorted(write_bw.keys())
    plt.figure()
    plt.plot(workers, [write_bw[w] for w in workers], marker="o", label="Write")
    plt.plot(workers, [read_bw[w] for w in workers], marker="s", label="Read")
    plt.xlabel("Parallel workers (processes)")
    plt.ylabel("Throughput [MB/s]")
    plt.title("File-system throughput scaling")
    plt.grid(True, which="both", ls="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out)
    print(f"[+] Plot saved to {out}")


# ───────────────────────────── main ───────────────────────────────────


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Measure and plot FS read/write throughput scaling."
    )
    ap.add_argument(
        "-d",
        "--directory",
        type=pathlib.Path,
        required=True,
        help="Directory on the target file-system (must be writable)",
    )
    ap.add_argument(
        "-s",
        "--file-size",
        type=int,
        default=128,
        metavar="MiB",
        help="Size of the test file each worker writes (default: 128)",
    )
    ap.add_argument(
        "-n",
        "--max-workers",
        type=int,
        default=os.cpu_count() or 4,
        help="Maximum number of parallel processes (default: CPU count)",
    )
    ap.add_argument(
        "-o",
        "--output",
        type=pathlib.Path,
        default=pathlib.Path("fs_benchmark.png"),
        help="Output PNG for the plot",
    )
    return ap.parse_args()


def main() -> None:
    if os.geteuid() == 0:
        print(
            "Warning: running as root may bypass user-space caches and skew numbers.",
            file=sys.stderr,
        )
    args = parse_args()

    args.directory.mkdir(parents=True, exist_ok=True)

    print(
        f"[*] Benchmarking in {args.directory} – "
        f"{args.file_size} MiB per worker – up to {args.max_workers} workers"
    )
    write_bw, read_bw = run_benchmark(
        args.directory, args.file_size, args.max_workers
    )

    # show simple table
    print("\nWorkers |  Write MB/s  |   Read MB/s")
    print("-----------------------------------------")
    for w in sorted(write_bw):
        print(
            f"{w:7} | {write_bw[w]:11.0f} | {read_bw[w]:11.0f}"
        )

    plot_results(write_bw, read_bw, args.output)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)

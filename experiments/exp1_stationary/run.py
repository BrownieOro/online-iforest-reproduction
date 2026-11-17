"""Run the group's stationary-stream comparison on Annthyroid and Mammography.

Each repetition uses one seeded permutation shared by both methods. The first
30% of the stream is a warm-up set; sklearn IsolationForest is fitted once on
that set, while OIF scores each later batch before learning that batch.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import time
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import IsolationForest
from sklearn.metrics import average_precision_score, roc_auc_score

from oif.forest import OnlineIsolationForest
from oif.tracking import log_run


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "processed"


def run_repetition(dataset: str, csv_path: Path, seed: int, output: Path,
                   batch_size: int, warmup_fraction: float,
                   n_trees: int, window_size: int, eta: float) -> dict:
    """Run one paired warm-up/prequential evaluation and persist its artifacts."""
    frame = pd.read_csv(csv_path)
    if "label" not in frame or frame.shape[1] < 2:
        raise ValueError(f"{csv_path} must contain numeric features and a label column")
    y_all = frame.pop("label").to_numpy(dtype=int)
    X_all = frame.to_numpy(dtype=float)
    if not np.isfinite(X_all).all() or not np.isin(y_all, [0, 1]).all():
        raise ValueError(f"{csv_path} contains invalid feature values or labels")
    if len(np.unique(y_all)) != 2:
        raise ValueError(f"{csv_path} must contain both label classes")

    rng = np.random.default_rng(seed)
    order = rng.permutation(len(X_all))
    X, y = X_all[order], y_all[order]
    warmup = max(2, min(len(X) - 2, int(len(X) * warmup_fraction)))
    X_initial, X_stream = X[:warmup], X[warmup:]
    y_stream = y[warmup:]

    # Both methods see the same initial observations and the same subsequent
    # order. Prepared inputs are finite, numeric and used without scaling.
    baseline = IsolationForest(n_estimators=100, contamination="auto",
                               random_state=seed, n_jobs=1)
    started = time.perf_counter()
    baseline.fit(X_initial)
    baseline_fit_seconds = time.perf_counter() - started
    started = time.perf_counter()
    baseline_scores = -baseline.score_samples(X_stream)
    baseline_score_seconds = time.perf_counter() - started

    oif = OnlineIsolationForest(
        n_trees=n_trees, window_size=window_size, eta=eta, seed=seed,
    )
    started = time.perf_counter()
    oif.learn_batch(X_initial)
    oif_warmup_seconds = time.perf_counter() - started
    oif_scores = np.empty(len(X_stream), dtype=float)
    oif_score_seconds = 0.0
    oif_update_seconds = 0.0
    for start in range(0, len(X_stream), batch_size):
        stop = min(start + batch_size, len(X_stream))
        batch = X_stream[start:stop]
        t0 = time.perf_counter()
        oif_scores[start:stop] = oif.score_samples(batch)
        oif_score_seconds += time.perf_counter() - t0
        t0 = time.perf_counter()
        oif.learn_batch(batch)
        oif_update_seconds += time.perf_counter() - t0

    if len(np.unique(y_stream)) != 2:
        raise ValueError(f"Seed {seed} leaves only one class after warm-up")
    metrics = {
        "n_total": int(len(X)), "n_warmup": int(warmup),
        "n_evaluated": int(len(X_stream)),
        "baseline_roc_auc": float(roc_auc_score(y_stream, baseline_scores)),
        "baseline_average_precision": float(average_precision_score(y_stream, baseline_scores)),
        "baseline_fit_seconds": float(baseline_fit_seconds),
        "baseline_score_seconds": float(baseline_score_seconds),
        "oif_roc_auc": float(roc_auc_score(y_stream, oif_scores)),
        "oif_average_precision": float(average_precision_score(y_stream, oif_scores)),
        "oif_warmup_seconds": float(oif_warmup_seconds),
        "oif_update_seconds": float(oif_update_seconds),
        "oif_score_seconds": float(oif_score_seconds),
        "baseline_total_seconds": float(baseline_fit_seconds + baseline_score_seconds),
        "oif_total_seconds": float(oif_warmup_seconds + oif_update_seconds + oif_score_seconds),
    }
    original_rows = order[warmup:]
    predictions = pd.DataFrame({
        "row_index": original_rows,
        "stream_index": np.arange(warmup, len(X)),
        "label": y_stream,
        "baseline_anomaly_score": baseline_scores,
        "oif_anomaly_score": oif_scores,
    })
    output.mkdir(parents=True, exist_ok=False)
    predictions.to_csv(output / "predictions.csv", index=False)
    git_dirty = bool(subprocess.run(
        ["git", "status", "--porcelain"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip())
    config = {
        "experiment": "stationary_prequential",
        "tags": ["reproduction", "stationary"],
        "git_commit": subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
            capture_output=True, text=True,
        ).stdout.strip(),
        "git_worktree_dirty": git_dirty,
        "oif_implementation_status": "experimental; formula and learning/scoring edge cases still need team review",
        "dataset": dataset,
        "dataset_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
        "protocol": "shared seeded shuffle; first 30% warm-up; score each later batch before OIF update; frozen sklearn baseline",
        "seed": seed, "batch_size": batch_size,
        "warmup_fraction": warmup_fraction,
        "oif": {"n_trees": n_trees, "window_size": window_size, "eta": eta},
        "baseline": {"model": "sklearn.ensemble.IsolationForest", "n_estimators": 100,
                     "contamination": "auto", "preprocessing": "none; prepared CSV is finite and numeric"},
        "python": platform.python_version(), "numpy": np.__version__,
        "pandas": pd.__version__, "sklearn": sklearn.__version__,
        "known_deviation": "Paper uses 30 shuffled runs and batches of 100; this group's protocol adds a 30% warm-up and freezes the offline baseline for a paired prequential comparison.",
    }
    for name, value in (("config", config), ("metrics", metrics)):
        (output / f"{name}.json").write_text(
            json.dumps(value, indent=2, allow_nan=False), encoding="utf-8")
    log_run(config, metrics, output)
    return {"dataset": dataset, "seed": seed, **metrics}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--datasets", nargs="+", choices=("annthyroid", "mammography"),
                        default=("annthyroid", "mammography"))
    parser.add_argument("--runs", type=int, default=30)
    parser.add_argument("--seed-start", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--warmup-fraction", type=float, default=0.30)
    parser.add_argument("--n-trees", type=int, default=32)
    parser.add_argument("--window-size", type=int, default=2048)
    parser.add_argument("--eta", type=float, default=32.0)
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "raw" / "stationary")
    args = parser.parse_args()
    if args.runs < 1 or args.batch_size < 1 or not 0 < args.warmup_fraction < 1:
        parser.error("runs/batch-size must be positive and warmup-fraction must be in (0, 1)")

    records = []
    for dataset in args.datasets:
        path = DATA_DIR / f"{dataset}.csv"
        if not path.is_file():
            raise FileNotFoundError(f"Missing {path}. Run: python scripts/prepare_dataset.py")
        for seed in range(args.seed_start, args.seed_start + args.runs):
            run_dir = args.output / dataset / f"seed-{seed}"
            record = run_repetition(dataset, path, seed, run_dir, args.batch_size,
                                    args.warmup_fraction, args.n_trees,
                                    args.window_size, args.eta)
            records.append(record)
            print(json.dumps(record, ensure_ascii=False), flush=True)

    args.output.mkdir(parents=True, exist_ok=True)
    results = pd.DataFrame(records)
    results.to_csv(args.output / "runs.csv", index=False)
    numeric = [c for c in results.columns if c not in ("dataset", "seed")]
    summary = results.groupby("dataset")[numeric].median().reset_index()
    summary.to_csv(ROOT / "results" / "stationary-summary.csv", index=False)
    summary.to_json(args.output / "summary.json", orient="records", indent=2)
    print("Median summary:")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()

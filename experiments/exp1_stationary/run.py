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


def _write_model_run(output: Path, config: dict, metrics: dict,
                     row_index: np.ndarray, stream_index: np.ndarray,
                     labels: np.ndarray, scores: np.ndarray) -> None:
    """Write one model's local C5 artifacts, then pass them to shared logging."""
    output.mkdir(parents=True, exist_ok=False)
    predictions = pd.DataFrame({
        "row_index": row_index,
        "stream_index": stream_index,
        "anomaly_score": scores,
        "label": labels,
    })
    predictions.to_csv(output / "predictions.csv", index=False)
    for name, value in (("config", config), ("metrics", metrics)):
        (output / f"{name}.json").write_text(
            json.dumps(value, indent=2, allow_nan=False), encoding="utf-8")
    log_run(config, metrics, output)


def run_repetition(dataset: str, csv_path: Path, seed: int, output_root: Path,
                   batch_size: int, warmup_fraction: float,
                   n_trees: int, window_size: int, eta: float) -> dict:
    """Run a paired evaluation and save separate model/dataset/seed artifacts."""
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
    # The forest derives the disjoint tree seed range from this run seed.
    oif_forest_seed = seed

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
        n_trees=n_trees, window_size=window_size, eta=eta, seed=oif_forest_seed,
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
    original_rows = order[warmup:]
    stream_indices = np.arange(warmup, len(X))
    model_dirs = {
        "isolation_forest": output_root / dataset / "isolation_forest" / f"seed-{seed}",
        "online_isolation_forest": output_root / dataset / "online_isolation_forest" / f"seed-{seed}",
    }
    existing = [str(path) for path in model_dirs.values() if path.exists()]
    if existing:
        raise FileExistsError(f"Run output already exists: {', '.join(existing)}")

    git_dirty = bool(subprocess.run(
        ["git", "status", "--porcelain"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip())
    common_config = {
        "experiment": "stationary_prequential",
        "tags": ["reproduction", "stationary"],
        "git_commit": subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
            capture_output=True, text=True,
        ).stdout.strip(),
        "git_worktree_dirty": git_dirty,
        "dataset": dataset,
        "dataset_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
        "seed": seed,
        "random_seeds": {
            "stream_permutation": seed,
            "baseline_model": seed,
            "oif_forest": oif_forest_seed,
            "oif_tree_seed_strategy": "forest_seed * n_trees + tree_index",
            "oif_tree_seeds": list(oif.tree_seeds),
        },
        "preprocessing": {
            "features": "numeric columns except label; used without scaling or imputation",
            "fit_scope": "none; prepared CSV is validated as finite before evaluation",
            "labels": "used only for metrics and predictions, never passed to either model",
        },
        "evaluation": {
            "order": "numpy.random.default_rng(seed).permutation(n_rows); same permutation for both models",
            "warmup_fraction": warmup_fraction,
            "warmup_rows": int(warmup),
            "batch_size": batch_size,
            "scoring_order": "score each post-warmup batch before updating OIF with that batch",
            "baseline_order": "fit once on the warm-up rows, then score all post-warmup rows in stream order",
        },
        "versions": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scikit_learn": sklearn.__version__,
        },
        "known_deviation": "The paper uses 30 shuffled runs and batches of 100; this protocol adds a 30% warm-up and freezes the offline baseline for a paired prequential comparison.",
    }

    baseline_auc = float(roc_auc_score(y_stream, baseline_scores))
    baseline_ap = float(average_precision_score(y_stream, baseline_scores))
    baseline_total = float(baseline_fit_seconds + baseline_score_seconds)
    baseline_metrics = {
        "n_total": int(len(X)), "n_warmup": int(warmup),
        "n_evaluated": int(len(X_stream)),
        "roc_auc": baseline_auc,
        "average_precision": baseline_ap,
        "training_time_seconds": float(baseline_fit_seconds),
        "scoring_time_seconds": float(baseline_score_seconds),
        "total_time_seconds": baseline_total,
    }
    baseline_config = {
        **common_config,
        "model": "sklearn.ensemble.IsolationForest",
        "parameters": {"n_estimators": 100, "contamination": "auto", "random_state": seed,
                       "n_jobs": 1},
        "timing": {
            "clock": "time.perf_counter", "unit": "seconds",
            "training": "fit on warm-up rows",
            "scoring": "score all post-warm-up rows; excludes model fitting",
        },
    }

    oif_auc = float(roc_auc_score(y_stream, oif_scores))
    oif_ap = float(average_precision_score(y_stream, oif_scores))
    oif_training = float(oif_warmup_seconds + oif_update_seconds)
    oif_total = float(oif_training + oif_score_seconds)
    oif_metrics = {
        "n_total": int(len(X)), "n_warmup": int(warmup),
        "n_evaluated": int(len(X_stream)),
        "roc_auc": oif_auc,
        "average_precision": oif_ap,
        "training_time_seconds": oif_training,
        "warmup_training_time_seconds": float(oif_warmup_seconds),
        "update_time_seconds": float(oif_update_seconds),
        "scoring_time_seconds": float(oif_score_seconds),
        "total_time_seconds": oif_total,
    }
    oif_config = {
        **common_config,
        "model": "OnlineIsolationForest",
        "parameters": {
            "n_trees": n_trees, "window_size": window_size, "eta": eta,
            "seed": oif_forest_seed, "evaluation_seed": seed,
        },
        "timing": {
            "clock": "time.perf_counter", "unit": "seconds",
            "training": "warm-up learning plus online updates after each scored batch",
            "scoring": "score each post-warm-up batch before updating it",
        },
    }

    _write_model_run(model_dirs["isolation_forest"], baseline_config, baseline_metrics,
                     original_rows, stream_indices, y_stream, baseline_scores)
    _write_model_run(model_dirs["online_isolation_forest"], oif_config, oif_metrics,
                     original_rows, stream_indices, y_stream, oif_scores)

    return {
        "dataset": dataset, "seed": seed,
        "n_total": int(len(X)), "n_warmup": int(warmup),
        "n_evaluated": int(len(X_stream)),
        "baseline_roc_auc": baseline_auc,
        "baseline_average_precision": baseline_ap,
        "baseline_fit_seconds": float(baseline_fit_seconds),
        "baseline_score_seconds": float(baseline_score_seconds),
        "baseline_total_seconds": baseline_total,
        "oif_roc_auc": oif_auc,
        "oif_average_precision": oif_ap,
        "oif_warmup_seconds": float(oif_warmup_seconds),
        "oif_update_seconds": float(oif_update_seconds),
        "oif_score_seconds": float(oif_score_seconds),
        "oif_total_seconds": oif_total,
    }


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
    parser.add_argument("--summary-output", type=Path,
                        default=ROOT / "results" / "stationary-summary.csv")
    args = parser.parse_args()
    if args.runs < 1 or args.batch_size < 1 or not 0 < args.warmup_fraction < 1:
        parser.error("runs/batch-size must be positive and warmup-fraction must be in (0, 1)")

    records = []
    for dataset in args.datasets:
        path = DATA_DIR / f"{dataset}.csv"
        if not path.is_file():
            raise FileNotFoundError(f"Missing {path}. Run: python scripts/prepare_dataset.py")
        for seed in range(args.seed_start, args.seed_start + args.runs):
            record = run_repetition(dataset, path, seed, args.output, args.batch_size,
                                    args.warmup_fraction, args.n_trees,
                                    args.window_size, args.eta)
            records.append(record)
            print(json.dumps(record, ensure_ascii=False), flush=True)

    args.output.mkdir(parents=True, exist_ok=True)
    results = pd.DataFrame(records)
    results.to_csv(args.output / "runs.csv", index=False)
    numeric = [c for c in results.columns if c not in ("dataset", "seed")]
    summary = results.groupby("dataset")[numeric].median().reset_index()
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.summary_output, index=False)
    summary.to_json(args.output / "summary.json", orient="records", indent=2)
    print("Median summary:")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()

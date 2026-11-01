"""Offline sklearn reference; this is NOT Online Isolation Forest."""
import argparse
import hashlib
import json
import platform
from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.metrics import average_precision_score, precision_recall_fscore_support, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .data import load_data
from .tracking import log_run


def run(path=None, label_column=None, seed=42, test_size=0.3, n_estimators=100,
        contamination=0.1, output="results/raw/baseline"):
    output = Path(output)
    # A new directory prevents accidental replacement of another experiment.
    output.mkdir(parents=True, exist_ok=False)
    X_train, X_test, y, indices, features = load_data(path, label_column, seed, test_size)
    model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                          IsolationForest(n_estimators=n_estimators, contamination=contamination,
                                          random_state=seed, n_jobs=1))
    start = perf_counter()
    model.fit(X_train)
    fit_seconds = perf_counter() - start
    start = perf_counter()
    scores = -model.score_samples(X_test)
    predicted = (model.predict(X_test) == -1).astype(int)
    score_seconds = perf_counter() - start
    metrics = dict(n_train=len(X_train), n_test=len(X_test), fit_seconds=fit_seconds,
                   score_seconds=score_seconds, roc_auc=None, average_precision=None,
                   precision=None, recall=None, f1=None)
    if y is not None:
        p, r, f, _ = precision_recall_fscore_support(y, predicted, average="binary", zero_division=0)
        metrics.update(precision=float(p), recall=float(r), f1=float(f))
        if len(np.unique(y)) == 2:
            metrics.update(roc_auc=float(roc_auc_score(y, scores)),
                           average_precision=float(average_precision_score(y, scores)))
    config = dict(model="sklearn.IsolationForest", protocol="offline_random_holdout",
                  dataset=str(path) if path else "synthetic", label_column=label_column,
                  seed=seed, test_size=test_size, n_estimators=n_estimators,
                  contamination=contamination, features=features,
                  sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest() if path else None,
                  python=platform.python_version(), numpy=np.__version__, pandas=pd.__version__,
                  sklearn=sklearn.__version__, preprocessing="train-only median imputation + standard scaling")
    predictions = pd.DataFrame(dict(row_index=indices, anomaly_score=scores, prediction=predicted))
    if y is not None:
        predictions["label"] = y
    predictions.to_csv(output / "predictions.csv", index=False)
    for name, value in (("config", config), ("metrics", metrics)):
        (output / f"{name}.json").write_text(json.dumps(value, indent=2, allow_nan=False), encoding="utf-8")
    log_run(config, metrics, output)
    return metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path)
    parser.add_argument("--label-column")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--test-size", type=float, default=0.3)
    parser.add_argument("--n-estimators", type=int, default=100)
    parser.add_argument("--contamination", type=float, default=0.1)
    parser.add_argument("--output", default="results/raw/baseline")
    args = parser.parse_args()
    if args.label_column and args.data is None:
        parser.error("--label-column requires --data")
    print(json.dumps(run(path=args.data, label_column=args.label_column, seed=args.seed,
                         test_size=args.test_size, n_estimators=args.n_estimators,
                         contamination=args.contamination, output=args.output), indent=2))


if __name__ == "__main__":
    main()

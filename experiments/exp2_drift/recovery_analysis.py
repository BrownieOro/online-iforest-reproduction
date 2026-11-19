"""Summarize recovery at drift points from completed prequential runs.

Baseline: last complete evaluation window ending before the change. Recovery:
first complete post-change window reaching that baseline before the next change.
The reported delay is the end of that window minus the change index.
"""
import argparse
import csv
import json
from pathlib import Path

import numpy as np

CHANGES = (51255, 74381, 100944, 142291, 152207)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = []
    for metrics_path in sorted(args.run_dir.glob("*_seed*/metrics.json")):
        m = json.loads(metrics_path.read_text(encoding="utf-8"))
        windows = m["sliding_window"]
        starts = np.asarray(windows["row_start"])
        auc = np.asarray([np.nan if x is None else x for x in windows["roc_auc"]])
        size = windows["size"]
        for i, change in enumerate(CHANGES):
            end = CHANGES[i + 1] if i + 1 < len(CHANGES) else m["n_samples"]
            before = np.flatnonzero((starts + size <= change) & np.isfinite(auc))
            after = np.flatnonzero((starts >= change) & (starts + size <= end) & np.isfinite(auc))
            baseline = float(auc[before[-1]]) if len(before) else None
            recovered = [j for j in after if baseline is not None and auc[j] >= baseline]
            first = recovered[0] if recovered else None
            rows.append({"model": m["model"], "seed": m["seed"], "change": change,
                         "baseline_auc": baseline,
                         "first_post_auc": float(auc[after[0]]) if len(after) else None,
                         "delay_samples": int(starts[first] + size - change) if first is not None else None,
                         "status": "recovered" if first is not None else "not_observed"})
    if not rows:
        raise SystemExit("No completed metrics.json files found")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()

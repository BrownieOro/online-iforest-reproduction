"""Plot per-seed rolling ROC-AUC for completed INSECTS runs."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

CHANGES = (51255, 74381, 100944, 142291, 152207)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("run_dir", type=Path)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    paths = sorted(args.run_dir.glob("oif_seed*/metrics.json"))
    if not paths:
        raise SystemExit("No completed OIF runs")
    fig, ax = plt.subplots(figsize=(11, 4.4))
    for path in paths:
        m = json.loads(path.read_text(encoding="utf-8"))
        w = m["sliding_window"]
        centers = np.asarray(w["row_start"]) + w["size"] / 2
        ax.plot(centers, w["roc_auc"], label=f"Seed {m['seed']}", linewidth=1.4)
    for i, cp in enumerate(CHANGES):
        ax.axvline(cp, color="#c0392b", linestyle="--", linewidth=0.9,
                   label="Mốc thay đổi" if i == 0 else None)
    ax.set(xlabel="Vị trí tâm cửa sổ trong luồng", ylabel="ROC-AUC",
           title="INSECTS: OIF, 10 đặc trưng, cửa sổ đánh giá 5.000 mẫu", ylim=(0, 1))
    ax.grid(alpha=.2)
    ax.legend(ncol=3, fontsize=8)
    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=160)


if __name__ == "__main__":
    main()

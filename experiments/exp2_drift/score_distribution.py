"""Plot OIF score distributions by label before and after an INSECTS change."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("predictions", type=Path)
    parser.add_argument("--change", type=int, default=51255)
    parser.add_argument("--width", type=int, default=5000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = pd.read_csv(args.predictions)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    for ax, (title, a, b) in zip(axes, [("Trước", args.change-args.width, args.change),
                                       ("Sau", args.change, args.change+args.width)]):
        segment = data[(data.row_index >= a) & (data.row_index < b)]
        for label, color, name in [(0, "#2563eb", "Bình thường"), (1, "#ea580c", "Bất thường")]:
            values = segment.loc[segment.label == label, "anomaly_score"]
            if len(values):
                ax.hist(values, bins=30, range=(0, 1), density=True, histtype="step", linewidth=2,
                        color=color, label=f"{name} (n={len(values)})")
        ax.set(title=f"{title} mốc {args.change}: [{a}, {b})", xlabel="Điểm bất thường")
        ax.legend(fontsize=8)
    axes[0].set_ylabel("Mật độ")
    fig.suptitle("Phân bố điểm OIF, seed 0; mỗi nhóm chuẩn hóa riêng")
    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=160)


if __name__ == "__main__":
    main()

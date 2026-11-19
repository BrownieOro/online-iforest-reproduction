"""Plot the one-seed INSECTS window-size sweep from results/window-sweep-10.csv."""
from pathlib import Path
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
SUMMARY = ROOT / "results" / "window-sweep-10.csv"
OUTPUT = ROOT / "figures" / "window-sweep-10.png"


def main() -> None:
    with SUMMARY.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    rows.sort(key=lambda row: int(row["window_size"]))
    windows = [int(row["window_size"]) for row in rows]
    auc = [float(row["roc_auc"]) for row in rows]
    ap = [float(row["average_precision"]) for row in rows]

    fig, axes = plt.subplots(1, 2, figsize=(9, 4), constrained_layout=True)
    for ax, values, label, title in (
        (axes[0], auc, "ROC-AUC", "ROC-AUC toàn luồng"),
        (axes[1], ap, "AP", "Average precision toàn luồng"),
    ):
        ax.plot(windows, values, marker="o", linewidth=2, color="#2a78d6")
        ax.set_xscale("log", base=2)
        ax.set_xticks(windows, [str(w) for w in windows])
        ax.set_ylim(0, 1)
        ax.set_xlabel("window_size")
        ax.set_ylabel(label)
        ax.set_title(title)
        ax.grid(axis="y", color="#e4e3df", linewidth=0.8)

    fig.suptitle("INSECTS, 10 đặc trưng đầu, seed 0 (một seed)")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=180)
    plt.close(fig)
    print(f"Wrote {OUTPUT.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()

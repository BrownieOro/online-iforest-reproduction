"""Create stationary experiment figures from the aggregated run CSV."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
SUMMARY = ROOT / "results" / "stationary-summary.csv"
FIGURES = ROOT / "figures"


def main() -> None:
    """Save median AUC and processing-time comparisons as PNG files."""
    summary = pd.read_csv(SUMMARY)
    FIGURES.mkdir(parents=True, exist_ok=True)
    labels = summary["dataset"].str.title().tolist()
    x = range(len(labels))

    fig, ax = plt.subplots(figsize=(7, 4.5), constrained_layout=True)
    width = 0.36
    ax.bar([i - width / 2 for i in x], summary["oif_roc_auc"], width,
           label="OIF (cập nhật theo luồng)")
    ax.bar([i + width / 2 for i in x], summary["baseline_roc_auc"], width,
           label="Isolation Forest (cố định)")
    ax.set_xticks(list(x), labels)
    ax.set_ylim(0, 1)
    ax.set_ylabel("ROC-AUC trung vị")
    ax.set_title("Dữ liệu ổn định: chất lượng phát hiện")
    ax.legend()
    fig.savefig(FIGURES / "stationary-auc.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4.5), constrained_layout=True)
    ax.bar([i - width / 2 for i in x], summary["oif_total_seconds"], width,
           label="OIF (cập nhật theo luồng)")
    ax.bar([i + width / 2 for i in x], summary["baseline_total_seconds"], width,
           label="Isolation Forest (cố định)")
    ax.set_xticks(list(x), labels)
    ax.set_ylabel("Thời gian trung vị (giây)")
    ax.set_title("Dữ liệu ổn định: thời gian xử lý")
    ax.legend()
    fig.savefig(FIGURES / "stationary-time.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()

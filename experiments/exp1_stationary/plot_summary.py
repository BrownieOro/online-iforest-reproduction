"""Create stationary experiment figures with medians and seed variability."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "results" / "raw" / "stationary" / "runs.csv"
FIGURES = ROOT / "figures"
METHODS = (
    ("oif", "Online Isolation Forest", "#2878B5", "o"),
    ("baseline", "Isolation Forest (scikit-learn)", "#E07A32", "s"),
)


def _seed_statistics(runs: pd.DataFrame, metric: str) -> pd.DataFrame:
    """Return median and interquartile range per dataset for a wide run table."""
    return runs.groupby("dataset")[metric].agg(
        median="median",
        q1=lambda values: values.quantile(0.25),
        q3=lambda values: values.quantile(0.75),
    )


def _plot_metric(runs: pd.DataFrame, datasets: list[str], metric_suffix: str,
                 title: str, ylabel: str, output_name: str,
                 output_dir: Path, log_scale: bool = False) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.7), constrained_layout=True)
    x = np.arange(len(datasets), dtype=float)
    offsets = {"oif": -0.13, "baseline": 0.13}

    for model_key, label, color, marker in METHODS:
        stats = _seed_statistics(runs, f"{model_key}_{metric_suffix}").reindex(datasets)
        medians = stats["median"].to_numpy(dtype=float)
        q1 = stats["q1"].to_numpy(dtype=float)
        q3 = stats["q3"].to_numpy(dtype=float)
        ax.errorbar(
            x + offsets[model_key], medians,
            yerr=np.vstack((medians - q1, q3 - medians)),
            fmt=marker, color=color, markerfacecolor=color,
            markeredgecolor="white", markeredgewidth=0.7,
            markersize=8, elinewidth=1.7, capsize=5,
            label=label, zorder=3,
        )

    counts = runs.groupby("dataset")["seed"].nunique().reindex(datasets)
    tick_labels = [f"{name.title()}\n(n={counts.loc[name]} seeds)" for name in datasets]
    ax.set_xticks(x, tick_labels)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_axisbelow(True)
    ax.grid(axis="y", color="#D9DEE5", linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if metric_suffix == "roc_auc":
        ax.set_ylim(0, 1)
    if log_scale:
        ax.set_yscale("log")
    ax.legend(frameon=False, loc="best")
    ax.text(
        0.01, -0.20, "Điểm: trung vị; thanh: Q1–Q3 qua các seed.",
        transform=ax.transAxes, ha="left", va="top", fontsize=9, color="#4C5664",
    )
    fig.savefig(output_dir / output_name, dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    """Save ROC-AUC and timing plots from per-seed stationary results."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, default=RUNS,
                        help="CSV containing one row per dataset and seed")
    parser.add_argument("--figures-dir", type=Path, default=FIGURES)
    args = parser.parse_args()
    if not args.runs.is_file():
        raise FileNotFoundError(
            f"Missing {args.runs}. Run the stationary experiment before plotting.")
    runs = pd.read_csv(args.runs)
    required = {
        "dataset", "seed", "oif_roc_auc", "baseline_roc_auc",
        "oif_total_seconds", "baseline_total_seconds",
    }
    missing = required.difference(runs.columns)
    if missing:
        raise ValueError(f"Run table is missing columns: {', '.join(sorted(missing))}")
    if runs.duplicated(["dataset", "seed"]).any():
        raise ValueError("Run table has duplicate dataset/seed rows")
    if runs[list(required - {"dataset", "seed"})].isna().any().any():
        raise ValueError("Run table contains missing metric values")
    counts = runs.groupby("dataset")["seed"].nunique()
    if (counts < 2).any():
        raise ValueError("At least two seeds per dataset are required to show Q1–Q3")
    if (runs[["oif_total_seconds", "baseline_total_seconds"]] <= 0).any().any():
        raise ValueError("Timing values must be positive for the logarithmic chart")

    datasets = sorted(runs["dataset"].unique())
    args.figures_dir.mkdir(parents=True, exist_ok=True)
    _plot_metric(
        runs, datasets, "roc_auc", "Dữ liệu ổn định: ROC-AUC theo seed",
        "ROC-AUC", "stationary-auc.png", args.figures_dir,
    )
    _plot_metric(
        runs, datasets, "total_seconds", "Dữ liệu ổn định: thời gian theo seed",
        "Tổng thời gian (giây, thang log)", "stationary-time.png",
        args.figures_dir, log_scale=True,
    )


if __name__ == "__main__":
    main()

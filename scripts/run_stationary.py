"""Run baseline on the two prepared stationary datasets and summarize results."""
import csv
import json
from pathlib import Path
from oif.baseline import run


def main():
    rows = []
    for name in ("annthyroid", "mammography"):
        data = Path("data/processed") / f"{name}.csv"
        output = Path("results/raw/stationary") / f"{name}-seed42"
        metrics = run(data, "label", seed=42, output=output)
        rows.append({"dataset": name, "seed": 42, **metrics})
    summary = Path("results/stationary-summary.csv")
    summary.parent.mkdir(parents=True, exist_ok=True)
    with summary.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    Path("results/stationary.md").write_text("# Stationary baseline\n\n" + json.dumps(rows, indent=2), encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()

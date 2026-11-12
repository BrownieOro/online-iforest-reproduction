"""Run implemented OIF on deterministic synthetic data."""
import json
from pathlib import Path
import numpy as np
from oif.forest import OnlineIsolationForest


def main():
    rng = np.random.default_rng(42)
    X = np.vstack([rng.normal(size=(80, 4)), rng.uniform(6, 9, size=(20, 4))])
    model = OnlineIsolationForest(n_trees=8, window_size=32, eta=2, seed=42)
    model.learn_batch(X)
    scores = model.score_samples(X[-10:])
    result = {"n_samples": len(X), "window_size": 32, "n_trees": 8,
              "score_min": float(scores.min()), "score_max": float(scores.max())}
    print(json.dumps(result, indent=2))
    output = Path("results/raw/oif-smoke-42.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

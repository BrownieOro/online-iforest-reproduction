import json
import numpy as np
import pandas as pd
import pytest
from oif.baseline import run
from oif.data import load_data
from oif.forest import OnlineIsolationForest
from oif.scoring import anomaly_scores


def test_smoke_reproducible(tmp_path, monkeypatch):
    monkeypatch.setenv("WANDB_MODE", "disabled")
    a = run(output=tmp_path / "a", n_estimators=30)
    run(output=tmp_path / "b", n_estimators=30)
    assert a["roc_auc"] > 0.95
    assert a["average_precision"] > 0.95
    pd.testing.assert_frame_equal(pd.read_csv(tmp_path / "a/predictions.csv"),
                                  pd.read_csv(tmp_path / "b/predictions.csv"))
    assert json.loads((tmp_path / "a/config.json").read_text())["seed"] == 42
    with pytest.raises(FileExistsError):
        run(output=tmp_path / "a")


def test_csv_missing_values_and_labels(tmp_path, monkeypatch):
    monkeypatch.setenv("WANDB_MODE", "disabled")
    frame = pd.DataFrame({"x": np.arange(100, dtype=float), "label": [0, 1] * 50})
    frame.loc[0, "x"] = np.nan
    path = tmp_path / "input.csv"
    frame.to_csv(path, index=False)
    metrics = run(path, "label", output=tmp_path / "labeled", n_estimators=10)
    assert metrics["roc_auc"] is not None
    metrics = run(path, output=tmp_path / "unlabeled", n_estimators=10)
    assert metrics["roc_auc"] is None


def test_invalid_and_single_class(tmp_path, monkeypatch):
    monkeypatch.setenv("WANDB_MODE", "disabled")
    path = tmp_path / "data.csv"
    pd.DataFrame({"x": range(20), "label": [0] * 20}).to_csv(path, index=False)
    assert run(path, "label", output=tmp_path / "single", n_estimators=10)["roc_auc"] is None
    pd.DataFrame({"x": [1, 2, 3, 4], "label": [0, 2, 0, 1]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="Labels"):
        load_data(path, "label")
    pd.DataFrame({"x": ["a"] * 4}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="numeric"):
        load_data(path)


def test_oif_learns_scores_and_window():
    forest = OnlineIsolationForest(n_trees=5, window_size=20, eta=2, seed=3)
    X = np.random.default_rng(4).normal(size=(40, 3))
    assert forest.learn_batch(X) is forest
    scores = forest.score_samples(X[-4:])
    assert scores.shape == (4,)
    assert np.isfinite(scores).all()
    assert len(forest._window) == 20
    with pytest.raises(ValueError):
        OnlineIsolationForest().score_samples(X[:1])
    assert anomaly_scores(np.ones((2, 4)), 20, 2).shape == (4,)

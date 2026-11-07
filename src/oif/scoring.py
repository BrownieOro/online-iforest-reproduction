"""Trân owns OIF score formula after paper/code reconciliation."""
import numpy as np


def anomaly_scores(depths: np.ndarray, window_size: int, eta: float) -> np.ndarray:
    """Input corrected depths (n_trees,n_samples); output (n_samples,), high=anomaly.

    Resolve normalization and small/empty window cases in docs/ghi-chu-doi-chieu.md first.
    """
    depths = np.asarray(depths, dtype=float)
    if depths.ndim != 2 or depths.shape[0] < 1 or not np.isfinite(depths).all():
        raise ValueError("depths must be a finite (n_trees, n_samples) array")
    if window_size < 1 or eta <= 0:
        raise ValueError("window_size and eta must be positive")
    c = 0.0 if window_size <= eta else np.log(window_size / eta) / np.log(4.0)
    scores = 2.0 ** (-depths.mean(axis=0) / (c + np.finfo(float).eps))
    return np.asarray(scores, dtype=float)

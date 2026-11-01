"""Trân owns OIF score formula after paper/code reconciliation."""
import numpy as np


def anomaly_scores(depths: np.ndarray, window_size: int, eta: float) -> np.ndarray:
    """Input corrected depths (n_trees,n_samples); output (n_samples,), high=anomaly.

    Resolve normalization and small/empty window cases in docs/ghi-chu-doi-chieu.md first.
    """
    raise NotImplementedError("Trân: implement and validate OIF normalization, not sklearn scores")

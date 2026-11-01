"""Trân: public forest scaffold; intentionally fails until OIF is implemented."""
import numpy as np


class OnlineIsolationForest:
    def __init__(self, n_trees=100, window_size=2048, eta=32.0, seed=42):
        if n_trees < 1 or window_size < 1 or eta <= 0:
            raise ValueError("n_trees, window_size and eta must be positive")
        self.n_trees = n_trees
        self.window_size = window_size
        self.eta = eta
        self.seed = seed

    def learn_batch(self, X: np.ndarray) -> "OnlineIsolationForest":
        """Finite (n,d); learn new then forget FIFO excess, retain <= window_size; return self."""
        raise NotImplementedError("Trân: wire Phúc tree and Thi learn/forget + FIFO")

    def score_samples(self, X: np.ndarray) -> np.ndarray:
        """Finite (n,d) -> finite (n,), high=anomaly, no state mutation."""
        raise NotImplementedError("Trân: aggregate depths and call scoring.anomaly_scores")

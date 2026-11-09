"""Trân: public forest scaffold; intentionally fails until OIF is implemented."""
import numpy as np
from collections import deque
from .tree import OnlineIsolationTree, _validate
from .scoring import anomaly_scores


class OnlineIsolationForest:
    def __init__(self, n_trees=100, window_size=2048, eta=32.0, seed=42):
        if n_trees < 1 or window_size < 1 or eta <= 0:
            raise ValueError("n_trees, window_size and eta must be positive")
        self.n_trees = n_trees
        self.window_size = window_size
        self.eta = eta
        self.seed = seed
        self._trees = None
        self._window = deque()
        self.n_features = None

    def learn_batch(self, X: np.ndarray) -> "OnlineIsolationForest":
        """Finite (n,d); learn new then forget FIFO excess, retain <= window_size; return self."""
        X = np.asarray(X, dtype=float)
        if X.ndim != 2 or X.shape[0] == 0 or not np.isfinite(X).all():
            raise ValueError("X must be a non-empty finite 2D array")
        if self.n_features is None:
            self.n_features = X.shape[1]
            self._trees = [OnlineIsolationTree(self.n_features, self.eta, self._depth_limit(), self.seed + i) for i in range(self.n_trees)]
        X = _validate(X, self.n_features)
        for x in X:
            self._set_depth_limit()
            for tree in self._trees:
                tree.max_depth = self._depth_limit()
                tree.learn_batch(x[None, :])
            self._window.append(x.copy())
            if len(self._window) > self.window_size:
                old = self._window.popleft()
                for tree in self._trees:
                    tree.forget_batch(old[None, :])
        return self

    def score_samples(self, X: np.ndarray) -> np.ndarray:
        """Finite (n,d) -> finite (n,), high=anomaly, no state mutation."""
        if self._trees is None or not self._window:
            raise ValueError("Forest must learn at least one sample before scoring")
        X = _validate(X, self.n_features)
        depths = np.vstack([tree.path_lengths(X) for tree in self._trees])
        return anomaly_scores(depths, len(self._window), self.eta)

    def _depth_limit(self):
        n = len(self._window)
        return 0.0 if n <= self.eta else np.log(n / self.eta) / np.log(4.0)

    def _set_depth_limit(self):
        if self._trees:
            limit = self._depth_limit()
            for tree in self._trees:
                tree.max_depth = limit

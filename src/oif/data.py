"""Numeric CSV input and reproducible smoke data; label 1 means anomaly."""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def load_data(path=None, label_column=None, seed=42, test_size=0.3):
    if path is None:
        rng = np.random.default_rng(seed)
        X = np.concatenate([rng.normal(0, 1, (900, 4)), rng.uniform(6, 10, (100, 4))])
        y = np.r_[np.zeros(900, dtype=int), np.ones(100, dtype=int)]
        frame = pd.DataFrame(X, columns=[f"x{i}" for i in range(4)])
    else:
        frame = pd.read_csv(path)
        y = None
        if label_column is not None:
            labels = frame.pop(label_column)
            if labels.isna().any() or not labels.isin([0, 1]).all():
                raise ValueError("Labels must be 0 (normal) or 1 (anomaly), without missing values")
            y = labels.to_numpy(dtype=int)
        if frame.shape[1] == 0 or not all(pd.api.types.is_numeric_dtype(t) for t in frame.dtypes):
            raise ValueError("Features must be numeric; remove ID/time/text columns before running")
    X = frame.to_numpy(dtype=float)
    if len(X) < 4 or np.isinf(X).any():
        raise ValueError("Need at least 4 rows and no infinite feature values")
    indices = np.arange(len(X))
    train, test = train_test_split(indices, test_size=test_size, random_state=seed,
                                   stratify=y if y is not None and len(np.unique(y)) == 2 else None)
    if np.isnan(X[train]).all(axis=0).any():
        raise ValueError("A feature is entirely missing in training data")
    return X[train], X[test], None if y is None else y[test], test, list(frame.columns)

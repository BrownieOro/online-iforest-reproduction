"""Thi: learn/forget contract; implement against Phúc's tree structure."""
from typing import Protocol
import numpy as np


class LearningTree(Protocol):
    def learn_batch(self, X: np.ndarray) -> None:
        """Update mass/bounds and split for finite float X (n,d)."""
        ...

    def forget_batch(self, X: np.ndarray) -> None:
        """Remove previously learned expired points; merge as required."""
        ...

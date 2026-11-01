"""Phúc: tree structure and traversal contract. No OIF implementation yet."""
from typing import Protocol
import numpy as np


class Tree(Protocol):
    def path_lengths(self, X: np.ndarray) -> np.ndarray:
        """Finite float (n,) corrected depths for numeric X (n,d); no mutation."""
        ...

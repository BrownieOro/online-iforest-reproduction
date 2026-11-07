"""Cấu trúc dùng chung đã chốt; Phúc triển khai khởi tạo và duyệt cây."""
from dataclasses import dataclass
from typing import Optional, Protocol
import numpy as np


@dataclass
class Node:
    """Một ô histogram; không lưu danh sách mẫu thật tại node.

    mass = h (khối lượng), depth = k (độ sâu), không dùng thay nhau.
    lower/upper: hai vector (n_features,) của miền bao R; None khi ô rỗng.
    Lá: split_feature/split_value/left/right đều None.
    Node trong: có đủ phép chia và hai con; x[q] < p sang trái, còn lại sang phải.
    Khi gộp: xóa cả phép chia và hai con. Không giữ parent pointer.
    """
    depth: int = 0
    mass: int = 0
    lower: Optional[np.ndarray] = None
    upper: Optional[np.ndarray] = None
    split_feature: Optional[int] = None
    split_value: Optional[float] = None
    left: Optional["Node"] = None
    right: Optional["Node"] = None

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


class Tree(Protocol):
    root: Node
    n_features: int
    eta: float
    max_depth: int
    rng: np.random.Generator

    def path_lengths(self, X: np.ndarray) -> np.ndarray:
        """X (n,d) -> độ sâu đã hiệu chỉnh (n,); không cập nhật cây."""
        ...


class OnlineIsolationTree:
    """Một cây dùng chung cho Phúc/Thi; Forest giữ FIFO, cây không giữ FIFO.

    Forest truyền max_depth sau khi chốt công thức; không ngầm chọn công thức ở đây.
    Mỗi cây nhận seed riêng từ Forest.
    """
    def __init__(self, n_features: int, eta: float, max_depth: float, seed: int = 42):
        if n_features < 1 or eta <= 0 or max_depth < 0:
            raise ValueError("n_features/eta phải dương; max_depth không âm")
        self.root = Node()
        self.n_features = n_features
        self.eta = eta
        self.max_depth = max_depth
        self.rng = np.random.default_rng(seed)

    def path_lengths(self, X: np.ndarray) -> np.ndarray:
        X = _validate(X, self.n_features)
        if self.root.mass <= 0:
            raise ValueError("Cannot score a tree before learning")
        return np.asarray([_path_length(self.root, x, self.eta) for x in X], dtype=float)

    def learn_batch(self, X: np.ndarray) -> None:
        from .learning import learn_batch
        learn_batch(self, X)

    def forget_batch(self, X: np.ndarray) -> None:
        from .learning import forget_batch
        forget_batch(self, X)


def _validate(X, n_features):
    X = np.asarray(X, dtype=float)
    if X.ndim != 2 or X.shape[1] != n_features or not np.isfinite(X).all():
        raise ValueError(f"X must be finite with shape (n, {n_features})")
    return X


def _path_length(node, x, eta):
    if node.is_leaf or node.split_feature is None:
        correction = 0.0 if node.mass <= eta else np.log(node.mass / eta) / np.log(4.0)
        return float(node.depth + correction)
    child = node.left if x[node.split_feature] < node.split_value else node.right
    return _path_length(child, x, eta)

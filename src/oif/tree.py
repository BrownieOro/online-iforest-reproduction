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
        if (not isinstance(n_features, (int, np.integer)) or isinstance(n_features, (bool, np.bool_))
                or n_features < 1 or not np.isfinite(eta) or eta <= 0
                or not np.isfinite(max_depth) or max_depth < 0):
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
        return np.asarray([_corrected_leaf_depth(self.find_leaf(x), self.eta) for x in X], dtype=float)

    def find_leaf(self, x: np.ndarray) -> Node:
        """Return the leaf reached by one finite feature vector without mutation."""
        x = np.asarray(x, dtype=float)
        if x.ndim != 1 or x.shape[0] != self.n_features or not np.isfinite(x).all():
            raise ValueError(f"x must be finite with shape ({self.n_features},)")
        node = self.root
        while True:
            has_left, has_right = node.left is not None, node.right is not None
            has_feature, has_value = node.split_feature is not None, node.split_value is not None
            if not (has_left or has_right or has_feature or has_value):
                return node
            if not (has_left and has_right and has_feature and has_value):
                raise ValueError("Invalid tree cấu trúc: internal node must have split and two children")
            if not isinstance(node.split_feature, (int, np.integer)) or not 0 <= node.split_feature < self.n_features:
                raise ValueError("Invalid tree structure: split_feature is out of range")
            if not np.isfinite(node.split_value):
                raise ValueError("Invalid tree structure: split_value must be finite")
            node = node.left if x[node.split_feature] < node.split_value else node.right

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


def _corrected_leaf_depth(node, eta):
    correction = 0.0 if node.mass <= eta else np.log(node.mass / eta) / np.log(4.0)
    return float(node.depth + correction)

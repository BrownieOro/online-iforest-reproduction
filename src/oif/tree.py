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
    def __init__(self, n_features: int, eta: float, max_depth: int, seed: int = 42):
        if n_features < 1 or eta <= 0 or max_depth < 0:
            raise ValueError("n_features/eta phải dương; max_depth không âm")
        self.root = Node()
        self.n_features = n_features
        self.eta = eta
        self.max_depth = max_depth
        self.rng = np.random.default_rng(seed)

    def path_lengths(self, X: np.ndarray) -> np.ndarray:
        raise NotImplementedError("Phúc: duyệt cây và hiệu chỉnh độ sâu lá")

    def learn_batch(self, X: np.ndarray) -> None:
        from .learning import learn_batch
        learn_batch(self, X)

    def forget_batch(self, X: np.ndarray) -> None:
        from .learning import forget_batch
        forget_batch(self, X)

    def find_leaf(self, x: np.ndarray):
        node = self.root
        while not node.is_leaf:
            if (node.left is None
                or node.right is None
                or node.split_feature is None
                or node.split_value is None):
                raise ValueError("Nút trong có cấu trúc không hợp lệ")

            q = node.split_feature
            p = node.split_value

            if x[q] < p:
                node = node.left
            else:
                node = node.right
        return node
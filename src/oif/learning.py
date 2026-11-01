"""Thi triển khai cập nhật trực tiếp Node/Tree trong tree.py; không tạo cây riêng."""
from typing import Protocol
import numpy as np
from .tree import Tree


class LearningTree(Tree, Protocol):
    def learn_batch(self, X: np.ndarray) -> None:
        """Nhận X hữu hạn (n,d), cập nhật tại chỗ."""
        ...

    def forget_batch(self, X: np.ndarray) -> None:
        """Nhận các mẫu đã học bị hết hạn, cập nhật tại chỗ."""
        ...


def learn_batch(tree: Tree, X: np.ndarray) -> None:
    """Thi: cập nhật mass/miền bao, tách theo paper; dùng tree.rng.

    Khi tách, lấy mẫu đều trong miền bao theo paper, không chia lại một kho mẫu thật.
    """
    raise NotImplementedError("Thi: học batch trên cấu trúc Node đã chốt")


def forget_batch(tree: Tree, X: np.ndarray) -> None:
    """Thi: giảm mass và gộp theo paper; FIFO do Forest chọn mẫu, không nằm ở đây."""
    raise NotImplementedError("Thi: quên batch trên cấu trúc Node đã chốt")

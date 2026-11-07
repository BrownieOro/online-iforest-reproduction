"""Thi triển khai cập nhật trực tiếp Node/Tree trong tree.py; không tạo cây riêng."""
from typing import Protocol
import numpy as np
from .tree import Tree, Node, _validate


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
    X = _validate(X, tree.n_features)
    for x in X:
        _learn(tree, tree.root, x)


def forget_batch(tree: Tree, X: np.ndarray) -> None:
    """Thi: giảm mass và gộp theo paper; FIFO do Forest chọn mẫu, không nằm ở đây."""
    X = _validate(X, tree.n_features)
    for x in X:
        if tree.root.mass <= 0:
            raise ValueError("Cannot forget from an empty tree")
        _forget(tree, tree.root, x)


def _expand(node, x):
    if node.lower is None:
        node.lower = x.copy(); node.upper = x.copy()
    else:
        node.lower = np.minimum(node.lower, x); node.upper = np.maximum(node.upper, x)


def _learn(tree, node, x):
    _expand(node, x); node.mass += 1
    if node.is_leaf:
        if node.mass < tree.eta * (2 ** node.depth) or node.depth >= tree.max_depth:
            return
        widths = node.upper - node.lower
        q = int(tree.rng.integers(tree.n_features))
        if widths[q] <= 0:
            q = int(np.argmax(widths))
        if widths[q] <= 0:
            return
        p = float(tree.rng.uniform(node.lower[q], node.upper[q]))
        if p <= node.lower[q] or p >= node.upper[q]:
            p = float((node.lower[q] + node.upper[q]) / 2)
        node.split_feature, node.split_value = q, p
        node.left = Node(depth=node.depth + 1)
        node.right = Node(depth=node.depth + 1)
        return
    child = node.left if x[node.split_feature] < node.split_value else node.right
    _learn(tree, child, x)


def _forget(tree, node, x):
    node.mass = max(0, node.mass - 1)
    if node.mass == 0:
        node.lower = node.upper = None
        return
    if node.is_leaf:
        return
    child = node.left if x[node.split_feature] < node.split_value else node.right
    _forget(tree, child, x)
    if node.left.mass + node.right.mass < tree.eta * (2 ** node.depth):
        node.lower = np.minimum(node.left.lower, node.right.lower) if node.left.lower is not None and node.right.lower is not None else node.lower
        node.upper = np.maximum(node.left.upper, node.right.upper) if node.left.upper is not None and node.right.upper is not None else node.upper
        node.split_feature = node.split_value = node.left = node.right = None

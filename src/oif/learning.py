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
    if len(X) > tree.root.mass:
        raise ValueError("Cannot forget more samples than the tree currently holds")
    for x in X:
        _forget(tree, tree.root, x)


def _threshold(tree, node):
    """Ngưỡng tách/gộp h_hat = eta * 2^k của node ở độ sâu k."""
    return tree.eta * (2 ** node.depth)


def _expand(node, x):
    """Nới miền bao R của node để chứa x (ô rỗng thì R = {x})."""
    if node.lower is None:
        node.lower = x.copy(); node.upper = x.copy()
    else:
        node.lower = np.minimum(node.lower, x); node.upper = np.maximum(node.upper, x)


def _learn(tree, node, x):
    """Thuật toán 2: tăng mass và nới R dọc đường đi; tách lá khi đủ điều kiện.

    Lá ở độ sâu k được tách khi mass >= eta * 2^k và k < tree.max_depth (delta kiểu float,
    không làm tròn).
    """
    while True:
        _expand(node, x); node.mass += 1
        if node.is_leaf:
            if node.mass >= _threshold(tree, node) and node.depth < tree.max_depth:
                _split(tree, node)
            return
        node = node.left if x[node.split_feature] < node.split_value else node.right


def _split(tree, node):
    """Tách lá thành hai con bằng m = node.mass mẫu ảo lấy đều trong R (Thuật toán 2, dòng 5-10).

    Lấy m = node.mass (thay vì đúng eta * 2^k) để luôn có left.mass + right.mass == node.mass,
    kể cả khi delta tăng theo n_eff làm một lá đã vượt ngưỡng từ trước. Không lưu mẫu ảo.

    Ngoại lệ so với paper (nhóm đã chốt), để không sinh phép chia vô nghĩa trên dữ liệu trùng:
    - chiều q lấy đều ngẫu nhiên; nếu chiều đó có độ rộng <= 0 thì đổi sang chiều rộng nhất;
    - nếu mọi chiều đều có độ rộng <= 0 (mọi điểm trùng nhau) thì không tách;
    - nếu p lấy đều trong [l_q, r_q] rơi đúng biên thì dùng trung điểm.
    """
    widths = node.upper - node.lower
    q = int(tree.rng.integers(tree.n_features))
    if widths[q] <= 0:
        q = int(np.argmax(widths))
    if widths[q] <= 0:
        return
    p = float(tree.rng.uniform(node.lower[q], node.upper[q]))
    if p <= node.lower[q] or p >= node.upper[q]:
        p = float((node.lower[q] + node.upper[q]) / 2)
    samples = tree.rng.uniform(node.lower, node.upper, size=(node.mass, tree.n_features))
    goes_left = samples[:, q] < p
    node.split_feature, node.split_value = q, p
    node.left = _child_from_samples(samples[goes_left], node.depth + 1)
    node.right = _child_from_samples(samples[~goes_left], node.depth + 1)


def _child_from_samples(samples, depth):
    """Tạo node con có mass = số mẫu ảo và R = hộp bao nhỏ nhất của chúng (rỗng thì None)."""
    if len(samples) == 0:
        return Node(depth=depth, mass=0)
    return Node(depth=depth, mass=len(samples), lower=samples.min(axis=0), upper=samples.max(axis=0))


def _forget(tree, node, x):
    """Thuật toán 3: giảm mass dọc đường đi; gộp node trong khi mass < eta * 2^k.

    Xét gộp ngay tại node sau khi giảm mass; nếu gộp thì R = hộp bao của các con không rỗng,
    xóa phép chia và hai con, rồi dừng. Ô có mass = 0 có R = None (C2).
    Vì mass con được khởi tạo từ mẫu ảo, x có thể rơi vào con đang có mass = 0; khi đó trừ
    vào con còn lại để giữ bất biến left.mass + right.mass == node.mass.
    """
    while True:
        node.mass -= 1
        if node.is_leaf:
            if node.mass == 0:
                node.lower = node.upper = None
            return
        if node.mass < _threshold(tree, node):
            _merge(node)
            return
        child = node.left if x[node.split_feature] < node.split_value else node.right
        if child.mass == 0:
            child = node.right if child is node.left else node.left
        node = child


def _merge(node):
    """Gộp hai con vào node: R = hộp bao nhỏ nhất của R_l, R_r (bỏ con rỗng); node thành lá."""
    filled = [c for c in (node.left, node.right) if c.lower is not None]
    if node.mass == 0 or not filled:
        node.lower = node.upper = None
    else:
        node.lower = np.min([c.lower for c in filled], axis=0)
        node.upper = np.max([c.upper for c in filled], axis=0)
    node.split_feature = node.split_value = node.left = node.right = None

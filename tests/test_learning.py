"""Kiểm tra học/quên, tách/gộp nút của Online-iTree (Thuật toán 2–3)."""
import numpy as np
import pytest

from oif.tree import OnlineIsolationTree


def _nodes(node):
    """Duyệt mọi node của cây theo thứ tự trước."""
    yield node
    if not node.is_leaf:
        yield from _nodes(node.left)
        yield from _nodes(node.right)


def _snapshot(node):
    """Biểu diễn cây thành tuple lồng nhau để so sánh bằng nhau."""
    bounds = None if node.lower is None else (tuple(node.lower), tuple(node.upper))
    if node.is_leaf:
        return (node.depth, node.mass, bounds)
    return (node.depth, node.mass, bounds, node.split_feature, node.split_value,
            _snapshot(node.left), _snapshot(node.right))


def _assert_invariants(tree):
    """Bất biến cấu trúc sau mỗi lần cập nhật."""
    for node in _nodes(tree.root):
        assert node.mass >= 0
        assert (node.lower is None) == (node.mass == 0)
        if node.is_leaf:
            continue
        assert node.left.mass + node.right.mass == node.mass
        assert node.mass >= tree.eta * 2 ** node.depth
        for child in (node.left, node.right):
            assert child.depth == node.depth + 1
            if child.lower is not None:
                assert np.all(child.lower >= node.lower)
                assert np.all(child.upper <= node.upper)


def test_learn_updates_mass_and_bounds():
    X = np.random.default_rng(0).normal(size=(20, 3))
    tree = OnlineIsolationTree(3, 32, 0.0, seed=1)
    assert tree.learn_batch(X) is None
    assert tree.root.is_leaf and tree.root.mass == 20
    np.testing.assert_array_equal(tree.root.lower, X.min(axis=0))
    np.testing.assert_array_equal(tree.root.upper, X.max(axis=0))


def test_split_threshold_and_children_mass():
    X = np.random.default_rng(1).uniform(size=(4, 2))
    tree = OnlineIsolationTree(2, 4, 5.0, seed=2)
    tree.learn_batch(X[:3])
    assert tree.root.is_leaf
    tree.learn_batch(X[3:])
    root = tree.root
    assert not root.is_leaf
    assert root.left.mass + root.right.mass == root.mass == 4
    assert root.left.depth == root.right.depth == 1
    assert root.lower[root.split_feature] < root.split_value < root.upper[root.split_feature]
    _assert_invariants(tree)


@pytest.mark.parametrize("max_depth, deepest", [(0.0, 0), (1.5, 2)])
def test_float_max_depth_limits_split(max_depth, deepest):
    X = np.random.default_rng(2).uniform(size=(500, 2))
    tree = OnlineIsolationTree(2, 2, max_depth, seed=3)
    tree.learn_batch(X)
    assert max(node.depth for node in _nodes(tree.root)) == deepest
    _assert_invariants(tree)


def test_invariants_hold_over_stream():
    X = np.random.default_rng(3).normal(size=(300, 3))
    tree = OnlineIsolationTree(3, 4, 4.0, seed=4)
    for start in range(0, 300, 50):
        tree.learn_batch(X[start:start + 50])
        _assert_invariants(tree)
    for start in range(0, 250, 25):
        tree.forget_batch(X[start:start + 25])
        _assert_invariants(tree)
    assert tree.root.mass == 50


def test_forget_keeps_split_while_mass_above_threshold():
    X = np.random.default_rng(4).uniform(size=(40, 2))
    tree = OnlineIsolationTree(2, 32, 3.0, seed=5)
    tree.learn_batch(X)
    tree.forget_batch(X[:1])
    assert not tree.root.is_leaf
    assert tree.root.mass == 39
    _assert_invariants(tree)


def test_merge_when_mass_below_threshold():
    X = np.random.default_rng(5).uniform(size=(10, 2))
    tree = OnlineIsolationTree(2, 4, 1.0, seed=6)
    tree.learn_batch(X)
    tree.forget_batch(X[:6])
    root = tree.root
    assert not root.is_leaf and root.mass == 4
    filled = [c for c in (root.left, root.right) if c.lower is not None]
    expected_lower = np.min([c.lower for c in filled], axis=0)
    expected_upper = np.max([c.upper for c in filled], axis=0)
    tree.forget_batch(X[6:7])
    assert root.is_leaf and root.mass == 3
    assert root.split_feature is None and root.split_value is None
    np.testing.assert_array_equal(root.lower, expected_lower)
    np.testing.assert_array_equal(root.upper, expected_upper)


def test_learn_then_forget_all_returns_empty_leaf():
    X = np.random.default_rng(6).normal(size=(100, 2))
    tree = OnlineIsolationTree(2, 4, 3.0, seed=7)
    tree.learn_batch(X)
    assert tree.forget_batch(X) is None
    assert tree.root.is_leaf and tree.root.mass == 0
    assert tree.root.lower is None and tree.root.upper is None


def test_same_seed_builds_same_tree():
    X = np.random.default_rng(7).normal(size=(200, 3))
    a, b = (OnlineIsolationTree(3, 4, 3.0, seed=8) for _ in range(2))
    for tree in (a, b):
        tree.learn_batch(X)
        tree.forget_batch(X[:80])
    assert _snapshot(a.root) == _snapshot(b.root)


def test_zero_width_features_are_not_split():
    tree = OnlineIsolationTree(2, 2, 3.0, seed=9)
    tree.learn_batch(np.ones((50, 2)))
    assert tree.root.is_leaf and tree.root.mass == 50

    X = np.random.default_rng(8).uniform(size=(200, 2))
    X[:, 0] = 1.0
    tree = OnlineIsolationTree(2, 2, 3.0, seed=10)
    tree.learn_batch(X)
    internal = [n for n in _nodes(tree.root) if not n.is_leaf]
    assert internal
    for node in internal:
        assert node.split_feature == 1
        assert node.lower[1] < node.split_value < node.upper[1]


@pytest.mark.parametrize("X", [np.ones((2, 3)), np.array([[np.nan, 1.0]]),
                               np.array([[np.inf, 1.0]]), np.ones(2)])
def test_invalid_input_raises(X):
    tree = OnlineIsolationTree(2, 4, 3.0)
    with pytest.raises(ValueError):
        tree.learn_batch(X)


def test_forget_more_than_learned_raises():
    tree = OnlineIsolationTree(2, 4, 3.0)
    with pytest.raises(ValueError):
        tree.forget_batch(np.ones((1, 2)))
    tree.learn_batch(np.ones((2, 2)))
    with pytest.raises(ValueError):
        tree.forget_batch(np.ones((3, 2)))

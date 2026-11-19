"""Kiểm tra cửa sổ FIFO và giới hạn độ sâu động của OnlineIsolationForest (C3)."""
import numpy as np
import pytest

from oif.forest import OnlineIsolationForest


def _C(m, eta):
    """C(m, eta) theo công thức nhóm đã chốt."""
    return 0.0 if m <= eta else float(np.log(m / eta) / np.log(4.0))


def _snapshot(node):
    """Biểu diễn cây thành tuple lồng nhau để so sánh trạng thái."""
    bounds = None if node.lower is None else (tuple(node.lower), tuple(node.upper))
    if node.is_leaf:
        return (node.depth, node.mass, bounds)
    return (node.depth, node.mass, bounds, node.split_feature, node.split_value,
            _snapshot(node.left), _snapshot(node.right))


def _learn_in_chunks(forest, X, sizes):
    """Học X theo các lô có kích thước khác nhau, giữ thứ tự."""
    start = 0
    for size in sizes:
        forest.learn_batch(X[start:start + size])
        start += size
    assert start == len(X)


def test_window_keeps_latest_samples_in_order():
    X = np.random.default_rng(0).normal(size=(120, 3))
    forest = OnlineIsolationForest(n_trees=3, window_size=50, eta=4, seed=1)
    _learn_in_chunks(forest, X, [7, 33, 80])
    assert len(forest._window) == 50
    np.testing.assert_array_equal(np.array(forest._window), X[-50:])


@pytest.mark.parametrize("n", [30, 50, 120])
def test_root_mass_equals_window_length(n):
    X = np.random.default_rng(1).normal(size=(n, 2))
    forest = OnlineIsolationForest(n_trees=4, window_size=50, eta=4, seed=2)
    forest.learn_batch(X)
    assert len(forest._window) == min(n, 50)
    for tree in forest._trees:
        assert tree.root.mass == len(forest._window)


def test_max_depth_matches_window_when_full():
    X = np.random.default_rng(2).normal(size=(200, 2))
    forest = OnlineIsolationForest(n_trees=3, window_size=64, eta=4, seed=3)
    forest.learn_batch(X)
    expected = _C(len(forest._window), forest.eta)
    for tree in forest._trees:
        assert isinstance(tree.max_depth, float)
        assert tree.max_depth == pytest.approx(expected)


def test_max_depth_matches_window_during_warmup():
    X = np.random.default_rng(3).normal(size=(40, 2))
    forest = OnlineIsolationForest(n_trees=2, window_size=64, eta=4, seed=4)
    forest.learn_batch(X)
    for tree in forest._trees:
        assert tree.max_depth == pytest.approx(_C(len(forest._window), forest.eta))


def test_score_samples_does_not_mutate_state():
    X = np.random.default_rng(4).normal(size=(100, 3))
    forest = OnlineIsolationForest(n_trees=3, window_size=40, eta=4, seed=5)
    forest.learn_batch(X)
    before = ([x.copy() for x in forest._window],
              [(_snapshot(t.root), t.max_depth, t.rng.bit_generator.state) for t in forest._trees])
    forest.score_samples(X[:10])
    after = ([x.copy() for x in forest._window],
             [(_snapshot(t.root), t.max_depth, t.rng.bit_generator.state) for t in forest._trees])
    np.testing.assert_array_equal(np.array(before[0]), np.array(after[0]))
    assert before[1] == after[1]


def test_empty_forest_score_raises():
    with pytest.raises(ValueError):
        OnlineIsolationForest(n_trees=2, window_size=10, eta=4).score_samples(np.ones((1, 2)))

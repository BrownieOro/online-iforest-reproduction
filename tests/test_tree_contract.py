import numpy as np
import pytest
from oif.tree import Node, OnlineIsolationTree


def test_tree_state_is_independent_and_seeded():
    a = OnlineIsolationTree(4, 32, 6, seed=7)
    b = OnlineIsolationTree(4, 32, 6, seed=7)
    a.root.mass = 3
    assert b.root.mass == 0
    assert a.root is not b.root
    np.testing.assert_array_equal(a.rng.random(5), b.rng.random(5))
    assert b.root.is_leaf
    assert b.root.lower is None and b.root.upper is None


def test_shared_tree_delegates_updates():
    tree = OnlineIsolationTree(4, 32, 6)
    tree.learn_batch(np.ones((2, 4)))
    assert tree.path_lengths(np.ones((2, 4))).shape == (2,)
    tree.forget_batch(np.ones((1, 4)))
    parent = Node(left=Node(depth=1), right=Node(depth=1), split_feature=0, split_value=0.5)
    assert not parent.is_leaf

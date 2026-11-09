import numpy as np
import pytest

from src.oif.tree import Node, OnlineIsolationTree

def make_tree():
    tree = OnlineIsolationTree(
        n_features=2,
        eta=2,
        max_depth=4,
        seed=42,
    )

    left_leaf = Node(depth=1, mass=3)
    right_left_leaf = Node(depth=2, mass=2)
    right_right_leaf = Node(depth=2, mass=1)

    right_node = Node(
        depth=1,
        mass=3,
        split_feature=1,
        split_value=10.0,
        left=right_left_leaf,
        right=right_right_leaf,
    )

    tree.root = Node(
        depth=0,
        mass=6,
        split_feature=0,
        split_value=5.0,
        left=left_leaf,
        right=right_node,
    )

    return tree

def test_initial_tree_is_empty_root():
    tree = OnlineIsolationTree(
        n_features=2, eta=2, max_depth=4)

    assert tree.root.is_leaf
    assert tree.root.depth == 0
    assert tree.root.mass == 0
    assert tree.root.lower is None
    assert tree.root.upper is None


@pytest.mark.parametrize(
    "x, expected_depth, expected_mass",
    [
        ([3.0, 20.0], 1, 3),  # Đi trái ngay tại gốc.
        ([7.0, 8.0], 2, 2),   # Phải rồi trái.
        ([7.0, 12.0], 2, 1),  # Phải rồi phải.
        ([5.0, 10.0], 2, 1),  # Bằng ngưỡng đều đi phải.
    ],
)
def test_find_leaf(x, expected_depth, expected_mass):
    tree = make_tree()

    leaf = tree.find_leaf(np.array(x))

    assert leaf.depth == expected_depth
    assert leaf.mass == expected_mass


def test_find_leaf_does_not_modify_tree():
    tree = make_tree()
    root = tree.root
    left = root.left
    right = root.right

    tree.find_leaf(np.array([7.0, 8.0]))

    assert tree.root is root
    assert root.left is left
    assert root.right is right
    assert root.mass == 6
    assert right.mass == 3
    assert right.left.mass == 2


def test_invalid_internal_node():
    tree = make_tree()
    tree.root.right = None

    with pytest.raises(ValueError, match="cấu trúc"):
        tree.find_leaf(np.array([7.0, 8.0]))
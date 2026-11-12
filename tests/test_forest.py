import numpy as np
import pytest
from oif.forest import OnlineIsolationForest


def test_forest_protocol_and_state_free_scoring():
    rng = np.random.default_rng(9)
    X = rng.normal(size=(40, 3))
    forest = OnlineIsolationForest(n_trees=4, window_size=12, eta=2, seed=7)
    with pytest.raises(ValueError):
        forest.score_samples(X[:1])
    forest.learn_batch(X)
    before = len(forest._window)
    a = forest.score_samples(X[:5])
    b = forest.score_samples(X[:5])
    np.testing.assert_allclose(a, b)
    assert len(forest._window) == before == 12
    assert a.shape == (5,)


def test_forest_rejects_dimension_change():
    forest = OnlineIsolationForest(n_trees=2, window_size=4, eta=2)
    forest.learn_batch(np.ones((3, 2)))
    with pytest.raises(ValueError):
        forest.learn_batch(np.ones((1, 3)))

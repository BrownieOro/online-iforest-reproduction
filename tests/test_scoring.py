"""Numerical contracts for Tran's score aggregation and untrained/small windows."""
import numpy as np
import pytest
from oif.scoring import anomaly_scores
from oif.forest import OnlineIsolationForest


def test_average_depth_before_exponential():
    # c(2048,32)=3; mean depths are both 3, although tree-wise scores differ.
    depths=np.array([[0.,3.],[6.,3.]])
    np.testing.assert_allclose(anomaly_scores(depths,2048,32),[.5,.5],rtol=0,atol=1e-14)


def test_effective_window_changes_normalization():
    depths=np.array([[1.,2.]])
    np.testing.assert_allclose(anomaly_scores(depths,128,32),[.5,.25],atol=1e-14)
    np.testing.assert_allclose(anomaly_scores(depths,512,32),[2**(-.5),.5],atol=1e-14)


def test_small_forest_scores_without_dividing_by_zero():
    model=OnlineIsolationForest(n_trees=3,window_size=64,eta=32,seed=0)
    model.learn_batch(np.ones((8,2)))
    np.testing.assert_array_equal(model.score_samples(np.ones((2,2))),[1.,1.])


def test_untrained_forest_rejects_scoring():
    with pytest.raises(ValueError,match="learn"):
        OnlineIsolationForest(n_trees=2).score_samples(np.ones((2,2)))


def test_nonfinite_depths_are_rejected():
    with pytest.raises(ValueError,match="finite"):
        anomaly_scores(np.array([[np.nan]]),2048,32)

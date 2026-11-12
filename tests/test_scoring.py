import numpy as np
import pytest
from oif.scoring import anomaly_scores


def test_score_order_and_shape():
    scores = anomaly_scores(np.array([[2.0, 3.0], [3.0, 4.0]]), 2048, 32)
    assert scores.shape == (2,)
    assert scores[0] > scores[1]
    assert np.isfinite(scores).all()


def test_score_rejects_invalid_inputs():
    with pytest.raises(ValueError):
        anomaly_scores(np.ones((2, 3)), 0, 32)
    with pytest.raises(ValueError):
        anomaly_scores(np.array([1.0, 2.0]), 10, 2)
    with pytest.raises(ValueError):
        anomaly_scores(np.array([[np.nan]]), 10, 2)

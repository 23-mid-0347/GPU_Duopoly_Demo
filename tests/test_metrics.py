"""
tests/test_metrics.py
=====================
Unit tests for models/metrics.py.

Covers: margin/payoff formulas, MAE/RMSE/bias guards, can_compute_validation.
"""

import pytest
from models.metrics import (
    per_unit_margin, model_payoff,
    mae, rmse, bias,
    can_compute_validation,
    MetricsInputError,
)


# ---------------------------------------------------------------------------
# Elementary formulas
# ---------------------------------------------------------------------------

class TestMarginPayoff:
    def test_margin(self):
        assert per_unit_margin(876.19, 550.0) == pytest.approx(326.19)

    def test_payoff(self):
        assert model_payoff(876.19, 550.0, 130.0) == pytest.approx(326.19 * 130.0)

    def test_payoff_matches_margin_times_qty(self):
        p, c, q = 800.0, 500.0, 100.0
        assert model_payoff(p, c, q) == per_unit_margin(p, c) * q


# ---------------------------------------------------------------------------
# MAE / RMSE / bias with valid inputs
# ---------------------------------------------------------------------------

class TestMAE:
    def test_perfect_prediction(self):
        assert mae([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]) == pytest.approx(0.0)

    def test_constant_error(self):
        assert mae([0.0, 0.0], [1.0, 1.0]) == pytest.approx(1.0)

    def test_asymmetric(self):
        # |3-1| + |4-6| = 2 + 2 = 4; MAE = 2
        assert mae([1.0, 6.0], [3.0, 4.0]) == pytest.approx(2.0)


class TestRMSE:
    def test_perfect(self):
        assert rmse([1.0, 2.0], [1.0, 2.0]) == pytest.approx(0.0)

    def test_constant_error(self):
        # sqrt((1^2 + 1^2)/2) = 1.0
        assert rmse([0.0, 0.0], [1.0, 1.0]) == pytest.approx(1.0)


class TestBias:
    def test_zero_bias(self):
        assert bias([1.0, 3.0], [2.0, 2.0]) == pytest.approx(0.0)

    def test_positive_bias(self):
        # (2-1) + (4-2) = 3; bias = 1.5
        assert bias([1.0, 2.0], [2.0, 4.0]) == pytest.approx(1.5)


# ---------------------------------------------------------------------------
# Guards: empty, mismatched, non-finite
# ---------------------------------------------------------------------------

class TestMetricGuards:
    def test_mae_empty_raises(self):
        with pytest.raises(MetricsInputError, match="empty"):
            mae([], [])

    def test_mae_mismatch_raises(self):
        with pytest.raises(MetricsInputError, match="Length mismatch"):
            mae([1.0, 2.0], [1.0])

    def test_mae_nan_raises(self):
        import math
        with pytest.raises(MetricsInputError):
            mae([float("nan")], [1.0])

    def test_mae_inf_raises(self):
        with pytest.raises(MetricsInputError):
            mae([float("inf")], [1.0])

    def test_rmse_empty_raises(self):
        with pytest.raises(MetricsInputError):
            rmse([], [])


# ---------------------------------------------------------------------------
# can_compute_validation
# ---------------------------------------------------------------------------

class TestCanComputeValidation:
    def test_none_inputs_returns_false(self):
        ok, _ = can_compute_validation(None, None)
        assert ok is False

    def test_empty_list_returns_false(self):
        ok, reason = can_compute_validation([], [])
        assert ok is False
        assert "empty" in reason.lower()

    def test_valid_inputs_returns_true(self):
        ok, reason = can_compute_validation([1.0, 2.0], [1.1, 1.9])
        assert ok is True
        assert reason == ""

    def test_mismatch_returns_false(self):
        ok, reason = can_compute_validation([1.0, 2.0], [1.0])
        assert ok is False
        assert "mismatch" in reason.lower()

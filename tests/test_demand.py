"""
tests/test_demand.py
====================
Unit tests for models/demand.py.
"""

import pytest
from models.demand import (
    validate_params, inverse_demand, direct_demand,
    ratio_to_D, DemandParamError,
)

# ---------------------------------------------------------------------------
# validate_params
# ---------------------------------------------------------------------------

class TestValidateParams:
    def test_valid_params(self):
        validate_params(1400, 2.5, 1.2)   # should not raise

    def test_B_zero_raises(self):
        with pytest.raises(DemandParamError, match="B must be > 0"):
            validate_params(1400, 0, 0)

    def test_B_negative_raises(self):
        with pytest.raises(DemandParamError, match="B must be > 0"):
            validate_params(1400, -1, 0)

    def test_D_negative_raises(self):
        with pytest.raises(DemandParamError, match="D must be >= 0"):
            validate_params(1400, 2.5, -0.1)

    def test_D_equal_B_raises(self):
        with pytest.raises(DemandParamError, match="D must be strictly less than B"):
            validate_params(1400, 2.5, 2.5)

    def test_D_greater_than_B_raises(self):
        with pytest.raises(DemandParamError, match="D must be strictly less than B"):
            validate_params(1400, 2.5, 3.0)

    def test_D_zero_valid(self):
        validate_params(1400, 2.5, 0.0)   # D=0 is admissible


# ---------------------------------------------------------------------------
# inverse_demand
# ---------------------------------------------------------------------------

class TestInverseDemand:
    def test_basic_values(self):
        A, B, D = 1400, 2.5, 1.2
        q1, q2 = 100, 150
        p1, p2 = inverse_demand(A, B, D, q1, q2)
        assert abs(p1 - (A - B * q1 - D * q2)) < 1e-10
        assert abs(p2 - (A - B * q2 - D * q1)) < 1e-10

    def test_D_zero_independent(self):
        """With D=0 the two demands are independent."""
        A, B = 1000, 2.0
        q1, q2 = 100, 80
        p1, p2 = inverse_demand(A, B, 0, q1, q2)
        assert abs(p1 - (A - B * q1)) < 1e-10
        assert abs(p2 - (A - B * q2)) < 1e-10


# ---------------------------------------------------------------------------
# direct_demand
# ---------------------------------------------------------------------------

class TestDirectDemand:
    def test_inversion_roundtrip(self):
        """q = direct_demand(inverse_demand(q)) should recover q."""
        A, B, D = 1400, 2.5, 1.2
        q1_orig, q2_orig = 130.0, 165.0
        p1, p2 = inverse_demand(A, B, D, q1_orig, q2_orig)
        q1_rec, q2_rec = direct_demand(A, B, D, p1, p2)
        assert abs(q1_rec - q1_orig) < 1e-8, f"q1 roundtrip failed: {q1_rec} vs {q1_orig}"
        assert abs(q2_rec - q2_orig) < 1e-8, f"q2 roundtrip failed: {q2_rec} vs {q2_orig}"

    def test_D_zero_independent(self):
        """With D=0 direct demand is also independent."""
        A, B = 1000, 2.0
        # monopoly price for q=100 is p=800; recover q from p
        p = 800.0
        q1, q2 = direct_demand(A, B, 0, p, p)
        # q = (A - p) / B = 200/2 = 100
        assert abs(q1 - 100.0) < 1e-8
        assert abs(q2 - 100.0) < 1e-8


# ---------------------------------------------------------------------------
# ratio_to_D
# ---------------------------------------------------------------------------

class TestRatioToD:
    def test_correct_conversion(self):
        B = 2.5
        ratio = 0.48
        D = ratio_to_D(ratio, B)
        assert abs(D - 0.48 * 2.5) < 1e-10

    def test_zero_ratio(self):
        assert ratio_to_D(0.0, 2.5) == 0.0

    def test_ratio_at_095(self):
        D = ratio_to_D(0.95, 2.5)
        assert abs(D - 0.95 * 2.5) < 1e-10

    def test_ratio_equal_one_raises(self):
        with pytest.raises(DemandParamError):
            ratio_to_D(1.0, 2.5)

    def test_ratio_above_one_raises(self):
        with pytest.raises(DemandParamError):
            ratio_to_D(1.1, 2.5)

    def test_negative_ratio_raises(self):
        with pytest.raises(DemandParamError):
            ratio_to_D(-0.1, 2.5)

    def test_slider_mapping_consistency(self):
        """Changing r updates D = r*B; displayed ratio == solver input."""
        B = 2.5
        for r in [0.0, 0.1, 0.3, 0.48, 0.7, 0.95]:
            D = ratio_to_D(r, B)
            reconstructed_ratio = D / B
            assert abs(reconstructed_ratio - r) < 1e-10, \
                f"Ratio round-trip failed for r={r}: got {reconstructed_ratio}"

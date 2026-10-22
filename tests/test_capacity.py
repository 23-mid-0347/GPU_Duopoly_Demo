"""
tests/test_capacity.py
======================
Unit tests for models/capacity.py.

Covers: binding cap, nonbinding cap, cap at unconstrained quantity,
AMD best-response, payoff formulas, parameter guards.
"""

import pytest
from models.capacity import solve_capacity_cournot
from models.cournot import solve_cournot

A, B = 1400.0, 2.5
D    = 0.48 * 2.5   # = 1.2
c1   = 550.0
c2   = 420.0

# Unconstrained NVIDIA Cournot qty ≈ 130.4754
UNCONSTRAINED_Q1 = solve_cournot(A, B, D, c1, c2).q1


# ---------------------------------------------------------------------------
# Binding cap (BUILD_PLAN.md §7: q1_cap=120 → q1=120, q2≈167.2)
# ---------------------------------------------------------------------------

class TestBindingCap:
    TOL = 0.1

    def setup_method(self):
        self.res = solve_capacity_cournot(A, B, D, c1, c2, q1_cap=120.0)

    def test_status_ok(self):
        assert self.res.status == "ok", self.res.message

    def test_cap_is_binding(self):
        assert self.res.binding is True

    def test_q1_equals_cap(self):
        assert abs(self.res.q1 - 120.0) < 1e-8, \
            f"q1={self.res.q1} should equal cap=120"

    def test_q2_amd_best_response(self):
        # AMD BR: q2 = (A - c2 - D*q1) / (2B) = (1400-420-1.2*120)/5 = (980-144)/5 = 167.2
        expected_q2 = (A - c2 - D * 120.0) / (2 * B)
        assert abs(self.res.q2 - expected_q2) < 1e-6, \
            f"q2={self.res.q2} vs expected={expected_q2}"

    def test_q2_approx_167_2(self):
        assert abs(self.res.q2 - 167.2) < self.TOL

    def test_prices_reference(self):
        # From BUILD_PLAN.md §7: p1≈899.36, p2≈838.00
        assert abs(self.res.p1 - 899.36) < self.TOL, f"p1={self.res.p1}"
        assert abs(self.res.p2 - 838.00) < self.TOL, f"p2={self.res.p2}"

    def test_payoffs_reference(self):
        assert abs(self.res.pi1 - 41923.20) < 1.0, f"pi1={self.res.pi1}"
        assert abs(self.res.pi2 - 69889.60) < 1.0, f"pi2={self.res.pi2}"


# ---------------------------------------------------------------------------
# Nonbinding cap (cap >= unconstrained)
# ---------------------------------------------------------------------------

class TestNonbindingCap:
    def test_cap_above_unconstrained_nonbinding(self):
        cap = UNCONSTRAINED_Q1 + 50   # clearly above
        res = solve_capacity_cournot(A, B, D, c1, c2, q1_cap=cap)
        assert res.status == "ok"
        assert res.binding is False

    def test_nonbinding_returns_unconstrained(self):
        """A nonbinding cap must return exactly the unconstrained equilibrium."""
        cap = UNCONSTRAINED_Q1 + 50
        res = solve_capacity_cournot(A, B, D, c1, c2, q1_cap=cap)
        uc  = solve_cournot(A, B, D, c1, c2)
        assert abs(res.q1 - uc.q1) < 1e-8
        assert abs(res.q2 - uc.q2) < 1e-8
        assert abs(res.p1 - uc.p1) < 1e-8
        assert abs(res.p2 - uc.p2) < 1e-8


# ---------------------------------------------------------------------------
# Cap at the unconstrained quantity  (BUILD_PLAN.md §11 item 11)
# ---------------------------------------------------------------------------

class TestCapAtUnconstrained:
    def test_cap_at_unconstrained_nonbinding(self):
        cap = UNCONSTRAINED_Q1
        res = solve_capacity_cournot(A, B, D, c1, c2, q1_cap=cap)
        assert res.status == "ok"
        assert res.binding is False

    def test_cap_at_unconstrained_results_match(self):
        cap = UNCONSTRAINED_Q1
        res = solve_capacity_cournot(A, B, D, c1, c2, q1_cap=cap)
        uc  = solve_cournot(A, B, D, c1, c2)
        assert abs(res.q1 - uc.q1) < 1e-8
        assert abs(res.pi1 - uc.pi1) < 1e-6


# ---------------------------------------------------------------------------
# Payoff formula
# ---------------------------------------------------------------------------

class TestCapacityPayoff:
    def test_payoff_formula_binding(self):
        res = solve_capacity_cournot(A, B, D, c1, c2, q1_cap=120.0)
        assert res.status == "ok"
        assert abs(res.pi1 - (res.p1 - c1) * res.q1) < 1e-8
        assert abs(res.pi2 - (res.p2 - c2) * res.q2) < 1e-8


# ---------------------------------------------------------------------------
# Parameter guard
# ---------------------------------------------------------------------------

class TestCapacityParamGuard:
    def test_negative_cap_returns_error(self):
        res = solve_capacity_cournot(A, B, D, c1, c2, q1_cap=-1.0)
        assert res.status == "error"

    def test_bad_demand_params(self):
        res = solve_capacity_cournot(A, 0, D, c1, c2, q1_cap=120.0)
        assert res.status == "error"

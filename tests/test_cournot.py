"""
tests/test_cournot.py
=====================
Unit tests for models/cournot.py.

Covers: numerical smoke test, D=0 monopoly equivalence, symmetry,
FOC verification, feasibility blocking, payoff formula, repeatability.
"""

import pytest
from models.cournot import solve_cournot, _check_foc, CournotResult
from models.demand import DemandParamError

# ---------------------------------------------------------------------------
# Default parameters from illustrative_defaults.json
# ---------------------------------------------------------------------------
A, B = 1400.0, 2.5
D    = 0.48 * 2.5   # = 1.2
c1   = 550.0        # NVIDIA
c2   = 420.0        # AMD


# ---------------------------------------------------------------------------
# Numerical smoke test (values from BUILD_PLAN.md §7)
# ---------------------------------------------------------------------------

class TestCournotSmokeTest:
    TOL = 1e-3  # tolerance for reference values

    def setup_method(self):
        self.res = solve_cournot(A, B, D, c1, c2)

    def test_status_ok(self):
        assert self.res.status == "ok", self.res.message

    def test_nvidia_price(self):
        assert abs(self.res.p1 - 876.1885) < self.TOL, \
            f"NVIDIA price {self.res.p1} != 876.1885"

    def test_amd_price(self):
        assert abs(self.res.p2 - 831.7148) < self.TOL, \
            f"AMD price {self.res.p2} != 831.7148"

    def test_nvidia_quantity(self):
        assert abs(self.res.q1 - 130.4754) < self.TOL, \
            f"NVIDIA qty {self.res.q1} != 130.4754"

    def test_amd_quantity(self):
        assert abs(self.res.q2 - 164.6859) < self.TOL, \
            f"AMD qty {self.res.q2} != 164.6859"

    def test_nvidia_margin(self):
        assert abs(self.res.m1 - 326.1885) < self.TOL

    def test_amd_margin(self):
        assert abs(self.res.m2 - 411.7148) < self.TOL

    def test_nvidia_payoff(self):
        assert abs(self.res.pi1 - 42559.56) < 1.0   # looser tol for payoff

    def test_amd_payoff(self):
        assert abs(self.res.pi2 - 67803.62) < 1.0


# ---------------------------------------------------------------------------
# D = 0 monopoly equivalence (BUILD_PLAN.md §6.7)
# ---------------------------------------------------------------------------

class TestCournotD0:
    """When D=0 each firm should be an independent monopolist."""

    def _monopoly(self, A, B, c):
        q_star = (A - c) / (2 * B)
        p_star = (A + c) / 2
        pi_star = (A - c) ** 2 / (4 * B)
        return q_star, p_star, pi_star

    def test_nvidia_d0(self):
        res = solve_cournot(A, B, 0, c1, c2)
        assert res.status == "ok"
        q_m, p_m, pi_m = self._monopoly(A, B, c1)
        assert abs(res.q1 - q_m)  < 1e-8, f"q1={res.q1} vs monopoly={q_m}"
        assert abs(res.p1 - p_m)  < 1e-8
        assert abs(res.pi1 - pi_m) < 1e-6

    def test_amd_d0(self):
        res = solve_cournot(A, B, 0, c1, c2)
        assert res.status == "ok"
        q_m, p_m, pi_m = self._monopoly(A, B, c2)
        assert abs(res.q2 - q_m)  < 1e-8
        assert abs(res.p2 - p_m)  < 1e-8
        assert abs(res.pi2 - pi_m) < 1e-6


# ---------------------------------------------------------------------------
# Symmetry test (c1 == c2 → equal outcomes)
# ---------------------------------------------------------------------------

class TestCournotSymmetry:
    def test_symmetric_costs(self):
        c = 450.0
        res = solve_cournot(A, B, D, c, c)
        assert res.status == "ok"
        assert abs(res.q1 - res.q2) < 1e-8, f"q1={res.q1} != q2={res.q2}"
        assert abs(res.p1 - res.p2) < 1e-8
        assert abs(res.m1 - res.m2) < 1e-8
        assert abs(res.pi1 - res.pi2) < 1e-6


# ---------------------------------------------------------------------------
# FOC verification
# ---------------------------------------------------------------------------

class TestCournotFOC:
    TOL = 1e-6

    def test_foc_residuals_near_zero(self):
        res = solve_cournot(A, B, D, c1, c2)
        assert res.status == "ok"
        r1, r2 = _check_foc(res)
        assert abs(r1) < self.TOL, f"FOC1 residual {r1} exceeds {self.TOL}"
        assert abs(r2) < self.TOL, f"FOC2 residual {r2} exceeds {self.TOL}"


# ---------------------------------------------------------------------------
# Payoff formula
# ---------------------------------------------------------------------------

class TestCournotPayoff:
    def test_payoff_formula(self):
        res = solve_cournot(A, B, D, c1, c2)
        assert res.status == "ok"
        assert abs(res.pi1 - (res.p1 - res.c1) * res.q1) < 1e-8
        assert abs(res.pi2 - (res.p2 - res.c2) * res.q2) < 1e-8


# ---------------------------------------------------------------------------
# Parameter guard
# ---------------------------------------------------------------------------

class TestCournotParamGuard:
    def test_B_zero(self):
        res = solve_cournot(A, 0, 0, c1, c2)
        assert res.status == "error"

    def test_D_negative(self):
        res = solve_cournot(A, B, -0.1, c1, c2)
        assert res.status == "error"

    def test_D_ge_B(self):
        res = solve_cournot(A, B, B, c1, c2)
        assert res.status == "error"


# ---------------------------------------------------------------------------
# Repeatability
# ---------------------------------------------------------------------------

class TestCournotRepeatability:
    def test_same_inputs_same_outputs(self):
        r1 = solve_cournot(A, B, D, c1, c2)
        r2 = solve_cournot(A, B, D, c1, c2)
        assert r1.q1 == r2.q1
        assert r1.p1 == r2.p1
        assert r1.pi1 == r2.pi1

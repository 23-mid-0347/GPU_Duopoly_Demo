"""
tests/test_bertrand.py
======================
Unit tests for models/bertrand.py.

Covers: numerical smoke test, D=0 monopoly equivalence, symmetry,
demand-inversion identity, FOC verification, feasibility, payoff formula.
"""

import pytest
from models.bertrand import solve_bertrand, _check_bertrand_foc
from models.demand import direct_demand, inverse_demand, DemandParamError

A, B = 1400.0, 2.5
D    = 0.48 * 2.5   # = 1.2
c1   = 550.0
c2   = 420.0


# ---------------------------------------------------------------------------
# Numerical smoke test (values from BUILD_PLAN.md §7)
# ---------------------------------------------------------------------------

class TestBertrandSmokeTest:
    TOL = 1e-3

    def setup_method(self):
        self.res = solve_bertrand(A, B, D, c1, c2)

    def test_status_ok(self):
        assert self.res.status == "ok", self.res.message

    def test_nvidia_price(self):
        assert abs(self.res.p1 - 824.2360) < self.TOL, \
            f"NVIDIA price {self.res.p1} != 824.2360"

    def test_amd_price(self):
        assert abs(self.res.p2 - 771.8166) < self.TOL, \
            f"AMD price {self.res.p2} != 771.8166"

    def test_nvidia_quantity(self):
        assert abs(self.res.q1 - 142.5343) < self.TOL, \
            f"NVIDIA qty {self.res.q1} != 142.5343"

    def test_amd_quantity(self):
        assert abs(self.res.q2 - 182.8569) < self.TOL, \
            f"AMD qty {self.res.q2} != 182.8569"

    def test_nvidia_margin(self):
        assert abs(self.res.m1 - 274.2360) < self.TOL

    def test_amd_margin(self):
        assert abs(self.res.m2 - 351.8166) < self.TOL

    def test_nvidia_payoff(self):
        assert abs(self.res.pi1 - 39088.04) < 1.0

    def test_amd_payoff(self):
        assert abs(self.res.pi2 - 64332.09) < 1.0


# ---------------------------------------------------------------------------
# D = 0 monopoly equivalence
# ---------------------------------------------------------------------------

class TestBertrandD0:
    """When D=0 Bertrand and Cournot both reduce to independent monopoly."""

    def _monopoly(self, A, B, c):
        q_star = (A - c) / (2 * B)
        p_star = (A + c) / 2
        pi_star = (A - c) ** 2 / (4 * B)
        return q_star, p_star, pi_star

    def test_nvidia_d0(self):
        res = solve_bertrand(A, B, 0, c1, c2)
        assert res.status == "ok"
        q_m, p_m, pi_m = self._monopoly(A, B, c1)
        assert abs(res.p1 - p_m) < 1e-8
        assert abs(res.q1 - q_m) < 1e-8
        assert abs(res.pi1 - pi_m) < 1e-6

    def test_amd_d0(self):
        res = solve_bertrand(A, B, 0, c1, c2)
        assert res.status == "ok"
        q_m, p_m, pi_m = self._monopoly(A, B, c2)
        assert abs(res.p2 - p_m) < 1e-8
        assert abs(res.q2 - q_m) < 1e-8
        assert abs(res.pi2 - pi_m) < 1e-6

    def test_cournot_bertrand_d0_agree(self):
        """With D=0, Cournot and Bertrand should give identical results."""
        from models.cournot import solve_cournot
        c = solve_cournot(A, B, 0, c1, c2)
        b = solve_bertrand(A, B, 0, c1, c2)
        assert c.status == "ok" and b.status == "ok"
        assert abs(c.p1 - b.p1) < 1e-8
        assert abs(c.p2 - b.p2) < 1e-8
        assert abs(c.q1 - b.q1) < 1e-8
        assert abs(c.q2 - b.q2) < 1e-8


# ---------------------------------------------------------------------------
# Symmetry
# ---------------------------------------------------------------------------

class TestBertrandSymmetry:
    def test_symmetric_costs(self):
        c = 450.0
        res = solve_bertrand(A, B, D, c, c)
        assert res.status == "ok"
        assert abs(res.p1 - res.p2) < 1e-8
        assert abs(res.q1 - res.q2) < 1e-8
        assert abs(res.pi1 - res.pi2) < 1e-6


# ---------------------------------------------------------------------------
# Demand inversion identity
# ---------------------------------------------------------------------------

class TestBertrandDemandInversion:
    def test_direct_demand_consistency(self):
        """
        Plugging Bertrand equilibrium prices back into direct demand
        must reproduce the equilibrium quantities.
        """
        res = solve_bertrand(A, B, D, c1, c2)
        assert res.status == "ok"
        q1_check, q2_check = direct_demand(A, B, D, res.p1, res.p2)
        assert abs(q1_check - res.q1) < 1e-8
        assert abs(q2_check - res.q2) < 1e-8

    def test_inverse_demand_consistency(self):
        """
        Plugging Bertrand equilibrium quantities into inverse demand
        must reproduce the equilibrium prices.
        """
        res = solve_bertrand(A, B, D, c1, c2)
        assert res.status == "ok"
        p1_check, p2_check = inverse_demand(A, B, D, res.q1, res.q2)
        assert abs(p1_check - res.p1) < 1e-8
        assert abs(p2_check - res.p2) < 1e-8


# ---------------------------------------------------------------------------
# Bertrand FOC
# ---------------------------------------------------------------------------

class TestBertrandFOC:
    TOL = 1e-6

    def test_foc_residuals_near_zero(self):
        res = solve_bertrand(A, B, D, c1, c2)
        assert res.status == "ok"
        r1, r2 = _check_bertrand_foc(res)
        assert abs(r1) < self.TOL, f"FOC1 residual {r1}"
        assert abs(r2) < self.TOL, f"FOC2 residual {r2}"


# ---------------------------------------------------------------------------
# Payoff formula
# ---------------------------------------------------------------------------

class TestBertrandPayoff:
    def test_payoff_formula(self):
        res = solve_bertrand(A, B, D, c1, c2)
        assert res.status == "ok"
        assert abs(res.pi1 - (res.p1 - res.c1) * res.q1) < 1e-8
        assert abs(res.pi2 - (res.p2 - res.c2) * res.q2) < 1e-8


# ---------------------------------------------------------------------------
# Parameter guard
# ---------------------------------------------------------------------------

class TestBertrandParamGuard:
    def test_B_zero(self):
        res = solve_bertrand(A, 0, 0, c1, c2)
        assert res.status == "error"

    def test_D_ge_B(self):
        res = solve_bertrand(A, B, B, c1, c2)
        assert res.status == "error"

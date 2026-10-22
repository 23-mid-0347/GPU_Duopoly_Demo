"""
models/cournot.py
=================
Analytical interior Nash equilibrium for the symmetric linear differentiated-
product Cournot duopoly.

Payoffs:
    π1 = (A - B*q1 - D*q2 - c1) * q1
    π2 = (A - B*q2 - D*q1 - c2) * q2

First-order conditions (interior):
    A - 2B*q1 - D*q2 - c1 = 0
    A - 2B*q2 - D*q1 - c2 = 0

Closed-form equilibrium quantities:
    q1* = [2B(A - c1) - D(A - c2)] / (4B² - D²)
    q2* = [2B(A - c2) - D(A - c1)] / (4B² - D²)

Prices and payoffs are recovered via the shared inverse demand system.

No Streamlit or Plotly dependency is permitted here.
"""

from dataclasses import dataclass
from typing import Optional
import math

from models.demand import validate_params, inverse_demand, DemandParamError


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class CournotResult:
    """
    All equilibrium outputs for the Cournot game.

    status : "ok" | "infeasible" | "error"
    message : human-readable explanation when status != "ok"
    """
    status: str = "ok"
    message: str = ""
    # quantities
    q1: Optional[float] = None
    q2: Optional[float] = None
    # prices
    p1: Optional[float] = None
    p2: Optional[float] = None
    # per-unit margins
    m1: Optional[float] = None
    m2: Optional[float] = None
    # model payoffs  π_i = (p_i - c_i) * q_i
    pi1: Optional[float] = None
    pi2: Optional[float] = None
    # stored inputs for reference
    A: Optional[float] = None
    B: Optional[float] = None
    D: Optional[float] = None
    c1: Optional[float] = None
    c2: Optional[float] = None


# ---------------------------------------------------------------------------
# FOC verifier (used in tests)
# ---------------------------------------------------------------------------

def _check_foc(result: CournotResult, tol: float = 1e-6) -> tuple[float, float]:
    """
    Return residuals of the two Cournot first-order conditions:

        r1 = A - 2B*q1 - D*q2 - c1   (should be ~0)
        r2 = A - 2B*q2 - D*q1 - c2   (should be ~0)
    """
    r = result
    r1 = r.A - 2 * r.B * r.q1 - r.D * r.q2 - r.c1
    r2 = r.A - 2 * r.B * r.q2 - r.D * r.q1 - r.c2
    return r1, r2


# ---------------------------------------------------------------------------
# Main solver
# ---------------------------------------------------------------------------

def solve_cournot(A: float, B: float, D: float,
                  c1: float, c2: float) -> CournotResult:
    """
    Solve the symmetric linear differentiated Cournot game and return a
    CournotResult.

    If the interior equilibrium produces any negative quantity, the result
    is marked infeasible (the interior formulas are not correct equilibria
    with a non-negativity constraint and we do NOT silently clip).

    Parameters
    ----------
    A  : float  — inverse-demand intercept
    B  : float  — own-quantity slope (> 0)
    D  : float  — cross-quantity term (0 <= D < B)
    c1 : float  — NVIDIA marginal cost input (illustrative)
    c2 : float  — AMD   marginal cost input (illustrative)
    """
    base = CournotResult(A=A, B=B, D=D, c1=c1, c2=c2)

    # --- parameter validation ---
    try:
        validate_params(A, B, D)
    except DemandParamError as exc:
        base.status = "error"
        base.message = str(exc)
        return base

    # --- closed-form quantities ---
    denom = 4 * B ** 2 - D ** 2   # = (2B - D)(2B + D); positive when D < B < 2B

    if denom <= 0:
        base.status = "error"
        base.message = (
            f"Denominator 4B² - D² = {denom:.6g} is non-positive under these "
            "parameters. Check that B > 0 and D < B."
        )
        return base

    q1 = (2 * B * (A - c1) - D * (A - c2)) / denom
    q2 = (2 * B * (A - c2) - D * (A - c1)) / denom

    # --- feasibility check: interior solution requires q >= 0 ---
    if q1 < 0 or q2 < 0:
        base.status = "infeasible"
        base.message = (
            f"Interior Cournot quantities are negative (q1={q1:.4f}, q2={q2:.4f}). "
            "This means the interior first-order conditions do not describe a valid "
            "Nash equilibrium under these parameters. Adjust A, B, D, c1, or c2."
        )
        base.q1 = q1
        base.q2 = q2
        return base

    # --- prices via inverse demand ---
    p1, p2 = inverse_demand(A, B, D, q1, q2)

    # --- margins and payoffs ---
    m1 = p1 - c1
    m2 = p2 - c2
    pi1 = m1 * q1
    pi2 = m2 * q2

    return CournotResult(
        status="ok",
        message="",
        q1=q1, q2=q2,
        p1=p1, p2=p2,
        m1=m1, m2=m2,
        pi1=pi1, pi2=pi2,
        A=A, B=B, D=D, c1=c1, c2=c2,
    )


# ---------------------------------------------------------------------------
# Reaction function helper (for plotting / educational use)
# ---------------------------------------------------------------------------

def cournot_reaction_q1(A: float, B: float, D: float,
                        c1: float, q2: float) -> float:
    """
    NVIDIA's Cournot best-response quantity given AMD's quantity q2:
        q1_BR = max(0, (A - c1 - D*q2) / (2B))
    """
    return max(0.0, (A - c1 - D * q2) / (2 * B))


def cournot_reaction_q2(A: float, B: float, D: float,
                        c2: float, q1: float) -> float:
    """
    AMD's Cournot best-response quantity given NVIDIA's quantity q1:
        q2_BR = max(0, (A - c2 - D*q1) / (2B))
    """
    return max(0.0, (A - c2 - D * q1) / (2 * B))

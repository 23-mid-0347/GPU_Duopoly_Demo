"""
models/bertrand.py
==================
Analytical interior Nash equilibrium for the symmetric linear differentiated-
product Bertrand (price-setting) duopoly.

Direct-demand system (inverted from inverse demand):
    q1(p1,p2) = [(B-D)*A - B*p1 + D*p2] / (B² - D²)
    q2(p1,p2) = [(B-D)*A - B*p2 + D*p1] / (B² - D²)

Define:
    r1 = (B - D)*A + B*c1
    r2 = (B - D)*A + B*c2

Interior equilibrium prices:
    p1* = (2B*r1 + D*r2) / (4B² - D²)
    p2* = (D*r1 + 2B*r2) / (4B² - D²)

Quantities are recovered via direct demand, margins and payoffs calculated
exactly as for Cournot.

Note: this is differentiated Bertrand (products are NOT homogeneous).
     Do NOT use the homogeneous-good shortcut p = MC.

No Streamlit or Plotly dependency is permitted here.
"""

from dataclasses import dataclass
from typing import Optional

from models.demand import validate_params, direct_demand, DemandParamError


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class BertrandResult:
    """
    All equilibrium outputs for the differentiated Bertrand game.

    status : "ok" | "infeasible" | "error"
    message : human-readable explanation when status != "ok"
    """
    status: str = "ok"
    message: str = ""
    # prices
    p1: Optional[float] = None
    p2: Optional[float] = None
    # quantities (recovered via direct demand)
    q1: Optional[float] = None
    q2: Optional[float] = None
    # per-unit margins
    m1: Optional[float] = None
    m2: Optional[float] = None
    # model payoffs
    pi1: Optional[float] = None
    pi2: Optional[float] = None
    # stored inputs
    A: Optional[float] = None
    B: Optional[float] = None
    D: Optional[float] = None
    c1: Optional[float] = None
    c2: Optional[float] = None


# ---------------------------------------------------------------------------
# Main solver
# ---------------------------------------------------------------------------

def solve_bertrand(A: float, B: float, D: float,
                   c1: float, c2: float) -> BertrandResult:
    """
    Solve the symmetric linear differentiated Bertrand game and return a
    BertrandResult.

    Parameters
    ----------
    A  : float  — inverse-demand intercept
    B  : float  — own-quantity slope (> 0)
    D  : float  — cross-quantity term (0 <= D < B)
    c1 : float  — NVIDIA marginal cost input (illustrative)
    c2 : float  — AMD   marginal cost input (illustrative)
    """
    base = BertrandResult(A=A, B=B, D=D, c1=c1, c2=c2)

    # --- parameter validation ---
    try:
        validate_params(A, B, D)
    except DemandParamError as exc:
        base.status = "error"
        base.message = str(exc)
        return base

    # --- common denominator (shared with Cournot) ---
    denom = 4 * B ** 2 - D ** 2   # positive when 0 <= D < B (guaranteed above)

    if denom <= 0:
        base.status = "error"
        base.message = (
            f"Denominator 4B² - D² = {denom:.6g} is non-positive. "
            "Check that B > 0 and D < B."
        )
        return base

    # --- auxiliary r terms ---
    r1 = (B - D) * A + B * c1
    r2 = (B - D) * A + B * c2

    # --- equilibrium prices ---
    p1 = (2 * B * r1 + D * r2) / denom
    p2 = (D * r1 + 2 * B * r2) / denom

    # --- recover quantities via direct demand ---
    q1, q2 = direct_demand(A, B, D, p1, p2)

    # --- feasibility ---
    if q1 < 0 or q2 < 0:
        base.status = "infeasible"
        base.message = (
            f"Bertrand-recovered quantities are negative (q1={q1:.4f}, q2={q2:.4f}). "
            "The interior price solution does not yield a valid equilibrium under "
            "these parameters. Adjust A, B, D, c1, or c2."
        )
        base.p1 = p1
        base.p2 = p2
        base.q1 = q1
        base.q2 = q2
        return base

    # --- margins and payoffs ---
    m1 = p1 - c1
    m2 = p2 - c2
    pi1 = m1 * q1
    pi2 = m2 * q2

    return BertrandResult(
        status="ok",
        message="",
        p1=p1, p2=p2,
        q1=q1, q2=q2,
        m1=m1, m2=m2,
        pi1=pi1, pi2=pi2,
        A=A, B=B, D=D, c1=c1, c2=c2,
    )


# ---------------------------------------------------------------------------
# FOC verifier (used in tests)
# ---------------------------------------------------------------------------

def _check_bertrand_foc(result: BertrandResult, tol: float = 1e-6) -> tuple[float, float]:
    """
    Verify the Bertrand FOCs (price best-response conditions) using the
    direct-demand system.

    Each firm's FOC in price space:
        ∂π_i/∂p_i = q_i + (p_i - c_i) * ∂q_i/∂p_i = 0
    where ∂q_i/∂p_i = -B / (B² - D²).

    Residuals r1, r2 should be ~0 at the equilibrium.
    """
    r = result
    B, D = r.B, r.D
    denom_dd = B ** 2 - D ** 2  # direct demand denominator
    dq1_dp1 = -B / denom_dd
    dq2_dp2 = -B / denom_dd

    r1 = r.q1 + (r.p1 - r.c1) * dq1_dp1
    r2 = r.q2 + (r.p2 - r.c2) * dq2_dp2
    return r1, r2

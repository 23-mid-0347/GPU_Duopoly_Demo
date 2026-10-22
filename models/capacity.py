"""
models/capacity.py
==================
Capacity-constrained Cournot scenario.

Treats q1_cap as a MAXIMUM on NVIDIA's output, not a forced production level.

Algorithm:
    1. Solve unconstrained Cournot.
    2. If q1_cap >= q1_unconstrained  → cap is nonbinding; return unconstrained result.
    3. If 0 <= q1_cap < q1_unconstrained → cap binds:
           set q1 = q1_cap,
           compute AMD best response: q2 = max(0, (A - c2 - D*q1) / (2B)),
           recompute prices, margins, payoffs.
    4. Never describe the cap as an observed NVIDIA/TSMC allocation.

No Streamlit or Plotly dependency is permitted here.
"""

from dataclasses import dataclass
from typing import Optional

from models.demand import validate_params, inverse_demand, DemandParamError
from models.cournot import solve_cournot, CournotResult


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class CapacityResult:
    """
    Capacity-constrained Cournot outcome plus binding/nonbinding diagnosis.
    """
    status: str = "ok"
    message: str = ""
    binding: bool = False          # True if the cap actually restricts output
    q1_cap: Optional[float] = None
    q1_unconstrained: Optional[float] = None
    # constrained (or unconstrained) equilibrium values
    q1: Optional[float] = None
    q2: Optional[float] = None
    p1: Optional[float] = None
    p2: Optional[float] = None
    m1: Optional[float] = None
    m2: Optional[float] = None
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

def solve_capacity_cournot(
    A: float, B: float, D: float,
    c1: float, c2: float,
    q1_cap: float,
) -> CapacityResult:
    """
    Solve the hypothetical capacity-constrained Cournot game.

    Parameters
    ----------
    A, B, D, c1, c2 : float  — same as for solve_cournot
    q1_cap          : float  — hypothetical maximum output for NVIDIA;
                               labelled "hypothetical output cap" in the UI.
                               This is NOT claimed to be an observed TSMC
                               allocation.
    """
    base = CapacityResult(A=A, B=B, D=D, c1=c1, c2=c2, q1_cap=q1_cap)

    # --- input validation ---
    try:
        validate_params(A, B, D)
    except DemandParamError as exc:
        base.status = "error"
        base.message = str(exc)
        return base

    if q1_cap < 0:
        base.status = "error"
        base.message = f"q1_cap must be >= 0 (got {q1_cap})."
        return base

    # --- step 1: unconstrained Cournot ---
    uc = solve_cournot(A, B, D, c1, c2)
    if uc.status != "ok":
        base.status = uc.status
        base.message = f"Unconstrained Cournot failed: {uc.message}"
        return base

    base.q1_unconstrained = uc.q1

    # --- step 2: check binding ---
    if q1_cap >= uc.q1:
        # Nonbinding — return exactly the unconstrained equilibrium
        base.binding = False
        base.q1 = uc.q1
        base.q2 = uc.q2
        base.p1 = uc.p1
        base.p2 = uc.p2
        base.m1 = uc.m1
        base.m2 = uc.m2
        base.pi1 = uc.pi1
        base.pi2 = uc.pi2
        base.message = (
            f"Cap ({q1_cap:.4f}) ≥ unconstrained NVIDIA quantity "
            f"({uc.q1:.4f}): cap is nonbinding — unconstrained equilibrium applies."
        )
        return base

    # --- step 3: binding cap ---
    base.binding = True
    q1 = q1_cap
    # AMD's best response to q1_cap
    q2 = max(0.0, (A - c2 - D * q1) / (2 * B))

    # Recompute prices via inverse demand
    p1, p2 = inverse_demand(A, B, D, q1, q2)

    m1 = p1 - c1
    m2 = p2 - c2
    pi1 = m1 * q1
    pi2 = m2 * q2

    base.q1 = q1
    base.q2 = q2
    base.p1 = p1
    base.p2 = p2
    base.m1 = m1
    base.m2 = m2
    base.pi1 = pi1
    base.pi2 = pi2
    base.message = (
        f"Cap ({q1_cap:.4f}) < unconstrained NVIDIA quantity "
        f"({uc.q1:.4f}): cap is binding."
    )
    return base

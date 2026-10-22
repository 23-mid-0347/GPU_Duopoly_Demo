"""
models/demand.py
================
Shared inverse-demand and direct-demand functions for the symmetric
linear differentiated-product duopoly:

    p1 = A - B*q1 - D*q2
    p2 = A - B*q2 - D*q1

Direct-demand system (inverse of the above):

    q1(p1,p2) = [(B-D)*A - B*p1 + D*p2] / (B² - D²)
    q2(p1,p2) = [(B-D)*A - B*p2 + D*p1] / (B² - D²)

Parameters
----------
A : float   — inverse-demand intercept (finite)
B : float   — own-quantity slope; must be > 0
D : float   — cross-quantity term; must satisfy 0 <= D < B
q1, q2      — quantities (model units, illustrative)
p1, p2      — prices    (model price units, illustrative)

No Streamlit, Plotly, or other UI dependency is permitted here.
"""

from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Parameter validation
# ---------------------------------------------------------------------------

class DemandParamError(ValueError):
    """Raised when demand parameters violate admissibility conditions."""


def validate_params(A: float, B: float, D: float) -> None:
    """
    Raise DemandParamError if (A, B, D) violate the shared admissibility
    conditions for the Cournot/Bertrand base model:

        B > 0,  0 <= D < B,  B² - D² > 0.

    A may be any finite float.
    """
    if not (B > 0):
        raise DemandParamError(f"B must be > 0 (got B={B}).")
    if not (D >= 0):
        raise DemandParamError(f"D must be >= 0 (got D={D}).")
    if not (D < B):
        raise DemandParamError(
            f"D must be strictly less than B to keep the demand system non-singular "
            f"(got D={D}, B={B}). Use a D/B slider capped below 1 (e.g. 0.95)."
        )


# ---------------------------------------------------------------------------
# Inverse demand  p_i = A - B*qi - D*qj
# ---------------------------------------------------------------------------

def inverse_demand(A: float, B: float, D: float,
                   q1: float, q2: float) -> tuple[float, float]:
    """
    Return (p1, p2) from the inverse demand system.

    p1 = A - B*q1 - D*q2
    p2 = A - B*q2 - D*q1
    """
    validate_params(A, B, D)
    p1 = A - B * q1 - D * q2
    p2 = A - B * q2 - D * q1
    return p1, p2


# ---------------------------------------------------------------------------
# Direct demand  qi(p1, p2)
# ---------------------------------------------------------------------------

def direct_demand(A: float, B: float, D: float,
                  p1: float, p2: float) -> tuple[float, float]:
    """
    Return (q1, q2) from the direct demand system (inverted from inverse demand).

    q1 = [(B - D)*A - B*p1 + D*p2] / (B² - D²)
    q2 = [(B - D)*A - B*p2 + D*p1] / (B² - D²)

    Raises DemandParamError if B² - D² <= 0 (i.e. D >= B).
    """
    validate_params(A, B, D)
    denom = B ** 2 - D ** 2   # guaranteed > 0 after validate_params
    q1 = ((B - D) * A - B * p1 + D * p2) / denom
    q2 = ((B - D) * A - B * p2 + D * p1) / denom
    return q1, q2


# ---------------------------------------------------------------------------
# D/B ratio helper
# ---------------------------------------------------------------------------

def ratio_to_D(ratio: float, B: float) -> float:
    """
    Convert a slider ratio r = D/B to the raw cross-term D = r * B.

    This is the ONLY correct way to translate the substitutability slider
    into the demand parameter; do NOT store the ratio directly as D.

    Raises DemandParamError if the derived D would violate admissibility.
    """
    if not (0.0 <= ratio < 1.0):
        raise DemandParamError(
            f"Substitutability ratio D/B must be in [0, 1) (got {ratio}). "
            "Cap the slider at 0.95 to avoid the singular boundary."
        )
    return ratio * B

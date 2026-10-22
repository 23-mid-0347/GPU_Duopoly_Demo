"""
models/metrics.py
=================
Output metrics helpers.

Defines:
    - per-unit margin  m_i = p_i - c_i
    - model payoff     pi_i = (p_i - c_i) * q_i
    - MAE / RMSE / bias functions with guards for missing inputs
      (MAE/RMSE compute ONLY when given matching arrays of actual and
       predicted values; they refuse empty or mismatched inputs.)

These functions do NOT invent validation results.
No Streamlit or Plotly dependency is permitted here.
"""

from __future__ import annotations
import math
from typing import Sequence, Optional


# ---------------------------------------------------------------------------
# Elementary metric calculations
# ---------------------------------------------------------------------------

def per_unit_margin(price: float, cost: float) -> float:
    """Per-unit margin m = p - c."""
    return price - cost


def model_payoff(price: float, cost: float, quantity: float) -> float:
    """Model payoff (contribution payoff) π = (p - c) * q."""
    return (price - cost) * quantity


# ---------------------------------------------------------------------------
# Validation-metric helpers with guards
# ---------------------------------------------------------------------------

class MetricsInputError(ValueError):
    """Raised when MAE/RMSE/bias inputs are invalid."""


def _validate_paired(actual: Sequence[float], predicted: Sequence[float]) -> None:
    """
    Raise MetricsInputError if:
      - Either sequence is empty.
      - Sequences have different lengths.
      - Any value is NaN or Inf.
    """
    if len(actual) == 0 or len(predicted) == 0:
        raise MetricsInputError(
            "MAE/RMSE require at least one observation. "
            "Inputs are empty — no validation metric can be calculated."
        )
    if len(actual) != len(predicted):
        raise MetricsInputError(
            f"Length mismatch: actual has {len(actual)} observations, "
            f"predicted has {len(predicted)}. Arrays must match."
        )
    for i, (a, p) in enumerate(zip(actual, predicted)):
        if not math.isfinite(a):
            raise MetricsInputError(f"actual[{i}] = {a} is not a finite number.")
        if not math.isfinite(p):
            raise MetricsInputError(f"predicted[{i}] = {p} is not a finite number.")


def mae(actual: Sequence[float], predicted: Sequence[float]) -> float:
    """
    Mean Absolute Error.

    Raises MetricsInputError if inputs are empty, mismatched, or non-finite.
    This function does NOT invent observations when data are missing.
    """
    _validate_paired(actual, predicted)
    n = len(actual)
    return sum(abs(a - p) for a, p in zip(actual, predicted)) / n


def rmse(actual: Sequence[float], predicted: Sequence[float]) -> float:
    """
    Root Mean Squared Error.

    Raises MetricsInputError if inputs are empty, mismatched, or non-finite.
    """
    _validate_paired(actual, predicted)
    n = len(actual)
    return math.sqrt(sum((a - p) ** 2 for a, p in zip(actual, predicted)) / n)


def bias(actual: Sequence[float], predicted: Sequence[float]) -> float:
    """
    Mean signed error (predicted - actual).

    Raises MetricsInputError if inputs are empty, mismatched, or non-finite.
    """
    _validate_paired(actual, predicted)
    n = len(actual)
    return sum(p - a for a, p in zip(actual, predicted)) / n


# ---------------------------------------------------------------------------
# Data-readiness guard
# ---------------------------------------------------------------------------

def can_compute_validation(actual: Optional[Sequence[float]],
                            predicted: Optional[Sequence[float]]) -> tuple[bool, str]:
    """
    Return (True, "") if validation metrics can be computed, or
    (False, reason_string) if they cannot.

    This is the gating check displayed on the Data & Validation page.
    """
    if actual is None or predicted is None:
        return False, "No compatible observation dataset provided."
    try:
        _validate_paired(actual, predicted)
        return True, ""
    except MetricsInputError as e:
        return False, str(e)

"""
utils/formatting.py
===================
Formatting helpers for prices, quantities, payoffs, margins, and status
messages displayed in the Streamlit app.

These are pure string/formatting functions — no Streamlit or Plotly import.
"""

from __future__ import annotations
from typing import Optional


# ---------------------------------------------------------------------------
# Number formatters
# ---------------------------------------------------------------------------

def fmt_price(value: Optional[float], decimals: int = 2,
              unit: str = "model price units") -> str:
    """Format a price with unit label."""
    if value is None:
        return "N/A"
    return f"{value:,.{decimals}f} {unit}"


def fmt_quantity(value: Optional[float], decimals: int = 2,
                 unit: str = "model units (illustrative)") -> str:
    """Format a quantity with unit label."""
    if value is None:
        return "N/A"
    return f"{value:,.{decimals}f} {unit}"


def fmt_payoff(value: Optional[float], decimals: int = 2) -> str:
    """Format a model payoff (contribution payoff)."""
    if value is None:
        return "N/A"
    return f"{value:,.{decimals}f}"


def fmt_margin(value: Optional[float], decimals: int = 2) -> str:
    """Format a per-unit margin."""
    if value is None:
        return "N/A"
    return f"{value:,.{decimals}f}"


def fmt_ratio(value: Optional[float], decimals: int = 4) -> str:
    """Format D/B ratio."""
    if value is None:
        return "N/A"
    return f"{value:.{decimals}f}"


# ---------------------------------------------------------------------------
# Status / warning message formatters
# ---------------------------------------------------------------------------

def feasibility_warning(status: str, message: str) -> str:
    """
    Format a visible warning string for infeasible or error equilibria.
    """
    if status == "ok":
        return ""
    tag = "⚠️ INFEASIBLE" if status == "infeasible" else "❌ ERROR"
    return f"{tag}: {message}"


def illustrative_note() -> str:
    """Short note to display near parameter inputs."""
    return (
        "All parameter values are **illustrative scenario inputs** — "
        "not empirically calibrated NVIDIA/AMD data."
    )


def msrp_disclaimer() -> str:
    """Disclaimer to show alongside MSRP table."""
    return (
        "**Note:** Launch MSRP is the officially announced suggested retail price "
        "at product introduction. It is **not** a realized transaction price, "
        "average selling price, sales quantity, or model calibration input."
    )


def payoff_disclaimer() -> str:
    """Short disclaimer for model payoff values."""
    return (
        "Model payoff = (price − marginal cost) × quantity. "
        "This is a model contribution payoff, **not** a firm's reported profit."
    )


def quantity_unit_label() -> str:
    """Canonical quantity unit label."""
    return "model units (illustrative)"


def price_unit_label() -> str:
    """Canonical price unit label."""
    return "model price units (illustrative; not calibrated USD forecast)"

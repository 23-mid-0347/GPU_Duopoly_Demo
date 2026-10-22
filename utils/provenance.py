"""
utils/provenance.py
===================
Consistent evidence-status labels and source-link helpers for the UI pages.

Status vocabulary follows BUILD_PLAN.md §10.3.
"""

from __future__ import annotations
from typing import Optional

# ---------------------------------------------------------------------------
# Status label constants
# ---------------------------------------------------------------------------

OFFICIALLY_REPORTED = "officially reported"
MARKET_RESEARCH     = "market-research source"
ESTIMATED           = "estimated from data"
DERIVED             = "derived"
SCENARIO_INPUT      = "scenario input"
PLACEHOLDER         = "placeholder"
MISSING             = "missing / not available"


# ---------------------------------------------------------------------------
# Badge renderer (returns a Markdown/HTML snippet for Streamlit)
# ---------------------------------------------------------------------------

STATUS_COLORS = {
    OFFICIALLY_REPORTED : "#3fa142",  # green
    MARKET_RESEARCH     : "#5b87c5",  # blue
    ESTIMATED           : "#8b72c9",  # purple
    DERIVED             : "#b09030",  # gold-ish
    SCENARIO_INPUT      : "#d4883a",  # orange
    PLACEHOLDER         : "#888888",  # grey
    MISSING             : "#c04040",  # red
}


def status_badge(status: str) -> str:
    """
    Return an HTML <span> badge for the given evidence status.
    Suitable for st.markdown(..., unsafe_allow_html=True).
    """
    color = STATUS_COLORS.get(status, "#888888")
    return (
        f'<span style="background:{color};color:#fff;padding:2px 8px;'
        f'border-radius:4px;font-size:0.75em;font-weight:600;'
        f'letter-spacing:0.05em">{status.upper()}</span>'
    )


def source_link(url: str, label: Optional[str] = None) -> str:
    """
    Return a Markdown link that opens in a new tab.
    If url is empty/None, returns '(source not available)'.
    """
    if not url:
        return "(source not available)"
    text = label or url
    return f"[{text}]({url}){{target='_blank'}}"


# ---------------------------------------------------------------------------
# Calibration gate
# ---------------------------------------------------------------------------

def is_calibrated() -> bool:
    """
    Version 1 is always illustrative — returns False.
    This function is a placeholder for a future calibration-gate check.
    """
    return False


def get_mode_banner() -> str:
    """
    Return the global status banner text for the top of every page.
    """
    if is_calibrated():
        return (
            "⚙️  CALIBRATED MODE — show data version, estimation status, "
            "units and sample coverage"
        )
    return (
        "⚠️  ILLUSTRATIVE MODE — parameters are scenario inputs; "
        "not empirically calibrated"
    )

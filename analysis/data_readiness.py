"""
analysis/data_readiness.py
==========================
Checks whether available data support specific analyses.

Rules:
  - MSRP-only data are descriptive; they do NOT unlock empirical validation.
  - An empirical validation metric (MAE/RMSE) requires matched price/quantity
    observations tied to a documented model version.
  - Missing fields are reported honestly, not filled with placeholders.

No Streamlit or Plotly dependency is permitted here.
"""

from __future__ import annotations
import pandas as pd
from typing import Dict, Any, List


# ---------------------------------------------------------------------------
# Required column schema for a calibration-eligible dataset
# ---------------------------------------------------------------------------

CALIBRATION_REQUIRED_COLUMNS = [
    "firm",
    "sku",
    "period",
    "price_usd",
    "quantity_units",
    "rival_price_usd",
    "source_url",
]

DESCRIPTIVE_MSRP_COLUMNS = [
    "firm",
    "product_name",
    "launch_msrp_usd",
    "source_url",
    "source_status",
]


# ---------------------------------------------------------------------------
# Status vocabulary (from BUILD_PLAN.md §10.3)
# ---------------------------------------------------------------------------

STATUS_VOCAB = {
    "officially_reported": "officially reported",
    "market_research": "market-research source",
    "estimated": "estimated from data",
    "derived": "derived",
    "scenario_input": "scenario input",
    "placeholder": "placeholder",
    "missing": "missing / not available",
}


# ---------------------------------------------------------------------------
# Readiness check functions
# ---------------------------------------------------------------------------

def check_msrp_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Check an MSRP-only DataFrame for completeness and correctness.

    Returns a dict with:
        present_columns    : list of columns found
        missing_columns    : required descriptive columns not found
        row_count          : int
        has_quantity_data  : bool  (should be False for MSRP-only data)
        supports_calibration : bool  (always False for MSRP-only data)
        supports_validation  : bool  (always False for MSRP-only data)
        validation_status    : str
        notes              : list[str]
    """
    present = [c for c in DESCRIPTIVE_MSRP_COLUMNS if c in df.columns]
    missing = [c for c in DESCRIPTIVE_MSRP_COLUMNS if c not in df.columns]
    has_qty = "quantity_units" in df.columns and df["quantity_units"].notna().any()

    notes: List[str] = []
    if has_qty:
        notes.append("WARNING: Quantity column detected but not verified as "
                     "compatible product-level data.")
    else:
        notes.append(
            "No product-level quantity data present. "
            "MSRP is a descriptive observation only."
        )

    notes.append(
        "These data support a descriptive MSRP reference table only. "
        "They do NOT support structural demand estimation or empirical "
        "model validation (MAE/RMSE winner badges)."
    )

    return {
        "present_columns": present,
        "missing_columns": missing,
        "row_count": len(df),
        "has_quantity_data": has_qty,
        "supports_calibration": False,
        "supports_validation": False,
        "validation_status": (
            "Not calibrated — no evidence-backed MAE/model winner is available. "
            "Compatible price/quantity observations and a documented estimation "
            "process are required before any validation metric can be reported."
        ),
        "notes": notes,
    }


def check_calibration_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Check a candidate calibration DataFrame against the full schema.

    Returns readiness status for each required field.
    Even if all columns are present, this function does NOT perform
    calibration itself — it only checks readiness.
    """
    present = [c for c in CALIBRATION_REQUIRED_COLUMNS if c in df.columns]
    missing = [c for c in CALIBRATION_REQUIRED_COLUMNS if c not in df.columns]

    all_present = len(missing) == 0
    has_data = len(df) > 0

    notes: List[str] = []
    if missing:
        notes.append(f"Missing required columns: {missing}")
    if not has_data:
        notes.append("Dataset is empty.")
    if all_present and has_data:
        qty_missing = df["quantity_units"].isna().sum()
        price_missing = df["price_usd"].isna().sum()
        if qty_missing > 0:
            notes.append(
                f"{qty_missing} rows missing quantity_units — "
                "quantity observations are required for demand estimation."
            )
        if price_missing > 0:
            notes.append(f"{price_missing} rows missing price_usd.")

    calibration_ready = all_present and has_data and not missing
    return {
        "present_columns": present,
        "missing_columns": missing,
        "row_count": len(df),
        "calibration_ready": calibration_ready,
        "validation_status": (
            "Calibration-ready dataset present — proceed to documented "
            "estimation phase."
            if calibration_ready
            else "Not calibration-ready — see missing_columns and notes."
        ),
        "notes": notes,
    }


def get_overall_validation_status(msrp_df: pd.DataFrame,
                                   calibration_df: pd.DataFrame | None = None
                                   ) -> str:
    """
    Return a one-line status string for the data/validation page banner.
    """
    if calibration_df is not None and len(calibration_df) > 0:
        cal = check_calibration_dataset(calibration_df)
        if cal["calibration_ready"]:
            return (
                "Calibration dataset present and schema-valid. "
                "Proceed to estimation phase (not yet completed)."
            )

    return (
        "ILLUSTRATIVE MODE — parameters are scenario inputs; "
        "not empirically calibrated. "
        "Only official launch MSRP data are available (descriptive only)."
    )

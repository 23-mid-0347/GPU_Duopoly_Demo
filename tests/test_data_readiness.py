"""
tests/test_data_readiness.py
============================
Unit tests for analysis/data_readiness.py.

Verifies that MSRP-only data are correctly flagged as non-calibrating and
that missing required columns are reported honestly.
"""

import pytest
import pandas as pd
from analysis.data_readiness import (
    check_msrp_dataset,
    check_calibration_dataset,
    get_overall_validation_status,
    CALIBRATION_REQUIRED_COLUMNS,
    DESCRIPTIVE_MSRP_COLUMNS,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def minimal_msrp_df():
    return pd.DataFrame({
        "firm": ["NVIDIA", "AMD"],
        "product_name": ["RTX 4080", "RX 7900 XTX"],
        "launch_msrp_usd": [1199, 999],
        "source_url": ["http://example.com/a", "http://example.com/b"],
        "source_status": ["officially reported", "officially reported"],
    })


def minimal_calibration_df():
    return pd.DataFrame({
        "firm": ["NVIDIA"],
        "sku": ["RTX 4070"],
        "period": ["2023Q2"],
        "price_usd": [599.0],
        "quantity_units": [1_000_000.0],
        "rival_price_usd": [499.0],
        "source_url": ["http://example.com"],
    })


# ---------------------------------------------------------------------------
# MSRP dataset checks
# ---------------------------------------------------------------------------

class TestMSRPDataset:
    def test_msrp_does_not_support_calibration(self):
        result = check_msrp_dataset(minimal_msrp_df())
        assert result["supports_calibration"] is False

    def test_msrp_does_not_support_validation(self):
        result = check_msrp_dataset(minimal_msrp_df())
        assert result["supports_validation"] is False

    def test_msrp_has_no_quantity_data(self):
        result = check_msrp_dataset(minimal_msrp_df())
        assert result["has_quantity_data"] is False

    def test_validation_status_says_not_calibrated(self):
        result = check_msrp_dataset(minimal_msrp_df())
        assert "not calibrated" in result["validation_status"].lower()

    def test_row_count_correct(self):
        result = check_msrp_dataset(minimal_msrp_df())
        assert result["row_count"] == 2

    def test_msrp_notes_mention_descriptive(self):
        result = check_msrp_dataset(minimal_msrp_df())
        full_notes = " ".join(result["notes"]).lower()
        assert "descriptive" in full_notes


# ---------------------------------------------------------------------------
# Calibration dataset checks
# ---------------------------------------------------------------------------

class TestCalibrationDataset:
    def test_full_schema_ready(self):
        result = check_calibration_dataset(minimal_calibration_df())
        assert result["calibration_ready"] is True

    def test_missing_column_not_ready(self):
        df = minimal_calibration_df().drop(columns=["quantity_units"])
        result = check_calibration_dataset(df)
        assert result["calibration_ready"] is False
        assert "quantity_units" in result["missing_columns"]

    def test_empty_df_not_ready(self):
        df = pd.DataFrame(columns=CALIBRATION_REQUIRED_COLUMNS)
        result = check_calibration_dataset(df)
        assert result["calibration_ready"] is False

    def test_multiple_missing_columns(self):
        df = pd.DataFrame({"firm": ["NVIDIA"]})
        result = check_calibration_dataset(df)
        assert len(result["missing_columns"]) > 0


# ---------------------------------------------------------------------------
# Overall validation status
# ---------------------------------------------------------------------------

class TestOverallStatus:
    def test_msrp_only_is_illustrative(self):
        status = get_overall_validation_status(minimal_msrp_df(), calibration_df=None)
        assert "illustrative" in status.lower()

    def test_msrp_only_not_calibrated(self):
        status = get_overall_validation_status(minimal_msrp_df(), calibration_df=None)
        assert "not empirically calibrated" in status.lower()

    def test_empty_calibration_df_stays_illustrative(self):
        empty = pd.DataFrame(columns=CALIBRATION_REQUIRED_COLUMNS)
        status = get_overall_validation_status(minimal_msrp_df(), calibration_df=empty)
        assert "illustrative" in status.lower()

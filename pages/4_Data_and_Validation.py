"""
pages/4_Data_and_Validation.py
===============================
Sourced launch MSRPs, data-readiness checks, and honest validation status.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from analysis.data_readiness import (
    check_msrp_dataset, get_overall_validation_status,
    DESCRIPTIVE_MSRP_COLUMNS, CALIBRATION_REQUIRED_COLUMNS,
)
from utils.provenance import status_badge
from utils.formatting import msrp_disclaimer

st.set_page_config(page_title="Data & Validation — GPU Duopoly", layout="wide", page_icon="📁")



ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

st.title("📁 Data Sources, Provenance & Validation Status")
st.markdown("""
This page shows **what empirical data are available**, what analyses they support,
and what is explicitly **missing**. No validation metric is fabricated from placeholder data.
""")

# ---------------------------------------------------------------------------
# Load MSRP CSV
# ---------------------------------------------------------------------------
csv_path = os.path.join(ROOT, "data", "gpu_launch_prices.csv")
msrp_df = pd.read_csv(csv_path)
readiness = check_msrp_dataset(msrp_df)
status_str = get_overall_validation_status(msrp_df)

# ---------------------------------------------------------------------------
# Overall status banner
# ---------------------------------------------------------------------------
st.subheader("📊 Overall Calibration / Validation Status")
st.markdown(f"""
<div style="background:#14161a;border:2px solid #c04040;border-radius:8px;
padding:18px 22px;color:#e07070;font-size:1.05em;font-weight:600;">
❌ NOT CALIBRATED<br>
<span style="font-weight:400;font-size:0.92em;">{readiness['validation_status']}</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
**What would be required for empirical calibration:**
1. Compatible price/quantity observations (SKU-level, matched by period and firm)
2. A documented demand specification and identification strategy
3. An estimation method addressing price endogeneity
4. Feasibility checks for estimated parameter region
5. A validation holdout sample or appropriate baseline

None of these are currently available in this dataset. See `data/data_dictionary.md` for the full schema.
""")

st.divider()

# ---------------------------------------------------------------------------
# Official launch MSRP table
# ---------------------------------------------------------------------------
st.header("📋 Official Launch MSRP Reference")
st.markdown(msrp_disclaimer())
st.caption(
    "Source: Official NVIDIA and AMD press releases and IR announcements. "
    "These are **announced launch prices** — not realized transaction prices, "
    "ASPs, or model calibration inputs."
)

# Display the full table with source links as Markdown
for _, row in msrp_df.iterrows():
    pass  # just checking columns are accessible

display_cols = ["firm", "product_name", "sku_configuration", "launch_msrp_usd",
                "price_type", "source_name", "source_date", "source_status", "notes"]
disp_df = msrp_df[[c for c in display_cols if c in msrp_df.columns]].copy()
disp_df.columns = [c.replace("_", " ").title() for c in disp_df.columns]
st.dataframe(disp_df, use_container_width=True, hide_index=True)

# Source links as clickable Markdown
st.subheader("🔗 Source URLs")
for _, row in msrp_df.iterrows():
    st.markdown(
        f"- **{row['firm']} {row['product_name']}** "
        f"({row.get('sku_configuration', '')} — ${row['launch_msrp_usd']:,.0f}): "
        f"[{row['source_name']}]({row['source_url']})"
    )

# MSRP bar chart (descriptive only, clearly labelled)
st.subheader("📊 Launch MSRP by SKU (Descriptive — Official Announcements Only)")
nvidia_rows = msrp_df[msrp_df["firm"] == "NVIDIA"].copy()
amd_rows    = msrp_df[msrp_df["firm"] == "AMD"].copy()

fig = go.Figure()
fig.add_trace(go.Bar(
    name="NVIDIA (announced MSRP)",
    x=nvidia_rows["product_name"] + " " + nvidia_rows["sku_configuration"].fillna(""),
    y=nvidia_rows["launch_msrp_usd"],
    marker_color="#c8a84b",
    text=["$" + str(int(v)) for v in nvidia_rows["launch_msrp_usd"]],
    textposition="outside",
))
fig.add_trace(go.Bar(
    name="AMD (announced MSRP)",
    x=amd_rows["product_name"] + " " + amd_rows["sku_configuration"].fillna(""),
    y=amd_rows["launch_msrp_usd"],
    marker_color="#4ec9b0",
    text=["$" + str(int(v)) for v in amd_rows["launch_msrp_usd"]],
    textposition="outside",
))
fig.update_layout(
    title="Official GPU Launch MSRP (USD) — Descriptive Reference Only",
    xaxis_title="SKU",
    yaxis_title="Announced launch MSRP (USD)",
    barmode="group",
    paper_bgcolor="#1a1c20",
    plot_bgcolor="#22252d",
    font=dict(color="#e6e0d4"),
    height=420,
    xaxis_tickangle=-30,
    annotations=[dict(
        text="⚠️ This chart shows announced launch MSRP only. Not realized prices, ASPs, or quantities.",
        xref="paper", yref="paper", x=0.01, y=-0.32,
        font=dict(size=11, color="#888"), showarrow=False,
    )],
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
> **Important distinction:** The MSRP values above are **separately displayed** from the
> equilibrium model outputs. The model operates with illustrative parameters that are
> *not* calibrated to these prices. Do not compare MSRP values directly with model outputs.
""")

st.divider()

# ---------------------------------------------------------------------------
# Data-readiness checks
# ---------------------------------------------------------------------------
st.header("🔍 Data-Readiness Check Results")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Current dataset: GPU Launch Prices CSV")
    st.markdown(f"**Rows:** {readiness['row_count']}")
    st.markdown(f"**Supports calibration:** {'✅' if readiness['supports_calibration'] else '❌ No'}")
    st.markdown(f"**Supports validation (MAE/RMSE):** {'✅' if readiness['supports_validation'] else '❌ No'}")
    st.markdown(f"**Has quantity data:** {'✅ Yes' if readiness['has_quantity_data'] else '❌ No'}")

    for note in readiness["notes"]:
        st.markdown(f"> {note}")

with col_b:
    st.subheader("Required columns for calibration")
    st.markdown("The following columns are required for structural demand estimation:")
    for col in CALIBRATION_REQUIRED_COLUMNS:
        present = col in msrp_df.columns
        icon = "✅" if present else "❌"
        st.markdown(f"- {icon} `{col}`")
    st.caption("Source: data/data_dictionary.md")

st.divider()

# ---------------------------------------------------------------------------
# What is missing
# ---------------------------------------------------------------------------
st.header("❌ What Empirical Data Are Missing")
st.markdown("""
The following types of data are required for any empirical demand estimation or model
validation. They are **not** currently available in this project.

| Data Type | Status | Why Needed |
|---|---|---|
| SKU-level quantity / unit sales | ❌ Missing | Required for demand equation estimation |
| Realized transaction prices (ASP) | ❌ Missing | MSRP ≠ transaction price |
| Matched rival price observations | ❌ Missing | Required for cross-price coefficient |
| Marginal cost proxies with provenance | ❌ Missing | Required for profit/payoff calibration |
| Panel data across periods | ❌ Missing | Needed for identification via variation |
| Performance quality index | ❌ Missing | For hedonic demand control (optional) |

**Sources that could potentially provide some of this data (but access or coverage is uncertain):**
- Jon Peddie Research AIB quarterly reports (paid; cover AIB shipments by firm)
- NVIDIA and AMD 10-K/10-Q gaming segment revenue + ASP derivation (not SKU-level)
- PCPartPicker or Camelcamelcamel historical street price data (not MSRPs)
- SemiAnalysis-style die-cost proxies (not true marginal costs; assumptions must be stated)

**Until this data is obtained and verified, the validation status remains:**
""")
st.error("**Not calibrated — no evidence-backed MAE/model winner is available.**")

st.divider()

# ---------------------------------------------------------------------------
# MAE method reference (not applied)
# ---------------------------------------------------------------------------
with st.expander("📖 MAE / RMSE method reference (not currently applicable)"):
    st.markdown("""
When a compatible matched dataset becomes available, validation metrics can be calculated as:

**Mean Absolute Error (MAE):**

$$\\text{MAE} = \\frac{1}{n} \\sum_{i=1}^{n} |p_i^{\\text{actual}} - p_i^{\\text{predicted}}|$$

**Root Mean Squared Error (RMSE):**

$$\\text{RMSE} = \\sqrt{\\frac{1}{n} \\sum_{i=1}^{n} (p_i^{\\text{actual}} - p_i^{\\text{predicted}})^2}$$

These metrics require:
- A **matched** panel of actual observations and model predictions (same period, same SKU)
- A **documented model version** generating the predictions
- A **separate validation sample** (not used in parameter estimation)
- Clear specification of whether prices are MSRPs, ASPs, or transaction prices

**Not computed here because there are no matched observations.**
""")

# ---------------------------------------------------------------------------
# Evidence status vocabulary
# ---------------------------------------------------------------------------
with st.expander("🏷️ Evidence status vocabulary"):
    st.markdown("""
| Status | Meaning |
|---|---|
| `officially reported` | From an official press release or product announcement |
| `market-research source` | From a paid market-research report (e.g. JPR) |
| `estimated from data` | Derived via a documented method from other observations |
| `derived` | Calculated from other values in this or another dataset |
| `scenario input` | User-specified scenario parameter, not measured |
| `placeholder` | Synthetic value; must be replaced before empirical claims |
| `missing / not available` | Required field not yet sourced |
""")
    st.markdown("""
All baseline model parameters (`A`, `B`, `D/B`, `c₁`, `c₂`) are **placeholder** /
**scenario input** — they are not empirically estimated from NVIDIA/AMD data.
""")

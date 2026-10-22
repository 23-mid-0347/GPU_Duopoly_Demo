"""
app.py — Main landing page for the GPU Duopoly Simulator (Streamlit entry point).
"""

import streamlit as st
import json
import os
import sys

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="NVIDIA vs. AMD: GPU Duopoly Simulator",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Ensure project root is on the path (so subpages can import models/)
# ---------------------------------------------------------------------------
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ---------------------------------------------------------------------------
# Load defaults
# ---------------------------------------------------------------------------
DEFAULTS_PATH = os.path.join(ROOT, "data", "illustrative_defaults.json")
with open(DEFAULTS_PATH, "r") as f:
    DEFAULTS = json.load(f)

# ---------------------------------------------------------------------------
# Shared CSS — dark academic theme (charcoal / warm-gold / teal)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
/* ── Global ── */
body, .stApp {
    background-color: #1a1c20;
    color: #e6e0d4;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #14161a;
    border-right: 1px solid #2e3038;
}
[data-testid="stSidebar"] * { color: #c9c3b8 !important; }

/* ── Status banner ── */
.status-banner {
    background: #2a1a00;
    border: 1px solid #c8a84b;
    border-radius: 6px;
    padding: 10px 18px;
    margin-bottom: 22px;
    color: #c8a84b;
    font-weight: 600;
    font-size: 0.93em;
    letter-spacing: 0.03em;
}

/* ── Section headers ── */
h1 { color: #c8a84b; font-weight: 700; }
h2 { color: #e6e0d4; font-weight: 600; }
h3 { color: #4ec9b0; }

/* ── KPI cards ── */
.kpi-card {
    background: #22252d;
    border: 1px solid #2e3038;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 10px;
}
.kpi-label  { font-size: 0.78em; color: #888; text-transform: uppercase; letter-spacing: 0.08em; }
.kpi-value  { font-size: 1.55em; font-weight: 700; color: #c8a84b; margin-top: 4px; }
.kpi-sub    { font-size: 0.8em; color: #666; margin-top: 2px; }

/* ── Metric table ── */
[data-testid="stDataFrame"] { border: 1px solid #2e3038; border-radius: 6px; }

/* ── Warning / info boxes ── */
.warn-box {
    background: #2d1a1a;
    border: 1px solid #c04040;
    border-radius: 6px;
    padding: 10px 16px;
    color: #e07070;
    margin: 10px 0;
}
.info-box {
    background: #1a2035;
    border: 1px solid #3a5888;
    border-radius: 6px;
    padding: 10px 16px;
    color: #a0b8d8;
    margin: 10px 0;
}

/* ── Tabs ── */
[data-testid="stTabs"] { border-bottom: 2px solid #2e3038; }

/* ── Dividers ── */
hr { border-color: #2e3038; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Global status banner helper (imported by all pages)
# ---------------------------------------------------------------------------
def show_status_banner():
    st.markdown(
        '<div class="status-banner">⚠️  ILLUSTRATIVE MODE — '
        'parameters are scenario inputs; not empirically calibrated</div>',
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Page content
# ---------------------------------------------------------------------------
show_status_banner()

st.title("🎮 NVIDIA vs. AMD: Cournot and Differentiated Bertrand Competition")

st.markdown("""
> **Research Question:** How do the predicted equilibrium price, quantity, and profit outcomes
> for NVIDIA and AMD differ under Cournot quantity competition and differentiated Bertrand
> price competition, and how do demand substitutability, cost asymmetry, and a binding output
> cap change those outcomes?

This is an **interactive game-theory teaching simulator** — not an empirically calibrated
market model. All parameter values are illustrative scenario inputs. See the Data & Validation
page for what empirical data would be required before any calibration claims could be made.
""")

# ---------------------------------------------------------------------------
# Three columns: What the app can / cannot do
# ---------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ What this app does")
    st.markdown("""
- Computes **Cournot** and **differentiated Bertrand** Nash equilibria  
  from closed-form analytical formulas
- Lets you adjust demand parameters (`A`, `B`, `D/B`) and cost inputs  
  (`c₁`, `c₂`) and see all outcomes update live
- Explains **why** the two games predict different outcomes  
  (quantity vs. price competition; D/B substitutability effect)
- Shows a **hypothetical capacity-constrained Cournot** scenario  
  (NVIDIA output cap — labelled hypothetical, not as TSMC allocation)
- Displays a sensitivity sweep over D/B values
- Shows a **source-backed MSRP reference table** (descriptive only)
- Reports **data-readiness status** honestly
    """)

with col2:
    st.subheader("❌ What this app cannot do")
    st.markdown("""
- Predict actual GPU market prices, shipments, or profits
- Call itself an empirically calibrated model  
  (no compatible price/quantity dataset has been estimated)
- Use MSRP data as quantity observations or as model calibration
- Report a valid MAE/RMSE winner between Cournot and Bertrand  
  (no matched panel data)
- Represent the full discrete GPU market  
  (only NVIDIA and AMD are modelled; Intel Arc and others are excluded)
- Claim that illustrative `c₁`, `c₂` values are true marginal costs
    """)

st.divider()

# ---------------------------------------------------------------------------
# Three model scenarios
# ---------------------------------------------------------------------------
st.subheader("📐 Three modelled scenarios")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
**1 · Cournot Quantity Competition**  
Both firms simultaneously choose output quantities.  
Equilibrium: each firm's quantity is its best response to the rival's quantity.  
*Closed-form interior solution.*
""")
with c2:
    st.markdown("""
**2 · Differentiated Bertrand Price Competition**  
Both firms simultaneously choose prices.  
Products are differentiated (not homogeneous), so the equilibrium  
is NOT p = MC.  
*Closed-form interior solution via direct demand inversion.*
""")
with c3:
    st.markdown("""
**3 · Capacity-Constrained Cournot (hypothetical)**  
NVIDIA faces a hypothetical output cap; AMD best-responds via its  
Cournot reaction function. Cap is nonbinding if it exceeds the  
unconstrained equilibrium quantity.  
*Labelled "hypothetical" throughout — not an observed TSMC allocation.*
""")

st.divider()

# ---------------------------------------------------------------------------
# Default illustrative parameters
# ---------------------------------------------------------------------------
st.subheader("📋 Default illustrative parameters")
st.caption(
    "These scenario inputs are inherited from the React prototype. "
    "They are **not** measured NVIDIA/AMD data. "
    "Status: **placeholder**"
)

defaults_display = {
    "Parameter": ["A (demand intercept)", "B (own-qty slope)", "D/B (substitutability ratio)",
                   "D (cross-qty term)", "c₁ NVIDIA cost", "c₂ AMD cost", "NVIDIA output cap"],
    "Value": [
        DEFAULTS["A"], DEFAULTS["B"],
        DEFAULTS["substitutability_ratio_D_over_B"],
        round(DEFAULTS["substitutability_ratio_D_over_B"] * DEFAULTS["B"], 4),
        DEFAULTS["c1_nvidia"], DEFAULTS["c2_amd"],
        DEFAULTS["nvidia_output_cap"],
    ],
    "Unit": [
        "model price units", "model price units / model unit",
        "dimensionless [0, 0.95)", "model price units / model unit",
        "model price units", "model price units", "model units (illustrative)",
    ],
    "Status": ["placeholder"] * 7,
}

import pandas as pd
st.dataframe(pd.DataFrame(defaults_display), use_container_width=True, hide_index=True)

st.divider()

# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------
st.subheader("🗺️ How to navigate")
st.markdown("""
Use the **sidebar pages** (expand the sidebar if collapsed):

| Page | What to do |
|---|---|
| **1 · Model & Equations** | Read the demand system, FOCs, and notation |
| **2 · Live Equilibrium** | Adjust sliders; compare Cournot vs. Bertrand outcomes |
| **3 · Capacity & Scenarios** | Explore the hypothetical NVIDIA output cap |
| **4 · Data & Validation** | View sourced MSRP table and calibration-readiness status |
| **5 · Demo Guide** | Presenter script and instructor Q&A |

**For a quick 5-minute demo:** start on page 2, change D/B from 0 → 0.5 → 0.9,  
then switch to page 3 and move the cap slider.
""")

st.divider()

# ---------------------------------------------------------------------------
# Research scope disclaimer
# ---------------------------------------------------------------------------
st.subheader("⚠️ Scope and limitations")
st.markdown("""
- This is a **two-firm** stylised model. Intel Arc, Qualcomm, and other GPU suppliers are **not** modelled.
- Model payoffs equal *(price − cost input) × quantity* in **model units** — they are  
  **not** NVIDIA's or AMD's reported profits or segment revenue.
- Per-unit margin is `p_i − c_i` in model price units — not a percentage margin.
- The capacity cap is **hypothetical** — it is not an observed wafer allocation or TSMC limit.
- Official launch MSRPs are sourced descriptive observations. They are not transaction prices,  
  ASPs, or quantity data, and they do not calibrate the demand model.
- All comparative statics are **model counterfactuals** — not causal evidence about actual  
  GPU market dynamics.
""")

# ---------------------------------------------------------------------------
# References footer
# ---------------------------------------------------------------------------
with st.expander("📚 Key references"):
    st.markdown("""
**GPU launch MSRPs (official announcements — descriptive only):**
- NVIDIA RTX 40/50 Series: [NVIDIA IR Press Releases](https://investor.nvidia.com/)
- AMD RX 7000/9000 Series: [AMD IR Press Releases](https://ir.amd.com/)

**Market context:**
- Jon Peddie Research AIB Shipments: [JPR Report](https://www.jonpeddie.com/news/q126-pc-graphics-add-in-board-shipments-decreased-0-6-from-last-quarter-to-12-million-units-with-a-cagr-to-2029-of-3-3/)
- NVIDIA FY2026 10-K (Gaming segment): [SEC](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)
- AMD FY2025 10-K (Client & Gaming): [SEC](https://www.sec.gov/Archives/edgar/data/2488/000000248826000021/amd-20251227.htm)

**Demand-model methodology:**
- Berry & Haile (2016), "Identification in Differentiated Products Markets": [Annual Review of Economics](https://www.annualreviews.org/doi/10.1146/annurev-economics-080315-015050)
- Choné & Linnemer (2020), "Linear demand systems for differentiated goods": [IJIO](https://doi.org/10.1016/j.ijindorg.2020.102663)
""")

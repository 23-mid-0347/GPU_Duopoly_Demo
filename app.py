"""
app.py — Main landing page for the GPU Duopoly Simulator (Streamlit entry point).
"""

import streamlit as st
import json
import os
import sys
import pandas as pd

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="NVIDIA vs. AMD: GPU Duopoly Simulator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Ensure project root is on the path
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
# Global CSS — pure black, premium dark theme
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Root reset ── */
html, body, .stApp, [data-testid="stAppViewContainer"] {
    background-color: #000000 !important;
    color: #e8e2d9;
    font-family: 'Inter', sans-serif;
}

/* ── Main content area ── */
[data-testid="stMain"] { background-color: #000000 !important; }
section[data-testid="stSidebar"] { background-color: #0a0a0a !important; border-right: 1px solid #1c1c22 !important; }
section[data-testid="stSidebar"] * { color: #c9c3b8 !important; }

/* ── Block containers ── */
.block-container { padding-top: 2rem; padding-bottom: 3rem; }

/* ── Headings ── */
h1 { font-family: 'Space Grotesk', sans-serif; color: #c8a84b; font-weight: 700; letter-spacing: -0.02em; }
h2 { font-family: 'Space Grotesk', sans-serif; color: #e8e2d9; font-weight: 600; }
h3 { color: #4ec9b0; font-weight: 600; }
h4 { color: #c8a84b; font-weight: 500; }

/* ── Hero gradient title ── */
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 800;
    background: linear-gradient(135deg, #c8a84b 0%, #e8d48b 40%, #4ec9b0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin-bottom: 0.3rem;
}
.hero-sub {
    font-family: 'Inter', sans-serif;
    font-size: 1.05rem;
    color: #888;
    font-weight: 400;
    margin-bottom: 2rem;
    letter-spacing: 0.01em;
}

/* ── Scenario cards ── */
.scenario-card {
    background: #0e0e12;
    border: 1px solid #1e1e28;
    border-radius: 12px;
    padding: 22px 24px;
    height: 100%;
    transition: border-color 0.2s;
}
.scenario-card:hover { border-color: #c8a84b55; }
.scenario-card .tag {
    font-size: 0.7em;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4ec9b0;
    margin-bottom: 8px;
}
.scenario-card h4 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: #e8e2d9;
    margin: 0 0 10px 0;
}
.scenario-card p { font-size: 0.88rem; color: #888; line-height: 1.6; margin: 0; }

/* ── Stat pills ── */
.stat-row { display: flex; gap: 12px; flex-wrap: wrap; margin: 28px 0; }
.stat-pill {
    background: #0e0e12;
    border: 1px solid #1e1e28;
    border-radius: 8px;
    padding: 14px 22px;
    text-align: center;
    min-width: 140px;
    flex: 1;
}
.stat-pill .val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #c8a84b;
}
.stat-pill .lbl { font-size: 0.75rem; color: #666; margin-top: 2px; }

/* ── Navigation table ── */
[data-testid="stDataFrame"] {
    border: 1px solid #1e1e28 !important;
    border-radius: 8px !important;
    background: #0e0e12 !important;
}

/* ── Dividers ── */
hr { border-color: #1c1c22; margin: 2rem 0; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #0e0e12;
    border: 1px solid #1e1e28;
    border-radius: 8px;
}

/* ── Sidebar nav links ── */
[data-testid="stSidebarNav"] a {
    color: #c9c3b8 !important;
    font-size: 0.9rem;
}
[data-testid="stSidebarNav"] a:hover { color: #c8a84b !important; }

/* ── Streamlit default overrides ── */
.stMetric { background: #0e0e12; border: 1px solid #1e1e28; border-radius: 8px; padding: 12px 16px; }
.stSelectbox > div, .stSlider > div { background: transparent; }
[data-testid="stMarkdownContainer"] p { color: #b0aaa4; }

/* ── KPI card (used in page 2) ── */
.kpi-card {
    background: #0e0e12;
    border: 1px solid #1e1e28;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 10px;
}
.kpi-label { font-size: 0.72em; color: #666; text-transform: uppercase; letter-spacing: 0.09em; }
.kpi-value { font-size: 1.5em; font-weight: 700; color: #c8a84b; margin-top: 4px;
             font-family: 'Space Grotesk', sans-serif; }
.kpi-sub   { font-size: 0.78em; color: #555; margin-top: 2px; }

/* ── Warn / info boxes ── */
.warn-box {
    background: #140808;
    border: 1px solid #8b2020;
    border-radius: 8px;
    padding: 12px 18px;
    color: #e07070;
    margin: 10px 0;
}
.info-box {
    background: #08101a;
    border: 1px solid #1e3a5a;
    border-radius: 8px;
    padding: 12px 18px;
    color: #7aabcf;
    margin: 10px 0;
}

/* ── Binding status badges ── */
.badge-binding {
    background: #0f1f0f; border: 1px solid #2d6b2d;
    border-radius: 8px; padding: 12px 18px; color: #6ec86e; margin: 10px 0;
}
.badge-nonbinding {
    background: #08101a; border: 1px solid #1e3a5a;
    border-radius: 8px; padding: 12px 18px; color: #7aabcf; margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Hero section
# ---------------------------------------------------------------------------
st.markdown("""
<div style="padding: 2rem 0 1rem 0;">
  <div class="hero-title">NVIDIA vs. AMD<br>GPU Duopoly Simulator</div>
  <div class="hero-sub">Game-Theory Equilibrium Analysis · Cournot · Differentiated Bertrand · Capacity Constraints</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Research goal statement
# ---------------------------------------------------------------------------
st.markdown("""
<div style="background:#0e0e12;border:1px solid #1e1e28;border-left:3px solid #c8a84b;
border-radius:0 8px 8px 0;padding:18px 24px;margin-bottom:2rem;">
<div style="font-size:0.72em;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;
color:#c8a84b;margin-bottom:8px;">Research Goal</div>
<div style="font-size:1.02rem;color:#d8d2ca;line-height:1.7;">
How do the predicted equilibrium price, quantity, and payoff outcomes for NVIDIA and AMD
differ under <strong style="color:#e8e2d9">Cournot quantity competition</strong> and
<strong style="color:#e8e2d9">differentiated Bertrand price competition</strong> —
and how do demand substitutability, cost asymmetry, and a binding output cap reshape
those outcomes?
</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Live stat pills (computed from defaults at load time)
# ---------------------------------------------------------------------------
from models.demand import ratio_to_D
from models.cournot import solve_cournot
from models.bertrand import solve_bertrand

_A  = float(DEFAULTS["A"])
_B  = float(DEFAULTS["B"])
_r  = float(DEFAULTS["substitutability_ratio_D_over_B"])
_D  = ratio_to_D(_r, _B)
_c1 = float(DEFAULTS["c1_nvidia"])
_c2 = float(DEFAULTS["c2_amd"])

_c = solve_cournot(_A, _B, _D, _c1, _c2)
_b = solve_bertrand(_A, _B, _D, _c1, _c2)

if _c.status == "ok" and _b.status == "ok":
    st.markdown(f"""
<div class="stat-row">
  <div class="stat-pill">
    <div class="val">{_c.p1:,.0f}</div>
    <div class="lbl">Cournot NVIDIA price</div>
  </div>
  <div class="stat-pill">
    <div class="val">{_b.p1:,.0f}</div>
    <div class="lbl">Bertrand NVIDIA price</div>
  </div>
  <div class="stat-pill">
    <div class="val">{_c.p2:,.0f}</div>
    <div class="lbl">Cournot AMD price</div>
  </div>
  <div class="stat-pill">
    <div class="val">{_b.p2:,.0f}</div>
    <div class="lbl">Bertrand AMD price</div>
  </div>
  <div class="stat-pill">
    <div class="val">{_r:.2f}</div>
    <div class="lbl">D/B substitutability</div>
  </div>
</div>
<div style="font-size:0.75rem;color:#444;margin-top:-16px;margin-bottom:24px;">
  Computed live from default scenario inputs. Adjust on the Live Equilibrium page.
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------------------------
# Three scenario cards
# ---------------------------------------------------------------------------
st.markdown("### Three Competition Scenarios")

sc1, sc2, sc3 = st.columns(3, gap="medium")

with sc1:
    st.markdown("""
<div class="scenario-card">
  <div class="tag">Scenario 01</div>
  <h4>Cournot Quantity Competition</h4>
  <p>Both firms simultaneously choose output quantities. Each firm's quantity is its
  best response to the rival's quantity. Closed-form interior Nash equilibrium via
  analytical first-order conditions.</p>
</div>
""", unsafe_allow_html=True)

with sc2:
    st.markdown("""
<div class="scenario-card">
  <div class="tag">Scenario 02</div>
  <h4>Differentiated Bertrand Price Competition</h4>
  <p>Both firms simultaneously set prices. Products are differentiated — the equilibrium
  price is <em>not</em> marginal cost. Prices and quantities are recovered via direct
  demand inversion. Lower prices and higher quantities than Cournot.</p>
</div>
""", unsafe_allow_html=True)

with sc3:
    st.markdown("""
<div class="scenario-card">
  <div class="tag">Scenario 03</div>
  <h4>Capacity-Constrained Cournot</h4>
  <p>NVIDIA faces a hypothetical output cap. AMD best-responds via its Cournot
  reaction function. The cap is nonbinding if it exceeds the unconstrained quantity —
  only a tight cap shifts equilibrium outcomes.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------------------------
# Default scenario parameters table
# ---------------------------------------------------------------------------
st.markdown("### Default Scenario Parameters")
st.caption("Scenario inputs — adjust freely on the Live Equilibrium page.")

defaults_display = {
    "Parameter": [
        "A — demand intercept",
        "B — own-quantity slope",
        "D/B — substitutability ratio",
        "D — cross-quantity term (= ratio × B)",
        "c₁ — NVIDIA cost input",
        "c₂ — AMD cost input",
        "NVIDIA output cap (hypothetical)",
    ],
    "Value": [
        DEFAULTS["A"],
        DEFAULTS["B"],
        DEFAULTS["substitutability_ratio_D_over_B"],
        round(DEFAULTS["substitutability_ratio_D_over_B"] * DEFAULTS["B"], 4),
        DEFAULTS["c1_nvidia"],
        DEFAULTS["c2_amd"],
        DEFAULTS["nvidia_output_cap"],
    ],
    "Unit": [
        "model price units",
        "model price units / model unit",
        "dimensionless [0, 0.95)",
        "model price units / model unit",
        "model price units",
        "model price units",
        "model units",
    ],
}

st.dataframe(pd.DataFrame(defaults_display), use_container_width=True, hide_index=True)

st.divider()

# ---------------------------------------------------------------------------
# Navigation guide
# ---------------------------------------------------------------------------
st.markdown("### Navigate the Simulator")
st.markdown("""
Use the **sidebar** to move between pages.

| Page | Purpose |
|---|---|
| **1 · Model & Equations** | Demand system, FOCs, equilibrium notation |
| **2 · Live Equilibrium** | Adjust sliders — compare Cournot vs. Bertrand live |
| **3 · Capacity & Scenarios** | Explore the NVIDIA output cap and cost scenarios |
| **4 · Data & Validation** | Official launch MSRP reference and data-readiness status |

**Quick demo path:** Open page 2, slide D/B from 0 → 0.5 → 0.9, then go to page 3 and move the cap slider. See `DOCS/demo.md` for the full presenter walkthrough.
""")

st.divider()

# ---------------------------------------------------------------------------
# Key references (collapsed by default)
# ---------------------------------------------------------------------------
with st.expander("References"):
    st.markdown("""
**Official launch MSRP sources:**
- [NVIDIA RTX 40/50 Series — NVIDIA IR](https://investor.nvidia.com/)
- [AMD RX 7000/9000 Series — AMD IR](https://ir.amd.com/)

**Market context:**
- [Jon Peddie Research — AIB Shipments Q1 2026](https://www.jonpeddie.com/news/q126-pc-graphics-add-in-board-shipments-decreased-0-6-from-last-quarter-to-12-million-units-with-a-cagr-to-2029-of-3-3/)
- [NVIDIA FY2026 10-K — SEC](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)
- [AMD FY2025 10-K — SEC](https://www.sec.gov/Archives/edgar/data/2488/000000248826000021/amd-20251227.htm)

**Demand-model methodology:**
- Berry & Haile (2016) — [Identification in Differentiated Products Markets](https://www.annualreviews.org/doi/10.1146/annurev-economics-080315-015050)
- Choné & Linnemer (2020) — [Linear demand systems for differentiated goods](https://doi.org/10.1016/j.ijindorg.2020.102663)
""")

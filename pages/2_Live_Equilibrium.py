"""
pages/2_Live_Equilibrium.py
============================
Interactive Cournot vs. Differentiated Bertrand comparison.

Controls: A, B, D/B ratio, c1, c2, metric selector.
Outputs: KPI cards, bar chart, result table, calculation details, dynamic narrative.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from models.demand import ratio_to_D
from models.cournot import solve_cournot
from models.bertrand import solve_bertrand
from analysis.sensitivity import sweep_substitutability
from utils.formatting import illustrative_note, payoff_disclaimer, feasibility_warning

st.set_page_config(page_title="Live Equilibrium — GPU Duopoly", layout="wide", page_icon="📊")



# Load defaults
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(ROOT, "data", "illustrative_defaults.json")) as f:
    DEFAULTS = json.load(f)

# ---------------------------------------------------------------------------
# Sidebar: parameter controls
# ---------------------------------------------------------------------------
st.sidebar.header("⚙️ Parameters")

A = st.sidebar.slider("Demand intercept A", min_value=500.0, max_value=3000.0,
                       value=float(DEFAULTS["A"]), step=50.0,
                       help="Inverse-demand intercept (model price units)")
B = st.sidebar.slider("Own-quantity slope B", min_value=0.5, max_value=10.0,
                       value=float(DEFAULTS["B"]), step=0.1,
                       help="B > 0; price falls by B per unit of own output")
ratio = st.sidebar.slider("Substitutability ratio D/B", min_value=0.0, max_value=0.95,
                            value=float(DEFAULTS["substitutability_ratio_D_over_B"]), step=0.01,
                            help="D/B in [0, 0.95). D is computed as ratio × B.")
c1 = st.sidebar.slider("NVIDIA cost input c₁", min_value=0.0, max_value=2000.0,
                         value=float(DEFAULTS["c1_nvidia"]), step=10.0,
                         help="Illustrative marginal cost input for NVIDIA")
c2 = st.sidebar.slider("AMD cost input c₂", min_value=0.0, max_value=2000.0,
                         value=float(DEFAULTS["c2_amd"]), step=10.0,
                         help="Illustrative marginal cost input for AMD")

# Derive D from slider ratio (fixing the old prototype's bug)
D = ratio_to_D(ratio, B)

metric = st.sidebar.selectbox(
    "Metric for bar chart",
    options=["price", "quantity", "margin", "payoff"],
    index=0,
)

# ---------------------------------------------------------------------------
# Solve both games
# ---------------------------------------------------------------------------
c_res = solve_cournot(A, B, D, c1, c2)
b_res = solve_bertrand(A, B, D, c1, c2)

# ---------------------------------------------------------------------------
# Title and derived D display
# ---------------------------------------------------------------------------
st.title("📊 Live Equilibrium: Cournot vs. Bertrand")

param_col1, param_col2, param_col3 = st.columns(3)
with param_col1:
    st.metric("A", f"{A:.1f}")
    st.metric("B", f"{B:.2f}")
with param_col2:
    st.metric("D/B (slider)", f"{ratio:.4f}")
    st.metric("D (derived = ratio × B)", f"{D:.4f}")
with param_col3:
    st.metric("c₁ NVIDIA", f"{c1:.1f}")
    st.metric("c₂ AMD", f"{c2:.1f}")

st.caption("⚠️ All parameter values are **illustrative scenario inputs** — not empirically calibrated data.")

# ---------------------------------------------------------------------------
# Feasibility warnings
# ---------------------------------------------------------------------------
if c_res.status != "ok":
    st.markdown(f"""
    <div style="background:#2d1a1a;border:1px solid #c04040;border-radius:6px;
    padding:10px 16px;color:#e07070;margin:10px 0;">
    ❌ Cournot: {feasibility_warning(c_res.status, c_res.message)}
    </div>""", unsafe_allow_html=True)

if b_res.status != "ok":
    st.markdown(f"""
    <div style="background:#2d1a1a;border:1px solid #c04040;border-radius:6px;
    padding:10px 16px;color:#e07070;margin:10px 0;">
    ❌ Bertrand: {feasibility_warning(b_res.status, b_res.message)}
    </div>""", unsafe_allow_html=True)

# Only continue to show results if at least one game solved ok
if c_res.status != "ok" and b_res.status != "ok":
    st.stop()

st.divider()

# ---------------------------------------------------------------------------
# KPI cards
# ---------------------------------------------------------------------------
def kpi(label, value, unit="", fmt=".2f"):
    val_str = f"{value:{fmt}}" if value is not None else "N/A"
    st.markdown(f"""
    <div style="background:#22252d;border:1px solid #2e3038;border-radius:8px;
    padding:14px 18px;margin-bottom:8px;">
    <div style="font-size:0.76em;color:#888;text-transform:uppercase;letter-spacing:0.08em;">{label}</div>
    <div style="font-size:1.45em;font-weight:700;color:#c8a84b;margin-top:4px;">{val_str}</div>
    <div style="font-size:0.77em;color:#666;margin-top:2px;">{unit}</div>
    </div>""", unsafe_allow_html=True)

col_h1, col_h2, col_h3, col_h4 = st.columns(4)
col_h1.markdown("### 🟡 NVIDIA — Cournot")
col_h2.markdown("### 🟢 AMD — Cournot")
col_h3.markdown("### 🔵 NVIDIA — Bertrand")
col_h4.markdown("### 🟣 AMD — Bertrand")

with col_h1:
    if c_res.status == "ok":
        kpi("Price p₁", c_res.p1, "model price units")
        kpi("Quantity q₁", c_res.q1, "model units (illustrative)")
        kpi("Margin m₁", c_res.m1, "model price units")
        kpi("Payoff π₁", c_res.pi1, "model payoff")
    else:
        st.error("Cournot infeasible — see warning above.")

with col_h2:
    if c_res.status == "ok":
        kpi("Price p₂", c_res.p2, "model price units")
        kpi("Quantity q₂", c_res.q2, "model units (illustrative)")
        kpi("Margin m₂", c_res.m2, "model price units")
        kpi("Payoff π₂", c_res.pi2, "model payoff")
    else:
        st.error("Cournot infeasible — see warning above.")

with col_h3:
    if b_res.status == "ok":
        kpi("Price p₁", b_res.p1, "model price units")
        kpi("Quantity q₁", b_res.q1, "model units (illustrative)")
        kpi("Margin m₁", b_res.m1, "model price units")
        kpi("Payoff π₁", b_res.pi1, "model payoff")
    else:
        st.error("Bertrand infeasible — see warning above.")

with col_h4:
    if b_res.status == "ok":
        kpi("Price p₂", b_res.p2, "model price units")
        kpi("Quantity q₂", b_res.q2, "model units (illustrative)")
        kpi("Margin m₂", b_res.m2, "model price units")
        kpi("Payoff π₂", b_res.pi2, "model payoff")
    else:
        st.error("Bertrand infeasible — see warning above.")

st.caption(payoff_disclaimer())
st.divider()

# ---------------------------------------------------------------------------
# Comparison bar chart
# ---------------------------------------------------------------------------
METRIC_MAP = {
    "price":    ("p₁", "p₂", "Price (model price units)"),
    "quantity": ("q₁", "q₂", "Quantity (model units, illustrative)"),
    "margin":   ("m₁", "m₂", "Per-unit margin (model price units)"),
    "payoff":   ("π₁", "π₂", "Model payoff"),
}

def _get_metric_values(res, metric_key):
    if res.status != "ok":
        return None, None
    if metric_key == "price":
        return res.p1, res.p2
    elif metric_key == "quantity":
        return res.q1, res.q2
    elif metric_key == "margin":
        return res.m1, res.m2
    elif metric_key == "payoff":
        return res.pi1, res.pi2

nv_label, amd_label, axis_label = METRIC_MAP[metric]
c_nv, c_amd = _get_metric_values(c_res, metric)
b_nv, b_amd = _get_metric_values(b_res, metric)

fig = go.Figure()

if c_nv is not None:
    fig.add_trace(go.Bar(
        name="Cournot — NVIDIA",
        x=["NVIDIA", "AMD"],
        y=[c_nv, c_amd],
        marker_color="#c8a84b",
        text=[f"{c_nv:.2f}", f"{c_amd:.2f}"],
        textposition="outside",
    ))

if b_nv is not None:
    fig.add_trace(go.Bar(
        name="Bertrand — NVIDIA / AMD",
        x=["NVIDIA", "AMD"],
        y=[b_nv, b_amd],
        marker_color="#4ec9b0",
        text=[f"{b_nv:.2f}", f"{b_amd:.2f}"],
        textposition="outside",
    ))

fig.update_layout(
    title=f"Equilibrium Comparison — {metric.capitalize()} (Illustrative Parameters)",
    yaxis_title=axis_label,
    xaxis_title="Firm",
    barmode="group",
    paper_bgcolor="#1a1c20",
    plot_bgcolor="#22252d",
    font=dict(color="#e6e0d4"),
    legend=dict(bgcolor="#22252d", bordercolor="#2e3038"),
    height=380,
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Dynamic narrative (based on computed values)
# ---------------------------------------------------------------------------
if c_res.status == "ok" and b_res.status == "ok":
    st.subheader("📝 Computed interpretation")

    # Generate direction-agnostic summary
    lines = []
    for firm, c_val, b_val, firm_label in [
        ("NVIDIA", c_nv, b_nv, "NVIDIA"),
        ("AMD", c_amd, b_amd, "AMD"),
    ]:
        if c_val is not None and b_val is not None:
            direction = "lower" if b_val < c_val else "higher"
            diff = abs(b_val - c_val)
            lines.append(
                f"Under the current illustrative inputs, **Bertrand predicts "
                f"{direction} {metric}** than Cournot for **{firm_label}** "
                f"(difference: {diff:.2f} {axis_label.split('(')[0].strip()})."
            )

    for line in lines:
        st.markdown(line)

    # D/B context
    if ratio < 0.1:
        st.markdown(
            f"With **D/B = {ratio:.2f}** (near zero), products are nearly independent. "
            "Both games converge toward independent-monopoly outcomes."
        )
    elif ratio > 0.8:
        st.markdown(
            f"With **D/B = {ratio:.2f}** (high substitutability), products are close "
            "substitutes. Price competition (Bertrand) becomes especially harsh."
        )

    st.caption(
        "This interpretation is generated from computed values. "
        "It is a model counterfactual, not a causal claim about actual GPU markets."
    )

st.divider()

# ---------------------------------------------------------------------------
# Full result table
# ---------------------------------------------------------------------------
st.subheader("📋 Full result table")

rows = []
for game, res in [("Cournot", c_res), ("Bertrand", b_res)]:
    for firm, p, q, m, pi, c_val in [
        ("NVIDIA", res.p1, res.q1, res.m1, res.pi1, c1),
        ("AMD",    res.p2, res.q2, res.m2, res.pi2, c2),
    ]:
        if res.status == "ok":
            rows.append({
                "Game": game, "Firm": firm,
                "Price": round(p, 4), "Quantity": round(q, 4),
                "Cost input": c_val,
                "Margin (p−c)": round(m, 4),
                "Model payoff": round(pi, 2),
                "Status": res.status,
            })
        else:
            rows.append({
                "Game": game, "Firm": firm,
                "Price": None, "Quantity": None,
                "Cost input": c_val,
                "Margin (p−c)": None, "Model payoff": None,
                "Status": f"{res.status}: {res.message[:60]}",
            })

df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True, hide_index=True)
st.caption("Quantities: model units (illustrative) | Prices/margins: model price units | Payoffs: model price units × model units")

# ---------------------------------------------------------------------------
# Calculation details
# ---------------------------------------------------------------------------
with st.expander("🔍 Show calculation details"):
    st.markdown(f"""
**Current parameter values:**
- A = {A}, B = {B}, D/B = {ratio}, D = {D:.4f}
- c₁ (NVIDIA) = {c1}, c₂ (AMD) = {c2}

**Cournot denominator:** 4B² - D² = 4×{B}²−{D:.4f}² = {4*B**2 - D**2:.4f}

**Cournot formulas:**
- q₁* = [2B(A−c₁) − D(A−c₂)] / (4B²−D²) = [{2*B*(A-c1):.2f} − {D*(A-c2):.2f}] / {4*B**2-D**2:.4f}
- q₂* = [2B(A−c₂) − D(A−c₁)] / (4B²−D²)

**Bertrand r-terms:**
- r₁ = (B−D)A + Bc₁ = {(B-D)*A + B*c1:.4f}
- r₂ = (B−D)A + Bc₂ = {(B-D)*A + B*c2:.4f}
- p₁* = (2B·r₁ + D·r₂) / (4B²−D²)
- p₂* = (D·r₁ + 2B·r₂) / (4B²−D²)
""")
    if c_res.status == "ok":
        from models.cournot import _check_foc
        r1, r2 = _check_foc(c_res)
        st.markdown(f"**Cournot FOC residuals:** r₁ = {r1:.2e}, r₂ = {r2:.2e} (should be ≈ 0)")
    if b_res.status == "ok":
        from models.bertrand import _check_bertrand_foc
        r1, r2 = _check_bertrand_foc(b_res)
        st.markdown(f"**Bertrand FOC residuals:** r₁ = {r1:.2e}, r₂ = {r2:.2e} (should be ≈ 0)")

st.divider()

# ---------------------------------------------------------------------------
# Substitutability sensitivity line chart
# ---------------------------------------------------------------------------
st.subheader("📈 Sensitivity: Varying D/B (other parameters fixed)")
st.caption("Each point solves the full game at the given D/B value with all other inputs held constant.")

sweep_data = sweep_substitutability(A, B, c1, c2, n_points=80)
df_sweep = pd.DataFrame(sweep_data)

sens_metric = st.selectbox(
    "Metric to plot vs. D/B",
    ["Prices (p₁, p₂)", "Quantities (q₁, q₂)", "Model Payoffs (π₁, π₂)"],
    index=0,
)

fig2 = go.Figure()

if sens_metric == "Prices (p₁, p₂)":
    fig2.add_trace(go.Scatter(x=df_sweep["ratio"], y=df_sweep["c_p1"],
        name="Cournot NVIDIA p₁", line=dict(color="#c8a84b", width=2)))
    fig2.add_trace(go.Scatter(x=df_sweep["ratio"], y=df_sweep["c_p2"],
        name="Cournot AMD p₂", line=dict(color="#c8a84b", dash="dash", width=2)))
    fig2.add_trace(go.Scatter(x=df_sweep["ratio"], y=df_sweep["b_p1"],
        name="Bertrand NVIDIA p₁", line=dict(color="#4ec9b0", width=2)))
    fig2.add_trace(go.Scatter(x=df_sweep["ratio"], y=df_sweep["b_p2"],
        name="Bertrand AMD p₂", line=dict(color="#4ec9b0", dash="dash", width=2)))
    y_label = "Price (model price units)"

elif sens_metric == "Quantities (q₁, q₂)":
    fig2.add_trace(go.Scatter(x=df_sweep["ratio"], y=df_sweep["c_q1"],
        name="Cournot NVIDIA q₁", line=dict(color="#c8a84b", width=2)))
    fig2.add_trace(go.Scatter(x=df_sweep["ratio"], y=df_sweep["c_q2"],
        name="Cournot AMD q₂", line=dict(color="#c8a84b", dash="dash", width=2)))
    fig2.add_trace(go.Scatter(x=df_sweep["ratio"], y=df_sweep["b_q1"],
        name="Bertrand NVIDIA q₁", line=dict(color="#4ec9b0", width=2)))
    fig2.add_trace(go.Scatter(x=df_sweep["ratio"], y=df_sweep["b_q2"],
        name="Bertrand AMD q₂", line=dict(color="#4ec9b0", dash="dash", width=2)))
    y_label = "Quantity (model units, illustrative)"

else:
    fig2.add_trace(go.Scatter(x=df_sweep["ratio"], y=df_sweep["c_pi1"],
        name="Cournot NVIDIA π₁", line=dict(color="#c8a84b", width=2)))
    fig2.add_trace(go.Scatter(x=df_sweep["ratio"], y=df_sweep["c_pi2"],
        name="Cournot AMD π₂", line=dict(color="#c8a84b", dash="dash", width=2)))
    fig2.add_trace(go.Scatter(x=df_sweep["ratio"], y=df_sweep["b_pi1"],
        name="Bertrand NVIDIA π₁", line=dict(color="#4ec9b0", width=2)))
    fig2.add_trace(go.Scatter(x=df_sweep["ratio"], y=df_sweep["b_pi2"],
        name="Bertrand AMD π₂", line=dict(color="#4ec9b0", dash="dash", width=2)))
    y_label = "Model payoff"

# Mark current D/B
fig2.add_vline(x=ratio, line_dash="dot", line_color="#ff8c00",
               annotation_text=f"Current D/B = {ratio:.2f}")

fig2.update_layout(
    title=f"Sensitivity to Substitutability — {sens_metric} (Illustrative)",
    xaxis_title="D/B (substitutability ratio)",
    yaxis_title=y_label,
    paper_bgcolor="#1a1c20",
    plot_bgcolor="#22252d",
    font=dict(color="#e6e0d4"),
    legend=dict(bgcolor="#22252d", bordercolor="#2e3038"),
    height=420,
)
st.plotly_chart(fig2, use_container_width=True)
st.caption(
    "Solid lines = NVIDIA (Firm 1), dashed = AMD (Firm 2). "
    "Gold = Cournot, teal = Bertrand. Orange vertical line = current slider position. "
    "Model counterfactual — not a causal forecast."
)

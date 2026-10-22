"""
pages/3_Capacity_and_Scenarios.py
==================================
Capacity-constrained Cournot and controlled scenario experiments.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from models.demand import ratio_to_D
from models.cournot import solve_cournot
from models.capacity import solve_capacity_cournot
from analysis.sensitivity import sweep_substitutability

st.set_page_config(
    page_title="Capacity & Scenarios — GPU Duopoly", layout="wide", page_icon="🏭"
)

st.markdown("""
<div style="background:#2a1a00;border:1px solid #c8a84b;border-radius:6px;
padding:10px 18px;margin-bottom:22px;color:#c8a84b;font-weight:600;font-size:0.93em;">
⚠️  ILLUSTRATIVE MODE — parameters are scenario inputs; not empirically calibrated
</div>""", unsafe_allow_html=True)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(ROOT, "data", "illustrative_defaults.json")) as f:
    DEFAULTS = json.load(f)

# ---------------------------------------------------------------------------
# Sidebar: shared parameters
# ---------------------------------------------------------------------------
st.sidebar.header("⚙️ Shared Parameters")
A = st.sidebar.slider("A (demand intercept)", 500.0, 3000.0, float(DEFAULTS["A"]), 50.0)
B = st.sidebar.slider("B (own-qty slope)", 0.5, 10.0, float(DEFAULTS["B"]), 0.1)
ratio = st.sidebar.slider("D/B (substitutability)", 0.0, 0.95,
                            float(DEFAULTS["substitutability_ratio_D_over_B"]), 0.01)
c1 = st.sidebar.slider("c₁ NVIDIA cost", 0.0, 2000.0, float(DEFAULTS["c1_nvidia"]), 10.0)
c2 = st.sidebar.slider("c₂ AMD cost", 0.0, 2000.0, float(DEFAULTS["c2_amd"]), 10.0)
D = ratio_to_D(ratio, B)

# ---------------------------------------------------------------------------
st.title("🏭 Capacity-Constrained Cournot & Scenario Experiments")

st.markdown("""
This page demonstrates the **hypothetical NVIDIA output cap** — a Cournot variant where
NVIDIA's quantity cannot exceed a ceiling you control. The cap is treated as a **maximum**,
not a forced production level. It is **not** described as an observed TSMC allocation.
""")

st.divider()

# ===========================================================================
# Section 1: Capacity-constrained Cournot
# ===========================================================================
st.header("1 · NVIDIA Output Cap (Hypothetical)")

# Unconstrained baseline
uc = solve_cournot(A, B, D, c1, c2)

col_info1, col_info2 = st.columns([1, 2])
with col_info1:
    if uc.status == "ok":
        st.metric("Unconstrained NVIDIA q₁*", f"{uc.q1:.4f}",
                  help="Unconstrained Cournot equilibrium quantity for NVIDIA")
    else:
        st.error(f"Unconstrained Cournot failed: {uc.message}")

with col_info2:
    if uc.status == "ok":
        default_cap = float(DEFAULTS["nvidia_output_cap"])
        q1_cap = st.slider(
            "NVIDIA output cap (hypothetical)",
            min_value=0.0,
            max_value=max(float(uc.q1) * 2, 300.0) if uc.status == "ok" else 300.0,
            value=min(default_cap, float(uc.q1) * 2),
            step=1.0,
            help="Hypothetical upper bound on NVIDIA's output. Nonbinding if ≥ unconstrained quantity.",
        )

if uc.status == "ok":
    cap_res = solve_capacity_cournot(A, B, D, c1, c2, q1_cap=q1_cap)

    # Binding/nonbinding badge
    if cap_res.binding:
        st.markdown("""
        <div style="background:#1a2d1a;border:1px solid #3a8843;border-radius:6px;
        padding:10px 16px;color:#7ec87e;margin:10px 0;">
        🔴 <strong>Cap is BINDING</strong> — NVIDIA's unconstrained quantity exceeds the cap.
        AMD best-responds to the capped quantity.
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#1a2035;border:1px solid #3a5888;border-radius:6px;
        padding:10px 16px;color:#a0b8d8;margin:10px 0;">
        🟢 <strong>Cap is NONBINDING</strong> — the cap exceeds NVIDIA's unconstrained quantity.
        The unconstrained Cournot equilibrium applies unchanged.
        </div>""", unsafe_allow_html=True)

    st.caption(f"Cap message: {cap_res.message}")

    # ---------------------------------------------------------------------------
    # Comparison table
    # ---------------------------------------------------------------------------
    st.subheader("Unconstrained vs. Constrained Outcome")

    rows = []
    if uc.status == "ok":
        rows.append({
            "Scenario": "Unconstrained Cournot",
            "NVIDIA q₁": round(uc.q1, 4),
            "AMD q₂": round(uc.q2, 4),
            "NVIDIA p₁": round(uc.p1, 4),
            "AMD p₂": round(uc.p2, 4),
            "NVIDIA margin": round(uc.m1, 4),
            "AMD margin": round(uc.m2, 4),
            "NVIDIA payoff": round(uc.pi1, 2),
            "AMD payoff": round(uc.pi2, 2),
            "Cap binding": "—",
        })
    rows.append({
        "Scenario": f"Cap = {q1_cap:.1f} (hypothetical)",
        "NVIDIA q₁": round(cap_res.q1, 4) if cap_res.status == "ok" else "N/A",
        "AMD q₂": round(cap_res.q2, 4) if cap_res.status == "ok" else "N/A",
        "NVIDIA p₁": round(cap_res.p1, 4) if cap_res.status == "ok" else "N/A",
        "AMD p₂": round(cap_res.p2, 4) if cap_res.status == "ok" else "N/A",
        "NVIDIA margin": round(cap_res.m1, 4) if cap_res.status == "ok" else "N/A",
        "AMD margin": round(cap_res.m2, 4) if cap_res.status == "ok" else "N/A",
        "NVIDIA payoff": round(cap_res.pi1, 2) if cap_res.status == "ok" else "N/A",
        "AMD payoff": round(cap_res.pi2, 2) if cap_res.status == "ok" else "N/A",
        "Cap binding": str(cap_res.binding),
    })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.caption("Quantities: model units (illustrative) | Prices/margins: model price units | Payoffs: model contribution payoff")

    # ---------------------------------------------------------------------------
    # Capacity comparison chart
    # ---------------------------------------------------------------------------
    if cap_res.status == "ok" and uc.status == "ok":
        labels = ["NVIDIA q₁", "AMD q₂", "NVIDIA p₁", "AMD p₂",
                  "NVIDIA payoff", "AMD payoff"]
        uc_vals = [uc.q1, uc.q2, uc.p1, uc.p2, uc.pi1, uc.pi2]
        cap_vals = [cap_res.q1, cap_res.q2, cap_res.p1, cap_res.p2,
                    cap_res.pi1, cap_res.pi2]

        fig = go.Figure()
        fig.add_trace(go.Bar(name="Unconstrained Cournot", x=labels, y=uc_vals,
                             marker_color="#c8a84b"))
        fig.add_trace(go.Bar(name=f"Cap = {q1_cap:.1f} (hypothetical)", x=labels, y=cap_vals,
                             marker_color="#4ec9b0"))
        fig.update_layout(
            title="Unconstrained vs. Cap Scenario (Illustrative)",
            barmode="group",
            paper_bgcolor="#1a1c20", plot_bgcolor="#22252d",
            font=dict(color="#e6e0d4"),
            legend=dict(bgcolor="#22252d"),
            height=360,
        )
        st.plotly_chart(fig, use_container_width=True)

    # AMD best-response explanation
    if cap_res.binding:
        with st.expander("📐 How AMD's best response is calculated"):
            st.markdown(f"""
When the cap binds (`q₁ = {q1_cap:.1f}`), AMD chooses its Cournot best response:

```
q₂ = max(0, (A − c₂ − D·q₁) / 2B)
   = max(0, ({A} − {c2} − {D:.4f} × {q1_cap:.1f}) / {2*B:.2f})
   = max(0, {(A - c2 - D * q1_cap):.4f} / {2*B:.2f})
   = {cap_res.q2:.4f}
```

Prices are then recomputed via inverse demand using these quantities.
""")

st.divider()

# ===========================================================================
# Section 2: Controlled Scenario Experiments
# ===========================================================================
st.header("2 · Controlled Scenario Experiments")
st.markdown("""
The following experiments change **one factor at a time** from the sidebar baseline,
so the effect of each change is interpretable. All results are model counterfactuals.
""")

if uc.status != "ok":
    st.warning("Unconstrained Cournot infeasible under current parameters. Adjust A, B, D/B, c1, c2.")
    st.stop()

# Scenario: NVIDIA cost variation
st.subheader("2a · NVIDIA Cost Variation (c₁ fixed; c₂ varies)")

c1_range = [c1 * 0.5, c1 * 0.75, c1, c1 * 1.25, c1 * 1.5]
scenario_rows = []
for c1_val in c1_range:
    r = solve_cournot(A, B, D, c1_val, c2)
    if r.status == "ok":
        scenario_rows.append({
            "c₁ NVIDIA": round(c1_val, 1),
            "c₂ AMD (fixed)": c2,
            "NVIDIA q₁": round(r.q1, 3),
            "AMD q₂": round(r.q2, 3),
            "NVIDIA p₁": round(r.p1, 3),
            "AMD p₂": round(r.p2, 3),
            "NVIDIA payoff": round(r.pi1, 2),
            "AMD payoff": round(r.pi2, 2),
        })

if scenario_rows:
    df_s = pd.DataFrame(scenario_rows)
    st.dataframe(df_s, use_container_width=True, hide_index=True)

    # Chart: NVIDIA payoff vs c1
    fig_c1 = go.Figure()
    fig_c1.add_trace(go.Scatter(x=df_s["c₁ NVIDIA"], y=df_s["NVIDIA payoff"],
                                 mode="lines+markers", name="NVIDIA model payoff",
                                 line=dict(color="#c8a84b")))
    fig_c1.add_trace(go.Scatter(x=df_s["c₁ NVIDIA"], y=df_s["AMD payoff"],
                                 mode="lines+markers", name="AMD model payoff",
                                 line=dict(color="#4ec9b0")))
    fig_c1.update_layout(
        title="Model Payoffs vs. NVIDIA Cost Input (Cournot, Illustrative)",
        xaxis_title="c₁ NVIDIA cost input (model price units)",
        yaxis_title="Model payoff",
        paper_bgcolor="#1a1c20", plot_bgcolor="#22252d",
        font=dict(color="#e6e0d4"), height=320,
    )
    st.plotly_chart(fig_c1, use_container_width=True)

# Scenario: D/B variation
st.subheader("2b · Substitutability D/B (A, B, c₁, c₂ fixed)")
st.caption("Recomputes Cournot and Bertrand at each D/B value with all other inputs held at sidebar values.")

sweep = sweep_substitutability(A, B, c1, c2, n_points=60)
df_sw = pd.DataFrame(sweep)

fig_sw = go.Figure()
fig_sw.add_trace(go.Scatter(x=df_sw["ratio"], y=df_sw["c_pi1"],
    name="Cournot NVIDIA π₁", line=dict(color="#c8a84b")))
fig_sw.add_trace(go.Scatter(x=df_sw["ratio"], y=df_sw["c_pi2"],
    name="Cournot AMD π₂", line=dict(color="#c8a84b", dash="dash")))
fig_sw.add_trace(go.Scatter(x=df_sw["ratio"], y=df_sw["b_pi1"],
    name="Bertrand NVIDIA π₁", line=dict(color="#4ec9b0")))
fig_sw.add_trace(go.Scatter(x=df_sw["ratio"], y=df_sw["b_pi2"],
    name="Bertrand AMD π₂", line=dict(color="#4ec9b0", dash="dash")))
fig_sw.add_vline(x=ratio, line_dash="dot", line_color="#ff8c00",
                  annotation_text=f"Current D/B={ratio:.2f}")
fig_sw.update_layout(
    title="Model Payoffs vs. D/B — Cournot and Bertrand (Illustrative)",
    xaxis_title="D/B (substitutability ratio)",
    yaxis_title="Model payoff",
    paper_bgcolor="#1a1c20", plot_bgcolor="#22252d",
    font=dict(color="#e6e0d4"),
    legend=dict(bgcolor="#22252d"),
    height=380,
)
st.plotly_chart(fig_sw, use_container_width=True)
st.caption(
    "Model counterfactual — not a causal claim. "
    "Solid = NVIDIA, dashed = AMD. Gold = Cournot, teal = Bertrand."
)

"""
pages/5_Demo_Guide.py
=====================
Presenter script (5–7 minutes), scenario walk-through steps,
and instructor Q&A section.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import json

st.set_page_config(page_title="Demo Guide — GPU Duopoly", layout="wide", page_icon="🎓")

st.markdown("""
<div style="background:#2a1a00;border:1px solid #c8a84b;border-radius:6px;
padding:10px 18px;margin-bottom:22px;color:#c8a84b;font-weight:600;font-size:0.93em;">
⚠️  ILLUSTRATIVE MODE — parameters are scenario inputs; not empirically calibrated
</div>""", unsafe_allow_html=True)

st.title("🎓 Presentation Demo Guide")
st.markdown("""
This page provides a **5–7 minute presenter script** for walking through the simulator
during a class or project presentation. Use the sidebar pages to navigate as described.
""")

# ---------------------------------------------------------------------------
st.header("🎯 Presentation Script (~5–7 minutes)")
# ---------------------------------------------------------------------------

with st.expander("**Step 1 · Introduction (1 min)** — Overview page", expanded=True):
    st.markdown("""
**Say:** "This simulator compares two classic game-theory models applied to a stylised
GPU duopoly — NVIDIA vs. AMD. The key question is: does Cournot quantity competition or
differentiated Bertrand price competition better describe equilibrium outcomes for these firms?"

**Emphasise:**
- This is a **scenario simulator**, not an empirically calibrated model.
- All parameter values are **illustrative placeholders** — not measured from real data.
- We compare model outcomes under different competition assumptions, not predict actual prices.

**Point to:** the "What this app does / cannot do" columns on the Overview page.

**Distinguish** clearly between:
- *Scenario simulation* (what we're doing): varying inputs to a theoretical model
- *Empirical estimation* (what we haven't done): fitting the model to real price/quantity data
""")

with st.expander("**Step 2 · Model Setup (1 min)** — Model & Equations page"):
    st.markdown("""
**Navigate to:** Page 1 — Model & Equations.

**Show** the inverse-demand system:
- p₁ = A − B·q₁ − D·q₂ (NVIDIA's price falls as own output or rival output rises)
- p₂ = A − B·q₂ − D·q₁ (symmetric for AMD)

**Explain** D/B:
- D/B = 0 → independent monopolies; D/B → 1 → nearly perfect substitutes
- The app keeps D/B < 1 to avoid singular Bertrand demand

**Say:** "The Cournot game: each firm chooses quantity to maximise payoff, taking the rival's
quantity as given. The Bertrand game: each firm chooses price, taking the rival's price as given.
For *differentiated* products, Bertrand does NOT give p = MC."
""")

with st.expander("**Step 3 · Live Comparison (2 min)** — Live Equilibrium page"):
    st.markdown("""
**Navigate to:** Page 2 — Live Equilibrium.

**With default parameters (A=1400, B=2.5, D/B=0.48):**
- Show that Bertrand prices are **lower** than Cournot prices for both firms.
- Show that Bertrand quantities are **higher** — consistent with more competitive outcome.
- This matches the theory: price competition is harsher than quantity competition.

**Then change D/B:**
1. Drag D/B to **0.0** → both games converge toward independent monopoly outcomes (same results)
2. Drag D/B to **0.90** → large gap between Cournot and Bertrand; price competition is very harsh

**Say:** "Notice the key result: as substitutability increases, the difference between the
two models grows. In highly competitive markets, the choice of competition mode matters a lot."

**Point out** the dynamic interpretation text below the chart — it's generated from computed
values, not pre-written.
""")

with st.expander("**Step 4 · Capacity Constraint (1–2 min)** — Capacity & Scenarios page"):
    st.markdown("""
**Navigate to:** Page 3 — Capacity & Scenarios.

**Show the default scenario (cap = 120, unconstrained q₁* ≈ 130.5):**
- Cap is **binding** → NVIDIA produces only 120
- AMD's best response increases (it best-responds to lower NVIDIA output)
- NVIDIA's price actually **rises** slightly relative to unconstrained (quantity restriction)
- AMD's payoff increases — it benefits from NVIDIA being constrained

**Then drag the cap slider** above the unconstrained quantity:
- Status changes to **nonbinding** — the cap has no effect
- Results are identical to unconstrained Cournot

**Say:** "A real cap would behave exactly this way — it only binds when it's tight enough.
This is labeled **hypothetical** throughout because we have no actual TSMC allocation data."

**Point out** the AMD best-response formula that appears when the cap binds.
""")

with st.expander("**Step 5 · Data and Missing Pieces (1 min)** — Data & Validation page"):
    st.markdown("""
**Navigate to:** Page 4 — Data & Validation.

**Show the MSRP table:**
- These are officially announced launch prices from NVIDIA and AMD press releases
- Click a source link to show it goes to a real official source

**Say:** "These prices are *descriptive context* — we can observe that NVIDIA typically launches
at a premium to AMD. But without matched quantity data, we can't fit the demand model to history."

**Show the data-readiness check:**
- Point to all the ❌ missing fields (quantities, ASPs, rival prices)

**Say:** "The honest answer is: the model is *not yet empirically calibrated*. If the team had
JPR shipment data matched to SKU-level prices, we could estimate B and D statistically. For now,
the parameters are illustrative — and the app says so clearly."
""")

with st.expander("**Step 6 · Close (30 sec)**"):
    st.markdown("""
**Say:** "To summarise: under the illustrative parameters, Bertrand consistently predicts lower
prices and higher quantities than Cournot — matching the theoretical prediction that price
competition is harsher. The capacity scenario shows how an output constraint shifts rents from
NVIDIA to AMD. The key limitation: none of these outputs are calibrated to real data, so they
are counterfactuals, not predictions. The next step would be obtaining JPR shipment data and
running a structural demand estimation."
""")

st.divider()

# ---------------------------------------------------------------------------
st.header("❓ Likely Instructor Questions and Grounded Responses")
# ---------------------------------------------------------------------------

with st.expander("Q1: What is a Nash equilibrium, and why is it the solution concept?"):
    st.markdown("""
**A:** A Nash equilibrium is a strategy profile (q₁*, q₂*) or (p₁*, p₂*) such that no firm
can unilaterally improve its payoff by deviating. In the Cournot game, q₁* is NVIDIA's best
response to q₂* and q₂* is AMD's best response to q₁* — neither firm benefits from changing
output alone. The same mutual best-response logic applies to Bertrand prices.

Nash equilibrium is used because it captures rational, simultaneous strategic interaction —
each firm accounts for its rival's likely response.
""")

with st.expander("Q2: Why differentiated Bertrand, not homogeneous-good Bertrand (p = MC)?"):
    st.markdown("""
**A:** In homogeneous-good Bertrand, identical products force prices to marginal cost (Bertrand
paradox). But RTX 4080 and RX 7900 XTX are differentiated — customers don't treat them as
perfect substitutes. RTX users may prefer DLSS; RX users may prefer open ecosystems. The
differentiated model allows both firms to charge above marginal cost, which is empirically
reasonable. The D/B ratio controls the degree of substitutability; only at D/B → 1 does the
model approach the homogeneous-good case.
""")

with st.expander("Q3: What does D/B mean, and why is it bounded below 1?"):
    st.markdown("""
**A:** D/B is the substitutability ratio — how strongly a rival's price/quantity affects your
own demand, relative to your own price/quantity effect. When D/B = 0, products are independent.
When D/B → 1, products are nearly perfect substitutes.

The Bertrand direct-demand system has denominator B² − D², which is zero when D = B (D/B = 1).
This corresponds to perfectly substitutable products, where differentiated Bertrand collapses.
The app caps the slider at 0.95 to avoid numerical instability near this boundary.
""")

with st.expander("Q4: Why does the capacity cap matter, and what happens when it's nonbinding?"):
    st.markdown("""
**A:** A binding cap (q1_cap < unconstrained q₁*) forces NVIDIA to produce less than it would
optimally choose. AMD's best response is to produce more (since rival output is lower, AMD's
marginal revenue is higher). This shifts output — and rents — toward AMD.

When the cap is nonbinding (q1_cap ≥ q₁*), NVIDIA wouldn't choose to produce that much anyway,
so the cap has no effect. The unconstrained equilibrium applies exactly. This is the correct
economic treatment of a maximum constraint, as opposed to incorrectly forcing q₁ = q1_cap
regardless of whether it binds.
""")

with st.expander("Q5: Why can't MSRP data calibrate the demand model?"):
    st.markdown("""
**A:** Calibrating a demand model requires observing how quantity responds to price variation.
MSRP data gives us one price per SKU at launch — no quantity, no variation over time, no
rival price at the same moment for the same consumer population. Even if MSRP were a valid
price proxy, a table of 8 launch prices is too small and lacks the variation needed to identify
two slope parameters (B and D) and a market size (A).

Additionally, prices and quantities are jointly determined — endogeneity means we'd need
instruments or specific variation to estimate causal demand slopes. MSRP alone doesn't solve
the identification problem.
""")

with st.expander("Q6: Why can't the model establish actual NVIDIA/AMD profits?"):
    st.markdown("""
**A:** The model computes (price − cost_input) × quantity. This is a *model contribution payoff*,
not reported profit because:

1. `c₁` and `c₂` are illustrative scenario inputs, not true marginal costs
2. Firms have fixed costs, R&D, SG&A, taxes, and multi-segment accounting
3. Quantities are in model units, not actual card shipments
4. The model omits inventory, channel margins, and regional price variation

NVIDIA's actual gaming segment revenue, gross margin, and operating income come from its 10-K
filings — none of those numbers come from this model.
""")

with st.expander("Q7: Could asymmetric D (D₁₂ ≠ D₂₁) change the results?"):
    st.markdown("""
**A:** Yes — if NVIDIA customers are less price-sensitive to AMD than AMD customers are to
NVIDIA, then D₁₂ ≠ D₂₁ and the symmetric model is an approximation. An asymmetric version
would require separate demand equations for each firm and could yield different equilibria.

The plan.md notes this as a potential extension if calibration data allows it. For version 1,
the symmetric model is a standard starting point for differentiated duopoly analysis.
""")

st.divider()

# ---------------------------------------------------------------------------
st.header("📋 Key Limitations to State in the Writeup")
# ---------------------------------------------------------------------------
st.markdown("""
These limitations should be clearly stated in the research report to prevent overclaiming:

1. **Not empirically calibrated** — parameters are illustrative; no compatible demand data exists yet
2. **Linear demand approximation** — real GPU demand is likely nonlinear at price extremes
3. **Static one-shot game** — no dynamics, inventory, mid-cycle price cuts, or anticipation effects
4. **Two firms only** — Intel Arc, Qualcomm, and others are excluded; this is a two-firm submarket model
5. **Symmetric D** — asymmetric substitutability is not modelled in v1
6. **MSRP ≠ transaction price** — the MSRP table is descriptive context, not model calibration
7. **Model payoff ≠ reported profit** — missing fixed costs, taxes, segment allocation
8. **Capacity cap is hypothetical** — no observed TSMC allocation or production capacity data
9. **Interior solutions only** — boundary equilibria (firm exits market) are not implemented

The project can be presented as a **theoretical interactive simulator** demonstrating game-theory
concepts. It cannot be presented as an empirically validated market model without completing
the calibration steps described in `data/data_dictionary.md`.
""")

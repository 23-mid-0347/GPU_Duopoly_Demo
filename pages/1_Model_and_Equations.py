"""
pages/1_Model_and_Equations.py
==============================
Explains the game, notation, equations, equilibrium meaning, and assumptions.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

st.set_page_config(page_title="Model & Equations — GPU Duopoly", layout="wide", page_icon="📐")



st.title("📐 Model Definition and Equations")

st.markdown("""
This page presents the formal demand system, equilibrium concepts, and closed-form solutions
used throughout the simulator. All notation matches `report.md`.
""")

# ---------------------------------------------------------------------------
st.header("1 · Players and Strategies")
# ---------------------------------------------------------------------------
st.markdown("""
| Symbol | Meaning |
|---|---|
| Firm 1 | **NVIDIA** |
| Firm 2 | **AMD** |
| **Cournot strategies** | Quantities `q₁`, `q₂` — each firm chooses how much to produce |
| **Bertrand strategies** | Prices `p₁`, `p₂` — each firm chooses its posted price |

The equilibrium concept in both games is **Nash equilibrium**: each firm's strategy is
a best response to the rival's strategy.
""")

# ---------------------------------------------------------------------------
st.header("2 · Inverse-Demand System")
# ---------------------------------------------------------------------------
st.markdown("""
We use a symmetric linear inverse-demand model. Given quantities `(q₁, q₂)`,
equilibrium prices are:
""")

st.latex(r"""
p_1 = A - B q_1 - D q_2, \qquad p_2 = A - B q_2 - D q_1
""")

st.markdown("""
| Parameter | Symbol | Admissible range | Meaning |
|---|---|---|---|
| Demand intercept | `A` | finite | Price when both quantities are zero |
| Own-quantity slope | `B` | `B > 0` | Price falls by `B` per unit of own output |
| Cross-quantity term | `D` | `0 ≤ D < B` | Price falls by `D` per unit of rival output |
| Substitutability ratio | `D/B` | `[0, 0.95)` | Dimensionless; slider control |

**Important:** `B` and `D` are inverse-demand slopes, not regression coefficients from
a quantity-on-price equation. The two mappings differ and require a documented identification method.
""")

with st.expander("Why D/B < 1?"):
    st.markdown("""
The Bertrand direct-demand system has denominator `B² - D²`.  
When `D → B`, this denominator → 0 and the system becomes singular (products are perfect substitutes
and differentiated Bertrand collapses to Bertrand-Nash with `p = MC`).  
The simulator caps the slider at **D/B ≤ 0.95** to stay well away from this boundary.
""")

# ---------------------------------------------------------------------------
st.header("3 · Direct Demand (Bertrand system)")
# ---------------------------------------------------------------------------
st.markdown("Inverting the demand system gives quantities as functions of prices:")
st.latex(r"""
q_1(p_1, p_2) = \frac{(B-D)A - Bp_1 + Dp_2}{B^2 - D^2}
""")
st.latex(r"""
q_2(p_1, p_2) = \frac{(B-D)A - Bp_2 + Dp_1}{B^2 - D^2}
""")
st.info("These are **not** homogeneous-good demand functions. With differentiated products, both firms earn positive margins at the Nash equilibrium price.")

# ---------------------------------------------------------------------------
st.header("4 · Cournot Equilibrium")
# ---------------------------------------------------------------------------
st.markdown("**Payoffs** (firm 1 notation; analogous for firm 2):")
st.latex(r"""
\pi_1 = (A - Bq_1 - Dq_2 - c_1)\,q_1
""")
st.markdown("**First-order conditions** (necessary for interior Nash equilibrium):")
st.latex(r"""
A - 2Bq_1 - Dq_2 - c_1 = 0, \qquad A - 2Bq_2 - Dq_1 - c_2 = 0
""")
st.markdown("**Reaction functions:**")
st.latex(r"""
q_1 = \frac{A - c_1 - Dq_2}{2B}, \qquad q_2 = \frac{A - c_2 - Dq_1}{2B}
""")
st.markdown("**Interior equilibrium quantities:**")
st.latex(r"""
q_1^* = \frac{2B(A-c_1) - D(A-c_2)}{4B^2 - D^2}, \qquad
q_2^* = \frac{2B(A-c_2) - D(A-c_1)}{4B^2 - D^2}
""")
st.markdown("Prices are then recovered from the inverse-demand system. Margins and payoffs:")
st.latex(r"""
m_i = p_i - c_i, \qquad \pi_i = m_i \cdot q_i
""")

# ---------------------------------------------------------------------------
st.header("5 · Differentiated Bertrand Equilibrium")
# ---------------------------------------------------------------------------
st.markdown("Define auxiliary terms (not raw demand slopes):")
st.latex(r"""
r_1 = (B-D)A + Bc_1, \qquad r_2 = (B-D)A + Bc_2
""")
st.markdown("**Interior equilibrium prices:**")
st.latex(r"""
p_1^* = \frac{2Br_1 + Dr_2}{4B^2 - D^2}, \qquad
p_2^* = \frac{Dr_1 + 2Br_2}{4B^2 - D^2}
""")
st.markdown("Quantities are recovered via direct demand; then margins and payoffs as above.")

with st.expander("Why prices are higher under Bertrand than Cournot (differentiated case)"):
    st.markdown("""
Counter-intuitively, **differentiated Bertrand prices are *lower*** than Cournot prices for the same
parameters — not higher. This matches standard theory: price competition is harsher than quantity
competition under product differentiation.

- Under Cournot, firms take rival quantity as fixed → higher equilibrium prices.
- Under Bertrand, each firm is tempted to undercut → lower equilibrium prices.

This is illustrated live on the **Live Equilibrium** page. The direction depends on computed values —
check the current parameters for the actual comparison.
""")

# ---------------------------------------------------------------------------
st.header("6 · Special Case: D = 0 (Independent Monopolies)")
# ---------------------------------------------------------------------------
st.markdown("""
When products are completely independent (`D = 0`), both games reduce to independent monopolies.
For firm `i` where `A > cᵢ`:
""")
st.latex(r"""
q_i^* = \frac{A - c_i}{2B}, \qquad
p_i^* = \frac{A + c_i}{2}, \qquad
\pi_i^* = \frac{(A - c_i)^2}{4B}
""")
st.success("This identity is verified in the test suite (test_cournot.py, test_bertrand.py).")

# ---------------------------------------------------------------------------
st.header("7 · Capacity-Constrained Cournot (Hypothetical)")
# ---------------------------------------------------------------------------
st.markdown("""
Treat `q1_cap` as a **maximum** on NVIDIA's output — not a forced production level.

1. Solve the unconstrained Cournot equilibrium.
2. If `q1_cap ≥ q1*` → cap is **nonbinding**; return the unconstrained equilibrium.
3. If `0 ≤ q1_cap < q1*` → cap **binds**; set `q1 = q1_cap` and AMD best-responds:
""")
st.latex(r"""
q_2 = \max\!\left(0,\; \frac{A - c_2 - D\,q_1}{2B}\right)
""")
st.markdown("""
Prices, margins, and payoffs are then recomputed via the shared inverse-demand system.

> **Label:** *NVIDIA output cap (hypothetical)*. This is **not** an observed TSMC wafer allocation.
""")

# ---------------------------------------------------------------------------
st.header("8 · Output Metrics")
# ---------------------------------------------------------------------------
st.markdown("""
| Metric | Formula | Unit |
|---|---|---|
| Equilibrium price `pᵢ` | from inverse/direct demand | model price units |
| Equilibrium quantity `qᵢ` | from Cournot/Bertrand solver | model units (illustrative) |
| Per-unit margin `mᵢ` | `pᵢ − cᵢ` | model price units |
| Model payoff `πᵢ` | `(pᵢ − cᵢ) × qᵢ` | model price units × model units |

**Model payoff ≠ reported profit.** Payoffs omit fixed costs, taxes, multi-segment
accounting, and all other adjustments present in GAAP income statements.

**Margin `mᵢ = pᵢ − cᵢ`** is a per-unit amount in model price units — not a percentage margin.
""")

# ---------------------------------------------------------------------------
st.header("9 · Assumptions and Limitations")
# ---------------------------------------------------------------------------
st.markdown("""
| Assumption | Consequence |
|---|---|
| Linear symmetric demand | Closed-form solution exists; non-linear effects are not captured |
| Static one-shot game | No dynamics, inventory, or inter-temporal strategies |
| Constant marginal cost | No economies of scale or capacity utilisation effects |
| Two firms only | Intel Arc and others not modelled |
| Symmetric `D` | Both products have the same cross-demand sensitivity (could be asymmetric) |
| Interior solution | Boundary solutions (a firm exits) are not implemented in v1 |
| Illustrative parameters | Not calibrated to real price/quantity data |

For a discussion of identification requirements for structural demand estimation in this
setting, see Berry & Haile (2016) — linked on the Overview page.
""")

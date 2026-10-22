# NVIDIA vs. AMD in the Discrete GPU Market: A Game-Theoretic Study of Cournot and Differentiated Bertrand Competition

**Working research report and implementation specification**  
**Prepared:** 22 October 2026  
**Project basis:** Team `plan.md` and `gpu-duopoly-model.jsx` prototype supplied for this project  
**Intended paper style:** IEEE conference-paper structure; the final submission must be transferred into the instructor's required IEEE Word/LaTeX template.

> **Important research-status statement.** This document is a comprehensive research/design draft, not proof that the model has already been empirically calibrated. The supplied React application explicitly contains illustrative placeholder values for the market intercept, demand slopes, market shares, and cost proxies. The calculations below reproduce the model using those values so that the mathematics and demo can be checked. They must not be described as measured market outcomes. The empirical conclusions can only be finalized after the team obtains and documents appropriate quantity/price data, estimates parameters correctly, and validates the model.

---

## Contents

1. Executive summary and status
2. IEEE-ready abstract and index terms
3. Problem statement, research questions, objectives, and hypotheses
4. Relationship to the existing team plan
5. Market definition and what public evidence can support
6. Verified launch-price evidence and gaps in the prototype dataset
7. Model, notation, assumptions, and game rules
8. Full mathematical derivations
9. Worked calculations using the prototype's baseline values
10. Capacity-constrained quantity game
11. Empirical data design and parameter-estimation protocol
12. Marginal-cost proxy design
13. Influencing factors and omitted variables
14. Validation metrics and experimental protocol
15. Audit of `gpu-duopoly-model.jsx`
16. End-to-end interactive demo specification and presentation script
17. Implementation algorithm and test plan
18. Limitations, risks, and interpretation rules
19. Work plan and team responsibilities
20. IEEE paper preparation notes
21. Comprehensive completion checklist
22. References

---

# 1. Executive summary and status

This project studies strategic competition between NVIDIA and AMD in the desktop discrete graphics-card market. The supplied plan proposes two competing game-theoretic models using a shared linear differentiated-product demand system:

- **Cournot quantity competition:** each firm chooses quantity while taking the rival's quantity as given.
- **Differentiated Bertrand price competition:** each firm chooses price while taking the rival's price as given.
- **Capacity-constrained Cournot scenario:** NVIDIA's output is capped and AMD chooses its best response.

The proposed application makes the model observable: a user changes model parameters, and the application recalculates equilibrium prices, quantities, per-unit margins, profits, and comparison charts. The intended research question is whether restrictions on quantity, differentiated demand, and cost differences can help explain why the firms may sustain different price/margin outcomes.

The core equations can be derived analytically. The current code's baseline equilibrium calculations are consistent with the symmetric linear inverse-demand model, but the existing data and some UI/constraint handling require correction before the project can claim an empirical finding. In particular:

1. The current code comments label several data values as placeholders. The market intercept and demand slopes are not estimated; cost values are not sourced manufacturing-cost observations; the historic share values are not supported by a cited dataset.
2. The parameter control displays `D/B` but writes the slider's raw value to `D`, so its displayed value and effective parameter become inconsistent after interaction.
3. The capacity scenario fixes NVIDIA's quantity at the selected value even when that quantity is above its unconstrained equilibrium. A cap should constrain a profit-maximizing choice; it should not force the firm to produce the cap quantity if the cap is nonbinding.
4. A regression of quantity on price does not return the inverse-demand parameters `B` and `D` directly. The calibration section below gives the correct parameter mapping and explains price endogeneity.
5. Public MSRP data can describe announced launch prices, but they do not reveal product-level unit sales. Company-wide “Gaming” revenue is not a clean measure of desktop discrete GPU sales. A genuine empirical calibration needs additional data or a narrower, explicitly illustrative claim.
6. The total add-in-board market includes Intel as well as NVIDIA and AMD; an NVIDIA–AMD two-firm model must explicitly define its scope or treat other vendors as an excluded outside option. Jon Peddie Research describes its AIB reports as covering desktop, workstation, and data-center display/computing boards, so its total market is broader than a consumer-gaming-only market [1], [2].

**Recommended submission position:** present the project as a game-theoretic model plus an interactive, reproducible scenario simulator. Report an empirical explanation only if the team completes the data collection and estimation steps specified here. If that data is unavailable by the deadline, disclose that limitation plainly and do not report placeholder-driven MAE values as evidence about real firms.

# 2. IEEE-ready abstract and index terms

## Abstract

This study develops an interactive game-theoretic model of price and quantity competition between NVIDIA and AMD in the discrete graphics-card market. A symmetric linear inverse-demand system is used to derive Nash equilibria under Cournot quantity competition and differentiated Bertrand price competition. A capacity-constrained Cournot scenario is also specified to represent the effect of a binding output limit. The model calculates equilibrium prices, quantities, per-unit contribution margins, and profits, and exposes the inputs through an interactive visualization so that counterfactual scenarios can be tested live. Publicly announced launch prices and market-structure reports are reviewed as potential evidence sources. However, launch prices, supplier-level shipment shares, and company-level Gaming revenues do not by themselves identify product-level demand parameters or true marginal costs. Therefore, placeholder-driven calculations are separated from empirical evidence, and a reproducible data and calibration protocol is specified. The current prototype is audited for parameter-control and capacity-constraint issues that could otherwise mislead users. The resulting deliverable is intended to connect equilibrium theory, transparent assumptions, evidence provenance, model validation, and an explainable live demonstration.

**Index Terms—** Cournot competition, differentiated Bertrand competition, Nash equilibrium, discrete graphics processing units, demand estimation, capacity constraints, interactive economic simulation.

> Replace the abstract's final wording only after the final run is complete. Do not add empirical claims, effect sizes, or “the model proves” language unless the results are supported by the final data and test logs.

# 3. Problem statement, research questions, objectives, and hypotheses

## 3.1 Problem statement

NVIDIA and AMD offer graphics cards that compete for some of the same buyers but are not perfectly identical products. Buyers may care about price, rasterization and ray-tracing performance, video memory, power consumption, software support, game-specific performance, creator/AI workloads, product availability, and other features. A textbook model of homogeneous-good Bertrand competition can be a poor literal description of this setting. The team therefore plans to use differentiated demand and compare the strategic implications of choosing output versus choosing price.

The economic question is not simply which company lists the lower MSRP. It is how equilibrium outcomes change when demand substitution, marginal-cost proxies, or output limits change, and whether a specified model can reproduce market observations closely enough to be informative.

## 3.2 Main research question

**How do the predicted equilibrium price, quantity, and profit outcomes for NVIDIA and AMD differ under Cournot quantity competition and differentiated Bertrand price competition, and how do demand substitutability, cost asymmetry, and a binding output cap change those outcomes?**

## 3.3 Secondary questions

1. How do model outcomes change as the cross-product substitution parameter `D` increases relative to own-quantity slope `B`?
2. How do cost asymmetries affect each firm's price, quantity, margin, and profit?
3. When does a binding cap on NVIDIA's quantity change equilibrium outcomes, and what happens when the cap is nonbinding?
4. Can publicly available data support estimation of the model's demand and cost parameters, or can it support only descriptive price comparisons and illustrative simulations?
5. After proper estimation and validation, does either game's price prediction fit held-out observations better? This remains an empirical question, not a foregone conclusion.

## 3.4 Objectives

- Define a market scope that matches the data used.
- Derive Cournot and differentiated Bertrand equilibria from the same demand system.
- Implement the equations transparently and show calculations in the interface.
- Clearly distinguish measured data, source-backed MSRP, estimated quantities, estimated cost proxies, and manually chosen scenario inputs.
- Measure predictive error only where observations and model inputs are appropriate and documented.
- Demonstrate counterfactuals live without implying that slider inputs represent proprietary real-world cost or capacity figures.
- Produce an IEEE-structured paper and a reproducible demo with a data/code checklist.

## 3.5 Hypotheses to test

These are hypotheses and theoretical expectations, not completed findings.

- **H1 — Interaction:** with `D = 0`, each firm's market is independent in the specified model and the Cournot and Bertrand solutions coincide.
- **H2 — Symmetric case:** for symmetric costs and the admissible parameter region `0 ≤ D < B`, stronger substitution should intensify strategic interaction. The numerical experiment should display the resulting price, quantity, and profit patterns; the report must not assume every individual-firm comparative static under asymmetric costs without checking it.
- **H3 — Model comparison:** after valid estimation and held-out validation, Cournot and differentiated Bertrand may have different price prediction errors. Which model fits better is an empirical result and must not be chosen in advance.
- **H4 — Binding cap:** when NVIDIA's feasible output cap is below its unconstrained Cournot equilibrium quantity, the cap binds and its output is fixed at the cap; AMD's best response and both prices then adjust. When the cap is at or above the unconstrained quantity, it should not change the unconstrained equilibrium.
- **H5 — Data adequacy:** announced MSRP and company-level revenue alone will not be sufficient to identify a fully credible SKU-level demand model. This is a data-availability issue to document, not something the interactive UI can solve by itself.

# 4. Relationship to the existing team plan

The following preserves the supplied `plan.md` structure and clarifies what is needed before the final result can be called empirical.

| Existing plan item | Preserved design | Clarification required before final submission |
|---|---|---|
| Thesis | NVIDIA–AMD differentiated-product duopoly; compare Cournot and Bertrand | Define the exact market, geography, product tier, and time window. State how Intel and other suppliers are handled. |
| Shared demand system | `p1 = A − Bq1 − Dq2`; `p2 = A − Bq2 − Dq1` | State units and admissible parameter conditions; verify the same model is used in both games. |
| Cournot model | Simultaneous quantity decisions | Derive and test the analytical best responses and Nash solution. |
| Bertrand model | Simultaneous prices with differentiated demand | Invert the demand system and derive price best responses; ensure `B² − D² > 0`. |
| Capacity variant | NVIDIA output cap and AMD best response | Implement a true upper bound; do not force output above the unconstrained optimum. Describe this as a hypothetical cap unless an actual quantity limit is sourced. |
| Data lead | JPR, launch MSRP, segment revenue, die size and wafer-cost proxy | JPR summary data may not expose SKU-level quantities; segment revenue has a broader accounting scope. Record data coverage and missingness. |
| Calibration lead | Estimate parameters and wire them into the app | Correct the regression interpretation; price endogeneity and inadequate sample size must be addressed. |
| Validation | Predicted vs. actual prices and MAE | Use sourced actual prices, measured/defensible costs, calibrated parameters, a comparison baseline, and preferably held-out validation. |
| Interactive app | Hero, model setup, prices, sliders, validation | Add provenance labels, live equation details, data status, model limitations, and testable scenario logs. |
| Stretch goal | Asymmetric substitutability; nested logit | Only attempt after the symmetric base model passes its tests and the data support additional parameters. |

The four-week schedule in the plan can be used as a relative sequence, but no calendar deadlines or team-member identities have been supplied. Assign owners explicitly with the team before treating the timeline as committed.

# 5. Market definition and what public evidence can support

## 5.1 Proposed primary scope

**Preferred scope:** consumer desktop discrete graphics cards sold by NVIDIA and AMD, analyzed over clearly specified product tiers and launch/retail windows.

That scope is narrower than several readily available public datasets. Jon Peddie Research describes its Add-in Board report as a quarterly report on PC graphics controllers for desktop, workstation, and data-center display and computing, with shipment and segment market-share data [2]. Its public Q1 2026 summary reports approximately 11.8 million global PC graphics add-in-board shipments, but the measure is total AIB market activity—not a SKU-level gaming-only sales panel [1].

The wider AIB market also includes Intel. JPR's Q1 2026 summary explicitly discusses NVIDIA, AMD, and Intel share movements [1]. Therefore, a two-player NVIDIA–AMD model needs one of these approaches:

1. **Restricted two-firm submarket:** define the modeled demand as sales among selected NVIDIA and AMD alternatives only, and say that Intel/other products are outside the model. Do not describe that as the entire discrete GPU market.
2. **Three-firm model:** add Intel as a third competitor and rederive the system. This is a larger model and is not part of the current prototype.
3. **Outside-option model:** model an outside option or the residual market share, which requires a consistent demand specification and data. Do not simply renormalize shares without explaining what that changes.

The recommended course-project scope is option 1 for the first working version, with the limitation made prominent.

## 5.2 Why company revenue is not enough

NVIDIA's filings describe its Gaming platform as including GeForce GPUs for desktop and laptop PCs, GeForce NOW, console SoCs, and related products/services [11]. AMD's fiscal-2025 filing reports Gaming revenue in a combined Client and Gaming segment and describes drivers that include Ryzen processors, semi-custom console SoCs, and Radeon gaming GPUs [12]. These accounting categories are useful context but are not clean measures of NVIDIA desktop GPU units or AMD desktop GPU units.

It would be invalid to divide these total segment revenues by a desktop-card MSRP and treat the quotient as observed desktop-card units. The scope mismatch must be solved with suitable data or retained as a stated limitation.

## 5.3 Price measures are not interchangeable

- **MSRP/SEP:** announced suggested launch price; easy to verify but not necessarily the price at which cards actually sold.
- **Street price:** actual retailer price over time; more useful for consumer price response but requires reliable historical tracking.
- **Average selling price (ASP):** revenue divided by units for the correct product scope; useful if both numerator and denominator refer to the same market.
- **Company segment revenue:** too broad for per-SKU quantity unless supported by a defensible allocation method.

Do not mix the MSRP of one SKU, a rival's street price months later, and a company-wide shipment estimate without labeling the time, scope, and units. A matched panel is preferable.

# 6. Verified launch-price evidence and gaps in the prototype dataset

The following official launch-price statements can be used for a **descriptive launch-MSRP table**. They do not provide unit sales and do not by themselves estimate demand.

| Product | Official announced price used here | Source | Compatibility / caveat |
|---|---:|---|---|
| NVIDIA GeForce RTX 4080 (16 GB version) | USD 1,199 | NVIDIA's RTX 40-series announcement [10] | The announcement also discussed a different 12 GB RTX 4080 configuration at a different price; identify the 16 GB SKU explicitly. |
| AMD Radeon RX 7900 XTX | USD 999 | AMD launch announcement [7] | MSRP/SEP, not guaranteed street price. |
| NVIDIA GeForce RTX 4070 | USD 599 | NVIDIA announcement dated April 12, 2023 [9] | MSRP/launch price, not unit sales. |
| AMD Radeon RX 7800 XT | USD 499 | AMD launch announcement [8] | Announced in August 2023; not the same launch month as RTX 4070. |
| NVIDIA GeForce RTX 5080 | USD 999 | NVIDIA official product/launch information [3], [5] | Launch in January 2025. |
| AMD Radeon RX 9070 XT | USD 599 | AMD official RX 9000 launch announcement [4] | Announced availability from March 6, 2025. |
| NVIDIA GeForce RTX 5070 | USD 549 | NVIDIA official RTX 50-series announcement [5] | Specify its actual launch window; do not assume same-day availability with the AMD comparison card. |
| AMD Radeon RX 9060 XT 16 GB | USD 349 | AMD official COMPUTEX announcement [6] | The 8 GB configuration is USD 299. The app's `349` must be labeled as the **16 GB** SKU. |

### 6.1 Product-pairing concerns

The prototype currently groups the following pairs:

- RTX 4080 / RX 7900 XTX
- RTX 4070 / RX 7800 XT
- RTX 5080 / RX 9070 XT
- RTX 5070 / RX 9060 XT 16 GB

These are useful illustrative comparisons, but should not automatically be called perfectly matched substitutes. Their release dates differ, performance is not identical across products, feature bundles differ, and the last pair is especially sensitive to the definition of performance tier. A rigorous price-response study should add measured performance/quality controls (for example, a fixed set of benchmark tests, resolution, game mix, settings, and driver dates) or explain the matching rule.

### 6.2 Values in the current code that are not yet evidence

The supplied `gpu-duopoly-model.jsx` defines `A = 1400`, `B = 2.5`, current `D = 1.2`, default cost values `c1 = 550` and `c2 = 420`, and four `HIST` rows with cost proxies. It also contains share values `82`, `80`, `84`, and `85`. The file's comments explicitly call these illustrative placeholder values. No source or estimation is supplied for the share figures or the cost proxies, and the share field is not used in the current validation output.

Treat these as test inputs only. Do not cite them as market facts or as the output of a regression.

# 7. Model, notation, assumptions, and game rules

## 7.1 Players and strategies

- Player 1: NVIDIA.
- Player 2: AMD.
- In the **Cournot game**, each player selects a nonnegative output quantity, `q1` or `q2`.
- In the **Bertrand game**, each player selects a nonnegative price, `p1` or `p2`.
- In the **capacity-constrained Cournot scenario**, NVIDIA's quantity must satisfy `0 ≤ q1 ≤ q1_cap`; AMD chooses `q2 ≥ 0`.

The labels identify the two firms in the simulation, but the parameters are not a representation of confidential company decisions.

## 7.2 Symbols and units

| Symbol | Meaning | Unit / interpretation |
|---|---|---|
| `A` | Intercept in each firm's inverse-demand equation | Price units, e.g. USD per card, for a specified quantity normalization |
| `B` | Own-quantity slope | Price change per model quantity unit |
| `D` | Cross-quantity slope / substitution term | Price change per rival quantity unit |
| `q1`, `q2` | NVIDIA and AMD output/sales quantities | Must be defined by the data. Prototype units are arbitrary model units, not observed cards. |
| `p1`, `p2` | NVIDIA and AMD prices | USD per card only if the price data are USD and the model is calibrated to those observations |
| `c1`, `c2` | Constant marginal-cost inputs | USD per model quantity unit only if cost and quantity scales match; presently illustrative proxies |
| `π1`, `π2` | Profit/payoff in the model | `(price − marginal cost) × quantity`; not firm-reported profit |
| `q1_cap` | Hypothetical NVIDIA output limit | Quantity units consistent with `q1` |
| `D/B` | Dimensionless substitution index | Under the symmetric linear specification, 0 means no cross-quantity effect; values approaching 1 approach the singular homogeneous-good boundary |

**Units requirement:** `A`, `B`, `D`, and `q` cannot be assigned independently arbitrary scales once the model is estimated. If quantities are recorded in thousands of units rather than single units, the estimated slope coefficients change accordingly. The current UI does not define that scale, so its displayed quantities/profits are model outputs rather than actual market-unit estimates.

## 7.3 Inverse demand

The shared symmetric linear inverse-demand system is

\[
p_1 = A - Bq_1 - Dq_2,
\qquad
p_2 = A - Bq_2 - Dq_1.
\]

Here `B > 0` measures the effect of a firm's own quantity on its price; `D ≥ 0` measures the effect of rival output on that price. With positive `D`, the rival's output lowers the price in this inverse-demand form. This is consistent with substitute products.

For the direct-demand inversion and the interior Bertrand solution to be well-defined, require `B > D ≥ 0` (so `B² − D² > 0`). The model also requires valid costs and equilibria with nonnegative quantities. Parameter controls should prevent or explicitly handle any input combination that yields negative quantities or economically infeasible prices.

## 7.4 Payoffs

For a firm with output `q_i`, price `p_i`, and constant marginal cost `c_i`, its operating payoff is

\[
\pi_i=(p_i-c_i)q_i.
\]

This simple payoff omits fixed costs, R&D, marketing, tax, financing, product mix, retailer/board-partner margins, memory and board components if not included in cost, and dynamic inventory effects. In the prototype, the calculated value should be called **model profit** or **contribution payoff**, not NVIDIA's or AMD's actual profit.

## 7.5 Nash equilibrium meaning

A Nash equilibrium is a set of strategies in which each firm's strategy is a best response to the rival's strategy. In Cournot, neither firm can increase its model payoff by unilaterally changing its quantity. In Bertrand, neither can increase its payoff by unilaterally changing its price. A numerical result is an equilibrium only when the best-response conditions and feasibility conditions are satisfied—not merely because a chart displays a number.

## 7.6 Baseline assumptions

1. Two modeled firms only; Intel/other vendors are excluded from the modeled submarket unless the team expands the model.
2. Symmetric functional form for the baseline demand system.
3. One-shot static game for each simulated market window.
4. Firms know the model parameters and costs (complete information).
5. Each firm maximizes its specified payoff.
6. Constant marginal costs within a scenario.
7. Quantities/prices are continuous in the algebraic solution; actual GPU production and retail prices are discrete.
8. There are no fixed costs or entry/exit decisions in the core model.
9. Features and product differentiation are compressed into the demand parameters instead of modeled directly.
10. `A`, `B`, `D`, and the cost values become empirical parameters only if a valid calibration estimates them from a compatible dataset. In the current code they are illustrative.

# 8. Full mathematical derivations

## 8.1 Cournot quantity competition

### Step 1 — Write each firm's payoff

Substitute inverse demand into the payoff function:

\[
\pi_1=(A-Bq_1-Dq_2-c_1)q_1,
\]
\[
\pi_2=(A-Bq_2-Dq_1-c_2)q_2.
\]

### Step 2 — Differentiate with respect to own quantity

Taking `q2` as fixed, NVIDIA's first-order condition (FOC) is

\[
\frac{\partial\pi_1}{\partial q_1}=A-2Bq_1-Dq_2-c_1=0.
\]

Likewise,

\[
\frac{\partial\pi_2}{\partial q_2}=A-2Bq_2-Dq_1-c_2=0.
\]

The second derivatives are `∂²π1/∂q1² = −2B` and `∂²π2/∂q2² = −2B`. When `B > 0`, each payoff is strictly concave in its own quantity, so an interior stationary point is a maximum. Nonnegative-quantity boundary cases still need to be checked if an estimated parameter set produces a nonpositive solution.

### Step 3 — Rearrange into best-response functions

\[
q_1=\frac{A-c_1-Dq_2}{2B},
\qquad
q_2=\frac{A-c_2-Dq_1}{2B}.
\]

These are the Cournot reaction functions: each firm's best-response quantity depends negatively on the rival's quantity if `D > 0`.

### Step 4 — Solve the simultaneous equations

The FOCs can be written as

\[
2Bq_1+Dq_2=A-c_1,
\qquad
Dq_1+2Bq_2=A-c_2.
\]

The determinant of the coefficient matrix is `4B² − D²`. Solving gives

\[
q_1^*=\frac{2B(A-c_1)-D(A-c_2)}{4B^2-D^2},
\]
\[
q_2^*=\frac{2B(A-c_2)-D(A-c_1)}{4B^2-D^2}.
\]

The React implementation uses an algebraically equivalent form. Let `k = D/(2B)`. Then

\[
q_1^*=\frac{(A-c_1)-k(A-c_2)}{2B(1-k^2)},
\qquad
q_2^*=\frac{(A-c_2)-k(A-c_1)}{2B(1-k^2)}.
\]

### Step 5 — Calculate prices, margins, and payoffs

\[
p_1^*=A-Bq_1^*-Dq_2^*,
\qquad
p_2^*=A-Bq_2^*-Dq_1^*.
\]

\[
m_1^*=p_1^*-c_1,\qquad m_2^*=p_2^*-c_2,
\]

\[
\pi_1^*=m_1^*q_1^*,\qquad \pi_2^*=m_2^*q_2^*.
\]

`m_i` is the model's per-unit margin, not a percentage margin. If a percentage is displayed, define whether the denominator is price or cost and calculate it separately.

## 8.2 Direct-demand system for Bertrand competition

The Bertrand game requires quantity demanded as a function of both firms' prices. Start with

\[
\begin{bmatrix}p_1\\p_2\end{bmatrix}
=\begin{bmatrix}A\\A\end{bmatrix}
-\begin{bmatrix}B&D\\D&B\end{bmatrix}
\begin{bmatrix}q_1\\q_2\end{bmatrix}.
\]

The inverse matrix exists if `B² − D² ≠ 0`. Inverting gives

\[
q_1(p_1,p_2)=\frac{(B-D)A-Bp_1+Dp_2}{B^2-D^2},
\]
\[
q_2(p_1,p_2)=\frac{(B-D)A-Bp_2+Dp_1}{B^2-D^2}.
\]

The sign pattern is important: the own-price coefficient is negative and the rival-price coefficient is positive, as expected for substitutes.

## 8.3 Differentiated Bertrand price competition

### Step 1 — Write payoffs using direct demand

\[
\pi_1=(p_1-c_1)q_1(p_1,p_2),
\qquad
\pi_2=(p_2-c_2)q_2(p_1,p_2).
\]

### Step 2 — Differentiate with respect to own price

Using the product rule,

\[
\frac{\partial\pi_1}{\partial p_1}=q_1+(p_1-c_1)\frac{\partial q_1}{\partial p_1}=0.
\]

Since `∂q1/∂p1 = −B/(B²−D²)`, multiplying through by `B²−D²` and substituting the direct-demand expression yields

\[
(B-D)A + Bc_1 + Dp_2 - 2Bp_1 = 0.
\]

Similarly,

\[
(B-D)A + Bc_2 + Dp_1 - 2Bp_2 = 0.
\]

Equivalently,

\[
2Bp_1-Dp_2=(B-D)A+Bc_1,
\]
\[
-Dp_1+2Bp_2=(B-D)A+Bc_2.
\]

### Step 3 — Solve for equilibrium prices

Let

\[
r_1=(B-D)A+Bc_1,\qquad r_2=(B-D)A+Bc_2.
\]

Then

\[
p_1^*=\frac{2Br_1+Dr_2}{4B^2-D^2},
\qquad
p_2^*=\frac{Dr_1+2Br_2}{4B^2-D^2}.
\]

This is equivalent to the current implementation's helper values

\[
m=\frac{D}{2B},\qquad
\text{base}_i=\frac{(B-D)A+Bc_i}{2B},
\]

\[
p_1^*=\frac{\text{base}_1+m\,\text{base}_2}{1-m^2},
\qquad
p_2^*=\frac{\text{base}_2+m\,\text{base}_1}{1-m^2}.
\]

### Step 4 — Recover quantities and payoffs

Use the direct-demand expressions from Section 8.2 to calculate `q1*` and `q2*`. Then calculate `m_i = p_i − c_i` and `π_i = (p_i − c_i)q_i` as in Cournot. Check that quantities are nonnegative and prices lie in the economically meaningful region. If not, the code must use a constrained/boundary solution or report that the scenario is infeasible rather than silently treating it as a valid interior equilibrium.

## 8.4 D = 0 sanity check

When `D = 0`, the demand system becomes

\[
p_i=A-Bq_i.
\]

Each firm operates independently. Both games must yield

\[
q_i^*=\frac{A-c_i}{2B},
\qquad p_i^*=\frac{A+c_i}{2},
\qquad \pi_i^*=\frac{(A-c_i)^2}{4B}
\]

when `A > c_i`. This is a critical unit test. The app's equations satisfy this equality algebraically.

## 8.5 What does `D/B` mean?

The ratio `D/B` summarizes the cross-quantity effect relative to the own-quantity effect under the symmetric specification. At `D/B = 0`, there is no cross-effect. As the ratio approaches `1`, the inverse-demand system approaches a homogeneous-good boundary and the direct-demand inversion becomes singular at exactly `D = B`. Do not set `D = B` in the direct-demand code. A value very close to `B` can also magnify numerical sensitivity, so the permitted slider range should stay strictly below that boundary and display any stability limitation.

`D/B` is a model parameter, not an observed statistic. It should only be called estimated substitutability when it has been inferred from an appropriate dataset using a documented method.

# 9. Worked calculations using the prototype's baseline values

This section independently checks the algebra with the values currently hard-coded in `gpu-duopoly-model.jsx`. **Every input in this example is illustrative, not calibrated market data.**

## 9.1 Inputs

| Parameter | Value | Status |
|---|---:|---|
| `A` | 1400 | Prototype constant; not estimated |
| `B` | 2.5 | Prototype constant; not estimated |
| `D` | 1.2 | Prototype starting value; not estimated |
| `c1` (NVIDIA cost input) | 550 | Prototype placeholder |
| `c2` (AMD cost input) | 420 | Prototype placeholder |
| `D/B` | `1.2 / 2.5 = 0.48` | Derived from placeholder values |
| `k = D/(2B)` | `1.2 / 5 = 0.24` | Derived |

The model quantity unit is not defined in the current application. Consequently, quantities and payoffs below are illustrative algebraic units. Prices are numerical outputs of the model but are not fitted forecasts of actual MSRP.

## 9.2 Cournot calculation, line by line

First calculate the shared denominator:

\[
2B(1-k^2)=5(1-0.24^2)=5(1-0.0576)=4.712.
\]

NVIDIA quantity:

\[
q_1^*=\frac{(1400-550)-0.24(1400-420)}{4.712}
=\frac{850-0.24(980)}{4.712}
=\frac{850-235.2}{4.712}
=\frac{614.8}{4.712}
\approx130.4754.
\]

AMD quantity:

\[
q_2^*=\frac{(1400-420)-0.24(1400-550)}{4.712}
=\frac{980-0.24(850)}{4.712}
=\frac{980-204}{4.712}
=\frac{776}{4.712}
\approx164.6859.
\]

NVIDIA price:

\[
\begin{aligned}
p_1^*&=1400-2.5(130.4754)-1.2(164.6859)\\
&\approx1400-326.1885-197.6231\\
&\approx876.1885.
\end{aligned}
\]

AMD price:

\[
\begin{aligned}
p_2^*&=1400-2.5(164.6859)-1.2(130.4754)\\
&\approx1400-411.7148-156.5705\\
&\approx831.7148.
\end{aligned}
\]

Per-unit margins:

\[
m_1=876.1885-550\approx326.1885,
\]
\[
m_2=831.7148-420\approx411.7148.
\]

Model payoffs:

\[
\pi_1\approx326.1885(130.4754)\approx42{,}559.56,
\]
\[
\pi_2\approx411.7148(164.6859)\approx67{,}803.62.
\]

**Interpretation limited to this synthetic scenario:** the model outputs greater quantity and payoff for AMD because the AMD cost input is lower in this example. That is a consequence of the chosen numbers and equations; it is not a finding about actual AMD output, costs, or earnings.

## 9.3 Bertrand calculation, line by line

Calculate

\[
m=\frac{D}{2B}=0.24,
\qquad 1-m^2=0.9424.
\]

For NVIDIA,

\[
\text{base}_1=\frac{(2.5-1.2)(1400)+2.5(550)}{5}
=\frac{1820+1375}{5}=639.
\]

For AMD,

\[
\text{base}_2=\frac{(2.5-1.2)(1400)+2.5(420)}{5}
=\frac{1820+1050}{5}=574.
\]

NVIDIA price:

\[
p_1^*=\frac{639+0.24(574)}{0.9424}
=\frac{776.76}{0.9424}
\approx824.2360.
\]

AMD price:

\[
p_2^*=\frac{574+0.24(639)}{0.9424}
=\frac{727.36}{0.9424}
\approx771.8166.
\]

The direct-demand denominator is

\[
B^2-D^2=2.5^2-1.2^2=6.25-1.44=4.81.
\]

NVIDIA quantity:

\[
\begin{aligned}
q_1^*&=\frac{(1.3)(1400)-2.5(824.2360)+1.2(771.8166)}{4.81}\\
&\approx\frac{1820-2060.5900+926.1799}{4.81}\\
&\approx142.5343.
\end{aligned}
\]

AMD quantity:

\[
\begin{aligned}
q_2^*&=\frac{(1.3)(1400)-2.5(771.8166)+1.2(824.2360)}{4.81}\\
&\approx\frac{1820-1929.5416+989.0832}{4.81}\\
&\approx182.8569.
\end{aligned}
\]

Margins and model payoffs:

| Measure | NVIDIA | AMD |
|---|---:|---:|
| Equilibrium price | 824.2360 | 771.8166 |
| Equilibrium quantity | 142.5343 | 182.8569 |
| Per-unit margin | 274.2360 | 351.8166 |
| Model payoff | 39,088.04 | 64,332.09 |

## 9.4 Baseline model comparison

| Metric | Cournot | Differentiated Bertrand |
|---|---:|---:|
| NVIDIA price | 876.1885 | 824.2360 |
| AMD price | 831.7148 | 771.8166 |
| NVIDIA quantity | 130.4754 | 142.5343 |
| AMD quantity | 164.6859 | 182.8569 |
| NVIDIA per-unit margin | 326.1885 | 274.2360 |
| AMD per-unit margin | 411.7148 | 351.8166 |
| NVIDIA model payoff | 42,559.56 | 39,088.04 |
| AMD model payoff | 67,803.62 | 64,332.09 |

For these starting inputs, the differentiated Bertrand prices and per-unit margins are lower, while quantities are higher. These are internally consistent outputs of the current parameterized example, not actual company results. Do not generalize this table to every asymmetric cost/parameter combination without testing the exact scenario.

## 9.5 Capacity scenario at the default cap

The prototype initializes `q1_cap = 120`. Under a **binding** cap, set `q1 = 120` and let AMD best-respond:

\[
q_2=\frac{A-c_2-Dq_1}{2B}
=\frac{1400-420-1.2(120)}{5}
=\frac{980-144}{5}=167.2.
\]

Prices become

\[
p_1=1400-2.5(120)-1.2(167.2)=899.36,
\]
\[
p_2=1400-2.5(167.2)-1.2(120)=838.00.
\]

Model payoffs are

\[
\pi_1=(899.36-550)(120)=41{,}923.20,
\]
\[
\pi_2=(838-420)(167.2)=69{,}889.60.
\]

Since the unconstrained Cournot quantity is approximately `130.4754`, a cap of `120` binds for this synthetic case. A cap above `130.4754` should not force NVIDIA to produce more than its unconstrained profit-maximizing output; the current implementation needs that nonbinding-case logic.

## 9.6 Prototype validation MAE is not a scientific result

At the code's initial `D = 1.2`, with its current uncalibrated `A`, `B`, and per-generation cost placeholders, the four-row illustration produces approximately:

- Cournot predicted NVIDIA prices: 915.42, 838.23, 878.34, and 814.36.
- Bertrand predicted NVIDIA prices: 867.74, 782.00, 826.99, and 755.69.
- The supplied actual-MSRP values: 1199, 599, 999, and 549.

Using the prototype's definition gives MAE of about **USD 227.21 for Cournot** and **USD 223.24 for Bertrand** at that starting parameter. The UI rounds these to around $227 and $223. These numbers must **not** be reported as evidence that Bertrand fits the real GPU market better: the model parameters/costs were not estimated, the four pairs are not a suitable held-out sample, and the chosen cost values are explicitly placeholders. This calculation only confirms how the current UI's MAE arithmetic behaves.

# 10. Capacity-constrained quantity game

## 10.1 Interpretation

A capacity cap is a scenario input, not a measured statement about NVIDIA's actual foundry allocation. The real production chain can be constrained by foundry capacity, packaging, memory, board production, yields, inventories, and allocations across many product families. The model includes just one exogenous bound for NVIDIA and holds all else fixed.

Rename the control **“NVIDIA output cap (hypothetical)”** unless the team obtains a source for an actual relevant output limit. A branded “TSMC-capped” toggle risks implying a verified real-world cap that the slider does not measure.

## 10.2 Correct cap logic

Let `q1_Cournot*` be the unconstrained equilibrium from Section 8.1.

- If `q1_cap ≥ q1_Cournot*`, the cap is nonbinding. Return the normal unconstrained Cournot equilibrium.
- If `0 ≤ q1_cap < q1_Cournot*` and AMD's best-response quantity is positive, set `q1 = q1_cap` and calculate

\[
q_2^*=\max\left(0,\frac{A-c_2-Dq_{1,cap}}{2B}\right).
\]

- Calculate both prices and payoffs using the common demand system.
- If any chosen output implies an infeasible or negative price under the modeled domain, warn the user and either solve the relevant constrained problem or block that parameter combination. Do not present the unconstrained closed-form result as valid without qualification.

The supplied function `capacityConstrainedCournot` sets `q1` equal to `q1_cap` for every cap value. It therefore models a **forced/precommitted output** when the cap is nonbinding, not a general upper-bound-constrained Cournot best response. That distinction needs correction in the implementation and paper.

# 11. Empirical data design and parameter-estimation protocol

## 11.1 Required dataset

The current prototype should not be called calibrated until the team can produce a versioned dataset, a code notebook/script that estimates parameters, and a log connecting each value to a source.

### Minimum data dictionary

| Field | Definition | Required? | Source / validation rule |
|---|---|---|---|
| `market_id` | Defined market scope, e.g. US consumer desktop GPU tier | Yes | Team methodology statement |
| `period_start`, `period_end` | Observation window | Yes | Date from data source |
| `geography` | Country/region | Yes | Keep comparable across firms |
| `firm` | NVIDIA or AMD in core model | Yes | Source definition |
| `sku` | Exact card SKU and VRAM configuration | For product-level study | Official product/spec page |
| `launch_date` | Official availability/launch date | Yes for launch study | Official announcement |
| `price_type` | MSRP, SEP, street price, or ASP | Yes | Never combine without explicit conversion/model |
| `price_usd` | Observed/sourced price in USD | Yes | Record observation date and retailer/source if street price |
| `quantity_units` | Units sold/shipped in the same market/window | Essential for quantity estimation | Document scope, unit, revision, and uncertainty |
| `quantity_source` | Source for quantity | Essential | Prefer SKU-level/compatible units; do not infer from broad revenue silently |
| `rival_price_usd` | Comparable rival SKU price in same period/region | For direct-demand regression | Matched time window and tier rule |
| `quality/performance_index` | Predefined comparative performance/quality metric | Strongly recommended | Benchmark method and source/date must be fixed |
| `die_area_mm2` | GPU die area | Optional for cost proxy | Exact chip and revision source |
| `process_node` | Manufacturing process designation | Optional for cost proxy | Source plus exact chip mapping |
| `wafer_cost_usd` | Estimate/quote for specific wafer process | Optional; not publicly uniform | Value, date, node, source, uncertainty label |
| `yield_estimate` | Fraction of dies passing yield assumptions | Optional for cost proxy | Source or sensitivity range; never hidden assumption |
| `cost_proxy_usd` | Derived unit cost estimate | If model uses costs | Include calculation, components included, and uncertainty |
| `source_url` | Primary source URL | Yes | Keep link and access date |
| `source_type` | Official / market analyst / review / estimate / assumption | Yes | Consistent evidence tags |

## 11.2 What the current sources can and cannot provide

- Official NVIDIA/AMD product releases provide announced SKU prices and stated availability [3]–[10]. They do not provide public unit sales for each matched retail SKU.
- JPR's public AIB summaries provide market context and shipment/share trends at the report's stated scope [1], [2]. The public summary alone is not the full underlying product-level panel, and the wider AIB coverage is not the same as consumer desktop gaming GPU sales.
- NVIDIA and AMD filings provide reported revenue at company/segment scope [11], [12]. Those categories do not isolate only the desktop discrete cards in the proposed model.
- Die-area and wafer-cost estimates may help construct a cost proxy, but wafer prices, yield, package/testing costs, memory, board design, cooler, and channel costs are distinct. The model must not label a partial semiconductor estimate as the true marginal cost of a finished graphics card.

If the team cannot access product-level unit data, retain a descriptive MSRP table and label the model **scenario analysis with assumed parameters**, not a data-estimated demand model. Do not reverse-engineer unit volume from incompatible revenue categories merely to fill a blank column.

## 11.3 Correct calibration logic

The team plan currently says to regress quantity on own price and rival price and treat the coefficients as `B` and `D`. That is **not the direct interpretation** of the specified inverse-demand parameters. The model's inverse demand is price as a function of quantities, while its direct-demand system has a different coefficient mapping.

There are two possible paths:

### Path A — Estimate direct demand, then map its coefficients

For a symmetric system, estimate with a compatible panel:

\[
q_{1t}=\alpha-\beta_{own}p_{1t}+\beta_{cross}p_{2t}+X_t\gamma+\varepsilon_{1t},
\]
\[
q_{2t}=\alpha-\beta_{own}p_{2t}+\beta_{cross}p_{1t}+X_t\gamma+\varepsilon_{2t},
\]

where `β_own > 0` is written here as the magnitude of the negative own-price effect, `β_cross ≥ 0` is the positive cross-price effect, and `X` contains declared controls. If no controls or extra intercept terms are used and the symmetric linear form is truly appropriate, the theoretical map is:

\[
s=-\text{coefficient on own price}>0,\qquad t=\text{coefficient on rival price}\ge0,
\]
\[
\frac{D}{B}=\frac{t}{s},\qquad
B=\frac{1}{s\left[1-(t/s)^2\right]},\qquad D=B(t/s).
\]

For the direct-demand intercept `g0 = A/(B+D)`, `A = g0(B+D)`. The mapping is only valid when the model form, quantity scale, symmetry, and coefficient units are consistent; with extra product-quality controls, varying market sizes, or richer demand forms, estimate the structural model accordingly rather than applying this shortcut.

### Path B — Estimate inverse demand directly

Regress price on own quantity and rival quantity in the specified inverse-demand form only if the data and model assumptions justify that equation. Then the coefficients on own and rival quantity can be mapped to `B` and `D`, respectively. But equilibrium prices/quantities can be jointly determined with unobserved demand shocks, so naïve ordinary least squares can be biased. Industrial-organization demand estimation literature emphasizes identification and the need for appropriate instruments when prices/quantities are endogenous [13].

### Endogeneity and identification warning

Observed price is often selected in response to unobserved demand conditions and costs. Quantity is also an equilibrium outcome. A fitted regression can show correlation rather than a causal demand response. For a defensible empirical estimate, the team should consult the instructor and either:

- use appropriate instruments/cost shifters and document the identification assumptions;
- use a structural demand estimation approach appropriate to the available data; or
- explicitly present coefficient values as illustrative scenario parameters and drop causal/empirical claims.

Do not make an instrumental-variable regression appear rigorous merely by adding arbitrary instruments. Each instrument needs a substantive exclusion argument and diagnostic checks.

## 11.4 Sample-size and design warning

Four generation-pair rows are not enough to estimate a multi-parameter structural demand system and then convincingly claim out-of-sample predictive accuracy. If the team uses only the four `HIST` entries, it can present them as a small descriptive MSRP comparison, not as sufficient estimation data. A larger panel should define product tier, geography, observation frequency, launch/retail period, quality controls, and quantity source before fitting.

## 11.5 Calibration workflow

1. **Freeze the market definition.** Record product scope, geography, period, and treatment of Intel/other products.
2. **Collect raw sources.** Preserve original CSVs/tables, links, access date, and source revision.
3. **Normalize observations.** Standardize dates, currency, units, SKU, price type, and the exact quantity definition.
4. **Match competitors.** State a tier/quality matching rule; do not pair products only because their names or generation numbers are similar.
5. **Inspect missing data.** Report missing quantity, price, and cost entries. Do not impute a market fact without recording the method.
6. **Plot/describe data.** Inspect price distributions, quantities, launch timing, market shares, and simple correlations before estimating.
7. **Estimate demand parameters.** Use a documented, theoretically compatible equation and address endogeneity.
8. **Estimate or bound cost proxies.** Document die, yield, wafer, packaging, memory/board assumptions and sensitivity range.
9. **Check parameter validity.** Require `B > 0`, `0 ≤ D < B`, valid cost units, and feasible predicted equilibrium.
10. **Store immutable calibration output.** Save parameter values, standard errors/uncertainty if available, model version, data hash/version, and estimation script.
11. **Run unit/structural tests.** Verify identities and FOCs.
12. **Validate on held-out data.** Avoid judging a model only on the rows used to tune parameters.
13. **Record results without spin.** Include all metrics, errors, sample size, comparison baseline, and limitations.
14. **Wire the output into the UI.** Show whether the visible values are `illustrative`, `estimated`, or `sourced directly`.

# 12. Marginal-cost proxy design

## 12.1 Do not call die-size inputs true marginal cost

The plan proposes die size multiplied by a wafer-cost estimate as a proxy. This can be a transparent approximation to part of the semiconductor cost, but it is not automatically the marginal cost of a sellable graphics card. Public foundry pricing is often estimated rather than disclosed as a single universal price, and chip cost depends on process, wafer size, yield, packaging, and production conditions [17].

The current code's `c1`, `c2`, and per-generation cost numbers are not the output of a documented cost calculation. They are placeholder input values and must remain labeled that way until calculated and sourced.

## 12.2 Optional die-cost calculation method

If the team can source a defensible wafer-cost estimate, a simple proxy may be built as follows. Each step must be documented; uncertain inputs need low/base/high scenarios.

Let:

- `W` = wafer diameter in millimeters (often 300 mm for the assumed wafer class, but verify for the process being modeled),
- `S` = GPU die area in mm²,
- `Cw` = wafer cost in USD for the exact process assumption,
- `Y` = die yield as a fraction between 0 and 1,
- `Cpkg/test` = packaging and testing cost per good die or chip, if sourced.

A commonly used approximate gross-dies-per-wafer calculation is

\[
N_{gross}\approx\frac{\pi(W/2)^2}{S}-\frac{\pi W}{\sqrt{2S}}.
\]

This is an approximation to geometric edge losses, not an exact count for a real wafer layout. Then an illustrative good-die estimate is

\[
N_{good}\approx N_{gross}Y,
\qquad C_{die}\approx\frac{C_w}{N_{good}}+C_{pkg/test}.
\]

For a multi-die package, sum the relevant die costs with the applicable yield/package assumptions. A finished add-in-board cost proxy would also need appropriate memory, substrate, PCB, voltage regulation, cooling, assembly, and other components. Avoid double counting any item already included in the chosen data.

## 12.3 Minimum reporting table for a cost proxy

| Item | Value | Source | Confidence/status |
|---|---:|---|---|
| Die area | Fill only when verified for exact chip | Product teardown/specification or specialist analysis | Sourced / uncertain |
| Process node | Fill only when verified | Foundry/vendor source | Sourced |
| Wafer price | Do not fill with a guessed point value | Credible estimate with date and method | Estimate, not disclosed fact |
| Gross dies per wafer | Calculated and reproducible | Formula above + geometric assumptions | Approximation |
| Yield | Sourced or varied in scenarios | Source/method stated | Estimate |
| Package/testing | Sourced or left out visibly | Source | Partial-cost warning |
| Finished-board components | Source or exclude visibly | Component/product sources | Partial-cost warning |
| `c1`, `c2` used by simulator | Final derived amount or scenario input | Calculation file | Calibrated estimate / scenario input |

If cost evidence cannot be assembled in time, use the cost sliders as explicit **scenario parameters** and remove wording that suggests actual NVIDIA/AMD marginal costs are known.

# 13. Influencing factors and omitted variables

The interface and report should explain how each factor enters the model and whether it is measured, estimated, or omitted.

| Factor | Economic role | Representation in baseline model | Evidence/status requirement |
|---|---|---|---|
| Market size / willingness to pay | Determines intercept `A` | One shared intercept | Estimate or label as scenario input |
| Own-output effect | More own quantity lowers own price in inverse demand | `B` | Estimate; document quantity units |
| Cross-firm substitution | Rival output affects own price | `D` and `D/B` | Estimate or illustrative slider; state symmetry assumption |
| Marginal-cost difference | Changes best responses, prices, and quantities | `c1`, `c2` | Sourced cost estimate or scenario input, not MSRP |
| Capacity/availability | Limits feasible output and can change best responses | `q1_cap` in extension | Actual cap not measured by default; model as hypothetical |
| GPU performance and product quality | Affects willingness to pay and substitution | Compressed into `A/B/D` in the baseline | Add measured quality controls or state omission |
| VRAM and memory bandwidth | Differentiates cards | Omitted explicitly | Product specifications can provide descriptive controls |
| Software ecosystem and feature support | Can alter switching and demand substitution | Omitted/compressed into `D` | Avoid claiming the model separately measures CUDA/DLSS/FSR effects unless data identify them |
| Driver maturity, game compatibility, ray tracing/upscaling | Changes quality for different workloads | Omitted | Use benchmark controls/consumer data if investigated |
| Launch timing and product availability | Changes observed price and quantity | Static, one-shot model omits dynamics | Match windows or add date/product-generation effects |
| Street price, promotions, bundles, tariffs, taxes, currency | Separates MSRP from actual market price | Omitted | Use a consistent market/region/time definition |
| Board partner and cooler variation | Adds product-level differences/costs | Omitted | Specify whether the target is GPU chip or retail add-in board |
| Retail channel and inventory | Affects market clearing and observed stock/price | Omitted | Discuss as limitations or add data |
| Foundry, packaging, memory supply | May constrain production | One abstract cap only | No actual allocation assumed without evidence |
| Fixed R&D/marketing costs | Affect total profit but not the constant-MC payoff in this model | Omitted | State that model payoff is not accounting profit |
| Intel and other alternatives | Can absorb demand and change substitution | Excluded in two-firm core model | Define the restricted market or expand the model |
| Consumer preferences/segments | Different groups value price, features, workloads differently | Aggregated into linear demand | Nested logit or other discrete-choice model is a stretch goal, not silently assumed |
| Strategic dynamics | Repeated launch cycles, price cuts, inventory clearance, expectations | Omitted by static one-shot game | State explicitly; consider dynamic model only if scope permits |

The base model has few parameters on purpose: it gives an explainable live demonstration. It cannot identify all these mechanisms separately. A plausible explanation of observed market outcomes is not automatically a measured causal explanation.

# 14. Validation metrics and experimental protocol

## 14.1 Mean absolute error

For `n` observations with actual target prices `y_i` and predicted prices `ŷ_i`,

\[
MAE=\frac{1}{n}\sum_{i=1}^{n}|y_i-\hat y_i|.
\]

MAE is in the same unit as the outcome (USD if prices are in USD); lower MAE indicates smaller average absolute prediction error on that evaluation set. It does not prove that the model's mechanism is correct, and its usefulness depends on meaningful inputs and a legitimate validation sample.

## 14.2 Metrics to report

- MAE in USD for prices, with sample size and evaluation rows.
- RMSE in USD as a complementary metric if justified; define its formula.
- Signed error / bias (average predicted minus actual price) to reveal systematic over- or under-prediction.
- Error by generation/tier, not only a single aggregate.
- Baseline comparator, such as a simple historical average or a no-change pricing baseline, where appropriate.
- Train/calibration versus validation/test sample distinction.
- Sensitivity of the metrics to cost proxies and demand parameters.

Do not report a “better fit” winner if the calibration is still a toy example. The current app calculates a training-like four-row MAE without a true calibration or hold-out set; its current value is a prototype display, not study evidence.

## 14.3 Required validation tests

1. **Analytical identity:** Cournot and Bertrand output the same values when `D = 0`.
2. **Symmetry:** with `c1 = c2`, the symmetric baseline returns equal firm values under the symmetric demand system.
3. **Direct-demand inversion:** substituting the direct-demand quantities back into the inverse-demand equations returns `p1` and `p2` within a documented numerical tolerance.
4. **FOC residual:** each unconstrained equilibrium satisfies its corresponding first-order conditions within tolerance.
5. **Feasibility:** equilibrium quantities are nonnegative and the direct-demand denominator is positive.
6. **Parameter guard:** the model blocks `B ≤ 0`, `D < 0`, or `D ≥ B` for the baseline specification (or clearly reports that a separate boundary model is needed).
7. **Cost sanity:** if `A ≤ c_i`, the solver does not display a negative interior quantity as a valid market equilibrium; it should switch to a boundary solution or warn.
8. **Binding capacity:** below the unconstrained NVIDIA equilibrium quantity, the cap is binding and `q1 = cap`.
9. **Nonbinding capacity:** at or above the unconstrained quantity, results equal the unconstrained Cournot equilibrium.
10. **Best response:** under a binding cap, AMD's quantity satisfies AMD's Cournot reaction function (subject to nonnegative bounds).
11. **UI state consistency:** the displayed `D/B` value, slider thumb position, and actual solver parameter agree.
12. **MAE reproducibility:** compute MAE from the displayed validation rows independently and confirm the UI result.
13. **Source/data labels:** no placeholder field appears as “actual”, “estimated”, or “calibrated” without evidence.
14. **Repeatability:** identical inputs and data versions produce identical outputs and plots.

# 15. Audit of `gpu-duopoly-model.jsx`

This audit is based on the uploaded prototype. It is not a claim that the frontend has already been modified.

## 15.1 What the prototype already contains

- A dark visual design with section headings and model explanations.
- Closed-form Cournot and differentiated Bertrand solver functions.
- A function for a fixed NVIDIA quantity and AMD's best response.
- Parameter controls for the substitution parameter and cost inputs.
- A view to compare price, quantity, and margin, along with bar/line charts.
- A four-row MSRP/cost placeholder table, a predicted-vs-actual chart, MAE cards, and a “better fit” label.

These are useful foundations for the live demo.

## 15.2 Issues that must be resolved

### Issue A — substitutability slider does not control what it says

The UI computes `substitutability = (D / B).toFixed(2)` and passes that value into a slider with range `0` to `2.3`, but the slider's change callback sets `D` directly to the selected slider value. Its thumb is driven by `D/B`, but moving it writes a raw `D` value. After interaction, the slider's position/value can jump or disagree with the label. The current starting display is `D/B = 0.48` although the underlying solver parameter is `D = 1.2`.

**Required fix:** use one consistent representation. Preferred: slider value is the ratio `r = D/B`, with bounds `0 ≤ r < 1`; when it changes, set `D = r * B`. Alternatively label the control `D`, use value `D`, and compute/display `D/B` separately. The first option is clearer for the stated research question.

### Issue B — actual/cost labels overstate evidence

`HIST` is commented as illustrative calibration data. The plotted MSRP rows are supported by publicly announced list prices if each SKU/VRAM version is cited, but the share and cost-proxy inputs are not sourced or estimated in the prototype. Label the chart **“Illustrative model output vs. announced launch MSRP (not calibrated)”** until real calibration is complete. Only then use **“predicted vs. observed”** with a precise observed-price definition.

### Issue C — MAE winner is invalid as an empirical conclusion

The app chooses “Cournot” or “Bertrand” by comparing four errors generated from arbitrary inputs. This is fine as a visual software test, but not as research evidence. Hide the “better fit” conclusion in illustrative mode or label it “lowest illustrative error under current placeholders; not a validation result.” In calibrated mode, expose the sample size, parameter version, data source, and validation method.

### Issue D — capacity toggle forces quantity instead of enforcing an upper bound

As described in Section 10, a cap above the unconstrained equilibrium should be nonbinding. Update the algorithm and add tests for both binding and nonbinding values.

### Issue E — output feasibility and numerical status

The code returns closed-form interior solutions without a general nonnegative-boundary solver. Add a validation layer that checks parameters and outputs; when the solution is outside the feasible region, show a visible warning rather than graphing a negative quantity as a normal equilibrium.

### Issue F — unclear quantity units

The controls refer to cap quantities such as 120 units, but the model has not defined whether one quantity unit is a card, thousand cards, an index unit, or a normalized quantity unit. For the existing illustration, explicitly label quantity as **model units (illustrative)**. In calibrated mode, set and show a real unit basis.

### Issue G — market-share values are not visibly used or sourced

The `nvShare` fields exist in `HIST` but are not used by the current validation calculation. Remove them from the final dataset unless they are sourced, properly defined, and used in a documented analysis. Market share should include vendor/market/period/denominator and source.

### Issue H — “TSMC-capped” implies unverified factual precision

The slider is an arbitrary model quantity limit, not an observed NVIDIA allocation. Rename unless a source supports the specific interpretation. It is appropriate to say a capacity constraint is a theoretical scenario; it is not appropriate to claim it measures NVIDIA's real supply limit.

### Issue I — historic comparisons share fixed parameters across unlike product tiers

The current validation code sends all four generations through the same `A=1400`, `B=2.5`, and slider `D`, while only `c1/c2` change. A truly calibrated panel needs a defensible pooling strategy or generation/quality controls; the code should not suggest that one fixed unestimated demand system is validated by four unpaired price observations.

## 15.3 Required UI evidence/provenance tags

Every parameter or datapoint in the UI should have one of these labels:

- **Officially reported:** direct official release/filing value.
- **Market-research source:** reported figure from a named market research source.
- **Estimated from data:** fitted parameter, linked to calibration version and method.
- **Derived:** computed from visibly stated sourced/estimated values.
- **Scenario input:** user-selected hypothetical value.
- **Placeholder:** illustrative value for software verification only.

A tooltip or data table should expose source URL, date, unit, and status where applicable.

# 16. End-to-end interactive demo specification and presentation script

This section defines the expected finished demo, based on the existing plan and React prototype. The current file is the foundation, but the items below are acceptance criteria—not a claim that each is already implemented.

## 16.1 What the audience should understand

By the end of the demo, the audience should be able to answer:

1. What is the research question and market scope?
2. What do NVIDIA and AMD choose in each game?
3. Why do the equations differ between Cournot and Bertrand?
4. Which values come from official sources, which are assumptions, and which are calculated?
5. What changes when substitutability, costs, and output caps change?
6. What can the current model conclude, and what data does it still lack?

## 16.2 Proposed page/interaction flow

### Screen 1 — project overview

Show title, research question, scope, model status (`Illustrative` or `Calibrated`), and a concise statement that all live outputs come from formulas. If the model remains illustrative, say so at the top, not only in a footnote.

### Screen 2 — data & provenance

Show the selected GPU-pair MSRP table with exact SKU/VRAM configuration, price type, launch date, source link, and a clear warning that MSRP is not sales quantity. Display a data-availability card showing whether product-level quantity and cost proxy fields are sourced, missing, or estimated.

### Screen 3 — game rules

Use a simple step-by-step view:

1. Select a market/scenario and parameter set.
2. Choose game mode: Cournot, differentiated Bertrand, or compare both.
3. Solver calculates the Nash equilibrium.
4. Demand equations convert decisions to prices/quantities.
5. Payoffs and constraints are checked.
6. Charts and plain-language interpretation update.

Show the relevant formulas and the meaning of each symbol. Do not label the parameter `D/B` as observed substitutability unless calibrated.

### Screen 4 — live equilibrium lab

Controls:

- `D/B` in a valid range below 1, with `D` derived as `r × B`.
- NVIDIA cost input `c1` with sourced/estimated/scenario label.
- AMD cost input `c2` with sourced/estimated/scenario label.
- Game mode: Cournot / differentiated Bertrand / compare.
- Optional hypothetical NVIDIA output cap.
- Metric selector: price, quantity, per-unit margin, model payoff.

Output cards:

- `p1`, `p2`, `q1`, `q2`;
- `p1 − c1`, `p2 − c2`;
- `π1`, `π2`;
- feasibility status, parameter version, and assumptions.

Charts:

- Cournot vs. Bertrand comparison;
- reaction curves or best-response illustration if there is time;
- sensitivity plot across `D/B` values;
- clear labels and units.

### Screen 5 — capacity experiment

Allow the audience to set a hypothetical cap below, at, and above the unconstrained Cournot quantity. Explain whether the cap is binding. In the nonbinding case, the output must return the unconstrained equilibrium. Do not call a particular cap an actual foundry allocation.

### Screen 6 — evidence and validation

When calibration is unfinished, show “Not calibrated: validation metrics are illustrative only” and show the sourcing gaps. When calibration is complete, show actual-vs-predicted prices with source, sample size, MAE/RMSE, train/test split, data version, and the selected validation model. Avoid a winner badge if the metric is not a valid out-of-sample comparison.

### Screen 7 — conclusions, assumptions, references

Show what is learned from the equation/scenario, what is empirical, what is unresolved, and sources. The limitations should be part of the normal demo flow rather than hidden in the final appendix.

## 16.3 Suggested live demo script (about 5–7 minutes; adjust to the class time limit)

**Opening (30 seconds):** “We compare two ways firms can compete: choosing quantities in Cournot and choosing prices in differentiated Bertrand. We use the same demand system for a fair theoretical comparison. Some values are currently scenario inputs; sourced data are separately marked.”

**Explain the demand system (60 seconds):** Show `p1 = A − Bq1 − Dq2` and `p2 = A − Bq2 − Dq1`. Explain `B`, `D`, and `D/B`; point out that increasing the rival's quantity lowers the modeled price.

**Run the baseline (60 seconds):** Show the equation inputs, solver output, and how price, quantity, margins, and model payoffs are calculated. Identify the numbers as placeholders if calibration is not complete.

**Change substitutability (45 seconds):** Increase `D/B` while staying below 1. Ask the audience to predict the direction of the outcome; move the control and use the live recalculation to compare the two games. Discuss the actual observed direction, not a memorized slogan.

**Change costs (45 seconds):** Raise `c1` and lower `c2`, then switch. Point out that cost effects depend on the model and other input values. Distinguish the scenario from the firms' true undisclosed costs.

**Run capacity scenarios (60 seconds):** Use a cap below the unconstrained NVIDIA quantity and observe the binding result. Move the cap above the unconstrained quantity and confirm that the cap no longer changes the Cournot equilibrium.

**Evidence and caveat (45 seconds):** Show official MSRP sources and explain that MSRP data alone do not identify quantities or cost. If calibrated data are ready, show the actual validation result. If not, show the honest data-gap status instead of a false accuracy claim.

**Close (20 seconds):** State the conclusion supported by the work to date, one main limitation, and the next step required for empirical validation.

## 16.4 Likely instructor questions and grounded answers

- **Why not homogeneous Bertrand?** The team models products as differentiated. A single-price homogeneous-good result is not treated as a literal description of this market. The differentiation assumption is represented by the cross-effect in the demand system and should be treated as a model choice.
- **Where did `D/B` come from?** In illustrative mode, it is a user-controlled scenario input. In calibrated mode, it must come from a documented estimation method and appropriate data. It is not taken from the current placeholder array.
- **Are these NVIDIA and AMD's real costs/profits?** No. Unless the team has defensible and properly scoped data, the values are scenario/model outputs. A die-cost proxy is not actual finished-card marginal cost, and a model payoff is not reported company profit.
- **What proves which game fits better?** A valid parameter estimate and a hold-out comparison on compatible observed data. The current four-row placeholder MAE does not prove this.
- **Does the cap represent TSMC's real allocation?** No, not by default. It is a hypothetical output cap to illustrate constrained optimization. Actual allocation data would be needed for that factual claim.
- **Why include launch MSRPs?** They provide verifiable public descriptive context and a reproducible list-price comparison. They do not provide sales volumes or a full demand estimate by themselves.

# 17. Implementation algorithm and test plan

## 17.1 Baseline solve algorithm

```text
INPUT A, B, D, c1, c2, game_mode

VALIDATE:
    require B > 0
    require 0 <= D < B
    verify input units/status are displayed

IF game_mode includes Cournot:
    k = D / (2*B)
    denominator = 2*B*(1 - k*k)
    q1 = ((A-c1) - k*(A-c2)) / denominator
    q2 = ((A-c2) - k*(A-c1)) / denominator
    check nonnegative-quantity/interior-solution conditions
    p1 = A - B*q1 - D*q2
    p2 = A - B*q2 - D*q1
    m1 = p1-c1; m2 = p2-c2
    pi1 = m1*q1; pi2 = m2*q2
    verify both Cournot FOC residuals

IF game_mode includes differentiated Bertrand:
    m = D / (2*B)
    base1 = ((B-D)*A + B*c1)/(2*B)
    base2 = ((B-D)*A + B*c2)/(2*B)
    p1 = (base1 + m*base2)/(1-m*m)
    p2 = (base2 + m*base1)/(1-m*m)
    denominator = B*B - D*D
    q1 = ((B-D)*A - B*p1 + D*p2)/denominator
    q2 = ((B-D)*A - B*p2 + D*p1)/denominator
    check feasible prices/quantities
    m1 = p1-c1; m2 = p2-c2
    pi1 = m1*q1; pi2 = m2*q2
    verify both Bertrand FOC residuals

IF capacity scenario is enabled:
    calculate unconstrained Cournot equilibrium first
    IF q1_cap >= unconstrained q1:
        return unconstrained Cournot equilibrium
    ELSE:
        q1 = q1_cap
        q2 = max(0, (A-c2-D*q1)/(2*B))
        calculate p1, p2, margins, payoffs
        check feasibility and AMD best response

RETURN results, status/warnings, equations and parameter provenance
```

The pseudocode is the intended behavior. Add boundary handling if a firm would optimally choose zero quantity or if an unconstrained interior solution is infeasible.

## 17.2 Reproducibility artifact set

The final repo or submission bundle should include:

- `report.md` — this research and demo specification.
- `data/raw/` — preserved source files or a README of source links if redistribution is not permitted.
- `data/processed/` — cleaned analysis-ready dataset, with a data dictionary.
- `notebooks/` or `scripts/` — repeatable cleaning, calibration, validation, and sensitivity analysis.
- `src/` — solver functions separated from UI code where practical.
- `tests/` — unit tests for mathematical identities, FOCs, constraints, and data validation.
- `calibration/parameters.json` — calibration version with parameter estimate/status/source and unit information.
- `README.md` — environment setup and launch instructions.
- `requirements.txt` or `package.json` with pinned/declared dependencies, whichever matches the final stack.
- `sources.md` or source metadata in the dataset — URL, access date, source type, quote/page/row, and usage.
- `screenshots/` — final demo outputs and key test scenarios, not substitute for raw data.

Do not include credentials, private API keys, or material the team is not permitted to redistribute.

# 18. Limitations, risks, and interpretation rules

1. **Linear demand is an approximation.** Real GPU demand may be nonlinear and quality differentiated; extrapolation to extreme prices/quantities can be implausible.
2. **Symmetric cross-effect may be too restrictive.** Consumers may switch from AMD to NVIDIA differently than in the reverse direction because of performance, software, workload, brand, and ecosystem differences. The asymmetric model is an extension, not a result of the baseline model.
3. **A two-firm market may omit Intel or other substitutes.** The paper must define the restricted submarket or change the model.
4. **MSRP is not transaction price.** Street prices depend on availability, retailer, timing, and geography.
5. **Launch windows are not aligned automatically.** The rival product may not be available on the same day and product tiers are not identical.
6. **Data may be insufficient.** Public market-share or broad segment revenue data may not identify quantity sold by SKU.
7. **Cost proxies are uncertain.** Die area and wafer-price estimates do not equal finished-board marginal cost. The uncertainty must be shown, not hidden.
8. **No causal interpretation without identification.** Correlations from a small price/quantity panel do not automatically identify consumer substitution.
9. **Static one-shot game omits dynamics.** It excludes future launches, repeated play, inventory clearance, expected price cuts, capacity investment, and entry/exit.
10. **Capacity is stylized.** A hypothetical cap does not verify an actual foundry allocation.
11. **Payoff is not accounting profit.** The model excludes fixed costs and many other costs/activities.
12. **MAE cannot validate placeholder parameters.** A small error produced by hand-picked inputs is not independent evidence.
13. **Numerical boundary matters.** The Bertrand direct-demand inverse fails at `D = B`; the app must not permit a singular parameter configuration.
14. **Historical price data need provenance.** Save access dates, distinguish MSRP from street price, and do not use current pages as proof of historical transaction prices if the page only states a current price.
15. **Result framing must be honest.** A live slider demonstrates sensitivity of the model under assumptions. It does not prove that real firms choose the modeled actions or that one strategic variable causally explains market outcomes.

# 19. Work plan and team responsibilities

Use the four roles from `plan.md`. Assign real names only after the team decides who owns each deliverable.

| Role | Core responsibility | Acceptance artifact |
|---|---|---|
| Data & Empirics Lead | Define market/data scope; collect source-backed price, quantity, and cost inputs; maintain evidence provenance | Versioned dataset, data dictionary, source log, missing-data note |
| Theory & Model Lead | Verify derivations, assumptions, Nash conditions, and capacity logic | Derivation note; equations checked against solver; test results |
| Computational/Calibration Lead | Implement robust solver, estimation workflow, validation and UI integration | Working app, parameter file, reproducible script, tests passing |
| Analysis & Counterfactual Lead | Design scenarios, interpret outputs, link every statement to evidence, support IEEE paper | Scenario table, results interpretation, limitations and demo narrative |

Roles 2 and 3 should compare the written derivation with the code before the demo. The entire team should review the data scope and the wording of the conclusions before locking the paper.

### Recommended milestones

1. **Milestone 1 — theory and source inventory:** equations reviewed; market definition set; public source links captured.
2. **Milestone 2 — dataset and status decision:** determine whether compatible quantity data are available. Decide whether the final paper is empirically calibrated or explicitly scenario-based.
3. **Milestone 3 — solver integrity:** fix the slider and cap bugs; tests pass; all outputs have units/status labels.
4. **Milestone 4 — experiments and write-up:** execute a fixed scenario matrix; generate plots/tables; document sources and limitations.
5. **Milestone 5 — presentation rehearsal:** run the entire demo from a fresh startup; verify that the explanation does not overstate findings.
6. **Milestone 6 — final submission audit:** use the instructor's IEEE template; remove all placeholders and template instructions; verify citations and output artifacts.

# 20. IEEE paper preparation notes

IEEE's official Author Center provides conference templates and recommends a concise, self-contained abstract of up to 250 words with three to five index terms/keywords, plus an introduction, methods, results/discussion, conclusion, and references [15], [16]. The final document must use the instructor's exact conference/template instructions. Do not assume this Markdown file itself meets page layout, margin, font, column, figure-resolution, or PDF requirements.

Suggested two-column paper flow:

1. Title and author/affiliation block.
2. Abstract and Index Terms.
3. Introduction and contributions.
4. Related background and market definition.
5. Model and equilibrium derivations.
6. Data, estimation, and assumptions.
7. Experiments/results and validation.
8. Discussion, limitations, and threats to validity.
9. Conclusion and future work.
10. References.

Recommended final-paper figures/tables:

- **Fig. 1:** Solver workflow from input parameters to Nash equilibrium and validation.
- **Fig. 2:** Verified descriptive launch-MSRP comparison, with exact SKU/price-type labels.
- **Fig. 3:** Cournot versus Bertrand live output for a clearly named scenario.
- **Fig. 4:** Sensitivity plot across `D/B` with cost parameters held constant and listed.
- **Fig. 5:** Binding versus nonbinding output-cap experiment.
- **Table I:** Notation, assumptions, and parameter provenance.
- **Table II:** Data sources, fields, period, unit, and coverage limitations.
- **Table III:** Validated parameter estimates and uncertainty, only if estimated.
- **Table IV:** Equilibrium outputs and held-out validation metrics, only if the data support them.

Every plot needs a caption that identifies whether it shows observed data, derived data, estimates, or simulation. Ensure the paper's claims match those labels.

# 21. Comprehensive completion checklist

Use this checklist for team review. A box marked `[x]` means the item is addressed in this report, not that implementation/data collection has already been completed. Items marked `[ ]` require an actual team action before final submission.

## A. Research scope and claim discipline

- [x] Research question and objectives written.
- [x] Hypotheses framed as hypotheses, not findings.
- [x] Baseline two-firm scope and third-firm limitation explained.
- [x] Difference between MSRP, street price, ASP, and broad segment revenue explained.
- [x] Placeholder values identified as placeholders.
- [ ] Team records the final market, geography, period, and product-tier definitions.
- [ ] Team decides whether the final paper is empirically calibrated or scenario-only and updates all wording consistently.

## B. Literature and citations

- [x] Official launch-price sources collected for prototype GPU examples.
- [x] Public market-research source identified with scope caveat.
- [x] Annual-report/10-K sources reviewed for revenue-scope caution.
- [x] Demand-estimation references included.
- [x] IEEE author-center guidance included.
- [ ] Team checks every in-text citation against the actual source and exact claim.
- [ ] Team records access dates and preserves permitted source extracts/data.
- [ ] Team adds any course-required theoretical textbook/papers assigned by the instructor.

## C. Model mathematics

- [x] Symbols and units described.
- [x] Inverse-demand system described.
- [x] Cournot payoff functions and FOCs derived.
- [x] Cournot reaction functions derived.
- [x] Cournot closed-form equilibrium derived.
- [x] Bertrand direct demand derived by matrix inversion.
- [x] Bertrand FOCs and closed-form prices derived.
- [x] Quantities, margins, and payoffs defined for both games.
- [x] `D = 0` identity established.
- [x] Admissible parameter region and singular boundary documented.
- [x] Capacity extension behavior specified.
- [ ] Theory lead verifies derivations independently and signs off.
- [ ] Implementation uses feasible boundary solutions or meaningful warnings.

## D. Data and calibration

- [x] Existing source/data gaps identified.
- [x] Verified launch-price table included with exact product distinctions.
- [x] Correct coefficient-mapping issue documented.
- [x] Endogeneity/identification risk discussed.
- [x] Minimum data dictionary provided.
- [ ] Data lead builds one versioned clean dataset.
- [ ] Every value has a source, date, unit, source type, and uncertainty/status label.
- [ ] Exact-SKU sales/quantity data are obtained, or the paper is explicitly scenario-based.
- [ ] Product tiers and matching rules are documented.
- [ ] Actual versus MSRP versus street-price observations are never silently mixed.
- [ ] Cost proxy is reproducibly calculated or retained as a clearly hypothetical input.
- [ ] Parameter estimates and uncertainty are saved, if estimation is performed.

## E. Solver and frontend

- [x] Existing JSX's major math/UI issues identified.
- [x] Slider mismatch (`D/B` display vs `D` update) identified.
- [x] Capacity cap's nonbinding-case bug identified.
- [x] Current validation MAE is flagged as illustrative rather than evidence.
- [ ] Slider is corrected and tested.
- [ ] Capacity solver handles both binding and nonbinding cases.
- [ ] UI shows parameter units, data status, provenance, and solver warnings.
- [ ] UI separates scenario mode from calibrated mode.
- [ ] No unverified input is labeled actual/estimated/calibrated.
- [ ] UI shows formulas/algorithm sufficiently for a classroom demonstration.
- [ ] Page works from a fresh launch without console errors or broken chart states.

## F. Numerical validation and experiments

- [x] Baseline Cournot and Bertrand calculations worked through.
- [x] Capacity calculation worked through for a binding cap.
- [x] MAE formula and interpretation specified.
- [ ] `D = 0` equality test passes in code.
- [ ] Symmetric-cost test passes.
- [ ] Direct-demand inversion test passes.
- [ ] FOC residual tests pass.
- [ ] Nonnegative/feasibility checks pass.
- [ ] Binding and nonbinding cap tests pass.
- [ ] MAE calculation independently reproduces UI values.
- [ ] Predefined scenario matrix is run and archived.
- [ ] Actual validation uses suitable held-out observations if data allow.
- [ ] Charts include source/status, axis units, and caption-level assumptions.

## G. Results and interpretation

- [x] Illustrative example explicitly separated from real market evidence.
- [x] No claim that NVIDIA or AMD actual marginal costs/profits are known.
- [x] Limitations and omitted factors included.
- [ ] Team writes results only from final run outputs.
- [ ] Team states negative, inconclusive, or unsupported findings honestly.
- [ ] The report's conclusion answers the research question without overclaiming causality.

## H. Demo readiness

- [x] End-to-end presentation flow provided.
- [x] Suggested 5–7-minute script provided.
- [x] Likely instructor questions and grounded responses included.
- [ ] Demo starts from a clean state on the presentation machine.
- [ ] Team tests keyboard/mouse interaction and screen resolution before class.
- [ ] Team prepares a fallback screenshot/video or static scenario page in case live UI fails.
- [ ] Presenter rehearses what each value means and identifies placeholders clearly.
- [ ] Every shown result can be traced to a parameter set and calculation.

## I. IEEE report and packaging

- [x] IEEE-style section structure and abstract provided.
- [x] References with hyperlinks provided below.
- [ ] Teammate moves final verified content into the official IEEE template.
- [ ] Final abstract stays within IEEE guidance and contains no unsupported conclusion.
- [ ] Figures and tables use IEEE-compatible style, captions, labels, and citations.
- [ ] All references are cited in the body and all body citations appear in references.
- [ ] All template instructions/example text are removed.
- [ ] Author names, affiliations, course details, and instructor-requested metadata are confirmed rather than guessed.
- [ ] PDF renders correctly, all equations/figures are legible, and formatting is checked.
- [ ] Final filenames, submission portal, due date, and any page limit are verified against the instructor's instructions.

## J. Final go/no-go gate

The project is ready to describe as an **empirically calibrated study** only if the team can check all of these:

- [ ] The dataset directly measures or defensibly estimates quantities and prices for the stated market.
- [ ] Market scope and competitor treatment are consistent with the data.
- [ ] Coefficient estimation matches the equations and addresses endogeneity or explicitly avoids causal interpretation.
- [ ] Cost inputs have provenance and are not misrepresented as true marginal cost.
- [ ] The solver passes equilibrium and constraint tests.
- [ ] Validation uses an appropriate sample and baseline.
- [ ] Results are reproducible from saved code/data/parameter files.

If any of these are not met, the project can still be presented as a useful **theoretical interactive simulator**, but the paper must say that it is scenario-based and must not claim that the model has empirically explained actual GPU prices or margins.

# 22. References

The sources below were checked on 22 October 2026. Official announcements are the preferred sources for announced MSRP/availability; they are not evidence of realized transaction prices or product quantities.

[1] Jon Peddie Research, “Q1’26 PC graphics add-in board shipments decreased -0.6% from last quarter, to 12 million units, with a CAGR to 2029 of -3.3%,” June 10, 2026. [Online]. Available: https://www.jonpeddie.com/news/q126-pc-graphics-add-in-board-shipments-decreased-0-6-from-last-quarter-to-12-million-units-with-a-cagr-to-2029-of-3-3/

[2] Jon Peddie Research, “Add-in Board report — a report on the Graphic Add-in Board market,” JPR Store description. [Online]. Available: https://www.jonpeddie.com/store/

[3] NVIDIA, “GeForce RTX 5080 Graphics Cards,” official product page. [Online]. Available: https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5080/

[4] Advanced Micro Devices, Inc., “AMD Unveils Next-Generation AMD RDNA 4 Architecture with the Launch of AMD Radeon RX 9000 Series Graphics Cards,” Feb. 28, 2025. [Online]. Available: https://ir.amd.com/news-events/press-releases/detail/1238/amd-unveils-next-generation-amd-rdna-4-architecture-with-the-launch-of-amd-radeon-rx-9000-series-graphics-cards

[5] NVIDIA, “NVIDIA Blackwell GeForce RTX 50 Series Opens New World of AI Computer Graphics,” Jan. 6, 2025. [Online]. Available: https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Blackwell-GeForce-RTX-50-Series-Opens-New-World-of-AI-Computer-Graphics/

[6] Advanced Micro Devices, Inc., “AMD Introduces New Radeon Graphics Cards and Ryzen Threadripper Processors at COMPUTEX 2025,” May 20, 2025. [Online]. Available: https://ir.amd.com/news-events/press-releases/detail/1253/amd-introduces-new-radeon-graphics-cards-and-ryzen-threadripper-processors-at-computex-2025

[7] Advanced Micro Devices, Inc., “AMD Unveils World’s Most Advanced Gaming Graphics Cards, Built on Groundbreaking AMD RDNA 3 Architecture with Chiplet Design,” Nov. 3, 2022. [Online]. Available: https://ir.amd.com/news-events/press-releases/detail/1099/amd-unveils-worlds-most-advanced-gaming-graphics-cards-built-on-groundbreaking-amd-rdna-3-architecture-with-chiplet-design

[8] Advanced Micro Devices, Inc., “New AMD Radeon RX 7800 XT and Radeon RX 7700 XT Graphics Cards Deliver High-Performance, Visually Stunning 1440p Gaming Experiences and Superior Performance-Per-Dollar,” Aug. 25, 2023. [Online]. Available: https://www.amd.com/en/newsroom/press-releases/2023-8-25-new-amd-radeon-rx-7800-xt-and-radeon-rx-7700-xt-gr.html

[9] NVIDIA, “NVIDIA GeForce RTX 4070 Brings Power of Ada Lovelace Architecture and DLSS 3 to Millions More Gamers and Creators, Starting at $599,” Apr. 12, 2023. [Online]. Available: https://investor.nvidia.com/news/press-release-details/2023/NVIDIA-GeForce-RTX-4070-Brings-Power-of-Ada-Lovelace-Architecture-and-DLSS-3-to-Millions-More-Gamers-and-Creators-Starting-at-599/default.aspx

[10] NVIDIA, “RTX 40 Series Graphics Cards Announcements,” Sept. 2022. [Online]. Available: https://www.nvidia.com/en-us/geforce/news/gfecnt/20229/rtx-40-series-graphics-cards-announcements/

[11] NVIDIA Corporation, “Form 10-K for the fiscal year ended January 25, 2026,” U.S. Securities and Exchange Commission, 2026. [Online]. Available: https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm

[12] Advanced Micro Devices, Inc., “Form 10-K for the fiscal year ended December 27, 2025,” U.S. Securities and Exchange Commission, 2026. [Online]. Available: https://www.sec.gov/Archives/edgar/data/2488/000000248826000021/amd-20251227.htm

[13] S. Berry and P. Haile, “Identification in Differentiated Products Markets,” *Annual Review of Economics*, vol. 8, pp. 27–52, 2016. [Online]. Available: https://www.annualreviews.org/doi/10.1146/annurev-economics-080315-015050

[14] P. Choné and L. Linnemer, “Linear demand systems for differentiated goods: Overview and user’s guide,” *International Journal of Industrial Organization*, vol. 73, article 102663, 2020. [Online]. Available: https://doi.org/10.1016/j.ijindorg.2020.102663

[15] IEEE Author Center, “Authoring Tools and Templates — Conferences.” [Online]. Available: https://conferences.ieeeauthorcenter.ieee.org/write-your-paper/authoring-tools-and-templates/

[16] IEEE Author Center, “Structure Your Paper — Conferences.” [Online]. Available: https://conferences.ieeeauthorcenter.ieee.org/write-your-paper/structure-your-paper/

[17] TechInsights, “Chip Costing and Process Models,” brochure. [Online]. Available: https://www.techinsights.com/sites/default/files/2023-03/TechInsights-Chip-Costing-and-Process-Brochure.pdf

---

## Final handoff note

Before converting this Markdown into the IEEE paper, the team should decide and record whether a defensible quantity dataset and cost proxy can actually be obtained. The source-backed launch prices are ready for descriptive context; the placeholder model is ready for mathematical/demo testing once the two implementation defects are fixed. The empirical result is **not yet established** by the current prototype. That separation is the main safeguard against submitting a polished but unsupported research claim.

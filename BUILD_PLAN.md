# Build Plan: NVIDIA vs. AMD GPU Duopoly Simulator

**Purpose:** Build a simple, reliable, classroom-ready Game Theory demo using **Python + Streamlit**.  
**Primary source documents:** `report.md`, `plan.md`, and the existing `gpu-duopoly-model.jsx` prototype.  
**Important:** This file is an implementation specification for Antigravity. It is not a substitute for the research report and it does not claim that the model is empirically calibrated.

---

## 1. Instructions to the build agent

Read this plan and the project's existing `report.md`, `plan.md`, and `gpu-duopoly-model.jsx` before changing anything. Build the app described here while preserving the report's research question, equations, assumptions, source labels, limitations, and open data gaps.

### Non-negotiable rules

1. Use **Python + Streamlit**. Do not build a React, JavaScript, TypeScript, or separate web-API application.
2. Keep the project simple. No database, login system, external API, web scraper, LLM, cloud service, or deployment dependency is required for the first version.
3. Implement and test the mathematical functions before connecting them to the UI.
4. Never fabricate sales volume, market share, marginal cost, capacity, regression results, or model-validation results.
5. The baseline values inherited from the React prototype are **illustrative placeholders**, not measured NVIDIA/AMD data.
6. Official GPU launch MSRPs may be displayed as source-backed descriptive observations. Do not treat MSRP alone as sales quantity or use it to claim the model is calibrated.
7. Hide or clearly mark predictive metrics as **not available / not empirically validated** unless compatible observations and a documented estimation process are provided.
8. Correct the existing substitutability-slider and capacity-cap errors described below.
9. If an input produces an infeasible or invalid equilibrium, show a visible explanation rather than silently displaying negative quantities or invalid prices as a valid Nash equilibrium.
10. Keep conclusions neutral. Do not force a conclusion that Cournot or Bertrand is better, or that a real-world supply constraint explains NVIDIA's margins.
11. Add tests and run them. Do not mark the build complete if the tests fail.
12. Do not rewrite `report.md` or change the project's research claims as part of building the app. If the code exposes a contradiction in the report, document it for the team instead of silently changing the research narrative.

### Build order

1. Inspect the supplied files.
2. Create the Python environment files and folder structure.
3. Implement demand, Cournot, Bertrand, metrics, and capacity functions.
4. Add mathematical tests and check the numerical smoke-test values in Section 7.
5. Build Streamlit pages and charts on top of the tested functions.
6. Add the sourced descriptive MSRP data and clear provenance/status labels.
7. Add data-readiness and validation views without inventing missing data.
8. Run the full test suite and launch the app from a clean environment.
9. Update `README.md` with exact setup and run instructions.
10. Report which requirements are complete and which remain blocked by missing empirical data.

---

## 2. Project aim

Build an interactive simulator for a two-firm differentiated-product duopoly representing NVIDIA and AMD in a **clearly defined, restricted discrete-GPU submarket**. The app compares:

- **Cournot competition:** both firms choose quantities.
- **Differentiated Bertrand competition:** both firms choose prices.
- **Capacity-constrained Cournot:** NVIDIA has a hypothetical upper bound on output and AMD chooses its best response.

The app is primarily a **game-theory teaching and counterfactual simulator**. It can display sourced launch-price context and a calibration-readiness status, but it must not call itself an empirically calibrated model until the team supplies suitable data and completes a defensible estimation and validation process.

### Main research question

> How do the predicted equilibrium price, quantity, and profit outcomes for NVIDIA and AMD differ under Cournot quantity competition and differentiated Bertrand price competition, and how do demand substitutability, cost asymmetry, and a binding output cap change those outcomes?

### Secondary questions the app should help explore

- What happens when the substitution ratio `D/B` changes?
- How do different cost inputs affect prices, quantities, margins, and model payoffs?
- When does the NVIDIA output cap bind, and what changes when it does not bind?
- Which values are sourced, derived, estimated, or merely scenario inputs?
- Is there enough compatible data to calibrate the demand model? The app must be able to report **no**, when that is the honest answer.

---

## 3. Scope and terminology

### Included in version 1

- Explanatory research overview.
- Model equations and notation.
- Live Cournot and differentiated-Bertrand solver comparison.
- Adjustable model parameters.
- Hypothetical capacity-constrained Cournot scenario.
- Price, quantity, per-unit margin, and model-payoff outputs.
- Sensitivity experiment for `D/B`.
- Official-launch-MSRP reference table with source links.
- Data-schema/readiness checks and transparent validation status.
- Calculation/assumption explanations, limitation notes, and a short demo guide.
- Automated numerical tests.

### Not included in version 1

- Real production-capacity claims about TSMC or NVIDIA.
- SKU-level sales quantities that are not available from a cited source.
- Automatically fabricated market shares or cost estimates.
- A fully identified structural demand-estimation system when compatible data/instruments are unavailable.
- Nested-logit demand, asymmetric substitution, repeated games, dynamics, inventory simulation, or more than two firms.
- Accounts, data persistence, remote APIs, scraping, a database, or a separate frontend/backend.

These could be future extensions, but are not required to deliver the first demo.

### Market-scope disclaimer

The model has two players only. Intel and other suppliers are not modeled. Do not call the two-firm simulation a full representation of the entire discrete GPU market unless the team narrows the stated scope to a two-firm submarket. Public add-in-board summaries can cover a broader market than consumer desktop gaming GPUs.

### Output and cost terminology

- In illustrative mode, quantities are **model units (illustrative)**, not actual cards sold.
- `c1` and `c2` are scenario marginal-cost inputs. Unless backed by a documented cost method, call them **illustrative cost inputs**, not NVIDIA's/AMD's true marginal costs.
- `profit` in the application means **model payoff** or **model contribution payoff**, calculated as `(price - marginal cost) × quantity`. It is not a firm's reported profit.
- Display `margin` as a per-unit amount `p_i - c_i`. Do not call it a percentage margin unless a precise formula and denominator are shown.
- A **capacity cap** is hypothetical unless a specific compatible, sourced output limit is obtained. Name the control `NVIDIA output cap (hypothetical)`, not `TSMC allocation` or `TSMC-capped`.

---

## 4. Technology stack

Use a small, conventional Python data app stack:

| Purpose | Technology | Requirement |
|---|---|---|
| App/UI | Streamlit | Required |
| Numeric operations | NumPy | Required |
| Data tables and CSV handling | pandas | Required |
| Interactive charts | Plotly | Required |
| Optional constrained/numeric routines | SciPy | Include only if the implementation uses it |
| Statistical estimation utilities | statsmodels | Optional; no structural calibration claims without valid data/method |
| Tests | pytest | Required for development and final verification |

Target **Python 3.12** for a straightforward supported environment. Keep the Python version and package versions in the README/requirements. No JavaScript framework is needed.

Reference documentation:

- Streamlit: https://docs.streamlit.io/
- NumPy: https://numpy.org/doc/
- pandas: https://pandas.pydata.org/docs/
- Plotly: https://plotly.com/python/
- SciPy: https://docs.scipy.org/doc/scipy/
- statsmodels: https://www.statsmodels.org/stable/index.html
- pytest: https://docs.pytest.org/

---

## 5. Folder and file structure

Keep this structure as the target. Do not add modules unless there is a clear reason.

```text
gpu-duopoly-project/
├── app.py
├── requirements.txt
├── README.md
├── BUILD_PLAN.md
├── report.md
├── plan.md
├── gpu-duopoly-model.jsx            # Legacy reference only; do not run in the app
│
├── pages/
│   ├── 1_Model_and_Equations.py
│   ├── 2_Live_Equilibrium.py
│   ├── 3_Capacity_and_Scenarios.py
│   ├── 4_Data_and_Validation.py
│   └── 5_Demo_Guide.py
│
├── models/
│   ├── __init__.py
│   ├── demand.py
│   ├── cournot.py
│   ├── bertrand.py
│   ├── capacity.py
│   └── metrics.py
│
├── analysis/
│   ├── __init__.py
│   ├── sensitivity.py
│   └── data_readiness.py
│
├── data/
│   ├── gpu_launch_prices.csv
│   ├── illustrative_defaults.json
│   └── data_dictionary.md
│
├── utils/
│   ├── __init__.py
│   ├── provenance.py
│   └── formatting.py
│
└── tests/
    ├── test_demand.py
    ├── test_cournot.py
    ├── test_bertrand.py
    ├── test_capacity.py
    ├── test_metrics.py
    └── test_data_readiness.py
```

### Responsibilities and connections

| File | What it does | Imports / used by |
|---|---|---|
| `app.py` | Project landing page, research question, scope, status banner, high-level navigation and links to pages. | `models`, `utils`; Streamlit launches this file. |
| `pages/1_Model_and_Equations.py` | Explains the game, notation, equations, equilibrium meaning, and assumptions. | Displays formulas in readable Markdown; refers to `report.md`. |
| `pages/2_Live_Equilibrium.py` | Inputs for `A`, `B`, `D/B`, `c1`, `c2`; runs Cournot and Bertrand; shows metrics and charts. | `models/demand.py`, `models/cournot.py`, `models/bertrand.py`, `models/metrics.py`, `utils/formatting.py`. |
| `pages/3_Capacity_and_Scenarios.py` | Demonstrates binding/nonbinding hypothetical NVIDIA cap and simple controlled scenarios. | `models/cournot.py`, `models/capacity.py`, `analysis/sensitivity.py`. |
| `pages/4_Data_and_Validation.py` | Displays sourced launch MSRPs, missing-data/readiness status, permitted descriptive comparisons, and validation availability. | `data/gpu_launch_prices.csv`, `analysis/data_readiness.py`, `models/metrics.py`, `utils/provenance.py`. |
| `pages/5_Demo_Guide.py` | A presentation walkthrough, scenario steps, explanation prompts, limitations, and instructor-question reminders. | Static project content from this plan/report; may use saved illustrative defaults. |
| `models/demand.py` | Shared inverse/direct demand functions and input/output validation. | Imported by all equilibrium solvers. |
| `models/cournot.py` | Analytical Cournot equilibrium and, if needed, reaction-function helpers. | Used by live-equilibrium and capacity pages. |
| `models/bertrand.py` | Analytical differentiated-Bertrand price equilibrium, direct-demand quantity recovery, and checks. | Used by live-equilibrium page. |
| `models/capacity.py` | Correct upper-bound logic for NVIDIA quantity with AMD best response. | Used by capacity/scenario page. |
| `models/metrics.py` | Per-unit margins, model payoffs, MAE/RMSE/bias functions with guards for missing inputs. | Used by output cards and data/validation page. |
| `analysis/sensitivity.py` | Runs repeated solver calls over an explicit list/range of `D/B` values for plotting. | Used by live-equilibrium and scenario pages. |
| `analysis/data_readiness.py` | Checks available columns, missingness, provenance, and whether a dataset supports the requested calculation. Does not pretend missing data exist. | Used by data/validation page and tests. |
| `data/gpu_launch_prices.csv` | Source-backed official launch MSRP facts only; descriptive data, not quantity data. | Loaded by data/validation page. |
| `data/illustrative_defaults.json` | Clearly labeled initial scenario parameters from the existing prototype. | Used to initialize simulator controls. |
| `data/data_dictionary.md` | Defines CSV columns, units, source fields, evidence statuses, and which analyses are/are not permitted. | Reference for team and data page. |
| `utils/provenance.py` | Consistent evidence-status labels and source link helpers. | Used by pages when displaying sources/status. |
| `utils/formatting.py` | Formatting of prices, quantities, payoffs, warnings, and status messages. | Used by UI pages. |
| `tests/*` | Unit and regression tests for model equations, feasibility, capacity logic, metrics, and dataset checks. | Run with `pytest -q`. |
| `report.md` | Research report source of truth. Preserve unless the user/team explicitly requests a report revision. | Read by agent/team; do not import it as runtime data. |
| `plan.md` | Original team plan / strategic brief. | Read by agent/team; do not import it as runtime data. |
| `gpu-duopoly-model.jsx` | Existing prototype used to understand desired features and baseline values. | Reference only; the Python app must not depend on it. |

### Keep the data flow one-way

```text
CSV + illustrative_defaults.json
             │
             ▼
       Streamlit page
             │
             ▼
    Validated model inputs
             │
             ▼
       Python solvers
             │
             ▼
  Results + feasibility status
             │
             ▼
    Metric cards and charts
```

The charts must use solver outputs, not separately hardcoded results. The model modules must not import Streamlit or Plotly. That separation is necessary so the same mathematical functions can be tested without starting the app.

---

## 6. Model definition and notation

### 6.1 Players

- Firm 1: NVIDIA.
- Firm 2: AMD.
- Cournot strategies: quantities `q1`, `q2`.
- Bertrand strategies: prices `p1`, `p2`.

### 6.2 Shared inverse-demand system

Use the exact symmetric linear inverse-demand model from `report.md`:

\[
p_1 = A - Bq_1 - Dq_2, \qquad p_2 = A - Bq_2 - Dq_1.
\]

Where:

- `A`: inverse-demand intercept.
- `B`: own-quantity slope, with `B > 0`.
- `D`: cross-quantity term / substitution parameter, with `D >= 0`.
- `D/B`: dimensionless substitution ratio used by the slider.
- `c1`, `c2`: constant marginal-cost inputs for the scenario.
- `q1`, `q2`: quantities in consistent model units.
- `p1`, `p2`: prices in model price units; treat as USD only if inputs are calibrated consistently.
- `m_i = p_i - c_i`: per-unit model margin.
- `pi_i = (p_i - c_i) q_i`: model payoff.

**Important notation correction:** in this inverse-demand specification, `B` and `D` are slopes with respect to quantities, not coefficients estimated by simply regressing quantity on prices. Do not claim that a regression coefficient from a quantity-on-price equation is `B` or `D` without a documented mapping and identification method.

### 6.3 Admissible base-model parameters

Use the symmetric differentiated-demand specification in the region:

- `A` finite.
- `B > 0`.
- `0 <= D < B` for the shared Cournot/Bertrand app.
- `c1`, `c2` finite and in units consistent with `p`.
- nonnegative equilibrium quantity and feasible modeled price/payoff values.

The Bertrand direct-demand inverse has denominator `B² - D²`, which must be strictly positive. Do not allow `D/B = 1` in the slider; cap it below one, for example at `0.95`, to avoid the singular boundary and numerical instability.

### 6.4 Cournot solution

Payoffs:

\[
\pi_1=(A-Bq_1-Dq_2-c_1)q_1,
\]
\[
\pi_2=(A-Bq_2-Dq_1-c_2)q_2.
\]

First-order conditions:

\[
A-2Bq_1-Dq_2-c_1=0,
\]
\[
A-2Bq_2-Dq_1-c_2=0.
\]

Reaction functions:

\[
q_1=\frac{A-c_1-Dq_2}{2B},\qquad q_2=\frac{A-c_2-Dq_1}{2B}.
\]

Interior equilibrium quantities:

\[
q_1^*=\frac{2B(A-c_1)-D(A-c_2)}{4B^2-D^2},
\]
\[
q_2^*=\frac{2B(A-c_2)-D(A-c_1)}{4B^2-D^2}.
\]

Then calculate `p1`, `p2` using inverse demand, margins using `p_i - c_i`, and model payoffs using `(p_i - c_i) q_i`.

### 6.5 Differentiated Bertrand solution

Direct demand obtained by inverting the shared system:

\[
q_1(p_1,p_2)=\frac{(B-D)A-Bp_1+Dp_2}{B^2-D^2},
\]
\[
q_2(p_1,p_2)=\frac{(B-D)A-Bp_2+Dp_1}{B^2-D^2}.
\]

Define:

\[
r_1=(B-D)A+Bc_1,\qquad r_2=(B-D)A+Bc_2.
\]

Interior equilibrium prices:

\[
p_1^*=\frac{2Br_1+Dr_2}{4B^2-D^2},
\qquad p_2^*=\frac{Dr_1+2Br_2}{4B^2-D^2}.
\]

Recover `q1`, `q2` using direct demand; then calculate margins and model payoffs exactly as for Cournot.

### 6.6 Output metrics

For each firm and model, display:

- Equilibrium price `p_i`.
- Equilibrium quantity `q_i`.
- Per-unit margin `m_i = p_i - c_i`.
- Model payoff `pi_i = (p_i - c_i) q_i`.
- Feasibility/solver status.

For comparisons, show both firms and both game models. Add a brief text interpretation based on actual computed values, not a prewritten conclusion. Avoid words such as “proves” and “actual profit.”

### 6.7 The `D = 0` identity

When `D = 0`, both games must reduce to independent monopolies. For each firm where `A > c_i`:

\[
q_i^*=\frac{A-c_i}{2B},\qquad p_i^*=\frac{A+c_i}{2},
\]
\[
\pi_i^*=\frac{(A-c_i)^2}{4B}.
\]

This is a required unit test.

### 6.8 Capacity-constrained Cournot logic

Treat `q1_cap` as a **maximum**, not a forced production target.

1. Solve the unconstrained Cournot equilibrium.
2. If `q1_cap >= q1_unconstrained`, the cap is nonbinding. Return exactly the unconstrained equilibrium.
3. If `0 <= q1_cap < q1_unconstrained`, set `q1 = q1_cap` and calculate AMD's best response:

\[
q_2=\max\left(0,\frac{A-c_2-Dq_1}{2B}\right).
\]

4. Recalculate both prices, margins, and payoffs using the same demand system.
5. Check that NVIDIA's best response is indeed at least as large as the cap; this verifies that the cap binds in the constrained game. If a domain/boundary condition invalidates the simple interior case, show a warning or block it instead of silently accepting the result.
6. Never describe this hypothetical cap as an observed NVIDIA/TSMC allocation.

---

## 7. Default scenario and numerical smoke tests

Use the original prototype's initial values, but visibly tag them as **Illustrative placeholders**:

```json
{
  "status": "illustrative",
  "A": 1400.0,
  "B": 2.5,
  "substitutability_ratio_D_over_B": 0.48,
  "c1_nvidia": 550.0,
  "c2_amd": 420.0,
  "nvidia_output_cap": 120.0,
  "quantity_unit_label": "model units (illustrative)",
  "price_unit_label": "model price units (illustrative; not calibrated USD forecast)"
}
```

When the slider changes `r = D/B`, calculate `D = r * B`. Do not store slider `r` as if it were raw `D`.

### Reference output for the default inputs

With `A=1400`, `B=2.5`, `D=1.2`, `c1=550`, and `c2=420`, the model should return approximately:

| Metric | Cournot | Differentiated Bertrand |
|---|---:|---:|
| NVIDIA price `p1` | 876.1885 | 824.2360 |
| AMD price `p2` | 831.7148 | 771.8166 |
| NVIDIA quantity `q1` | 130.4754 | 142.5343 |
| AMD quantity `q2` | 164.6859 | 182.8569 |
| NVIDIA margin `m1` | 326.1885 | 274.2360 |
| AMD margin `m2` | 411.7148 | 351.8166 |
| NVIDIA model payoff `pi1` | 42559.56 | 39088.04 |
| AMD model payoff `pi2` | 67803.62 | 64332.09 |

These values are for checking implementation math only. They are not predictions of actual GPU market prices, shipments, costs, or profits.

With a binding hypothetical cap `q1_cap=120`, the capacity scenario from the report should give:

- `q1 = 120`
- `q2 = 167.2`
- `p1 = 899.36`
- `p2 = 838.00`
- NVIDIA model payoff `= 41923.20`
- AMD model payoff `= 69889.60`

For a cap at or above the unconstrained NVIDIA quantity (approximately `130.4754` under these inputs), the capacity result must be the unconstrained Cournot result, not the cap value.

---

## 8. Known defects in the old React prototype to avoid

1. **Substitutability slider mismatch:** the interface displays `D/B`, but the callback writes the selected ratio directly into `D`. Fix this by letting the slider control `r=D/B` and deriving `D=r*B` every time inputs change.
2. **Capacity cap incorrectly forces output:** the old function always sets `q1=q1_cap`; a true cap must be nonbinding if it is above the unconstrained optimum.
3. **Illustrative values appear alongside actual MSRP values:** the UI must display a prominent status tag and explanation. Actual MSRP does not validate a model with unestimated demand and cost values.
4. **Misleading MAE winner:** do not show “Cournot wins” or “Bertrand fits better” from the current four arbitrary cost-proxy rows. In version 1, validation status should be `Not calibrated` unless an appropriate matched dataset and estimation process exist.
5. **Potential infeasible interior solutions:** do not plot negative quantities or invalid price outputs as normal equilibrium results. Raise a typed/clear validation error or return a solver status that the UI handles visibly.
6. **Undefined quantity units:** call them model units in illustrative mode.
7. **Unused and unsourced share fields:** do not copy placeholder `nvShare` values into the new dataset.
8. **Unsupported production-capacity claim:** use “hypothetical output cap”.
9. **Overly broad market claim:** do not imply that two players fully represent the total discrete GPU market.

---

## 9. UI requirements

Use Streamlit's standard multi-page app feature and a restrained dark research-dashboard look. The original React prototype's charcoal background with muted gold and teal accents may be used as inspiration, but functional clarity comes first.

### Global status banner

At the top of every page show one of:

- `ILLUSTRATIVE MODE — parameters are scenario inputs; not empirically calibrated`, or
- `CALIBRATED MODE — show data version, estimation status, units and sample coverage` only after all calibration gates are met.

Version 1 should start in illustrative mode.

### Page 1 — `app.py`: Overview

Show:

- Project title: “NVIDIA vs. AMD: Cournot and Differentiated Bertrand Competition”.
- Research question.
- What the app can and cannot establish.
- The three model scenarios.
- Current status: illustrative / empirical calibration incomplete.
- Short “How to run the demo” navigation.
- Link to the supplied report and source/reference section.

### Page 2 — `1_Model_and_Equations.py`

Show:

- Inverse-demand equations.
- Payoff equation.
- Cournot and Bertrand strategy explanation.
- Reaction functions and closed-form expressions.
- Meaning and limits of `D/B`.
- Units and baseline assumptions.
- `D=0` sanity check.
- Note that the two products are differentiated; do not use the homogeneous-good Bertrand `p=MC` shortcut.

Use readable LaTeX via Streamlit's `st.latex` / Markdown. Do not add a new math renderer dependency.

### Page 3 — `2_Live_Equilibrium.py`

Controls (all inputs visibly labeled as illustrative by default):

- Demand intercept `A`.
- Own-quantity slope `B`.
- Substitutability ratio `D/B`; set bounds in `[0, 0.95]`; compute `D` internally as `ratio * B`.
- NVIDIA cost input `c1`.
- AMD cost input `c2`.
- Metric selector: price / quantity / per-unit margin / model payoff.

Outputs:

- KPI cards for NVIDIA and AMD under each game.
- Cournot vs. Bertrand chart for the selected metric.
- Result table with all prices, quantities, margins, payoffs, and status.
- Current parameter table, including both `D/B` and derived `D`.
- Expandable “Show calculation details” area showing formulas and substituted parameter values.
- Concise computed interpretation, e.g. “Under the current illustrative inputs, Bertrand predicts lower/higher [selected metric] than Cournot for NVIDIA.” Generate this from the numerical results; never bake in the direction as fixed text.
- Visible warnings if a scenario is invalid or at a boundary.

### Page 4 — `3_Capacity_and_Scenarios.py`

Show:

- Unconstrained Cournot outcome.
- Slider for `q1_cap` labelled hypothetical.
- Whether the cap is binding or nonbinding.
- Constrained outcome and change from the unconstrained result.
- Chart/table comparing both cases.
- Scenario tests such as lower/higher NVIDIA cost, lower/higher AMD cost, and a range of `D/B` values. Change one factor at a time for interpretable experiments.

### Page 5 — `4_Data_and_Validation.py`

Show:

- Table of source-backed launch MSRPs from the CSV.
- SKU/version, firm, announced MSRP, currency, source type, source URL, and notes.
- State clearly that MSRP is not a realized street price, sales quantity, average selling price, or model calibration.
- Display data-readiness checks: what required fields are present/missing, whether the data contain comparable quantity-price observations, and whether a real validation metric can be calculated.
- Default validation status: `Not calibrated — no evidence-backed MAE/model winner is available`.
- If no compatible observations exist, do not invent a chart of “predicted vs actual”, do not display a winner badge, and do not calculate a pseudo-validation MAE using placeholder costs.
- Include the MAE definition only as a method reference, and compute it only when the user has an eligible dataset with actual and predicted observations tied to a documented model version.
- Do not infer SKU quantities from company-wide segment revenue or convert overall market shares into SKU sales without an explicit defensible method.

### Page 6 — `5_Demo_Guide.py`

Provide a simple presenter script (around 5–7 minutes, adjustable):

1. Introduce the question and distinguish scenario simulation from empirical estimation.
2. Explain the demand equations.
3. Run the default Cournot/Bertrand comparison.
4. Change `D/B` and explain the recalculation.
5. Show binding versus nonbinding output cap.
6. Display the source-backed MSRP table and missing empirical data.
7. Close with what the model can conclude and its limitations.

Add a small “Questions the instructor may ask” section covering Nash equilibrium, why differentiated Bertrand is used, what `D/B` means, why cap logic matters, why MSRP alone cannot calibrate quantity demand, and why the current model cannot establish actual company profits.

---

## 10. Data files and source provenance

### 10.1 `data/illustrative_defaults.json`

Store the synthetic baseline from Section 7. Required field: `status: illustrative`. Include the unit labels and explanatory note. Do not label this file `calibrated_parameters.json`.

### 10.2 `data/gpu_launch_prices.csv`

Create a small, source-backed descriptive table using only the official announcements already listed in `report.md`. Suggested columns:

- `firm`
- `product_name`
- `sku_configuration`
- `launch_msrp_usd`
- `price_type` (for these rows: announced launch MSRP/SEP)
- `source_url`
- `source_name`
- `source_date` (use the date stated in the cited announcement; if uncertain, leave blank and flag for team verification rather than guessing)
- `source_status` (e.g. `officially reported`)
- `notes`

Seed the descriptive file with these sourced MSRP observations from the research report:

| Firm | SKU / configuration | Announced price | Source |
|---|---|---:|---|
| NVIDIA | GeForce RTX 4080 16 GB | 1199 USD | https://www.nvidia.com/en-us/geforce/news/gfecnt/20229/rtx-40-series-graphics-cards-announcements/ |
| AMD | Radeon RX 7900 XTX | 999 USD | https://ir.amd.com/news-events/press-releases/detail/1099/amd-unveils-worlds-most-advanced-gaming-graphics-cards-built-on-groundbreaking-amd-rdna-3-architecture-with-chiplet-design |
| NVIDIA | GeForce RTX 4070 | 599 USD | https://investor.nvidia.com/news/press-release-details/2023/NVIDIA-GeForce-RTX-4070-Brings-Power-of-Ada-Lovelace-Architecture-and-DLSS-3-to-Millions-More-Gamers-and-Creators-Starting-at-599/default.aspx |
| AMD | Radeon RX 7800 XT | 499 USD | https://www.amd.com/en/newsroom/press-releases/2023-8-25-new-amd-radeon-rx-7800-xt-and-radeon-rx-7700-xt-gr.html |
| NVIDIA | GeForce RTX 5080 | 999 USD | https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Blackwell-GeForce-RTX-50-Series-Opens-New-World-of-AI-Computer-Graphics/ |
| AMD | Radeon RX 9070 XT | 599 USD | https://ir.amd.com/news-events/press-releases/detail/1238/amd-unveils-next-generation-amd-rdna-4-architecture-with-the-launch-of-amd-radeon-rx-9000-series-graphics-cards |
| NVIDIA | GeForce RTX 5070 | 549 USD | https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Blackwell-GeForce-RTX-50-Series-Opens-New-World-of-AI-Computer-Graphics/ |
| AMD | Radeon RX 9060 XT 16 GB | 349 USD | https://ir.amd.com/news-events/press-releases/detail/1253/amd-introduces-new-radeon-graphics-cards-and-ryzen-threadripper-processors-at-computex-2025 |

Keep configuration-specific names clear, especially RTX 4080 16 GB (the 12 GB configuration announced under that name had a different price) and RX 9060 XT 16 GB (the 8 GB configuration has a different price).

These entries allow a descriptive MSRP chart/table only. They do **not** supply `quantity_units`, unit sales, actual consumer transaction price, or marginal cost. Do not feed them to a structural demand regression as if they were a complete panel.

### 10.3 Evidence statuses

Use the following status vocabulary consistently:

- `officially reported`
- `market-research source`
- `estimated from data`
- `derived`
- `scenario input`
- `placeholder`
- `missing / not available`

Display status close to the number, not only in an appendix. Where appropriate, expose source name, URL, price type, unit, and date.

### 10.4 `data/data_dictionary.md`

Document the required schema for any later calibration dataset. At minimum it should define market scope, period, geography, firm, SKU, price type, price and currency, quantity units/source, rival price, quality/performance index, cost proxy, source URL, source type, and missing-value handling. Document that the data currently shipped with the first version have no compatible product-level quantities.

### 10.5 Calibration policy

Do not make the app perform a misleading regression simply because `statsmodels` is installed. Demand calibration requires compatible price and quantity observations and a documented identification strategy. Prices can be endogenous, quantity/price observations need matched periods and products, and small MSRP tables are insufficient.

If the team later adds appropriate data, calibration must be a clearly separate, documented phase with:

1. scope and units validation;
2. missingness and descriptive checks;
3. a written demand specification;
4. an estimation method appropriate to its identification assumptions;
5. parameter uncertainty/diagnostics where feasible;
6. feasibility checks for the estimated parameter region;
7. saved data version and parameter output;
8. separate calibration and validation observations if the sample supports it;
9. honest reporting when the data cannot identify the model.

For version 1, a **data-readiness page** is more important than pretending a full empirical calibration exists.

---

## 11. Validation and unit-test requirements

Write mathematical model functions as pure functions: inputs in, structured result out. They must not depend on Streamlit session state or chart code.

### Required unit tests

1. **`D=0` equivalence:** Cournot and Bertrand return the same independent-monopoly price, quantity, and payoff for each firm when the interior solution is feasible.
2. **Symmetry:** if `c1 == c2`, a symmetric admissible model returns equal outcomes for the two firms in each game.
3. **Demand inversion:** plugging direct-demand quantities back into inverse demand reproduces the stated prices within numerical tolerance.
4. **Cournot FOCs:** results satisfy both first-order conditions within a tolerance such as `1e-6` for the standard test values.
5. **Bertrand FOCs:** results satisfy each firm's price first-order condition within tolerance.
6. **Parameter guard:** reject or clearly mark `B <= 0`, `D < 0`, and `D >= B` for this shared base model.
7. **Feasibility:** a negative interior quantity or invalid price must not be presented as a valid equilibrium. Return an explicit failure/warning or implement and test the appropriate boundary solution.
8. **Slider mapping:** if `r=D/B`, changing `r` updates `D=r*B`, and the displayed ratio matches the solver input.
9. **Binding cap:** for the baseline, `q1_cap=120` gives `q1=120` and AMD best response `q2=167.2`.
10. **Nonbinding cap:** a cap higher than the unconstrained NVIDIA Cournot quantity returns exactly the unconstrained equilibrium.
11. **Cap equality:** a cap at the unconstrained quantity should not change results except for tiny floating-point tolerance.
12. **Payoff formula:** `pi_i == (p_i - c_i) * q_i`.
13. **Metrics guards:** MAE/RMSE functions reject missing values or mismatched array lengths and do not run if there are no valid observations.
14. **Data status:** MSRP-only data are categorized as descriptive and do not unlock empirical model validation.
15. **Repeatability:** repeated identical inputs return the same outputs.

Run `pytest -q` and fix all failures before declaring the project complete.

### Feasibility strategy for version 1

To avoid making the first version too complex, either:

- restrict input ranges to a known valid interior region and still show a solver warning when any unexpected invalid output occurs; or
- implement and test the relevant nonnegative boundary case.

Do not silently clip negative Cournot/ Bertrand quantities to zero while leaving the rest of the closed-form solution unchanged; that would generally not be a correct equilibrium.

---

## 12. Charts and interpretation rules

Use Plotly for interactive charts, but keep charts focused.

Required charts:

1. **Equilibrium comparison bar chart:** Cournot vs. Bertrand for the selected metric, with NVIDIA and AMD clearly distinguished.
2. **Substitutability sensitivity line chart:** calculated outcomes over a bounded set of `D/B` values, keeping other inputs fixed. Plot at least one interpretable metric such as both firms' prices or payoffs.
3. **Capacity comparison:** unconstrained Cournot vs. cap scenario, clearly indicating binding/nonbinding status.
4. **Launch MSRP descriptive chart/table:** official MSRP values by specified SKU, without mixing them up with predicted equilibrium prices.

Optional only if straightforward:

- reaction functions / best-response illustration;
- actual-vs-predicted chart when proper compatible validation data become available.

Every chart must have a title, readable axis names, and units/status in a caption or subtitle. Do not show a fabricated “Actual” series. A launch MSRP chart must be visually and verbally separate from equilibrium output charts.

### Interpretation rules

- The UI's dynamic narrative must be based on the numeric result.
- Treat changes from sliders as model counterfactuals, not causal evidence.
- Do not assume every comparative static is monotonic under asymmetric costs; compute and show the result.
- No “winner” badge based on toy MAE.
- No unsupported claims about true NVIDIA/AMD margin, profit, market share, die cost, wafer allocation, or consumer switching behavior.

---

## 13. Research sources to carry into the app/report

Use the links already listed in `report.md`. Show a concise subset in the app, and retain the full bibliography in the paper/report.

### Market context and data boundaries

- Jon Peddie Research, AIB market summary: https://www.jonpeddie.com/news/q126-pc-graphics-add-in-board-shipments-decreased-0-6-from-last-quarter-to-12-million-units-with-a-cagr-to-2029-of-3-3/
- Jon Peddie Research, AIB report description: https://www.jonpeddie.com/store/
- NVIDIA FY2026 Form 10-K (Gaming segment scope): https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm
- AMD FY2025 Form 10-K (Client and Gaming segment scope): https://www.sec.gov/Archives/edgar/data/2488/000000248826000021/amd-20251227.htm

### Model and demand-estimation context

- S. Berry and P. Haile, “Identification in Differentiated Products Markets”: https://www.annualreviews.org/doi/10.1146/annurev-economics-080315-015050
- P. Choné and L. Linnemer, “Linear demand systems for differentiated goods: Overview and user’s guide”: https://doi.org/10.1016/j.ijindorg.2020.102663

### Paper-format reference

- IEEE conference authoring tools and templates: https://conferences.ieeeauthorcenter.ieee.org/write-your-paper/authoring-tools-and-templates/
- IEEE conference paper structure guidance: https://conferences.ieeeauthorcenter.ieee.org/write-your-paper/structure-your-paper/

The full launch-price links are included in Section 10.2. Source links should open in a new browser tab or be clickable through Streamlit Markdown. If a source is inaccessible, do not replace it with an invented citation; mark it for team verification.

---

## 14. `requirements.txt` and environment

Keep dependencies small. A suitable starting point is:

```text
streamlit
numpy
pandas
plotly
pytest
```

Add `scipy` or `statsmodels` only if the shipped code actually uses them. Pin versions after verifying that the app installs and tests pass in the target Python environment. Do not add libraries for features not in scope.

### Commands the README must include

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -q
streamlit run app.py
```

Windows PowerShell alternative:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -q
streamlit run app.py
```

Also explain how to stop Streamlit (`Ctrl+C`) and how to start it again. Do not require environment variables or secrets for version 1.

---

## 15. README requirements

`README.md` must contain:

1. Project title and 2–3 sentence description.
2. Features list.
3. Explicit model-status warning: built-in parameters are illustrative and not empirically calibrated.
4. Technology stack.
5. Folder structure with brief file descriptions.
6. Installation and run instructions for macOS/Linux and Windows.
7. Test command.
8. Definition of parameters `A`, `B`, `D`, `D/B`, `c1`, `c2`, `q1_cap`.
9. Data-source/provenance rules and the limitation that MSRP data do not provide product quantities.
10. Scope limits and disclaimer that model payoffs are not company-reported profits.
11. A short 5–7 minute demo walkthrough.
12. Known limitations and requirements for future empirical calibration.

---

## 16. Design requirements

- Academic, readable, and restrained; a charcoal/dark-green background with warm-gold and teal accents is acceptable as a nod to the old prototype.
- No decorative elements that crowd out equations or findings.
- Display one source/status label near every important input or observation.
- Use clear labels: “NVIDIA” and “AMD” in every chart and table.
- Use `USD` only for the documented official MSRP table. In the illustrative model, label values “model price units” unless the full parameter system has been calibrated in compatible USD units.
- Label quantity as “model units (illustrative)” in scenario mode.
- Maintain readable layout on a normal laptop screen and during screen sharing.
- Use enough explanation so a student can present the app without inspecting source code.
- No “live market data” language unless the app actually fetches a current data source; version 1 is local/static data plus live mathematical recomputation.

---

## 17. Completion checklist

### A. Research alignment

- [ ] App has the correct research question and two-firm scope disclaimer.
- [ ] Cournot, differentiated Bertrand, and capacity-constrained Cournot are explained correctly.
- [ ] Shared demand model and notation match `report.md`.
- [ ] Homogeneous-good Bertrand shortcut is not used.
- [ ] Illustrative, source-backed, derived, and estimated values are distinguishable.
- [ ] No claim of empirical calibration is made without the required data and estimation evidence.

### B. Mathematical correctness

- [ ] Cournot closed form and output metrics match the equations.
- [ ] Bertrand demand inversion, price solution, and recovered quantities match the equations.
- [ ] `D=0` Cournot/Bertrand equivalence test passes.
- [ ] FOC and demand-identity tests pass.
- [ ] Invalid/infeasible outputs are blocked or visibly flagged.
- [ ] Slider ratio is implemented consistently as `D/B`.
- [ ] Capacity cap is nonbinding above the unconstrained equilibrium and binding below it.
- [ ] Model payoff and margin definitions are shown correctly.

### C. Data and provenance

- [ ] MSRP CSV has source URLs and SKU configurations.
- [ ] RTX 4080 is identified as 16 GB in its $1,199 row.
- [ ] RX 9060 XT is identified as 16 GB in its $349 row.
- [ ] MSRP is not confused with transaction prices, quantities, or ASP.
- [ ] No fabricated quantities, shares, or cost proxies are shipped as data.
- [ ] Data-readiness check correctly says empirical validation is unavailable when only MSRP rows exist.
- [ ] No illustrative MAE is presented as a scientific model-comparison result.

### D. User experience

- [ ] Overview page states the research question, scope, and status.
- [ ] Equation page explains parameters and models.
- [ ] Live equilibrium page updates all outputs from solver results.
- [ ] Capacity page explains binding vs. nonbinding status.
- [ ] Data page includes source links and missing-data explanation.
- [ ] Demo guide includes a presentable walkthrough and likely questions.
- [ ] Charts have names, axis labels, units, and evidence status.
- [ ] Application opens without a runtime error from a clean launch.

### E. Packaging and tests

- [ ] Folder structure and module responsibilities are followed or any changes are documented.
- [ ] `requirements.txt` includes only used dependencies.
- [ ] README instructions work in a clean virtual environment.
- [ ] `pytest -q` passes.
- [ ] The app runs via `streamlit run app.py`.
- [ ] A final note records completed features and any remaining empirical blockers.

### Final acceptance gate

The build is **demo-ready** when the Streamlit app launches, every interactive output comes from the tested Python model, required tests pass, all scenario values are labeled honestly, and the user can demonstrate the three games/scenarios.

The project is **not empirically calibrated** merely because it contains an MSRP table or computes MAE. It may be called calibrated only after compatible price/quantity data, a justified estimation design, parameter provenance, feasibility checks, and appropriate validation are completed and documented.

---

## 18. Expected handoff from Antigravity

When finished, provide:

1. A brief summary of the app that was built.
2. The final folder tree.
3. The exact commands to install, test, and launch it.
4. The test output/result.
5. Any deviations from this specification and the reason for each.
6. A short list of unfinished items, especially missing empirical data or uncompleted calibration.
7. Confirmation that no fabricated market values or unsupported empirical conclusions were added.

**End of build specification.**

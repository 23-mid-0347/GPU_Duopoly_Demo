# NVIDIA vs. AMD: GPU Duopoly Simulator

An interactive game-theory teaching simulator built with Python + Streamlit that compares
**Cournot quantity competition** and **differentiated Bertrand price competition** in a
stylised two-firm duopoly representing NVIDIA and AMD.

> ⚠️ **Model-status warning:** All built-in parameters are **illustrative scenario inputs** —
> they are *not* empirically calibrated to NVIDIA/AMD data. The app is a theoretical simulator,
> not a market forecast tool. See the Data & Validation page for the full calibration-readiness status.

---

## Features

- Live Cournot and differentiated Bertrand equilibrium solver (closed-form, analytical)
- Adjustable demand intercept (`A`), own-quantity slope (`B`), substitutability ratio (`D/B`),
  and cost inputs (`c₁`, `c₂`)
- Hypothetical NVIDIA output-cap scenario with correct binding/nonbinding logic
- Sensitivity sweep across D/B values with interactive Plotly charts
- Source-backed official launch MSRP reference table (descriptive only — not model calibration)
- Honest data-readiness and validation status page (reports what is missing)
- Calculation details with FOC residual verification
- 5–7 minute presenter demo guide with instructor Q&A section
- 101-test suite covering all model functions, feasibility checks, and data-readiness logic

---

## Technology Stack

| Purpose | Library | Version |
|---|---|---|
| App / UI | Streamlit | ≥ 1.32.0 |
| Numerical operations | NumPy | ≥ 1.26.0 |
| Data tables | pandas | ≥ 2.2.0 |
| Interactive charts | Plotly | ≥ 5.20.0 |
| Tests | pytest | ≥ 8.0.0 |

**Python target:** 3.12 (tested on 3.12+)

---

## Folder Structure

```text
gpu-duopoly-project/
├── app.py                        # Landing page (Streamlit entry point)
├── requirements.txt
├── README.md
├── BUILD_PLAN.md                 # Implementation specification
├── report.md                     # Research report (source of truth; do not modify via app)
├── plan.md                       # Original project plan
├── gpu-duopoly-model.jsx         # Legacy React prototype (reference only; not run)
│
├── pages/
│   ├── 1_Model_and_Equations.py  # Demand equations, notation, D=0 identity
│   ├── 2_Live_Equilibrium.py     # Interactive Cournot vs. Bertrand comparison
│   ├── 3_Capacity_and_Scenarios.py # Hypothetical NVIDIA cap and scenario experiments
│   ├── 4_Data_and_Validation.py  # Sourced MSRP table and calibration-readiness status
│   └── 5_Demo_Guide.py           # Presenter script and instructor Q&A
│
├── models/
│   ├── __init__.py
│   ├── demand.py                 # Inverse/direct demand, input validation, D/B → D
│   ├── cournot.py                # Cournot equilibrium solver and reaction functions
│   ├── bertrand.py               # Differentiated Bertrand solver and FOC checker
│   ├── capacity.py               # Capacity-constrained Cournot (binding/nonbinding)
│   └── metrics.py                # Margin, payoff, MAE/RMSE guards
│
├── analysis/
│   ├── __init__.py
│   ├── sensitivity.py            # D/B sensitivity sweep (solver calls, returns dicts)
│   └── data_readiness.py         # MSRP/calibration dataset readiness checks
│
├── data/
│   ├── gpu_launch_prices.csv     # Official launch MSRPs (descriptive, sourced)
│   ├── illustrative_defaults.json # Scenario baseline parameters (status: illustrative)
│   └── data_dictionary.md        # Column definitions, evidence statuses, permitted analyses
│
├── utils/
│   ├── __init__.py
│   ├── provenance.py             # Status badges and mode banner
│   └── formatting.py             # Number and message formatters
│
└── tests/
    ├── test_demand.py            # Demand validation, inversion roundtrip, ratio mapping
    ├── test_cournot.py           # Smoke test, D=0, symmetry, FOC, payoff, repeatability
    ├── test_bertrand.py          # Smoke test, D=0, demand inversion, FOC, payoff
    ├── test_capacity.py          # Binding/nonbinding cap, AMD best response, reference values
    ├── test_metrics.py           # MAE/RMSE guards, payoff formula
    └── test_data_readiness.py    # MSRP-only cannot unlock validation; missing column reporting
```

---

## Installation and Run Instructions

### macOS / Linux

```bash
# 1. Create a virtual environment
python3 -m venv .venv

# 2. Activate it
source .venv/bin/activate

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the test suite (must pass before running the app)
pytest -q

# 6. Launch the app
streamlit run app.py
```

### Windows PowerShell

```powershell
# 1. Create a virtual environment
py -m venv .venv

# 2. Activate it
.venv\Scripts\Activate.ps1

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the test suite
pytest -q

# 6. Launch the app
streamlit run app.py
```

### Stopping and restarting

- Stop the app: press `Ctrl+C` in the terminal running Streamlit
- Restart: run `streamlit run app.py` again (virtual environment must be activated)
- No environment variables or secrets are required for version 1

---

## Test Command

```bash
pytest -q
```

Expected output: `101 passed` (or similar count as tests are added). All tests must pass
before the build is considered complete.

---

## Parameter Definitions

| Symbol | Parameter | Meaning |
|---|---|---|
| `A` | Demand intercept | Price when both quantities are zero (model price units) |
| `B` | Own-quantity slope | `B > 0`; price falls by `B` per unit of own output |
| `D` | Cross-quantity term | `0 ≤ D < B`; price falls by `D` per unit of rival output |
| `D/B` | Substitutability ratio | Dimensionless; slider range `[0, 0.95)` — D is derived as `ratio × B` |
| `c₁` | NVIDIA cost input | Illustrative marginal cost input for NVIDIA (model price units) |
| `c₂` | AMD cost input | Illustrative marginal cost input for AMD (model price units) |
| `q1_cap` | NVIDIA output cap | Hypothetical upper bound on NVIDIA output (model units; NOT an observed TSMC allocation) |

**Critical note:** `D` is always computed internally as `ratio × B`. The slider controls `D/B`.
Do not store the slider ratio directly as `D` — this was a bug in the original React prototype.

---

## Data Sources and Provenance

| Data type | Status | Permitted uses |
|---|---|---|
| Official launch MSRP | `officially reported` | Descriptive reference table and chart only |
| Model parameters (A, B, D/B, c₁, c₂) | `placeholder` / `scenario input` | Illustrative simulation only |
| SKU-level quantities | `missing / not available` | Cannot be used — data do not exist |
| Marginal cost proxies | `missing / not available` | Cannot be used — data do not exist |

**MSRP limitation:** The CSV contains officially announced launch prices (Manufacturer's Suggested
Retail Price). This is NOT:
- A realized consumer transaction price
- An average selling price (ASP)
- A quantity observation
- A demand-model calibration input

Product-level quantity data are required for structural demand estimation and are not currently
available in this project.

---

## Scope Limits and Disclaimers

- **Two firms only:** Intel Arc and other GPU suppliers are not modelled. This is a two-firm submarket model.
- **Model payoffs ≠ reported profits:** payoff = (price − cost_input) × quantity in model units. This omits fixed costs, R&D, taxes, multi-segment accounting, and channel margins.
- **Per-unit margin = `p − c` in model price units** — not a percentage margin.
- **NVIDIA output cap is hypothetical** — not claimed to be an observed TSMC wafer allocation.
- **All quantities are model units (illustrative)** — not actual GPU cards shipped.
- **Comparative statics are model counterfactuals** — not causal evidence about real GPU markets.

---

## 5–7 Minute Demo Walkthrough

1. **Overview page** — introduce the research question and explain scenario vs. empirical simulation
2. **Model & Equations page** — show the inverse-demand system and D/B concept
3. **Live Equilibrium page** — run default parameters; show Bertrand < Cournot prices; change D/B from 0 to 0.9
4. **Capacity & Scenarios page** — show binding cap (q1_cap=120) and then move cap to nonbinding
5. **Data & Validation page** — show the MSRP table, source links, and the ❌ missing data fields
6. **Close** — summarise: the model demonstrates game-theory concepts; empirical calibration requires the missing data

See **Page 5 — Demo Guide** in the app for the full scripted walkthrough and instructor Q&A.

---

## Known Limitations and Future Calibration Requirements

### Version 1 limitations
- Interior solutions only (boundary equilibria not implemented)
- No dynamics, inventory, or repeated-game effects
- Symmetric D (asymmetric substitutability not modelled)
- No identification strategy for demand estimation has been implemented

### Requirements for future empirical calibration
1. Compatible price/quantity observations (SKU-level, matched by period and firm)
2. A documented demand specification and identification strategy
3. An estimation method addressing price endogeneity (e.g., instruments)
4. Feasibility checks for estimated parameter region (B > 0, 0 ≤ D < B)
5. A validation holdout sample or appropriate baseline
6. Saved data version and parameter output for reproducibility
7. Honest reporting when the data cannot identify the model

See `data/data_dictionary.md` for the full calibration dataset schema.

---

## References

- Berry & Haile (2016), "Identification in Differentiated Products Markets": https://www.annualreviews.org/doi/10.1146/annurev-economics-080315-015050
- Choné & Linnemer (2020), "Linear demand systems for differentiated goods": https://doi.org/10.1016/j.ijindorg.2020.102663
- Jon Peddie Research AIB shipments: https://www.jonpeddie.com/news/q126-pc-graphics-add-in-board-shipments-decreased-0-6-from-last-quarter-to-12-million-units-with-a-cagr-to-2029-of-3-3/
- NVIDIA FY2026 10-K: https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm
- AMD FY2025 10-K: https://www.sec.gov/Archives/edgar/data/2488/000000248826000021/amd-20251227.htm

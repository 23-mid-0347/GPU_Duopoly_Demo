# Data Dictionary — GPU Duopoly Simulator

**Version:** 1.0 (illustrative mode)  
**Last updated:** October 2026  
**Status:** No compatible product-level quantities available. The shipped dataset is descriptive MSRP only.

---

## 1. `gpu_launch_prices.csv` — Official Launch MSRP Reference

This file contains **descriptive, source-backed** official launch MSRP (Manufacturer's Suggested Retail Price / Suggested Retail Price) observations for selected NVIDIA and AMD discrete GPU SKUs. It does **not** contain realized transaction prices, unit sales quantities, average selling prices, or marginal costs.

### Column Definitions

| Column | Type | Description |
|---|---|---|
| `firm` | string | "NVIDIA" or "AMD" |
| `product_name` | string | Official product family name (e.g. GeForce RTX 4080) |
| `sku_configuration` | string | Memory size or variant if relevant to the price (e.g. "16 GB GDDR6X"). Blank if only one configuration was announced at that MSRP. |
| `launch_msrp_usd` | float | Announced launch MSRP or SEP in USD at product introduction |
| `price_type` | string | Always "announced launch MSRP/SEP" for this file |
| `source_url` | string | URL of the primary official source (press release or product page) |
| `source_name` | string | Human-readable citation label |
| `source_date` | string | Date stated in or associated with the announcement (YYYY-MM-DD or YYYY-MM). Left blank if uncertain — do not guess. |
| `source_status` | string | Evidence status (see vocabulary below). All rows in this file are "officially reported". |
| `notes` | string | Configuration clarifications, caveats, or additional context |

### Evidence Status Vocabulary

- `officially reported` — from an official press release or product announcement
- `market-research source` — from a paid market-research report (e.g. JPR)
- `estimated from data` — derived via a documented method from other observations
- `derived` — calculated from other values in this or another dataset
- `scenario input` — user-specified scenario parameter, not measured
- `placeholder` — synthetic value; must be replaced before empirical claims
- `missing / not available` — required field not yet sourced

---

## 2. `illustrative_defaults.json` — Baseline Simulator Parameters

| Field | Type | Description |
|---|---|---|
| `status` | string | Always "illustrative" — these are NOT calibrated parameters |
| `A` | float | Inverse-demand intercept (model price units) |
| `B` | float | Own-quantity slope — must be > 0 |
| `substitutability_ratio_D_over_B` | float | D/B slider default — must be in [0, 1) |
| `c1_nvidia` | float | NVIDIA marginal cost scenario input (model price units) |
| `c2_amd` | float | AMD marginal cost scenario input (model price units) |
| `nvidia_output_cap` | float | Hypothetical output cap for NVIDIA capacity scenario |
| `quantity_unit_label` | string | "model units (illustrative)" |
| `price_unit_label` | string | "model price units (illustrative; not calibrated USD forecast)" |

**D is computed internally** as `D = substitutability_ratio_D_over_B × B`. The ratio is the slider control; D is never stored directly.

---

## 3. Calibration Dataset Schema (required for future empirical phase)

The following schema defines what a calibration-eligible dataset MUST contain before structural demand estimation can begin. **This dataset does not yet exist.**

| Column | Type | Description |
|---|---|---|
| `firm` | string | "NVIDIA" or "AMD" |
| `sku` | string | Specific SKU identifier |
| `period` | string | Time period (e.g. quarter: "2023Q1") |
| `price_usd` | float | Realized transaction price or ASP — NOT just MSRP |
| `quantity_units` | float | Compatible unit-sales volume (source must be stated) |
| `rival_price_usd` | float | Contemporaneous rival firm's price for a comparable tier |
| `quality_index` | float | Optional: performance index for hedonic control |
| `cost_proxy_usd` | float | Optional: documented die-cost proxy (e.g. SemiAnalysis method) |
| `source_url` | string | URL of the primary data source |
| `source_type` | string | Evidence status (see vocabulary above) |
| `notes` | string | Caveats about data quality or coverage |

### Missing-value policy

- Do not fill missing `quantity_units` values with company-wide segment revenue ÷ ASP without a documented defensible method.
- Do not infer SKU-level sales from overall market share percentages without a compatible share definition and period.
- Missing values must be flagged; they do not default to zero or any estimate.

---

## 4. Analyses Permitted by Current Data

| Analysis | Permitted? | Reason |
|---|---|---|
| Descriptive MSRP table | ✅ Yes | Source-backed official announcements |
| Equilibrium simulation with scenario inputs | ✅ Yes | Illustrative mode — clearly labeled |
| Sensitivity analysis over D/B range | ✅ Yes | Model counterfactual — clearly labeled |
| Structural demand regression | ❌ No | No compatible price/quantity observations |
| MAE/RMSE model comparison | ❌ No | No matched observations for validation |
| "Cournot fits better than Bertrand" winner badge | ❌ No | Requires calibration and validation data |
| Claims about NVIDIA/AMD actual marginal costs | ❌ No | No cost data with documented estimation |
| Claims about TSMC wafer allocations | ❌ No | No compatible capacity data |

---

## 5. Market Scope Disclaimer

The model has **two players only**. Intel Arc and other discrete GPU suppliers are not modeled. Do not call the two-firm simulation a full representation of the total discrete GPU market. The Jon Peddie Research AIB summaries cover a broader market than the two-firm submarket modeled here.

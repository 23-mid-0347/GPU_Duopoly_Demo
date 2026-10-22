# The NVIDIA vs. AMD Duopoly — Project Plan
### Cournot vs. Bertrand Competition in the Discrete GPU Market

---

## 1. Thesis

NVIDIA and AMD compete in the desktop discrete-GPU market as a two-firm, differentiated-product
duopoly. We model this as both a **Cournot game** (firms compete on quantity/supply) and a
**Bertrand game** (firms compete on price), derive the Nash equilibrium for each, calibrate both
against real launch-window data, and use the gap between the two models' predictions — and between
each model and reality — to explain why NVIDIA sustains higher margins than AMD despite AMD
often offering more VRAM per dollar.

**Core methodological decision:** we do NOT use textbook homogeneous-good Bertrand (price =
marginal cost, winner-take-all). NVIDIA and AMD GPUs are differentiated products — brand,
CUDA/DLSS lock-in, and driver ecosystem create real switching costs. Using homogeneous Bertrand
would predict a market collapse to one firm, which plainly doesn't happen. Instead we use a
**linear differentiated-demand system** that both games share, so the Cournot/Bertrand comparison
is apples-to-apples.

---

## 2. The model

### 2.1 Demand system

Two-firm inverse demand, with `A` = market size/intercept, `B` = own-price sensitivity, `D` =
cross-price sensitivity (substitutability):

```
p1 = A − B·q1 − D·q2
p2 = A − B·q2 − D·q1
```

- `D / B` is the **substitutability index**. `D/B → 0` means the two firms behave like independent
  monopolies (no competitive pressure). `D/B → 1` means the goods are near-perfect substitutes
  (classic homogeneous Bertrand).
- We allow the possibility of an **asymmetric** substitutability parameter (`D12 ≠ D21`) as a
  stretch goal — this is the sharpest available explanation for margin asymmetry: a price cut by
  AMD may pull relatively few NVIDIA buyers away (CUDA/mindshare moat = low D from NVIDIA's
  perspective), while a price cut by NVIDIA pulls many price-sensitive AMD buyers over (higher D
  from AMD's perspective).

### 2.2 Cournot equilibrium (quantity competition)

Each firm chooses quantity `qi` to maximize `(pi − ci)·qi`, taking the rival's quantity as given.
First-order condition: `A − 2B·qi − D·qj − ci = 0`. Solving the resulting 2×2 linear system for
`q1, q2` gives closed-form Nash quantities, and prices follow from the inverse demand equations.

### 2.3 Bertrand equilibrium (price competition)

Invert the demand system to get direct demand `qi(p1, p2)`. Each firm chooses price `pi` to
maximize `(pi − ci)·qi(p1, p2)`, taking the rival's price as given. Solving the resulting 2×2
system gives closed-form Nash prices, and quantities follow from direct demand.

**Sanity check already verified:** at `D = 0` both games collapse to the same independent-monopoly
solution (no strategic interaction to model), and as `D` increases, Bertrand consistently predicts
lower prices and lower profits than Cournot for the same cost structure — matching standard theory
that price competition is harsher than quantity competition under substitutes.

### 2.4 Capacity-constrained variant (bonus)

Real GPU output is bounded by TSMC wafer allocation, not a free strategic choice. We model this as
a **capacity-constrained Cournot** scenario: fix NVIDIA's quantity at an exogenous cap (its fab
allocation) and let AMD best-respond via its normal Cournot reaction function. This is the closest
formal analogue to "NVIDIA doesn't flood the market because it structurally can't," and it directly
supports the original research question about why NVIDIA sustains margins.

---

## 3. Data plan

| Data needed | Source | Used for |
|---|---|---|
| Discrete GPU unit shipments / market share, by quarter | Jon Peddie Research (JPR) reports | Calibrating quantities; validating share predictions |
| Launch MSRP by SKU (RTX 40/50-series, RX 6000/7000/9000-series) | Public launch coverage, company press releases | Price data points per generation |
| Street price drift over time | Historical price-tracking sources (e.g. PCPartPicker price history) | Optional — richer than MSRP-only if time allows |
| Gaming-segment revenue | NVIDIA and AMD 10-Q / 10-K filings | Backing out average selling price (ASP); sanity-checking unit estimates |
| Marginal cost proxy | Die size × TSMC wafer cost estimates (e.g. SemiAnalysis-style public estimates) | Estimating `c1`, `c2` per generation — **not** a true MC, but a standard, defensible proxy if the assumption is stated explicitly |

**Data lead's deliverable:** one clean spreadsheet, one row per GPU generation/launch, columns for
firm, SKU, MSRP, estimated unit shipments or share, estimated die-cost proxy, and launch date.

---

## 4. Calibration plan

1. From the dataset, run a regression of each firm's quantity (or share) on its **own price** and
   the **rival's price**, per generation or pooled across generations.
2. The coefficient on own-price gives `B`; the coefficient on rival's price gives `D`. This is a
   real, data-driven estimate of substitutability rather than an assumed parameter — this is the
   headline empirical result of the project.
3. Cross-check: if time allows, also try an **asymmetric** version (separate regressions for
   NVIDIA's D and AMD's D) to test the "asymmetric substitutability explains the margin gap"
   hypothesis directly.
4. Use the SemiAnalysis-style die-cost proxies as `c1`, `c2` inputs — do not attempt to derive true
   marginal cost; state the proxy assumption explicitly in the writeup.

*(Stretch, if the team is comfortable with it: replace the linear demand system with a nested-logit
discrete-choice demand model, which is the actual industry/antitrust standard for differentiated
products. Higher rigor, more estimation work — only pursue if calibration finishes early.)*

---

## 5. Deliverable format: interactive web app, not a static report

Rationale: the project's core content — "what would have happened if X changed" — is inherently a
live recalculation, not a fixed narrative. A scrollable single-page app lets the audience see the
model, the calibration, and the counterfactuals in one continuous, provable flow rather than
reading claims about what a spreadsheet showed.

### App structure (already prototyped — see `gpu-duopoly-model.jsx`)

1. **Hero** — thesis statement, live headline numbers (current Cournot vs. Bertrand predicted
   price) computed on load, not hardcoded.
2. **Section 01 — The Setup** — demand equations and both games' first-order conditions, shown as
   reference cards.
3. **Section 02 — Calibration Data** — chart of real (or currently placeholder, to be replaced)
   launch-window prices by generation.
4. **Section 03 — Live Equilibrium** — interactive sliders for substitutability (`D/B`), NVIDIA
   marginal cost proxy, AMD marginal cost proxy, and a capacity-constraint toggle. A bar chart and
   a plain-language takeaway sentence recompute live from the closed-form solutions as sliders move.
5. **Section 04 — Predicted vs. Actual** — runs each historical generation's own cost proxy through
   the same equations (still driven by the live substitutability slider) and plots actual MSRP
   against Cournot- and Bertrand-predicted prices, with mean-absolute-error cards showing which
   model fits history better.

### What's already built vs. what's left

- **Built:** full closed-form Cournot/Bertrand math, working sliders, live chart recomputation,
  predicted-vs-actual validation section, visual design system.
- **Left to do:** replace every placeholder number (`A`, `B`, `c1`, `c2`, historical prices/shares)
  with the calibration lead's real regression output; decide whether to add the asymmetric-`D`
  version; write final narrative copy once findings are in.

---

## 6. Team roles

| Role | Owner | Responsibilities | Deliverable |
|---|---|---|---|
| **1. Data & Empirics Lead** | TBD | Source JPR share data, 10-K/10-Q segment revenue, launch MSRP history, and die-size/wafer-cost proxies. Clean into one dataset. | Calibration spreadsheet (Section 3) |
| **2. Theory & Model Lead** | TBD | Formal derivation of the demand system, Cournot Nash equilibrium, Bertrand Nash equilibrium, and (if pursued) the asymmetric-substitutability and capacity-constrained variants. Verify the app's math matches the derivation. | Written derivation + math verification of the app |
| **3. Computational/Calibration Lead** | TBD | Run the regression to estimate `B`/`D` from real data; wire calibrated values into the app; maintain and extend `gpu-duopoly-model.jsx`. | Calibrated live model (replaces placeholders in the app) |
| **4. Analysis & Counterfactual Lead** | TBD | Run and interpret the "what if" scenarios once the model is calibrated; write the plain-language takeaways used in Sections 03–04; drive the final report/deck narrative. | Counterfactual writeup + final presentation structure |

Roles 2 and 3 should sync continuously (theory feeds code directly). Everyone should sit in on the
calibration review — that's where the project's actual finding gets generated, not just its
mechanics.

---

## 7. Timeline

| Week | Focus | Key milestone |
|---|---|---|
| 1 | Data collection + theory derivation, in parallel | Clean dataset ready; Cournot/Bertrand equations formally derived and matched against the app's math |
| 2 | Calibration | Real `B`, `D`, `c1`, `c2` estimated via regression; placeholders in the app replaced with real values |
| 3 | Counterfactuals + validation | Predicted-vs-actual fit assessed (Section 04); asymmetric-D and capacity-constraint scenarios run if time allows |
| 4 | Writeup + polish | Final narrative copy written into the app; presentation/deck assembled from the counterfactual lead's findings |

---

## 8. Open decisions to make as a team before Week 2

- [ ] Symmetric `D` vs. asymmetric `D12`/`D21` — decide based on how much time calibration takes.
- [ ] Linear demand vs. nested-logit discrete choice — default to linear unless the team is
      comfortable with logit MLE estimation.
- [ ] How much of the capacity-constrained scenario to formalize vs. leave as narrative discussion.
- [ ] Final presentation format — live app walkthrough, recorded demo, or app + slide deck hybrid.

---

## 9. Known limitations to state explicitly in the writeup

- Marginal cost is proxied via die size/wafer cost, not true MC — this is standard practice for
  this kind of analysis but should not be overstated as precise.
- Linear demand is an approximation; real GPU demand is likely nonlinear near price extremes.
- The model treats each "generation" as a static one-shot game; it does not capture dynamic effects
  like inventory clearance, mid-cycle price cuts, or anticipation of the next generation's launch.

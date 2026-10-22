"""
analysis/sensitivity.py
========================
Runs repeated Cournot and Bertrand solver calls over a range of D/B values
to produce data suitable for line-chart visualisation.

Returns plain Python dicts/lists — no Streamlit or Plotly dependency.
"""

from __future__ import annotations
import numpy as np
from typing import List, Dict, Any

from models.demand import ratio_to_D, DemandParamError
from models.cournot import solve_cournot
from models.bertrand import solve_bertrand


# ---------------------------------------------------------------------------
# Sensitivity sweep
# ---------------------------------------------------------------------------

def sweep_substitutability(
    A: float,
    B: float,
    c1: float,
    c2: float,
    ratio_min: float = 0.0,
    ratio_max: float = 0.95,
    n_points: int = 50,
) -> List[Dict[str, Any]]:
    """
    Sweep D/B from ratio_min to ratio_max (inclusive, n_points steps) and
    solve Cournot and Bertrand at each point.

    Returns a list of dicts, one per D/B value:
        {
            "ratio"       : float,   # D/B
            "D"           : float,
            "c_status"    : "ok" | "infeasible" | "error",
            "b_status"    : "ok" | "infeasible" | "error",
            # Cournot fields (None if not ok)
            "c_p1", "c_p2", "c_q1", "c_q2",
            "c_m1", "c_m2", "c_pi1", "c_pi2",
            # Bertrand fields (None if not ok)
            "b_p1", "b_p2", "b_q1", "b_q2",
            "b_m1", "b_m2", "b_pi1", "b_pi2",
        }

    Parameters
    ----------
    A, B, c1, c2     — shared demand / cost inputs
    ratio_min / max  — bounds for D/B sweep (capped internally at [0, 0.95])
    n_points         — number of evaluation points
    """
    ratio_min = max(0.0, ratio_min)
    ratio_max = min(0.95, ratio_max)
    ratios = np.linspace(ratio_min, ratio_max, n_points)

    rows = []
    for r in ratios:
        try:
            D = ratio_to_D(float(r), B)
        except DemandParamError:
            D = r * B  # fallback; validator will catch it in solve_*

        c = solve_cournot(A, B, D, c1, c2)
        b = solve_bertrand(A, B, D, c1, c2)

        row: Dict[str, Any] = {"ratio": float(r), "D": D}
        # Cournot
        row["c_status"] = c.status
        row["c_p1"]  = c.p1  if c.status == "ok" else None
        row["c_p2"]  = c.p2  if c.status == "ok" else None
        row["c_q1"]  = c.q1  if c.status == "ok" else None
        row["c_q2"]  = c.q2  if c.status == "ok" else None
        row["c_m1"]  = c.m1  if c.status == "ok" else None
        row["c_m2"]  = c.m2  if c.status == "ok" else None
        row["c_pi1"] = c.pi1 if c.status == "ok" else None
        row["c_pi2"] = c.pi2 if c.status == "ok" else None
        # Bertrand
        row["b_status"] = b.status
        row["b_p1"]  = b.p1  if b.status == "ok" else None
        row["b_p2"]  = b.p2  if b.status == "ok" else None
        row["b_q1"]  = b.q1  if b.status == "ok" else None
        row["b_q2"]  = b.q2  if b.status == "ok" else None
        row["b_m1"]  = b.m1  if b.status == "ok" else None
        row["b_m2"]  = b.m2  if b.status == "ok" else None
        row["b_pi1"] = b.pi1 if b.status == "ok" else None
        row["b_pi2"] = b.pi2 if b.status == "ok" else None

        rows.append(row)

    return rows

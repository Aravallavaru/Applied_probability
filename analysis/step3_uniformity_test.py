"""
Step 3 - Testing uniform play (chi-square goodness-of-fit).

Reads ../data/rps_rounds.csv (produced in Step 2) and tests H0 from Step 1:
each move is drawn i.i.d. Uniform{Rock, Paper, Scissors}. Produces:
  - step3_results.json  (all numeric results)
  - step3_move_frequencies.png  (pooled move-frequency chart with 95% CIs)

Run from the analysis/ folder: `python3 step3_uniformity_test.py`
"""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

MOVES = ["Rock", "Paper", "Scissors"]

# ---- Load data ----
df = pd.read_csv("../data/rps_rounds.csv")
n_rounds = len(df)

# ---- 1. Pooled move frequencies (both players combined) ----
pooled = pd.concat([df["move_a_name"], df["move_b_name"]])
pooled_counts = pooled.value_counts().reindex(MOVES)
n_pooled = int(pooled_counts.sum())
expected_pooled = np.array([n_pooled / 3] * 3)
chi2_pooled, p_pooled = stats.chisquare(pooled_counts.values, f_exp=expected_pooled)

# Wald 95% CI for each pooled proportion
z = stats.norm.ppf(0.975)
props = pooled_counts / n_pooled
ci_pooled = {}
for m in MOVES:
    p_hat = props[m]
    se = np.sqrt(p_hat * (1 - p_hat) / n_pooled)
    ci_pooled[m] = (float(p_hat), float(p_hat - z * se), float(p_hat + z * se))

# ---- 2. Separate tests for position A and position B ----
position_results = {}
for label, col in [("A", "move_a_name"), ("B", "move_b_name")]:
    counts = df[col].value_counts().reindex(MOVES)
    n = int(counts.sum())
    expected = np.array([n / 3] * 3)
    chi2, p = stats.chisquare(counts.values, f_exp=expected)
    position_results[label] = {
        "counts": {k: int(v) for k, v in counts.items()},
        "n": n,
        "chi2": float(chi2),
        "p": float(p),
    }

# ---- 3. Outcome distribution test (Tie / A_win / B_win) ----
outcome_counts = df["outcome"].value_counts().reindex(["Tie", "A_win", "B_win"])
n_out = int(outcome_counts.sum())
expected_out = np.array([n_out / 3] * 3)
chi2_out, p_out = stats.chisquare(outcome_counts.values, f_exp=expected_out)

results = {
    "n_rounds": int(n_rounds),
    "pooled_counts": {k: int(v) for k, v in pooled_counts.items()},
    "n_pooled": n_pooled,
    "chi2_pooled": float(chi2_pooled),
    "p_pooled": float(p_pooled),
    "ci_pooled": ci_pooled,
    "position_results": position_results,
    "outcome_counts": {k: int(v) for k, v in outcome_counts.items()},
    "chi2_out": float(chi2_out),
    "p_out": float(p_out),
}
with open("step3_results.json", "w") as f:
    json.dump(results, f, indent=2)

# ---- Chart: pooled move frequencies vs. 1/3 benchmark ----
BLUE, INK, INK2 = "#2a78d6", "#0b0b0b", "#52514e"
GRID, SURFACE, BASELINE = "#e1e0d9", "#fcfcfb", "#c3c2b7"

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

fig, ax = plt.subplots(figsize=(6.2, 4.6), dpi=200)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)

x = range(len(MOVES))
props_list = [ci_pooled[m][0] for m in MOVES]
los = [ci_pooled[m][0] - ci_pooled[m][1] for m in MOVES]
his = [ci_pooled[m][2] - ci_pooled[m][0] for m in MOVES]

ax.bar(x, props_list, width=0.5, color=BLUE, zorder=3,
       yerr=[los, his], capsize=5,
       error_kw={"ecolor": INK2, "elinewidth": 1.3, "capthick": 1.3, "zorder": 4})

ax.axhline(1 / 3, color=INK2, linestyle="--", linewidth=1.4, zorder=2)
ax.text(-0.85, 1 / 3 + 0.012, "theoretical 1/3", color=INK2, fontsize=9, ha="left", va="bottom")

for i, (p, hi) in enumerate(zip(props_list, his)):
    ax.text(i, p + hi + 0.012, f"{p:.1%}", ha="center", va="bottom",
            color=INK, fontsize=10.5, fontweight="bold")

ax.set_xlim(-0.9, 2.5)
ax.set_xticks(list(x))
ax.set_xticklabels(MOVES, color=INK, fontsize=11)
ax.set_ylabel("Share of moves played", color=INK2, fontsize=10)
ax.set_ylim(0, 0.45)
ax.set_yticks([0, 0.1, 0.2, 1 / 3, 0.4])
ax.set_yticklabels(["0%", "10%", "20%", "33.3%", "40%"], color=INK2, fontsize=9)

ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
ax.set_axisbelow(True)
for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color(BASELINE)
ax.tick_params(axis="both", length=0)

ax.set_title("Pooled move frequencies vs. the uniform-play benchmark",
             color=INK, fontsize=12.5, fontweight="bold", pad=14, loc="left")
fig.text(0.01, 0.94, f"n = {n_pooled:,} moves (both players combined) · error bars = 95% CI",
          color=INK2, fontsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig("step3_move_frequencies.png", facecolor=SURFACE, bbox_inches="tight")

print(f"n_rounds={n_rounds}, pooled chi2={chi2_pooled:.4f} p={p_pooled:.6f}")
print("Wrote step3_results.json and step3_move_frequencies.png")

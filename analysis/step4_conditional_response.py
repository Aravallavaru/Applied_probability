"""
Step 4 - Does the previous round affect the next move?

Reads ../data/rps_rounds.csv (from Step 2) and tests whether a player's
next move depends on what happened in their previous round, within the
same game (consecutive round_in_game values, same game_id).

Two complementary analyses:
  (a) Direct move-to-move transitions: does move_t depend on move_{t-1}?
  (b) Outcome-conditioned response type (the classic "win-stay/lose-shift"
      test): relative to a player's own previous move, was their next move
      a Stay (same move), Upgrade (switch to the move that beats their own
      last move), or Downgrade (switch to the move their last move beat)?
      Tested against the previous round's outcome (Win/Lose/Tie) for that
      player. This framing removes the confound of "which move was played"
      and isolates the psychological response pattern.

Outputs: step4_results.json, step4_response_heatmap.png
Run from the analysis/ folder: `python3 step4_conditional_response.py`
"""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

MOVES = ["Rock", "Paper", "Scissors"]
# WINNER_OF[m] = the move that m beats; LOSER_TO[m] = the move that beats m
WINNER_OF = {"Rock": "Scissors", "Scissors": "Paper", "Paper": "Rock"}
LOSER_TO = {"Rock": "Paper", "Paper": "Scissors", "Scissors": "Rock"}

df = pd.read_csv("../data/rps_rounds.csv")

# ---- Build per-player consecutive-round transition records ----
records = []
for game_id, g in df.groupby("game_id"):
    g = g.sort_values("round_in_game")
    for player, move_col in [("A", "move_a_name"), ("B", "move_b_name")]:
        moves = g[move_col].tolist()
        outcomes_raw = g["outcome"].tolist()
        win_label = f"{player}_win"
        lose_label = "B_win" if player == "A" else "A_win"
        outcomes = ["Win" if o == win_label else ("Lose" if o == lose_label else "Tie") for o in outcomes_raw]
        for t in range(1, len(moves)):
            prev_move, curr_move = moves[t - 1], moves[t]
            prev_outcome = outcomes[t - 1]
            if curr_move == prev_move:
                transition = "Stay"
            elif curr_move == LOSER_TO[prev_move]:
                transition = "Upgrade"
            else:
                transition = "Downgrade"
            records.append({
                "game_id": game_id, "player": player,
                "prev_move": prev_move, "curr_move": curr_move,
                "prev_outcome": prev_outcome, "transition": transition,
            })

trans_df = pd.DataFrame(records)
n_transitions = len(trans_df)
print(f"Total within-game consecutive-round transitions: {n_transitions}")

# ---- (a) Direct move-to-move contingency table ----
move_table = pd.crosstab(trans_df["prev_move"], trans_df["curr_move"]).reindex(index=MOVES, columns=MOVES)
chi2_move, p_move, dof_move, _ = stats.chi2_contingency(move_table)
print("\n=== (a) Direct move-to-move transitions ===")
print(move_table)
print(f"chi2 = {chi2_move:.4f}, df = {dof_move}, p = {p_move:.6f}")

# ---- (b) Outcome-conditioned response type (win-stay/lose-shift) ----
OUTCOMES = ["Win", "Lose", "Tie"]
TRANSITIONS = ["Stay", "Upgrade", "Downgrade"]
resp_table = pd.crosstab(trans_df["prev_outcome"], trans_df["transition"]).reindex(index=OUTCOMES, columns=TRANSITIONS)
chi2_resp, p_resp, dof_resp, expected_resp = stats.chi2_contingency(resp_table)
resp_row_pct = resp_table.div(resp_table.sum(axis=1), axis=0)
std_resid = (resp_table - expected_resp) / np.sqrt(expected_resp)

print("\n=== (b) Outcome-conditioned response type (counts) ===")
print(resp_table)
print("\nRow percentages:")
print((resp_row_pct * 100).round(1))
print(f"\nchi2 = {chi2_resp:.4f}, df = {dof_resp}, p = {p_resp:.6f}")
print("\nStandardized residuals (>|2| notable):")
print(std_resid.round(2))

# Baseline (unconditional) transition-type rates for comparison
overall_rates = trans_df["transition"].value_counts(normalize=True).reindex(TRANSITIONS)
print("\nUnconditional transition-type rates:", (overall_rates * 100).round(1).to_dict())

# "Excess switching" check: expected Stay rate under simple independence
# (moves i.i.d. with Step 3's marginal probabilities, ignoring any memory)
# is sum(p_m^2); compare to the observed Stay rate above.
step3_marginal = {"Rock": 951 / 3058, "Paper": 972 / 3058, "Scissors": 1135 / 3058}
expected_stay_under_independence = sum(p ** 2 for p in step3_marginal.values())
print(f"\nExpected 'Stay' rate under independence (sum p_m^2): "
      f"{expected_stay_under_independence * 100:.1f}% vs observed {overall_rates['Stay'] * 100:.1f}%")

# ---- (c) A proper Markov chain: states = moves, transitions = move_table ----
P_counts = move_table.values.astype(float)
P = P_counts / P_counts.sum(axis=1, keepdims=True)
print("\n=== (c) Move-to-move transition matrix P (rows=prev, cols=curr) ===")
print(np.round(P, 4))

# Stationary distribution: solve pi P = pi, sum(pi) = 1
A_mat = np.vstack([P.T - np.eye(3), np.ones(3)])
b_vec = np.array([0, 0, 0, 1])
pi, *_ = np.linalg.lstsq(A_mat, b_vec, rcond=None)
print("Stationary distribution pi:", dict(zip(MOVES, np.round(pi, 4))))
print("Compare to Step 3 pooled marginal:", {k: round(v, 4) for k, v in step3_marginal.items()})

results = {
    "n_transitions": int(n_transitions),
    "move_table": move_table.to_dict(),
    "chi2_move": float(chi2_move), "dof_move": int(dof_move), "p_move": float(p_move),
    "resp_table": resp_table.to_dict(),
    "resp_row_pct": resp_row_pct.to_dict(),
    "chi2_resp": float(chi2_resp), "dof_resp": int(dof_resp), "p_resp": float(p_resp),
    "std_resid": std_resid.to_dict(),
    "overall_transition_rates": overall_rates.to_dict(),
    "expected_stay_under_independence": float(expected_stay_under_independence),
    "move_transition_matrix": {row: {col: float(P[i, j]) for j, col in enumerate(MOVES)} for i, row in enumerate(MOVES)},
    "stationary_distribution": {m: float(p) for m, p in zip(MOVES, pi)},
    "step3_pooled_marginal": step3_marginal,
}
with open("step4_results.json", "w") as f:
    json.dump(results, f, indent=2, default=str)
print("\nSaved step4_results.json")

# ---- Chart: response-type heatmap conditioned on previous outcome ----
INK, INK2, SURFACE = "#0b0b0b", "#52514e", "#fcfcfb"
CMAP = matplotlib.colors.LinearSegmentedColormap.from_list(
    "seq_blue", ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]
)
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

pct = (resp_row_pct.reindex(index=OUTCOMES, columns=TRANSITIONS) * 100).values

fig, ax = plt.subplots(figsize=(6.4, 4.4), dpi=200)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
im = ax.imshow(pct, cmap=CMAP, vmin=15, vmax=50, aspect="auto")

ax.set_xticks(range(3))
ax.set_xticklabels(TRANSITIONS, color=INK, fontsize=11)
ax.set_yticks(range(3))
ax.set_yticklabels([f"Previous round:\n{o}" for o in OUTCOMES], color=INK, fontsize=10.5)

for i in range(3):
    for j in range(3):
        val = pct[i, j]
        text_color = "#ffffff" if val > 34 else INK
        ax.text(j, i, f"{val:.1f}%", ha="center", va="center",
                 color=text_color, fontsize=13, fontweight="bold")

ax.set_xticks(np.arange(-0.5, 3, 1), minor=True)
ax.set_yticks(np.arange(-0.5, 3, 1), minor=True)
ax.grid(which="minor", color=SURFACE, linewidth=3)
ax.tick_params(which="minor", length=0)
ax.tick_params(which="major", length=0)
for spine in ax.spines.values():
    spine.set_visible(False)

ax.set_title("Next-move response, by previous round's outcome",
              color=INK, fontsize=12.5, fontweight="bold", pad=14, loc="left")
fig.text(0.01, 0.94, f"row percentages · n = {n_transitions:,} within-game transitions (both players pooled)",
          color=INK2, fontsize=9)

cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.ax.tick_params(labelsize=8, length=0, colors=INK2)
cbar.outline.set_visible(False)

plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig("step4_response_heatmap.png", facecolor=SURFACE, bbox_inches="tight")
print("Saved step4_response_heatmap.png")

"""
Step 5 - Bayesian estimation of move probabilities, updated round by round.

Reads ../data/rps_rounds.csv (from Step 2). Puts a Dirichlet prior on the
move probabilities (Rock, Paper, Scissors), updates it sequentially as each
move is observed (Dirichlet is the conjugate prior for a multinomial), and
tracks how the posterior mean and 95% credible interval evolve as data
accumulates - a hands-on illustration of the Law of Large Numbers, and a
direct comparison point against Step 3's frequentist confidence interval.

A second run with a deliberately biased prior demonstrates that, given
enough data, the choice of prior stops mattering (the posterior "forgets"
a wrong starting belief).

Outputs: step5_results.json, step5_posterior_convergence.png,
         step5_prior_comparison.png
Run from the analysis/ folder: `python3 step5_bayesian_updating.py`
"""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

MOVES = ["Rock", "Paper", "Scissors"]

df = pd.read_csv("../data/rps_rounds.csv")
df = df.sort_values("round_overall")

# Sequential pooled move sequence: for each round (in order), Player A's
# move then Player B's move. n = 3,058, matching Step 3's pooled count.
sequence = []
for _, row in df.iterrows():
    sequence.append(row["move_a_name"])
    sequence.append(row["move_b_name"])
n_total = len(sequence)
print(f"Sequential pooled move sequence length: {n_total}")

move_idx = {m: i for i, m in enumerate(MOVES)}


def run_updating(prior_alpha, sequence):
    """Return arrays of posterior mean and 95% CI bounds at each step."""
    alpha = np.array(prior_alpha, dtype=float)
    means = np.zeros((len(sequence), 3))
    los = np.zeros((len(sequence), 3))
    his = np.zeros((len(sequence), 3))
    for t, move in enumerate(sequence):
        alpha[move_idx[move]] += 1
        alpha0 = alpha.sum()
        means[t] = alpha / alpha0
        for i in range(3):
            lo, hi = stats.beta.ppf([0.025, 0.975], alpha[i], alpha0 - alpha[i])
            los[t, i] = lo
            his[t, i] = hi
    return means, los, his, alpha


# ---- Run 1: uniform (uninformative) prior Dirichlet(1,1,1) ----
uniform_prior = [1, 1, 1]
means_u, los_u, his_u, final_alpha_u = run_updating(uniform_prior, sequence)

# ---- Run 2: deliberately biased prior, favoring Rock/Paper over Scissors ----
biased_prior = [20, 20, 2]
means_b, los_b, his_b, final_alpha_b = run_updating(biased_prior, sequence)

final_mean_u = means_u[-1]
final_ci_u = list(zip(los_u[-1], his_u[-1]))
final_mean_b = means_b[-1]
final_ci_b = list(zip(los_b[-1], his_b[-1]))

print("\n=== Final posterior (uniform prior Dirichlet(1,1,1)), n =", n_total, "===")
for m, mean, ci in zip(MOVES, final_mean_u, final_ci_u):
    print(f"  {m}: mean={mean:.4f}, 95% credible interval=({ci[0]:.4f}, {ci[1]:.4f})")

print("\n=== Final posterior (biased prior Dirichlet(20,20,2)) ===")
for m, mean, ci in zip(MOVES, final_mean_b, final_ci_b):
    print(f"  {m}: mean={mean:.4f}, 95% credible interval=({ci[0]:.4f}, {ci[1]:.4f})")

# Step 3's frequentist Wald CIs, for direct comparison (hardcoded from Step 3 results)
step3_wald_ci = {
    "Rock": (0.3110, 0.2946, 0.3274),
    "Paper": (0.3179, 0.3014, 0.3344),
    "Scissors": (0.3712, 0.3540, 0.3883),
}
print("\n=== Step 3 frequentist Wald 95% CI (for comparison) ===")
for m, (p, lo, hi) in step3_wald_ci.items():
    print(f"  {m}: p_hat={p:.4f}, 95% CI=({lo:.4f}, {hi:.4f})")

# Early-stage snapshot to show how much the two priors initially disagree
snap_n = 50
print(f"\n=== After only n={snap_n} moves ===")
for m, mu, mb in zip(MOVES, means_u[snap_n - 1], means_b[snap_n - 1]):
    print(f"  {m}: uniform-prior posterior mean={mu:.3f}, biased-prior posterior mean={mb:.3f}")

results = {
    "n_total": int(n_total),
    "uniform_prior": uniform_prior,
    "biased_prior": biased_prior,
    "final_posterior_mean_uniform": dict(zip(MOVES, final_mean_u.tolist())),
    "final_posterior_ci_uniform": {m: list(ci) for m, ci in zip(MOVES, final_ci_u)},
    "final_posterior_mean_biased": dict(zip(MOVES, final_mean_b.tolist())),
    "final_posterior_ci_biased": {m: list(ci) for m, ci in zip(MOVES, final_ci_b)},
    "step3_wald_ci": step3_wald_ci,
    "snapshot_n": snap_n,
    "snapshot_means_uniform": dict(zip(MOVES, means_u[snap_n - 1].tolist())),
    "snapshot_means_biased": dict(zip(MOVES, means_b[snap_n - 1].tolist())),
}
with open("step5_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nSaved step5_results.json")

# ---- Chart 1: posterior convergence (uniform prior) ----
BLUE_FAMILY = ["#2a78d6", "#eb6834", "#1baf7a"]  # Rock, Paper, Scissors (categorical slots)
INK, INK2, SURFACE, GRID = "#0b0b0b", "#52514e", "#fcfcfb", "#e1e0d9"

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

n_axis = np.arange(1, n_total + 1)
fig, ax = plt.subplots(figsize=(7.0, 4.8), dpi=200)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)

for i, m in enumerate(MOVES):
    ax.plot(n_axis, means_u[:, i], color=BLUE_FAMILY[i], linewidth=1.6, label=m, zorder=3)
    ax.fill_between(n_axis, los_u[:, i], his_u[:, i], color=BLUE_FAMILY[i], alpha=0.15, zorder=2, linewidth=0)

ax.axhline(1 / 3, color=INK2, linestyle="--", linewidth=1.2, zorder=1)
ax.text(n_total * 0.995, 1 / 3 + 0.006, "1/3", color=INK2, fontsize=9, ha="right", va="bottom")

ax.set_xscale("log")
ax.set_xlim(1, n_total)
ax.set_ylim(0.15, 0.55)
ax.set_xlabel("Number of moves observed (log scale)", color=INK2, fontsize=10)
ax.set_ylabel("Posterior mean probability", color=INK2, fontsize=10)
ax.tick_params(colors=INK2, labelsize=9, length=0)
ax.grid(color=GRID, linewidth=0.8, zorder=0)
ax.set_axisbelow(True)
for spine in ax.spines.values():
    spine.set_visible(False)

legend = ax.legend(loc="upper right", frameon=False, fontsize=10, labelcolor=INK)
ax.set_title("Bayesian posterior mean ± 95% credible interval, as moves accumulate",
              color=INK, fontsize=12.5, fontweight="bold", pad=14, loc="left")
fig.text(0.01, 0.94, "uniform (uninformative) prior Dirichlet(1,1,1); shaded band = 95% credible interval",
          color=INK2, fontsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig("step5_posterior_convergence.png", facecolor=SURFACE, bbox_inches="tight")
print("Saved step5_posterior_convergence.png")

# ---- Chart 2: prior washing out (Scissors probability under 2 priors) ----
fig2, ax2 = plt.subplots(figsize=(7.0, 4.2), dpi=200)
fig2.patch.set_facecolor(SURFACE)
ax2.set_facecolor(SURFACE)

s_idx = move_idx["Scissors"]
ax2.plot(n_axis, means_u[:, s_idx], color=BLUE_FAMILY[0], linewidth=1.8,
          label="Uniform prior: Dirichlet(1,1,1)", zorder=3)
ax2.plot(n_axis, means_b[:, s_idx], color=BLUE_FAMILY[1], linewidth=1.8,
          label="Biased prior: Dirichlet(20,20,2) — assumes Scissors is rare", zorder=3)
ax2.axhline(1 / 3, color=INK2, linestyle="--", linewidth=1.1, zorder=1)

ax2.set_xscale("log")
ax2.set_xlim(1, n_total)
ax2.set_ylim(0, 0.5)
ax2.set_xlabel("Number of moves observed (log scale)", color=INK2, fontsize=10)
ax2.set_ylabel("Posterior mean P(Scissors)", color=INK2, fontsize=10)
ax2.tick_params(colors=INK2, labelsize=9, length=0)
ax2.grid(color=GRID, linewidth=0.8, zorder=0)
ax2.set_axisbelow(True)
for spine in ax2.spines.values():
    spine.set_visible(False)

ax2.legend(loc="lower right", frameon=False, fontsize=9.5, labelcolor=INK)
ax2.set_title("A wrong prior gets overwhelmed by data",
               color=INK, fontsize=12.5, fontweight="bold", pad=14, loc="left")
fig2.text(0.01, 0.94, "posterior mean for P(Scissors) under two very different starting beliefs",
           color=INK2, fontsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig("step5_prior_comparison.png", facecolor=SURFACE, bbox_inches="tight")
print("Saved step5_prior_comparison.png")

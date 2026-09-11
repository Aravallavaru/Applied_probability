# Step 9 — Appendix

## 9.1 Math derivations

### 9.1.1 The 9-outcome enumeration (Step 1)

Two players each independently choose a move in {R, P, S}. There are
3 × 3 = 9 equally likely joint outcomes under H0. Using the standard
rule (Rock beats Scissors, Scissors beats Paper, Paper beats Rock),
define WINNER_OF[m] = the move that beats m, and LOSER_TO[m] = the move
that m beats:

| move m | WINNER_OF[m] (beats m) | LOSER_TO[m] (m beats) |
|---|---|---|
| Rock | Paper | Scissors |
| Paper | Scissors | Rock |
| Scissors | Rock | Paper |

Enumerating all 9 pairs (X, Y):

| X \\ Y | Rock | Paper | Scissors |
|---|---|---|---|
| **Rock** | Tie | B wins | A wins |
| **Paper** | A wins | Tie | B wins |
| **Scissors** | B wins | A wins | Tie |

3 of 9 cells are ties (the diagonal), 3 favor A, 3 favor B, giving
P(Tie) = P(A wins) = P(B wins) = 1/3 under H0 — the prediction tested
descriptively in Step 2 and formally (for moves, not outcomes) in Step 3.

### 9.1.2 Chi-square goodness-of-fit test (Step 3)

For k categories with observed counts O_i (i = 1..k) summing to n, and
expected counts E_i = n·p_i under a fully specified null distribution
(here p_i = 1/3 for all i, k = 3):

  χ² = Σ_i (O_i − E_i)² / E_i

Under H0, χ² is asymptotically distributed as chi-square with k − 1
degrees of freedom (one degree of freedom is "used up" because the
counts are constrained to sum to n). Here k − 1 = 2. The approximation
is reliable when every E_i is reasonably large (a common rule of thumb
is E_i ≥ 5); here E_i = 3,058/3 ≈ 1,019, far above that threshold.

### 9.1.3 Wald confidence interval for a single proportion (Steps 3, 5)

For an estimated proportion p̂ = O_i / n, the Wald (normal-approximation)
95% confidence interval is

  p̂ ± z₀.₉₇₅ · sqrt( p̂(1 − p̂) / n ),   z₀.₉₇₅ ≈ 1.96.

This is the standard error of a single binomial proportion (treating
"move = category i" vs. "move ≠ category i" as a Bernoulli trial),
evaluated at the sample estimate p̂. It is the simplest interval to
compute and is adequate here because n is large and p̂ is not extreme
(not near 0 or 1); the Wilson interval is a common more robust
alternative for smaller n or more extreme p̂, not needed at this sample
size.

### 9.1.4 Chi-square test of independence for a contingency table (Step 4)

For an r × c contingency table with observed counts O_ij, row totals
R_i, column totals C_j, and grand total n, the expected count under the
null hypothesis of independence (row and column variables are
unrelated) is

  E_ij = R_i · C_j / n,

and the test statistic is again χ² = Σ_ij (O_ij − E_ij)² / E_ij, now
distributed (under independence) as chi-square with (r − 1)(c − 1)
degrees of freedom. Both Step 4 tables are 3 × 3, giving
(3 − 1)(3 − 1) = 4 degrees of freedom, matching the df = 4 reported for
both the direct move-to-move test and the outcome-conditioned
Stay/Upgrade/Downgrade test.

**Standardized residuals.** To localize *which* cells drive a
significant χ², each cell's standardized residual is

  e_ij = (O_ij − E_ij) / sqrt( E_ij · (1 − R_i/n) · (1 − C_j/n) ),

which is approximately standard normal under independence, so |e_ij| > 2
(roughly) flags a cell as an unusually large contributor. This is what
identified the Win→Upgrade (+3.25), Win→Downgrade (−3.18),
Loss→Downgrade (+3.78), and Loss→Upgrade (−3.62) cells in §4.3 as the
source of the significant result, rather than, say, the Tie row or the
Stay column.

### 9.1.5 Expected repeat rate under independence (Step 4.4)

If a player's moves were independent draws from a fixed marginal
distribution (p_R, p_P, p_S) — not necessarily uniform, just memoryless —
then the probability that two consecutive independent draws are the
*same* move is

  P(move_t = move_{t−1}) = Σ_m p_m · p_m = Σ_m p_m² ,

by summing the joint probability of each "same move twice" event over
the three possible moves. Plugging in Step 3's pooled estimates
(p_R ≈ 0.311, p_P ≈ 0.318, p_S ≈ 0.371) gives Σp_m² ≈ 0.336, the 33.6%
benchmark that the observed 23.6% repeat rate falls well below in §4.4.

### 9.1.6 Markov chain stationary distribution (Step 4.5)

For a discrete-time Markov chain with a finite state space and
transition matrix P (P_ij = probability of moving from state i to state
j, rows summing to 1), a stationary distribution π (a row vector with
non-negative entries summing to 1) satisfies

  πP = π,  equivalently  π(P − I) = 0,

together with the normalization constraint Σ_i π_i = 1. Because P − I is
singular (its rows sum to 0, so it has a nontrivial null space), the
system π(P − I) = 0 alone has infinitely many solutions up to scale; the
normalization constraint pins down the unique one. In code, this was
solved as an over-determined least-squares system: stacking (P^T − I)
(three equations) with an extra row of all-ones (the normalization
equation) and solving for π against the target vector (0, 0, 0, 1) via
`numpy.linalg.lstsq`. This gives the same answer as solving the
homogeneous system directly but is numerically convenient and robust to
the singularity of P − I.

### 9.1.7 Dirichlet-multinomial conjugacy and sequential updating (Step 5)

The Dirichlet distribution with parameters (α_R, α_P, α_S), all > 0, has
density (over the probability simplex, p_R + p_P + p_S = 1)

  f(p_R, p_P, p_S) ∝ p_R^(α_R − 1) · p_P^(α_P − 1) · p_S^(α_S − 1).

If (p_R, p_P, p_S) has prior Dirichlet(α_R, α_P, α_S) and we observe one
multinomial draw that lands on category m, the likelihood is
proportional to p_m, so the posterior density is proportional to

  p_R^(α_R − 1) · p_P^(α_P − 1) · p_S^(α_S − 1) · p_m,

which is exactly the Dirichlet density with α_m increased by 1 and all
other parameters unchanged — i.e., the posterior is again Dirichlet, with
the observed category's count added to its α. This is the conjugacy
property that makes sequential updating trivial: starting from
Dirichlet(1,1,1) (uniform prior) and observing moves one at a time, after
seeing n_R Rocks, n_P Papers, and n_S Scissors the posterior is simply

  Dirichlet(1 + n_R, 1 + n_P, 1 + n_S),

updated by incrementing one counter per observed move, with no
re-fitting required — exactly the round-by-round updating shown in
§5.2's convergence plot. The posterior *mean* for category m is
α_m / (α_R + α_P + α_S), which is what is plotted as the running estimate.

**Beta marginal and the credible interval.** Each individual component of
a Dirichlet-distributed vector, marginally, follows a Beta distribution:
if (p_R, p_P, p_S) ~ Dirichlet(α_R, α_P, α_S), then

  p_m ~ Beta(α_m, α_R + α_P + α_S − α_m)

marginally, for each m. The reported 95% credible intervals for each
move's posterior probability are the 2.5th and 97.5th percentiles of
this Beta distribution, evaluated at the final (or, for the convergence
plot, running) Dirichlet parameters — the direct Bayesian analogue of
the frequentist Wald interval in §9.1.3, but derived from the exact
posterior rather than a normal approximation.

### 9.1.8 Bootstrap confidence interval (Step 6.3)

For the real-data backtest win rate, a percentile bootstrap was used: the
2,572 within-game transitions (with the exploit bot's win/loss/tie
outcome against each) were resampled with replacement 5,000 times, the
bot's win rate recomputed on each resample, and the reported 95% interval
is the 2.5th and 97.5th percentiles of that distribution of 5,000
resampled win rates. This makes no normality assumption and directly
reflects the sampling variability of the observed transition sequence
(subject to the independence caveat noted in Step 8.3 — the bootstrap
still treats each transition as exchangeable/independent, which is only
approximately true).

### 9.1.9 Exact binomial test and one-sided z-test (Steps 6.2–6.3)

For a single proportion, an exact binomial test computes the probability
of observing a result at least as extreme as the data under a fully
specified null success probability p_0, using the exact binomial
distribution rather than a normal approximation — appropriate here as a
strict, assumption-free check on the (already normally-approximated)
z-test result. The one-sided z-test used for the simulated exploit bot's
win rate uses the same standard-error formula as §9.1.3, testing
p̂ = 0.440 against p_0 = 1/3 with a very large simulated n (400,000
rounds), giving the extreme z ≈ 143 reported in §6.2 — expected given how
large the simulated sample is relative to the effect size.

### 9.1.10 Statistical power (Step 6.4)

The power of a test, for a given true effect size and sample size, is
the probability the test correctly rejects a false null hypothesis. It
was estimated here by simulation: for each assumed "excess Scissors
probability" value on a grid, many synthetic datasets of the real
dataset's size (3,058 moves, drawn via `numpy.random.Generator.multinomial`)
were generated under that assumed true distribution, the Step 3
chi-square test was run on each, and power was recorded as the fraction
of simulated datasets where the test rejected uniformity at α = 0.05.
This is the standard simulation-based approach to power analysis when an
exact analytic power formula is inconvenient (as is typical for
chi-square tests with a non-uniform alternative).

## 9.2 Data collection notes

Full documentation of the data source, raw format, parsing decisions,
column definitions, and known limitations lives in
`data/DATA_DICTIONARY.md`, with the source's own (minimal) documentation
preserved unmodified at `data/raw/SOURCE_README.md`. In summary: the
dataset comes from the PizzaRollExpert/Rock-paper-scissors-data GitHub
repository, itself sourced from a Rock-Paper-Scissors study at
Katedralskolan, Uppsala, Sweden, in autumn 2014; 1,529 valid rounds
across 243 games were parsed from the raw two-character-per-line format
(one malformed trailing line dropped), with no player identifiers or
timestamps available beyond round order. See Step 8.3 for how these
limitations bear on interpreting the results.

## 9.3 Inventory of analysis and simulation code

Every number and chart in this report is reproducible by running the
scripts below, in order, against `data/rps_rounds.csv`.

| Script | Reads | Produces | Report step |
|---|---|---|---|
| `analysis/step3_uniformity_test.py` | `data/rps_rounds.csv` | `step3_results.json`, `step3_move_frequencies.png` | Step 3 |
| `analysis/step4_conditional_response.py` | `data/rps_rounds.csv` | `step4_results.json`, `step4_response_heatmap.png` | Step 4 |
| `analysis/step5_bayesian_updating.py` | `data/rps_rounds.csv` | `step5_results.json`, `step5_posterior_convergence.png`, `step5_prior_comparison.png` | Step 5 |
| `analysis/step6_monte_carlo_exploit_bot.py` | `data/rps_rounds.csv`, `analysis/step4_results.json` | `step6_results.json`, `step6_clt_demo.png`, `step6_exploit_bot_results.png`, `step6_power_curve.png` | Step 6 |

Each script is self-contained (reads only from `data/` and, in Step 6's
case, Step 4's results file) and can be re-run independently; none
mutate `data/rps_rounds.csv`. The `.json` results files hold every raw
number quoted in this report (test statistics, p-values, interval
bounds, transition matrices, simulation win rates) for anyone who wants
to check a specific figure or extend the analysis without re-deriving it
from scratch.

## Files

This step's content — the derivations and inventory above — lives
entirely in this document; it does not add new code or charts.

## Next step

None — this completes the project skeleton (Steps 1–9). See the `README.md`
for the full project status and a one-paragraph summary of every step.

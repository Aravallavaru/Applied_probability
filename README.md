# Rock-Paper-Scissors Probability Project

## What is this project?

Game theory says that if two people play Rock-Paper-Scissors perfectly, each move
(Rock, Paper, Scissors) should be picked completely at random, with an equal
1/3 chance each, and with no memory of what happened before.

Real humans probably don't play like that. This project uses actual RPS data
(played by real people) to check, using probability and statistics, whether
that "perfectly random" assumption holds up — and if it doesn't, to measure
and model exactly how people deviate from it.

The focus is on the **probability and statistics tools**, not on game
strategy. RPS is just a simple, fun setting to practice them on real data.

## The skeleton of the project

**1. Setup — done** (`report/01_setup.md`)
The theoretical benchmark: if play is truly random, each move has
probability 1/3, and one round doesn't affect the next.

**2. Get real data — done** (`report/02_data.md`)
Ended up using an existing real dataset (PizzaRollExpert/Rock-paper-scissors-data
on GitHub) instead of collecting our own — see `data/`.

**3. Are the moves actually 1/3-1/3-1/3? — done** (`report/03_uniformity_test.md`)
**No.** Chi-square goodness-of-fit test: pooled play is not uniform
(chi² = 19.90, df = 2, p ≈ 0.00005) — Scissors is over-played (37.1% vs.
the 33.3% benchmark).

**4. Does the previous round affect the next move? — done** (`report/04_conditional_response.md`)
**Yes, strongly.** Chi-square independence test: people cycle *forward*
(toward the move that beats their own last move) after winning, and cycle
*backward* after losing (chi² = 48.59, df = 4, p < 0.000001). Modeled as a
Markov chain (states = Rock/Paper/Scissors) with stationary distribution
≈ (31.9%, 32.6%, 35.5%).

**5. Update beliefs as more data comes in — done** (`report/05_bayesian_updating.md`)
Dirichlet-multinomial Bayesian updating, round by round, from a uniform
"no assumption" prior. The posterior converges to essentially the same
answer as Step 3's frequentist confidence interval, and a second run
starting from a deliberately wrong prior shows that enough data
overwhelms even a confidently incorrect starting belief. Also doubles as
a hands-on demo of the **Law of Large Numbers**.

**6. Simulate on the computer — done** (`report/06_monte_carlo_exploit_bot.md`)
Three Monte Carlo pieces: (a) simulated random players show the Central
Limit Theorem narrowing their move-frequency estimate onto 1/3 as rounds
grow; (b) a simple "exploit" bot built from Step 4's pattern beats a
synthetic opponent 44.0% of the time (vs. 33.2% for a naive random bot),
and gets 42.9% in a direct backtest on the real historical data too
(both far above the 1/3 chance baseline, p ≈ 0 either way); (c) a power
analysis confirms our sample size had ~98% power to detect an effect the
size we actually found.

**7. Results — done** (`report/07_results.md`)
Pulls Steps 3–6 into a single results summary: tables of every test
statistic, confidence/credible interval, and simulation result, plus the
four headline plots, tying everything back to Step 1's game-theory
benchmark.

**8. Discussion & limitations — done** (`report/08_discussion.md`)
What the results say about human "randomness" (people avoid repeating
moves far more than chance predicts, and cycle forward after winning /
backward after losing) and how that connects to the Nash-equilibrium
benchmark; limitations (undocumented data source, no player IDs, the
Position A/B split, non-independence of within-game transitions,
generalizability, model simplifications, an untested "reacting to the
opponent" alternative hypothesis); and what would increase confidence.

**9. Appendix — done** (`report/09_appendix.md`)
Full math derivations for every method used (chi-square GoF and
independence tests with standardized residuals, Wald and Beta/credible
intervals, the Markov stationary-distribution linear system, Dirichlet-
multinomial conjugacy, bootstrap and power-analysis methodology), a
pointer to the data collection notes, and a table inventorying every
analysis script and what it produces.

## What's actually in this repo

- `data/` — the cleaned dataset (`rps_rounds.csv`) with its data dictionary,
  plus the original raw source kept for reproducibility (`data/raw/`)
- `analysis/` — the Python scripts and result files behind each report step
  (`step3_uniformity_test.py`, `step4_conditional_response.py`,
  `step5_bayesian_updating.py`, `step6_monte_carlo_exploit_bot.py`, their
  `.json` results, and their charts — Steps 7–9 are a synthesis of these,
  with no new scripts of their own)
- `report/` — the full write-up, one file per step (`01_setup.md` through
  `09_appendix.md`)
- `simulation/` — folded into `analysis/step6_monte_carlo_exploit_bot.py`
  rather than a separate folder

## Status

Updated 2026-09-11: **all 9 steps are complete** — the project skeleton
is done.

- Step 3: pooled move frequencies are **not** uniform — Scissors is
  over-played (37.1%), chi² = 19.90, p ≈ 0.00005.
- Step 4: strong round-to-round dependence — people cycle forward after a
  win and backward after a loss (chi² = 48.59, p < 0.000001); modeled as a
  Markov chain with stationary distribution ≈ (Rock 31.9%, Paper 32.6%,
  Scissors 35.5%).
- Step 5: Bayesian (Dirichlet-multinomial) updating converges to the same
  answer as Step 3's frequentist interval, and shows a wrong prior gets
  overwhelmed by enough data.
- Step 6: a bot exploiting Step 4's pattern wins 44.0% of simulated
  rounds and 42.9% in a real-data backtest (both vs. 33.3% chance,
  p ≈ 0); a power analysis confirms our sample size was easily big
  enough (~98% power) to detect the effect we found.
- Step 7: all of the above consolidated into one results summary with
  tables and the four headline plots.
- Step 8: discussion of what this means for human "randomness" and the
  game-theory benchmark, plus a full accounting of limitations (data
  provenance, no player IDs, non-independent transitions,
  generalizability, model simplifications).
- Step 9: appendix with complete math derivations, data collection
  notes, and a reproducibility table for every analysis script.

Next: optional — assemble `report/01_setup.md` through
`report/09_appendix.md` into one combined document for final submission.

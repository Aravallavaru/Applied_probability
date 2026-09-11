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

**6. Simulate on the computer**
Use **Monte Carlo simulation** to:
- show that a simulated random player's move-frequencies settle around 1/3
  as the number of rounds grows (Central Limit Theorem in action)
- build a simple "smart" bot that guesses the opponent's next move using the
  pattern found in step 4, and test (statistically) whether it wins more
  than 1/3 of the time
- check how many rounds of real data we'd actually need to reliably detect
  a pattern, if one exists (a power analysis)

**7. Results**
Report the test results, confidence/credible intervals, and simulation
findings, with plots.

**8. Discussion & limitations**
What did we learn about randomness in human behavior? What would we need to
be more confident (bigger sample, different game, etc.)?

**9. Appendix**
Math derivations, data collection notes, and simulation code.

## What's actually in this repo

- `data/` — the cleaned dataset (`rps_rounds.csv`) with its data dictionary,
  plus the original raw source kept for reproducibility (`data/raw/`)
- `analysis/` — the Python scripts and result files behind each report step
  (Steps 3–5 so far: `step3_uniformity_test.py`, `step4_conditional_response.py`,
  `step5_bayesian_updating.py`, their `.json` results, and their charts)
- `report/` — the write-up, one file per step (`01_setup.md` through
  `05_bayesian_updating.md` so far)
- `simulation/` — not started yet; arrives with Steps 6–7

## Status

Updated 2026-09-11: Steps 1–5 are complete.

- Step 3: pooled move frequencies are **not** uniform — Scissors is
  over-played (37.1%), chi² = 19.90, p ≈ 0.00005.
- Step 4: strong round-to-round dependence — people cycle forward after a
  win and backward after a loss (chi² = 48.59, p < 0.000001); modeled as a
  Markov chain with stationary distribution ≈ (Rock 31.9%, Paper 32.6%,
  Scissors 35.5%).
- Step 5: Bayesian (Dirichlet-multinomial) updating converges to the same
  answer as Step 3's frequentist interval, and shows a wrong prior gets
  overwhelmed by enough data.

Next: Step 6, Monte Carlo simulation — build and test an "exploit" bot
using the Step 4 response pattern.

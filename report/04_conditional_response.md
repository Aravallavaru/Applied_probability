# Step 4 — Does the Previous Round Affect the Next Move?

## 4.1 What we're testing

Step 1's H0 assumed each move is independent of everything before it —
"no memory." Step 4 tests that directly: within a single game (a
continuous run of rounds between the same pair, using `round_in_game`),
does a player's next move depend on what just happened?

Two complementary tests are run, both using only consecutive rounds
within the same game (2,572 such within-game transitions, pooling both
players):

**(a) Direct move-to-move dependence.** Does `move_t` depend on
`move_{t-1}`, ignoring outcome entirely?

**(b) Outcome-conditioned response type (win-stay/lose-shift).** Relative
to a player's *own* previous move, is their next move a **Stay** (same
move again), an **Upgrade** (switch to the move that would beat their own
last move), or a **Downgrade** (switch to the move their last move would
have beaten)? These three categories exhaust every possible next move for
any previous move, and — unlike looking at raw move-to-move counts —
this framing isn't confounded by *which* move was played last, so it
isolates the psychological response pattern. We then test whether this
response type depends on the previous round's outcome for that player
(Win / Lose / Tie).

## 4.2 (a) Direct move-to-move test

|  | → Rock | → Paper | → Scissors |
|---|---|---|---|
| **Rock** → | 214 | 243 | 335 |
| **Paper** → | 241 | 195 | 364 |
| **Scissors** → | 370 | 411 | 199 |

**chi² = 158.10, df = 4, p < 0.000001** — an extremely strong rejection of
independence between consecutive moves. Two things stand out: every
diagonal cell (repeating your own last move) is well below a third of its
row, and Scissors is the most common response after *either* Rock or
Paper.

## 4.3 (b) Outcome-conditioned response type — the main result

|  | Stay | Upgrade | Downgrade |
|---|---|---|---|
| **Previous round: Win** | 23.5% | **45.4%** | 31.1% |
| **Previous round: Lose** | 23.2% | 29.8% | **47.0%** |
| **Previous round: Tie** | 24.0% | 38.5% | 37.5% |

**chi² = 48.59, df = 4, p < 0.000001.**

![Next-move response by previous outcome](../analysis/step4_response_heatmap.png)

The standardized residuals pin down exactly where the deviation lives:
after a **Win**, Upgrade is elevated (+3.25) and Downgrade is suppressed
(−3.18); after a **Loss**, it's the mirror image — Downgrade is elevated
(+3.78) and Upgrade is suppressed (−3.62). The Stay rate barely moves
across all three conditions (23–24%). So the classic "win-stay" label is
slightly misleading for this dataset: people here aren't repeating a
winning move more often — they're **cycling forward** (Rock→Paper→
Scissors→Rock) after winning and **cycling backward** after losing,
while rarely repeating a move outright either way.

## 4.4 A striking side finding: people switch far more than chance

Overall, players repeat their previous move only **23.6%** of the time.
If moves were simply independent draws from Step 3's (slightly
non-uniform) marginal distribution — no memory at all — simple
probability says the repeat rate should be sum(p_move²) ≈ **33.6%**
(since P(same move twice) = ΣP(move)² for independent draws). The
observed rate is 10 points below that. People aren't just failing to be
perfectly uniform (Step 3) — they're actively avoiding repetition far
more than randomness alone would ever produce, a well-known bias in
human "randomization" attempts (related to the gambler's fallacy).

## 4.5 A proper Markov chain model

Since move choices clearly depend on the previous move, we can formalize
the sequence as a discrete-time Markov chain with states {Rock, Paper,
Scissors} and transition matrix P estimated directly from the table in
§4.2 (each row normalized to sum to 1):

|  | → Rock | → Paper | → Scissors |
|---|---|---|---|
| **Rock** → | 0.270 | 0.307 | 0.423 |
| **Paper** → | 0.301 | 0.244 | 0.455 |
| **Scissors** → | 0.378 | 0.419 | 0.203 |

Solving πP = π gives the stationary distribution **π = (Rock 31.9%,
Paper 32.6%, Scissors 35.5%)**. This is a useful consistency check: it's
close to, though not identical to, Step 3's raw pooled marginal (Rock
31.1%, Paper 31.8%, Scissors 37.1%) — as expected for a chain that's
approximately, but not perfectly, stationary over the dataset. This
transition matrix (or the outcome-conditioned version in §4.3) is what
Step 6's "exploit bot" will use to predict an opponent's next move.

## 4.6 Conclusion

Both tests agree, emphatically: **the previous round does affect the next
move.** People don't just fail to randomize their marginal move
frequencies (Step 3) — they carry real, statistically overwhelming
structure from round to round, structure that is systematic enough to
name precisely (cycle forward after winning, cycle backward after
losing, avoid repeating either way). This is exactly the kind of
exploitable pattern a predicting strategy could use, which is where
Step 6's simulation comes in — but first, Step 5 puts a Bayesian lens on
the same question, updating our belief about a player's response
tendencies round by round rather than testing on the whole dataset at
once.

## Files

- `analysis/step4_conditional_response.py` — the script that produced
  every number and the chart here, reproducible from `data/rps_rounds.csv`
- `analysis/step4_results.json` — raw numeric results (both contingency
  tables, chi-square statistics, standardized residuals, transition
  matrix, stationary distribution)
- `analysis/step4_response_heatmap.png` — the chart above

## Next step

Step 5: Bayesian estimation — put a Dirichlet prior on a player's
response tendencies and update it round by round, watching the estimate
sharpen as more data arrives (and comparing the resulting credible
intervals to the frequentist ones used here).

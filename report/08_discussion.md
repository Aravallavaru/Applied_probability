# Step 8 — Discussion and Limitations

## 8.1 What we learned about "randomness" in human behavior

The headline finding, stated plainly: people asked (or choosing) to play
Rock-Paper-Scissors are bad at being random, in two distinct and
compounding ways. First, their *marginal* move frequencies aren't
uniform — Scissors gets over-played (Step 3). Second, and more
interestingly, their moves aren't *independent* over time — knowing what
just happened (their own last move, and whether they won or lost)
predicts their next move far better than chance (Step 4). The second
effect is both statistically stronger (χ² = 48.59 vs. 19.90) and more
psychologically specific: people cycle forward through Rock→Paper→
Scissors→Rock after winning and backward after losing, and they avoid
repeating their previous move (23.6% observed vs. an already-reduced
33.6% expected under independence) far more than pure randomness would
ever produce on its own.

That second habit — avoiding repetition — is a well-documented human bias
sometimes linked to the gambler's fallacy: people conflate "random"
with "evenly spread out and non-repeating," when true randomness
actually repeats itself more often than intuition expects. Our data is a
clean, quantified example of exactly that bias in a setting where
repeating *should* carry no cost or benefit under the game's theoretical
equilibrium.

Critically, Steps 3 and 5 (frequentist and Bayesian) don't just agree —
they *have to* agree at this sample size, since both are converging on
the same underlying frequency using different but asymptotically
equivalent machinery. What Step 5 adds is not a different final number
but a demonstration that the conclusion is robust to how confident (or
wrongly confident) one starts out: even a prior that confidently expected
the *opposite* pattern (Scissors underused) gets overwhelmed by a few
hundred rounds of real data. That is itself a small, self-contained
illustration of the Law of Large Numbers and a reason to trust the Step 3
finding beyond just "the p-value was small."

## 8.2 Connection to the game-theory benchmark

Step 1's benchmark came from game theory, not statistics: Rock-Paper-
Scissors has a unique mixed-strategy Nash equilibrium at uniform,
memoryless play, precisely because any deviation from it is, in
principle, exploitable by an opponent who notices. Steps 3–6 turn that
"in principle" into a measured, tested, and *demonstrated* fact for this
dataset: the deviation is not just statistically significant, it is
practically exploitable (Step 6's bot beats chance by roughly 10–11
percentage points, verified in both simulation and a real-data backtest,
with the effect essentially certain to be real, not sampling noise, per
the p ≈ 3 × 10⁻²⁴ backtest result and the ~98–99% power estimate). This
project's real point was never really about Rock-Paper-Scissors strategy
— it's that a game-theoretic equilibrium concept, "no exploitable
pattern," turns out to be directly testable with the tools of applied
probability and statistics: goodness-of-fit tests, contingency-table
independence tests, Bayesian updating, Markov chains, and Monte Carlo
simulation each contributed a different angle on the same underlying
question, and they all point the same way.

## 8.3 Limitations

**Data source and provenance.** The dataset (Katedralskolan, Uppsala,
Sweden, autumn 2014, via the PizzaRollExpert/Rock-paper-scissors-data
GitHub repository) documents almost nothing about its own collection: no
information on how many distinct people played, how pairs were formed,
whether there was any incentive (competition, prize, or just a class
exercise), or how play was recorded. We cannot rule out that some
context-specific factor of that one classroom setting shaped the results
in a way that wouldn't hold elsewhere.

**No player identifiers.** Because games aren't linked to real player
identities, we cannot tell whether the same person appears across
multiple games, cannot separate a strong pattern from a *few* strongly
patterned players versus a mild pattern shared by *everyone*, and cannot
study individual heterogeneity in the win-upgrade/lose-downgrade
tendency at all — every test in this project treats the pooled data as
if it came from one representative behavioral process.

**Position A/B asymmetry, only partly investigated.** Step 3 found
Position A's deviation from uniform play (p ≈ 0.00009) was clearly
significant on its own while Position B's (p ≈ 0.128) was not, though
both leaned the same direction. We treated this as a sample-size
artifact of splitting one modest effect in half rather than a real
structural difference, and the Step 6 power analysis supports that
reading (the *pooled* effect had ample power; a half-sized subsample
naturally has less) — but we did not run a *formal* test of whether
Position A and B differ from each other, only informal side-by-side
comparison. The `move_a` / `move_b` labels are also an arbitrary naming
convention imposed during cleaning (documented in
`data/DATA_DICTIONARY.md`), not a real player attribute, which limits
how much can be read into this split in the first place.

**Non-independence in the within-game transitions.** Step 4's 2,572
within-game transitions, and Step 6's bootstrap confidence interval built
from them, both implicitly treat each transition as an independent data
point. In reality, transitions from the same game (and possibly the same
underlying player, given the no-player-ID limitation above) are not
statistically independent of each other — a form of pseudo-replication.
This likely doesn't change the *direction* of any finding here (the
effects are large and consistent across many separate games), but it
means the reported p-values and confidence intervals are probably a bit
too narrow/optimistic, since the effective sample size in terms of truly
independent observations is smaller than the raw transition count
suggests.

**Generalizability.** This is one convenience sample from one school, in
one country, in 2014, with unknown incentives. Whether "win-upgrade,
lose-downgrade" and "Scissors over-play" are stable human tendencies
across cultures, age groups, competitive contexts (e.g., real money on
the line), or eras is an open question this dataset cannot answer on its
own.

**Model simplifications.** The Step 6 exploit bot always predicts the
single *most likely* response (Upgrade after win/tie, Downgrade after
loss) rather than weighing the full three-way response distribution, and
it only ever looks one round back — a first-order Markov assumption.
Neither the bot nor the Markov model tested whether looking two or more
rounds back would predict even better, and the Markov chain is fit and
evaluated as if the transition probabilities were constant across the
whole dataset (i.e., stationary), which was only checked informally by
comparing the fitted stationary distribution to the raw marginal, not
tested formally for time-drift (e.g., early games vs. late games, or
fatigue effects within a long game).

**An untested alternative hypothesis: response to the opponent, not just
to oneself.** Every test in Step 4 asks whether a player's next move
depends on *their own* previous move and outcome. It does not separately
test whether a player's next move depends directly on the *opponent's*
previous move (a related but distinct hypothesis — reacting to what the
other person just played, rather than to one's own prior choice and its
result). Because outcome already encodes some information about the
opponent's move (win/lose/tie is a joint function of both players'
moves), the two explanations are not fully separable with the tests run
here, and disentangling them would need a purpose-built test.

## 8.4 What would increase confidence

A few concrete next steps, roughly in order of how much new machinery
they'd require: (1) replicate the analysis on an independent RPS
dataset from a different population to check whether the same
win-upgrade/lose-downgrade pattern and Scissors bias reappear; (2) obtain
or collect data with player identifiers, to separate within-player
consistency from between-player heterogeneity, and to test the
Position A/B question formally with paired or mixed-effects methods
instead of two separate chi-square tests; (3) fit and compare higher-
order Markov models (looking two or three rounds back) to see whether
memory extends further than one round; (4) run the exploit bot live and
adaptively against real human opponents (rather than only backtesting it
against historical transitions) to get a genuinely out-of-sample,
causal test of exploitability; and (5) if possible, compare play with and
without real incentives (a class exercise vs. a paid tournament) to see
whether the deviation from the game-theoretic benchmark shrinks under
higher stakes, which game theory would actually predict.

## Files

This step is a discussion of results already established; no new
analysis files or charts.

## Next step

Step 9: the appendix — full mathematical derivations for every method
used, a pointer to the data collection notes, and an inventory of all
simulation and analysis code.

# Step 5 — Updating Beliefs as Data Arrives (Bayesian Estimation)

## 5.1 Setup: the Dirichlet-multinomial model

Steps 3 and 4 both worked with the *whole* dataset at once — one test, one
answer. This step asks a different kind of question: what would our
estimate of a player's move probabilities look like if we only ever saw
the data one round at a time, updating our belief as we went?

The move probabilities (P(Rock), P(Paper), P(Scissors)) live on the
2-dimensional probability simplex (they sum to 1). The natural prior
distribution over that simplex is the **Dirichlet distribution**, and it
happens to be the *conjugate* prior for multinomial data: if the prior is
Dirichlet(α_R, α_P, α_S) and we observe one more move, the posterior is
again Dirichlet, just with the count of whichever move occurred added to
its corresponding α. This makes sequential updating trivial — no
re-fitting, just adding 1 to a counter — and it is exactly the same
"start with no assumption, update as data arrives" idea the project
skeleton describes for this step.

We start from the **uninformative uniform prior** Dirichlet(1, 1, 1) —
"no assumption" — and feed it the same 3,058 pooled moves from Step 3, in
the order they occurred (round by round, Player A's move then Player B's
move within each round).

## 5.2 Watching the posterior converge

![Bayesian posterior mean and 95% credible interval as moves accumulate](../analysis/step5_posterior_convergence.png)

Early on (fewer than ~30 moves), the posterior mean for each move swings
wildly and the 95% credible bands are enormous — with almost no data, the
Dirichlet(1,1,1) prior barely constrains anything. By a few hundred moves,
the swings settle down and the bands visibly narrow. By the full 3,058
moves, all three posterior means have locked onto essentially the same
values Step 3 found by direct calculation:

| Move | Posterior mean (Bayesian) | 95% credible interval |
|---|---|---|
| Rock | 0.3110 | (0.2947, 0.3275) |
| Paper | 0.3179 | (0.3015, 0.3345) |
| Scissors | 0.3711 | (0.3541, 0.3883) |

## 5.3 Bayesian vs. frequentist: the same answer, for a reason

Compare this directly to Step 3's frequentist Wald confidence intervals:

| Move | Frequentist p̂ | Frequentist 95% CI | Bayesian posterior mean | Bayesian 95% credible interval |
|---|---|---|---|---|
| Rock | 0.3110 | (0.2946, 0.3274) | 0.3110 | (0.2947, 0.3275) |
| Paper | 0.3179 | (0.3014, 0.3344) | 0.3179 | (0.3015, 0.3345) |
| Scissors | 0.3712 | (0.3540, 0.3883) | 0.3711 | (0.3541, 0.3883) |

They match to three decimal places. This isn't a coincidence: with a
large sample and an uninformative prior, the data overwhelms the prior
and the Bayesian credible interval converges to essentially the same
interval the frequentist approach produces (a general fact — the
Bernstein–von Mises phenomenon, informally). The two frameworks answer
philosophically different questions ("what range of values would 95% of
repeated experiments' confidence intervals cover?" vs. "given this data,
where do I believe the true probability lies, with 95% credibility?"),
but at this sample size, with a neutral prior, they land in the same
place numerically. The real payoff of the Bayesian framing here isn't a
different final answer — it's the ability to track a *coherent, evolving
belief* round by round, which the frequentist approach doesn't naturally
provide.

## 5.4 Does the starting belief matter? A wrong prior gets overwhelmed

To make the "no assumption" framing concrete, we reran the same updating
process starting from a deliberately **wrong, informative prior** —
Dirichlet(20, 20, 2), which starts out strongly believing Rock and Paper
are common and Scissors is rare (the opposite of what the data actually
shows).

![A wrong prior gets overwhelmed by data](../analysis/step5_prior_comparison.png)

After only 50 moves, the two priors still disagree substantially on
P(Scissors) — 0.396 (uniform prior) vs. 0.239 (biased prior). By a few
hundred moves the gap has almost closed, and by the full dataset the
biased-prior posterior (Scissors ≈ 0.367) and the uniform-prior posterior
(Scissors ≈ 0.371) are nearly identical — both far from the biased
prior's original assumption that Scissors was rare. Enough real data
overwhelms even a confidently wrong starting belief.

## 5.5 Connection to the Law of Large Numbers

The Dirichlet posterior's variance shrinks proportionally to 1/n as data
accumulates (visible directly as the narrowing credible band in §5.2's
chart), and the posterior mean converges to the true long-run frequency —
which is exactly the content of the Law of Large Numbers, just viewed
through a Bayesian lens instead of a frequentist one. Steps 3 and 5 are
really two different routes to the same underlying convergence fact.

## 5.6 Conclusion

Bayesian updating gives the same substantive conclusion as Step 3 (moves
are not uniform; Scissors is over-played), but adds two things: a
round-by-round view of how confidence builds as data accumulates, and a
concrete demonstration that a wrong prior belief is not fatal — it just
takes data to correct it. This sets up Step 6 nicely: since we now have
solid estimates of both the raw move probabilities (Steps 3/5) and the
outcome-conditioned response pattern (Step 4), we have everything needed
to build and simulate an actual "exploit" strategy that tries to profit
from these predictable deviations.

## Files

- `analysis/step5_bayesian_updating.py` — the script that produced these
  numbers and both charts, reproducible from `data/rps_rounds.csv`
- `analysis/step5_results.json` — raw numeric results (final and
  early-snapshot posteriors under both priors, plus the Step 3 comparison)
- `analysis/step5_posterior_convergence.png`, `analysis/step5_prior_comparison.png`
  — the charts above

## Next step

Step 6: Monte Carlo simulation — simulate a random player to illustrate
the Central Limit Theorem, build a "smart" bot that exploits the Step 4
response pattern to predict the opponent's next move, and test via
simulation whether it wins more than chance.

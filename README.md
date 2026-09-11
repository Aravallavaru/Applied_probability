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

**1. Setup**
Explain the theoretical benchmark: if play is truly random, each move has
probability 1/3, and one round doesn't affect the next.

**2. Collect data**
Play a decent number of rounds (friends/classmates, or a public dataset).
Record, for every round: what move each player made, and who won.

**3. Are the moves actually 1/3-1/3-1/3?**
Count how often Rock/Paper/Scissors were each played. Use a **chi-square
goodness-of-fit test** to check if this matches the "equal 1/3 each" theory,
and build a **confidence interval** around each estimated probability.

**4. Does the previous round affect the next move?**
Build a table of "what happened last round" vs. "what move came next."
Use a **chi-square independence test** to check for patterns (e.g., do people
switch moves after losing?). If a pattern exists, describe it as a **Markov
chain** (a simple model of "next move depends a bit on the last outcome").

**5. Update beliefs as more data comes in**
Use **Bayesian estimation**: start with no assumption about a player's
habits, then update our estimate round by round as more data arrives. Watch
the estimate get more confident over time — a nice hands-on demo of the
**Law of Large Numbers**.

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

## What this project will eventually include

- `data/` — recorded rounds from the RPS experiment
- `analysis/` or notebook — the statistical tests and Bayesian updating
- `simulation/` — Monte Carlo simulation code
- `report` — the final write-up following the skeleton above

## Status

Currently at the planning stage. Next steps: finalize the data collection
plan, then start on the statistical tests.

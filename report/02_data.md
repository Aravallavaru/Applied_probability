# Step 2 — Getting and Preparing Real Data

## 2.1 Source

We use the PizzaRollExpert/Rock-paper-scissors-data dataset from GitHub
(https://github.com/PizzaRollExpert/Rock-paper-scissors-data), chosen during
project planning. Per its own README, the data comes from a study in
Rock-Paper-Scissors performed at Katedralskolan, Uppsala, Sweden, in autumn
2014. Beyond that one sentence, the source does not document its collection
methodology (number of players, how pairs were formed, or how play was
recorded).

## 2.2 Raw format

Each line of the raw file (`data/raw/data.txt`) is a two-character code for
one round, using s = rock, x = scissors, p = paper, or a single `-` marking
the end of one continuous run of play between (presumably) the same two
players.

## 2.3 Parsing decisions

- Each run of round-lines between `-` markers is treated as one "game" —
  assumed to be the same pair of players throughout.
- The first character of each round-line is assigned to move_a, the second
  to move_b. This labeling is arbitrary but internally consistent within a
  game, since the source does not identify the two players otherwise.
- One malformed trailing line (a stray, unpaired character at the very end
  of the file) was dropped rather than guessed at.
- Each round's outcome (A_win / B_win / Tie) is computed from the two moves
  using the standard rule (Rock beats Scissors, Scissors beats Paper, Paper
  beats Rock).

Full column documentation is in `data/DATA_DICTIONARY.md`. The cleaned data
is `data/rps_rounds.csv`; the untouched original is kept at
`data/raw/data.txt` for reproducibility.

## 2.4 What we ended up with

1,529 valid rounds across 243 games (games range from 1 to 20 rounds,
averaging 6.29 rounds each).

Pooled across both players (3,058 individual move choices):

- Rock: 951 (31.1%)
- Paper: 972 (31.8%)
- Scissors: 1,135 (37.1%)

Outcome proportions:

- Tie: 36.0%
- A_win: 32.8%
- B_win: 31.1%

## 2.5 A first look against Step 1's predictions

Step 1 predicted that, under i.i.d. uniform play, each move should appear
about 1/3 of the time, and Tie/A_win/B_win should each land near 1/3 too.
The raw counts already hint that Scissors is over-played relative to Rock
and Paper, and that Tie is a little higher than 1/3 — consistent with a
mild bias rather than exact uniform randomness. This is only descriptive
at this stage: Step 3 puts these observations through a formal chi-square
goodness-of-fit test rather than treating them as conclusions.

## 2.6 Limitations carried forward

No player identifiers (so we can't tell whether the same person appears in
more than one game), no timestamps beyond round order, and an undocumented
collection methodology from the source beyond "one Swedish school, 2014."
These are noted here so they can be cited directly in the report's
Discussion & Limitations section (Step 8).

## Next step

Step 3: test H0 (i.i.d. uniform play) formally with a chi-square
goodness-of-fit test on the pooled move frequencies, plus confidence
intervals for each move's estimated probability.

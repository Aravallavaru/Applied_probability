# Data dictionary — `rps_rounds.csv`

## Source

Raw data: `raw/data.txt`, downloaded as-is from
https://github.com/PizzaRollExpert/Rock-paper-scissors-data (file `data.txt`,
`master` branch). The repo's own description (`raw/SOURCE_README.md`) says
the data comes from a study in Rock-Paper-Scissors performed at
Katedralskolan, Uppsala, Sweden, in autumn 2014. No further methodology
(number of distinct players, how pairs were formed, how play was recorded)
is documented by the source repo.

Raw format: each line is either a two-character code for one round (first
character = one player's move, second character = the other player's move),
using `s` = rock, `x` = scissors, `p` = paper, or a single `-` marking the
end of one continuous game (a run of consecutive rounds, presumably between
the same pair of players before they stopped or swapped).

## How the raw file was parsed

- Consecutive non-`-` lines between two `-` markers (or between the start of
  the file and the first `-`) are treated as one "game": a sequence of
  rounds assumed to be the same two players playing repeatedly.
- The first character of each round-line is always assigned to `move_a`,
  the second to `move_b`. This is a naming convention we impose (there is no
  information in the source distinguishing the two players otherwise) — it
  does *not* imply "player A" in game 1 is the same physical person as
  "player A" in game 2. Each game's A/B labels should be treated as
  arbitrary but internally consistent within that game.
- One malformed line (a single stray `x` with no pairing character,
  at the very end of the file) was dropped rather than guessed at.
- Blank lines are ignored.

## Columns in `rps_rounds.csv`

- `game_id` — integer, increments each time a `-` delimiter is crossed.
  Rounds sharing a `game_id` come from one uninterrupted run of play between
  what is assumed to be the same pair of players.
- `round_in_game` — round number within its game, starting at 1.
- `round_overall` — round number across the whole dataset, starting at 1
  (ignores game boundaries; convenient for a single running index).
- `move_a`, `move_b` — raw one-letter move codes (`s`/`x`/`p`) for the two
  players in that round, in the order they appeared in the source line.
- `move_a_name`, `move_b_name` — the same moves spelled out
  (`Rock`/`Paper`/`Scissors`).
- `outcome` — `A_win`, `B_win`, or `Tie`, computed from `move_a`/`move_b`
  using the standard rule (Rock beats Scissors, Scissors beats Paper, Paper
  beats Rock).

## Summary (for reference — formal testing happens in Step 3)

- 1,529 valid rounds parsed, across 243 games.
- Games range from 1 to 20 rounds long (mean 6.29 rounds/game).
- Pooled move counts (both players combined, 3,058 individual moves):
  Rock 951 (31.1%), Paper 972 (31.8%), Scissors 1,135 (37.1%).
- Outcome proportions: Tie 36.0%, A_win 32.8%, B_win 31.1%.

These raw counts already hint that Scissors may be over-played relative to
the 1/3 benchmark from Step 1 — Step 3 tests this formally rather than
eyeballing it.

## Known limitations

- No player identifiers: we cannot tell whether the same individual appears
  in more than one game, so games cannot be grouped by person.
- No timestamps, so within-game "time" is only the round order.
- Collection methodology beyond "a study at one Swedish school in 2014" is
  undocumented by the source; sample may not generalize beyond that
  population.
- One line was dropped as malformed (see above) — a negligible loss (1 of
  1,530 potential rounds).

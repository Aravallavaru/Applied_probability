# Step 1 — Setup: The Theoretical Benchmark

This section lays out the formal probability model that the rest of the
project tests against real data. Everything after this step is either
testing this model or refining it when the data disagrees with it.

## 1.1 The game and the data

Two players, A and B, play Rock-Paper-Scissors repeatedly for n rounds,
indexed t = 1, 2, ..., n (in our case, using recorded games from the
PizzaRollExpert/Rock-paper-scissors-data dataset). For round t, define two
random variables:

- X_t = Player A's move in round t, taking a value in {R, P, S}
- Y_t = Player B's move in round t, taking a value in {R, P, S}

## 1.2 Why we expect uniform, independent play (the one paragraph of game theory)

Rock-Paper-Scissors is a symmetric, zero-sum game whose unique Nash
equilibrium is a mixed strategy: each player randomizes uniformly over
{R, P, S}, i.e. P(X_t = R) = P(X_t = P) = P(X_t = S) = 1/3. The intuition:
if a player favored one move even slightly, an opponent who noticed could
exploit it, so the only strategy that leaves an opponent with nothing to
exploit is playing all three moves equally often, with no pattern over
time. Game theory only tells us this is the *theoretical* benchmark — it
does not tell us people actually play this way. That is exactly the
empirical question this project investigates.

## 1.3 The null model, stated formally

**H0 (i.i.d. uniform play).** For a given player, the sequence of moves
X_1, X_2, ..., X_n is independent and identically distributed, with

  P(X_t = R) = P(X_t = P) = P(X_t = S) = 1/3   for every round t,

and each move is independent of everything that happened before it:

  P(X_t = a | history before round t) = P(X_t = a) = 1/3   for all a in {R, P, S}.

The second line is the precise version of "one round doesn't affect the
next": it says the process has no memory — knowing the full history of
moves and outcomes up to round t-1 gives no information about round t.

We also assume the two players' move sequences are independent of each
other, since neither can see the other's move before playing (true by the
rules of the game).

## 1.4 A first concrete prediction: the distribution of outcomes under H0

Define the outcome of round t as O_t, one of {A wins, B wins, Tie}, using
the standard rule: Rock beats Scissors, Scissors beats Paper, Paper beats
Rock; equal moves are a tie.

Under H0, the pair (X_t, Y_t) is uniform over all 9 equally likely
combinations of the two players' moves (3 choices x 3 choices, each with
probability 1/9). Enumerating them: 3 of the 9 combinations are ties
(same move for both players), 3 are wins for A, and 3 are wins for B. So
under H0:

  P(Tie) = 3/9 = 1/3,   P(A wins) = 1/3,   P(B wins) = 1/3.

This is a first checkable prediction: before even testing individual move
frequencies, we can check whether the dataset's actual win/lose/tie rates
are close to 1/3 each.

## 1.5 Notation we will reuse in later steps

Over n rounds, if H0 holds, the vector of move counts (n_R, n_P, n_S) for
one player follows a Multinomial(n, (1/3, 1/3, 1/3)) distribution. This is
the distribution the observed data will be tested against in Step 3
(chi-square goodness-of-fit test).

If the independence part of H0 fails (moves are not memoryless), the move
sequence will instead be modeled as a discrete-time Markov chain in Step 4,
where the "state" is the previous move or previous outcome, and the next
move follows a transition probability matrix instead of being drawn fresh
each round.

## 1.6 What is, and is not, being tested

To be explicit: this project does not test whether players are playing
"well" or "optimally" in a strategic sense — that would be game theory or
behavioral economics. It tests one specific, falsifiable probability
model (i.i.d. uniform play) against real recorded human data, using
hypothesis testing, confidence intervals, Markov chains, Bayesian
estimation, and simulation.
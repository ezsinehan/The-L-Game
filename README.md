# The L-Game

Two-player abstract game on a 4×4 board. Each player has one L-shaped piece (4 cells); two neutral pieces (1 cell each) block squares. On your turn you must move your L to a new position and may optionally move one neutral piece to any empty cell. You lose if you cannot make a legal move.

## Requirements

- **Python 3** (stdlib only: `sys`, `os`, `math`, `time`, `itertools`). No extra packages.

## Run

```bash
python L-game.py
```

## Using the game

1. **Start**
   - (1) Start Game — use default board
   - (2) Edit Starting States — enter custom initial setup (see format below)

2. **Mode**
   - (1) Human vs Human
   - (2) Human vs Computer
   - (3) Computer vs Computer

3. **First player**
   - Enter `1` for Player 1 (L1), `2` for Player 2 (L2).

4. **If AI is used**
   - **Search depth** — e.g. `3` (higher = stronger, slower).
   - **Pause between steps** — seconds to pause the AI visualizer (e.g. `0.5` or `0` for none).

5. **During play**
   - Grid: rows/columns 1–4; row 1 top, column 1 left.
   - Type `help` when prompted for a move to see the move format.
   - Type `q` when prompted for a move to quit.

## Move input (human)

- **L only:** `COL ROW ORIENTATION`  
  Example: `2 1 n`  
  Orientations: `n` (north), `s` (south), `e` (east), `w` (west).

- **L + neutral:** `COL ROW ORIENTATION  COL_FROM ROW_FROM  COL_TO ROW_TO`  
  Example: `2 1 n  1 2  3 2` (L at 2,1 with orientation n; move neutral from 1,2 to 3,2).

Coordinates are 1-indexed. The L must end in a legal position.

## Edit starting state (option 2)

Single line, 10 numbers (1-indexed):

`L1_COL L1_ROW L1_ORIENTATION  N1_COL N1_ROW  N2_COL N2_ROW  L2_COL L2_ROW L2_ORIENTATION`

Example (default-like): `1 1 n  2 2  3 3  4 4 s`

## Technical details

- **Board:** 4×4 grid; cells are `L1`, `L2`, `N`, or empty (`0`).
- **L move generation:** All 8 L orientations (4 rotations × 2 mirrors) placed at each of 16 positions; filtered for in-bounds, no overlap with other pieces, and not identical to current position.
- **AI (L move):** Minimax with alpha–beta pruning. Search depth set at startup. Transposition cache keyed by grid, L1/L2 positions, neutral positions, player, depth, and maximizing flag.
- **Heuristic:** Mobility — `(legal moves for L2) − (legal moves for L1)`. L2 is maximizer, L1 minimizer.
- **AI (neutral move):** After the chosen L move, the AI picks a neutral move that minimizes the opponent’s legal moves (greedy, no search).
- **Visualizer:** When the AI thinks, it shows root move index, board state, score, and best move so far; optional pause between root moves.

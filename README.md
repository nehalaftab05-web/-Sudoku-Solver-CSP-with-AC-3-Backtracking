# Sudoku-Solver-CSP-with-AC-3-Backtracking
A Python implementation of a Constraint Satisfaction Problem (CSP) solver for 9×9 Sudoku puzzles. Uses AC-3 arc consistency preprocessing, backtracking search, MRV heuristic, and forward checking to efficiently solve puzzles across four difficulty levels.


## 📋 Table of Contents

- [Overview](#overview)
- [Algorithm Pipeline](#algorithm-pipeline)
- [CSP Formulation](#csp-formulation)
- [Code Structure](#code-structure)
- [Puzzle Boards](#puzzle-boards)
- [How to Run](#how-to-run)
- [Sample Output](#sample-output)
- [Performance & Metrics](#performance--metrics)
- [Author](#author)

---

## Overview

Rather than brute-forcing all possibilities, this solver models Sudoku as a **CSP** and applies layered AI search techniques to find solutions with minimal computational overhead:

1. **AC-3** prunes impossible values from cell domains before any guessing begins
2. **MRV** picks the most-constrained cell first to minimize branching
3. **Forward Checking** propagates constraints immediately after each assignment
4. **Backtracking** explores the remaining search tree and undoes bad choices

This combination guarantees a correct solution (if one exists) while avoiding exponential blowup even on Very Hard boards.

---

## Algorithm Pipeline

```
Input Board (.txt file)
        │
        ▼
┌──────────────────┐
│   SudokuCSP      │  ← Build variables, domains, neighbor graph
│   (Model)        │     (row peers + column peers + 3×3 box peers)
└───────┬──────────┘
        │
        ▼
┌──────────────────┐
│   AC-3           │  ← Arc consistency preprocessing
│   (Propagation)  │     Remove values with no valid support
└───────┬──────────┘
        │
        ▼
┌──────────────────────────────────┐
│   Backtracking Search            │
│   ├─ MRV Variable Selection      │  ← Pick cell with fewest legal values
│   ├─ Consistency Check           │  ← Validate against assigned neighbors
│   ├─ Forward Checking            │  ← Prune neighbors' domains immediately
│   └─ Undo on failure (backtrack) │  ← Restore removed values, try next
└───────┬──────────────────────────┘
        │
        ▼
   Solved Grid + Metrics
   (backtrack calls, failures)
```

---

## CSP Formulation

| CSP Component   | Sudoku Mapping                                              |
|-----------------|-------------------------------------------------------------|
| **Variables**   | 81 cells represented as `(row, col)` tuples                 |
| **Domains**     | Digits `1–9`; pre-filled cells have a single-value domain   |
| **Constraints** | No two peers may share the same digit                       |
| **Neighbors**   | All cells in the same row, column, or 3×3 box               |

### AC-3 (Arc Consistency — Preprocessing)

Processes every arc `(Xi, Xj)` in the constraint graph. Removes values from `Xi`'s domain that have no valid support in `Xj`. If any domain empties, the puzzle is unsolvable. For easy puzzles, AC-3 alone often resolves the majority of cells.

### MRV — Minimum Remaining Values (Variable Selection)

When choosing the next cell to assign, always picks the one with the fewest remaining legal values. This **fail-first** strategy reaches dead ends sooner, reducing unnecessary tree exploration.

### Forward Checking (Constraint Propagation During Search)

After assigning a value to a cell, immediately removes that value from all unassigned neighbors' domains. If any neighbor's domain becomes empty, triggers backtracking without exploring further — saving the solver from dead paths before entering them.

---

## Code Structure

```
sudoku-csp-solver/
│
├── q2.py            # Full solver — all logic and entry point
├── easy.txt         # Auto-generated at runtime
├── medium.txt       # Auto-generated at runtime
├── hard.txt         # Auto-generated at runtime
├── veryhard.txt     # Auto-generated at runtime
└── README.md
```

### Key Components

| Component | Role |
|---|---|
| `BOARDS` dict | Hardcoded raw string representations of all four puzzles |
| `SudokuCSP` class | Initializes variables, domains, and peer/neighbor graph |
| `Stats` class | Tracks `calls` and `failures` during backtracking search |
| `ac3()` / `revise()` | Constraint propagation — prunes domains before search |
| `select_unassigned_variable()` | MRV heuristic — picks the most constrained cell |
| `is_consistent()` | Validates a candidate value against already-assigned neighbors |
| `forward_check()` | Propagates assignment to unassigned neighbors immediately |
| `backtrack()` | Recursive DFS engine — assigns, propagates, undoes on failure |
| `solve_sudoku_file()` | Orchestrates the full pipeline for a given `.txt` board |

---

## Puzzle Boards

Four puzzles are embedded in `q2.py` and written to disk automatically on first run. `0` represents an empty cell.

| File | Difficulty | Behavior |
|---|---|---|
| `easy.txt` | Easy | AC-3 solves most cells; near-zero backtracking |
| `medium.txt` | Medium | Minimal backtracking required |
| `hard.txt` | Hard | Visible increase in calls and failures |
| `veryhard.txt` | Very Hard | Highest backtrack count; MRV is critical here |

---

## How to Run

### Prerequisites

- Python 3.6+
- No external libraries — standard library only

### Steps

```bash
# Clone the repository
git clone https://github.com/naynay575/Sudoku-Boards-as-CSPs.git
cd Sudoku-Boards-as-CSPs

# Run the solver
python q2.py
```

On first run, the script:
1. Generates `easy.txt`, `medium.txt`, `hard.txt`, `veryhard.txt`
2. Solves each puzzle in sequence
3. Prints the completed grid with box dividers
4. Reports backtracking metrics for each puzzle

---

## Sample Output

```
Generated easy.txt
Generated medium.txt
Generated hard.txt
Generated veryhard.txt
------------------------------

Solved easy.txt:
SOLUTION:
8 4 2 | 6 3 7 | 1 5 9
6 3 9 | 4 5 1 | 2 7 8
7 1 5 | 8 2 9 | 4 6 3
- - - + - - - + - - -
4 5 7 | 2 1 6 | 8 3 ...
...

Metrics for easy.txt:
BACKTRACK calls: 14
BACKTRACK failures: 0
```

---

## Performance & Metrics

The solver reports two values per puzzle after each run:

| Metric | What It Measures |
|---|---|
| `BACKTRACK calls` | Total recursive invocations of `backtrack()` |
| `BACKTRACK failures` | Times no valid value existed for a variable (forced undo) |

### Expected Scaling Behavior

- **Easy / Medium** — AC-3 resolves most of the board up front. Expect low call counts and zero or near-zero failures.
- **Hard / Very Hard** — More assumptions required. AC-3 and forward checking still aggressively prune, but wrong guesses will occur. Both metrics rise noticeably. MRV keeps the scaling manageable and avoids exponential blowup.

---

## Author

**Nehal Aftab**
Roll No: 24F-0518 · BCS-2E
FAST-NUCES CFD Campus, Faisalabad

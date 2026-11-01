# Principles of Artificial Intelligence (POAI) Lab Record

This repository contains lab assignments and implementations for the **Principles of Artificial Intelligence (POAI)** laboratory course.

---

## 📋 Table of Contents

- [Task 1: 8-Queens Problem](#task-1-8-queens-problem)
  - [1. Aim](#1-aim)
  - [2. Problem Description](#2-problem-description)
  - [3. Problem Formulation (CSP)](#3-problem-formulation-csp)
  - [4. Algorithm (Backtracking Search)](#4-algorithm-backtracking-search)
  - [5. Complexity Analysis](#5-complexity-analysis)
  - [6. How to Run](#6-how-to-run)
  - [7. Sample Output](#7-sample-output)

---

## Task 1: 8-Queens Problem

### 1. Aim
To formulate and implement the **8-Queens Problem** using the **Backtracking Algorithm** in Python, ensuring that 8 queens are placed on an $8 \times 8$ chessboard such that no two queens attack each other.

---

### 2. Problem Description
The 8-Queens puzzle is the problem of placing eight chess queens on an $8 \times 8$ chessboard so that no two queens threaten each other. Under standard chess rules, a queen can attack any piece lying in the same:
1. **Row**
2. **Column**
3. **Diagonal** (both main diagonal and anti-diagonal)

---

### 3. Problem Formulation (CSP)
The problem is modeled as a **Constraint Satisfaction Problem (CSP)**:
- **Variables**: $X = \{Q_0, Q_1, \dots, Q_7\}$, where variable $Q_c$ represents the queen placed in column $c$.
- **Domain**: $D_c = \{0, 1, 2, 3, 4, 5, 6, 7\}$ representing the row number in which queen $Q_c$ can be placed.
- **Constraints**: For any two queens $Q_i$ and $Q_j$ placed at column $i$ and column $j$ ($i \neq j$):
  - **Different Rows**: $Q_i \neq Q_j$
  - **Different Diagonals**: $|Q_i - Q_j| \neq |i - j|$

---

### 4. Algorithm (Backtracking Search)

Backtracking is an algorithmic paradigm that tests possibilities systematically and backtracks when a constraint violation is reached.

#### Step-by-Step Logic:
1. Start with the leftmost column (Column 0).
2. If all queens are placed successfully (Column index equals $N$), record/print the solution.
3. For the current column, try placing a queen in all rows from `0` to `N - 1`:
   - Check if the position `(row, col)` is safe from previously placed queens:
     - No queen in the same row: $board[prev\_col] \neq row$.
     - No queen in the upper or lower diagonal: $|board[prev\_col] - row| \neq |prev\_col - col|$.
   - If safe, mark this row in the current column and recursively try placing a queen in the next column (`col + 1`).
   - If placing the queen leads to no solution in subsequent columns, **backtrack** (unmark the position and try the next row).
4. If all rows in the current column have been tried without success, return failure to trigger backtracking in the previous column.

---

### 5. Complexity Analysis

- **State Space**:
  - Naive brute-force space: $\binom{64}{8} \approx 4.4 \times 10^9$ states.
  - Constrained search space (one queen per column): $8^8 \approx 16,777,216$ states.
  - Permutations (one queen per row & column): $8! = 40,320$ states.
- **Time Complexity with Backtracking**:
  - Worst Case: $O(N!)$
  - In practice, pruning branches drastically reduces the number of evaluated configurations.
- **Space Complexity**:
  - $O(N)$ auxiliary space for recursion stack and board state array.

---

### 6. How to Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sunilkumarv2025aiml-create/POAI_RECORD.git
   cd POAI_RECORD
   ```

2. **Execute the Python script**:
   ```bash
   python task1_8_queens.py
   ```

---

### 7. Sample Output

```text
============================================================
   PRINCIPLES OF ARTIFICIAL INTELLIGENCE (POAI) LAB RECORD
   Task 1: 8-Queens Problem using Backtracking Search
============================================================

Solving 8-Queens problem using Backtracking Search...

Total solutions found for N=8: 92
Search Statistics:
  - Total nodes/states explored : 2057
  - Total backtracks occurred   : 644

Displaying the FIRST valid solution:

=== Solution 1 ===
   A B C D E F G H
  +----------------+
8 | Q . . . . . . . | 8
7 | . . . . . . Q . | 7
6 | . . . . Q . . . | 6
5 | . . . . . . . Q | 5
4 | . Q . . . . . . | 4
3 | . . . Q . . . . | 3
2 | . . . . . Q . . | 2
1 | . . Q . . . . . | 1
  +----------------+
   A B C D E F G H
Queen Coordinates (Algebraic): A8, B4, C1, D3, E6, F2, G7, H5
Row indices by column: [0, 4, 7, 5, 2, 6, 1, 3]

============================================================
Verification:
Expected solutions for 8-Queens: 92
Actual solutions found         : 92
Result: SUCCESS (Matches theoretical 92 solutions)
============================================================
```

---

## 📌 Repository Structure

```
POAI_RECORD/
├── README.md              # Detailed documentation & theory for lab record
└── task1_8_queens.py      # Task 1 Python implementation with Backtracking
```

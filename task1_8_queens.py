"""
Task 1: 8-Queens Problem
Course: Principles of Artificial Intelligence (POAI) Lab
Description:
    Solve the 8-Queens problem using the Backtracking algorithm.
    The goal is to place 8 queens on an 8x8 chessboard such that
    no two queens attack each other (no two queens share the same
    row, column, or diagonal).
"""

from typing import List, Tuple


class NQueensSolver:
    """
    A class to solve the N-Queens problem using Constraint Satisfaction
    and Backtracking Search.
    """

    def __init__(self, n: int = 8):
        """
        Initialize the solver for an N x N chessboard.
        :param n: Size of the board (default is 8 for 8-Queens).
        """
        self.n = n
        self.solutions: List[List[int]] = []
        self.nodes_explored: int = 0
        self.backtracks: int = 0

    def is_safe(self, board: List[int], current_row: int, current_col: int) -> bool:
        """
        Check if placing a queen at (current_row, current_col) is safe from attacks
        by already placed queens in previous columns (0 to current_col - 1).

        board[col] stores the row position of the queen in that column.
        """
        for prev_col in range(current_col):
            prev_row = board[prev_col]

            # 1. Check same row attack
            if prev_row == current_row:
                return False

            # 2. Check diagonal attacks:
            # If absolute difference between rows equals difference between cols,
            # they lie on the same diagonal.
            if abs(prev_row - current_row) == abs(prev_col - current_col):
                return False

        return True

    def _solve_backtracking(self, board: List[int], current_col: int):
        """
        Recursive helper function to place queens column by column.
        """
        self.nodes_explored += 1

        # Base case: If all queens are placed (current_col reached n), save solution
        if current_col == self.n:
            self.solutions.append(list(board))
            return

        placed_any = False
        # Try placing a queen in every row of the current column
        for row in range(self.n):
            if self.is_safe(board, row, current_col):
                board[current_col] = row
                placed_any = True

                # Recur to place queen in the next column
                self._solve_backtracking(board, current_col + 1)

                # Backtrack: Reset position
                board[current_col] = -1

        if not placed_any:
            self.backtracks += 1

    def solve(self) -> List[List[int]]:
        """
        Find all valid non-attacking configurations of N queens.
        Returns a list of solutions, where each solution is a list of length N
        and solution[col] is the row index of the queen in column `col`.
        """
        self.solutions = []
        self.nodes_explored = 0
        self.backtracks = 0

        # board[i] will store the row where queen in column i is placed (-1 = empty)
        initial_board = [-1] * self.n
        self._solve_backtracking(initial_board, 0)
        return self.solutions

    def print_board(self, solution: List[int], solution_num: int = None):
        """
        Nicely prints the chessboard representation of a solution.
        """
        header = f"=== Solution {solution_num} ===" if solution_num else "=== Chessboard Configuration ==="
        print(f"\n{header}")

        # Column headers (A to H for N=8)
        col_labels = "   " + " ".join(chr(ord('A') + i) for i in range(self.n))
        print(col_labels)
        print("  +" + "--" * self.n + "+")

        for r in range(self.n):
            row_str = f"{self.n - r} | "
            for c in range(self.n):
                if solution[c] == r:
                    row_str += "Q "  # Queen placed
                else:
                    row_str += ". "  # Empty square
            row_str += f"| {self.n - r}"
            print(row_str)

        print("  +" + "--" * self.n + "+")
        print(col_labels)

        # Print coordinate list
        coords = [f"{chr(ord('A') + c)}{self.n - solution[c]}" for c in range(self.n)]
        print(f"Queen Coordinates (Algebraic): {', '.join(coords)}")
        print(f"Row indices by column: {solution}\n")


def main():
    print("=" * 60)
    print("   PRINCIPLES OF ARTIFICIAL INTELLIGENCE (POAI) LAB RECORD")
    print("   Task 1: 8-Queens Problem using Backtracking Search")
    print("=" * 60)

    # Initialize solver for standard 8x8 chessboard
    n = 8
    solver = NQueensSolver(n=n)
    print(f"\nSolving {n}-Queens problem using Backtracking Search...")
    solutions = solver.solve()

    print(f"\nTotal solutions found for N={n}: {len(solutions)}")
    print(f"Search Statistics:")
    print(f"  - Total nodes/states explored : {solver.nodes_explored}")
    print(f"  - Total backtracks occurred   : {solver.backtracks}")

    if solutions:
        print("\nDisplaying the FIRST valid solution:")
        solver.print_board(solutions[0], solution_num=1)

        # Prompt / display sample solutions
        if len(solutions) > 1:
            print("Additional sample solutions:")
            # Display solution 2 and the last solution
            solver.print_board(solutions[1], solution_num=2)
            if len(solutions) > 2:
                solver.print_board(solutions[-1], solution_num=len(solutions))

    print("=" * 60)
    print("Verification:")
    print(f"Expected solutions for 8-Queens: 92")
    print(f"Actual solutions found         : {len(solutions)}")
    print("Result: " + ("SUCCESS (Matches theoretical 92 solutions)" if len(solutions) == 92 else "FAILURE"))
    print("=" * 60)


if __name__ == "__main__":
    main()

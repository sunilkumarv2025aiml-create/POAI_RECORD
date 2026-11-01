"""
Task 3: Minimax Algorithm
Course: Principles of Artificial Intelligence (POAI) Lab
Description:
    Implementation of the Minimax Algorithm for Adversarial Search (Game Theory).
    This implementation covers:
    1. Game Tree Evaluation: Finding the optimal minimax value on a game tree.
    2. Tic-Tac-Toe AI: Using Minimax to find the best move for an unbeatable AI player.
    
    The algorithm assumes two players:
    - MAX (aims to maximize the score)
    - MIN (aims to minimize the score)
"""

import math
from typing import List, Tuple, Optional


# =====================================================================
# Part 1: Minimax on a Game Tree
# =====================================================================

def minimax_tree(
    depth: int,
    node_index: int,
    is_maximizing: bool,
    scores: List[int],
    height: int
) -> int:
    """
    Computes the optimal value for the current player using Minimax on a binary game tree.

    :param depth: Current depth in the game tree (0 at root).
    :param node_index: Index of the current node at the current depth.
    :param is_maximizing: True if current turn is MAX, False if MIN.
    :param scores: Leaf node utility values (length = 2^height).
    :param height: Maximum height of the tree.
    :return: Optimal minimax value.
    """
    # Base case: Leaf node reached
    if depth == height:
        return scores[node_index]

    if is_maximizing:
        # MAX player's turn: maximize the utility of child nodes
        best_val = -math.inf
        left_child = minimax_tree(depth + 1, node_index * 2, False, scores, height)
        right_child = minimax_tree(depth + 1, node_index * 2 + 1, False, scores, height)
        best_val = max(left_child, right_child)
        return best_val
    else:
        # MIN player's turn: minimize the utility of child nodes
        best_val = math.inf
        left_child = minimax_tree(depth + 1, node_index * 2, True, scores, height)
        right_child = minimax_tree(depth + 1, node_index * 2 + 1, True, scores, height)
        best_val = min(left_child, right_child)
        return best_val


# =====================================================================
# Part 2: Minimax Application - Tic-Tac-Toe AI
# =====================================================================

PLAYER_X = 'X'   # AI / MAX player (+10)
PLAYER_O = 'O'   # Human / MIN player (-10)
EMPTY = ' '


class TicTacToe:
    """
    Tic-Tac-Toe board and Minimax decision solver.
    """

    def __init__(self, board: Optional[List[str]] = None):
        # 3x3 board indexed 0 to 8
        self.board = board if board else [EMPTY] * 9

    def print_board(self):
        """Display the current 3x3 board."""
        print("\n  Current Board:")
        for row in range(3):
            r = self.board[row * 3:(row + 1) * 3]
            display_row = [cell if cell != EMPTY else str(row * 3 + i) for i, cell in enumerate(r)]
            print(f"    {display_row[0]} | {display_row[1]} | {display_row[2]}")
            if row < 2:
                print("   ---+---+---")
        print()

    def get_empty_cells(self) -> List[int]:
        """Return list of indices that are currently empty."""
        return [i for i, cell in enumerate(self.board) if cell == EMPTY]

    def check_winner(self) -> Optional[str]:
        """
        Check if there is a winner.
        Returns 'X', 'O', 'Tie' (if full), or None (game ongoing).
        """
        winning_combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)               # Diagonals
        ]

        for a, b, c in winning_combos:
            if self.board[a] != EMPTY and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]

        if not self.get_empty_cells():
            return "Tie"

        return None

    def evaluate(self, depth: int) -> int:
        """
        Terminal evaluation function for Tic-Tac-Toe:
        +10 - depth for X (favor quicker wins)
        -10 + depth for O (favor delayed losses)
        0 for Tie
        """
        winner = self.check_winner()
        if winner == PLAYER_X:
            return 10 - depth
        elif winner == PLAYER_O:
            return depth - 10
        elif winner == "Tie":
            return 0
        return 0

    def minimax(self, depth: int, is_maximizing: bool) -> int:
        """
        Recursive Minimax implementation for Tic-Tac-Toe.
        """
        winner = self.check_winner()
        if winner is not None:
            return self.evaluate(depth)

        if is_maximizing:
            max_eval = -math.inf
            for move in self.get_empty_cells():
                self.board[move] = PLAYER_X
                evaluation = self.minimax(depth + 1, False)
                self.board[move] = EMPTY
                max_eval = max(max_eval, evaluation)
            return max_eval
        else:
            min_eval = math.inf
            for move in self.get_empty_cells():
                self.board[move] = PLAYER_O
                evaluation = self.minimax(depth + 1, True)
                self.board[move] = EMPTY
                min_eval = min(min_eval, evaluation)
            return min_eval

    def find_best_move(self) -> Tuple[int, int]:
        """
        Finds the optimal move for PLAYER_X (MAX) using Minimax.
        Returns (best_move_index, best_score).
        """
        best_score = -math.inf
        best_move = -1

        for move in self.get_empty_cells():
            self.board[move] = PLAYER_X
            score = self.minimax(0, False)
            self.board[move] = EMPTY

            if score > best_score:
                best_score = score
                best_move = move

        return best_move, best_score


# =====================================================================
# Main Driver & Demonstrations
# =====================================================================

def main():
    print("=" * 65)
    print("   PRINCIPLES OF ARTIFICIAL INTELLIGENCE (POAI) LAB RECORD")
    print("   Task 3: Minimax Algorithm for Adversarial Search")
    print("=" * 65)

    # -------------------------------------------------------------
    # Demonstration 1: Minimax Evaluation on a Binary Game Tree
    # -------------------------------------------------------------
    print("\n--- DEMONSTRATION 1: GAME TREE EVALUATION ---")
    # Tree height = 3 (8 leaf nodes)
    # Root (MAX, depth 0) -> Level 1 (MIN) -> Level 2 (MAX) -> Level 3 (Leaves)
    leaf_scores = [3, 5, 2, 9, 12, 5, 23, 23]
    tree_height = int(math.log2(len(leaf_scores)))

    print(f"Leaf Node Values (Left to Right): {leaf_scores}")
    print(f"Tree Height                     : {tree_height}")
    print("Root Player                     : MAX")

    optimal_root_val = minimax_tree(
        depth=0,
        node_index=0,
        is_maximizing=True,
        scores=leaf_scores,
        height=tree_height
    )
    print(f"\n=> Optimal Minimax Value at Root: {optimal_root_val}")

    # -------------------------------------------------------------
    # Demonstration 2: Minimax Decision on Tic-Tac-Toe
    # -------------------------------------------------------------
    print("\n" + "-" * 65)
    print("--- DEMONSTRATION 2: ADVERSARIAL TIC-TAC-TOE MOVE SELECTION ---")
    print("Scenario: AI is playing 'X' (MAX) against Opponent 'O' (MIN).")
    
    # Board state where AI needs to make a strategic move:
    #  X | O | X
    #  O | O | .
    #  . | . | X
    sample_board = [
        'X', 'O', 'X',
        'O', 'O', ' ',
        ' ', ' ', 'X'
    ]
    game = TicTacToe(sample_board)
    game.print_board()

    best_move, score = game.find_best_move()
    row, col = divmod(best_move, 3)

    print(f"Available Empty Cells : {game.get_empty_cells()}")
    print(f"Optimal Move by Minimax: Cell {best_move} (Row {row}, Column {col})")
    print(f"Predicted Outcome Score : {score} (Positive = AI Win / Advantage)")

    # Apply best move and display board
    game.board[best_move] = PLAYER_X
    print("\nBoard after AI (X) plays optimal move:")
    game.print_board()

    # -------------------------------------------------------------
    # Theoretical Characteristics of Minimax
    # -------------------------------------------------------------
    print("=" * 65)
    print("Minimax Algorithm Characteristics:")
    print("  - Strategy        : Depth-First Game Tree Exploration")
    print("  - Players         : Two-player Zero-Sum Game (MAX and MIN)")
    print("  - Time Complexity : O(b^m) where b = branching factor, m = maximum depth")
    print("  - Space Complexity: O(b * m) for recursive state stack")
    print("  - Completeness    : Yes, if the game tree is finite")
    print("  - Optimality      : Yes, against an optimal opponent")
    print("=" * 65)


if __name__ == "__main__":
    main()

"""
Minimax Algorithm (with Alpha-Beta Pruning)
Course: Principles of Artificial Intelligence (POAI) Lab
Description:
    Implementation of the Minimax Algorithm and Alpha-Beta Pruning for Adversarial Search.
    
    Topics covered:
    1. Minimax on Game Trees (Evaluation of leaf utilities)
    2. Alpha-Beta Pruning (Optimizing Minimax by pruning subtrees)
    3. Tic-Tac-Toe Game AI (Unbeatable AI player using Minimax)
"""

import math
from typing import List, Tuple, Optional


# =====================================================================
# 1. Classical Minimax on Game Trees
# =====================================================================

def minimax(
    depth: int,
    node_index: int,
    is_maximizing: bool,
    scores: List[int],
    height: int
) -> int:
    """
    Standard Minimax algorithm for a binary game tree.
    """
    if depth == height:
        return scores[node_index]

    if is_maximizing:
        return max(
            minimax(depth + 1, node_index * 2, False, scores, height),
            minimax(depth + 1, node_index * 2 + 1, False, scores, height)
        )
    else:
        return min(
            minimax(depth + 1, node_index * 2, True, scores, height),
            minimax(depth + 1, node_index * 2 + 1, True, scores, height)
        )


# =====================================================================
# 2. Minimax with Alpha-Beta Pruning
# =====================================================================

def alpha_beta_minimax(
    depth: int,
    node_index: int,
    is_maximizing: bool,
    scores: List[int],
    height: int,
    alpha: float = -math.inf,
    beta: float = math.inf,
    pruned_count: Optional[List[int]] = None
) -> int:
    """
    Minimax search enhanced with Alpha-Beta Pruning to skip evaluation
    of branches that cannot influence the final decision.
    """
    if depth == height:
        return scores[node_index]

    if is_maximizing:
        best_val = -math.inf
        for i in range(2):
            val = alpha_beta_minimax(depth + 1, node_index * 2 + i, False, scores, height, alpha, beta, pruned_count)
            best_val = max(best_val, val)
            alpha = max(alpha, best_val)
            if beta <= alpha:
                if pruned_count is not None:
                    pruned_count[0] += 1
                break  # Beta cut-off
        return best_val
    else:
        best_val = math.inf
        for i in range(2):
            val = alpha_beta_minimax(depth + 1, node_index * 2 + i, True, scores, height, alpha, beta, pruned_count)
            best_val = min(best_val, val)
            beta = min(beta, best_val)
            if beta <= alpha:
                if pruned_count is not None:
                    pruned_count[0] += 1
                break  # Alpha cut-off
        return best_val


# =====================================================================
# 3. Tic-Tac-Toe AI Application
# =====================================================================

PLAYER_X = 'X'   # AI / Maximizer
PLAYER_O = 'O'   # Human / Minimizer
EMPTY = ' '


class TicTacToe:
    def __init__(self, board: Optional[List[str]] = None):
        self.board = board if board else [EMPTY] * 9

    def print_board(self):
        print("\n  Board:")
        for row in range(3):
            r = self.board[row * 3:(row + 1) * 3]
            display = [c if c != EMPTY else str(row * 3 + i) for i, c in enumerate(r)]
            print(f"    {display[0]} | {display[1]} | {display[2]}")
            if row < 2:
                print("   ---+---+---")
        print()

    def get_empty_cells(self) -> List[int]:
        return [i for i, c in enumerate(self.board) if c == EMPTY]

    def check_winner(self) -> Optional[str]:
        lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in lines:
            if self.board[a] != EMPTY and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        if not self.get_empty_cells():
            return "Tie"
        return None

    def minimax(self, depth: int, is_maximizing: bool) -> int:
        winner = self.check_winner()
        if winner == PLAYER_X:
            return 10 - depth
        elif winner == PLAYER_O:
            return depth - 10
        elif winner == "Tie":
            return 0

        if is_maximizing:
            best = -math.inf
            for move in self.get_empty_cells():
                self.board[move] = PLAYER_X
                score = self.minimax(depth + 1, False)
                self.board[move] = EMPTY
                best = max(best, score)
            return best
        else:
            best = math.inf
            for move in self.get_empty_cells():
                self.board[move] = PLAYER_O
                score = self.minimax(depth + 1, True)
                self.board[move] = EMPTY
                best = min(best, score)
            return best

    def find_best_move(self) -> Tuple[int, int]:
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
# Main Execution
# =====================================================================

def main():
    print("=" * 65)
    print("   PRINCIPLES OF ARTIFICIAL INTELLIGENCE (POAI) LAB RECORD")
    print("   Minimax Algorithm & Alpha-Beta Pruning")
    print("=" * 65)

    # 1. Game Tree Demo
    scores = [3, 5, 6, 9, 1, 2, 0, -1]
    height = int(math.log2(len(scores)))
    
    print("\n--- 1. GAME TREE EVALUATION ---")
    print(f"Leaf Node Values : {scores}")
    print(f"Tree Height      : {height}")
    
    result_minimax = minimax(0, 0, True, scores, height)
    print(f"Minimax Value at Root      : {result_minimax}")

    pruned = [0]
    result_ab = alpha_beta_minimax(0, 0, True, scores, height, pruned_count=pruned)
    print(f"Alpha-Beta Value at Root   : {result_ab}")
    print(f"Branches Pruned            : {pruned[0]}")

    # 2. Tic-Tac-Toe AI Move Selection Demo
    print("\n--- 2. TIC-TAC-TOE AI MOVE SELECTION ---")
    sample_board = [
        'X', 'O', 'X',
        'O', 'O', ' ',
        ' ', ' ', 'X'
    ]
    game = TicTacToe(sample_board)
    game.print_board()

    best_move, score = game.find_best_move()
    print(f"Optimal Move Calculated: Cell {best_move} (Row {best_move // 3}, Col {best_move % 3})")
    print(f"Minimax Score          : {score} (+10 indicates guaranteed win for AI)")

    game.board[best_move] = PLAYER_X
    print("\nBoard after AI Move:")
    game.print_board()

    print("=" * 65)


if __name__ == "__main__":
    main()

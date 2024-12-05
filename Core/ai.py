import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Util.constants import HUMAN_PLAYER_VALUE, AI_PLAYER_VALUE

class AI:
    def __init__(self, difficulty="medium"):
        self.difficulty_levels = {"easy": 2, "medium": 4, "hard": 6}
        self.depth = self.difficulty_levels.get(difficulty, 4)

    def heuristic1(self, board):
        ai_score = sum(row.count(AI_PLAYER_VALUE) for row in board.board)
        human_score = sum(row.count(HUMAN_PLAYER_VALUE) for row in board.board)
        return ai_score - human_score
    def heuristic2(self, board):
        def score_line(line):
            score = 0
            if line.count(AI_PLAYER_VALUE) == 4 and line.count(0) == 1:
                score += 1000  # Almost winning
            if line.count(HUMAN_PLAYER_VALUE) == 4 and line.count(0) == 1:
                score -= 1000  # Block opponent
            if line.count(AI_PLAYER_VALUE) == 3 and line.count(0) == 2:
                score += 100  # Good position
            if line.count(HUMAN_PLAYER_VALUE) == 3 and line.count(0) == 2:
                score -= 100  # Block opponent's position
            return score
        total_score = 0
        size = board.size
        # Rows, Columns, and Diagonals
        for i in range(size):
            for j in range(size - 4):
                total_score += score_line([board.board[i][j + k] for k in range(5)])  # Rows
                total_score += score_line([board.board[j + k][i] for k in range(5)])  # Columns
        for i in range(size - 4):
            for j in range(size - 4):
                total_score += score_line([board.board[i + k][j + k] for k in range(5)])  # Diagonal \
                total_score += score_line([board.board[i + k][j + 4 - k] for k in range(5)])  # Diagonal /
        return total_score

    def minimax(self, board, depth, maximizing_player, alpha=-float('inf'), beta=float('inf')):
        winner = board.check_winner()
        if winner == AI_PLAYER_VALUE:
            return 10000, None
        elif winner == HUMAN_PLAYER_VALUE:
            return -10000, None
        elif winner == 0 or depth == 0:
            return self.heuristic1(board), None

        best_move = None
        valid_moves = self.get_valid_moves(board)

        # Move ordering: Sort by heuristic scores
        valid_moves.sort(key=lambda move: self.heuristic1(board), reverse=maximizing_player)

        if maximizing_player:
            max_eval = -float('inf')
            for move in valid_moves:
                board.place_marker(move[0], move[1], AI_PLAYER_VALUE)
                evaluation, _ = self.minimax(board, depth - 1, False, alpha, beta)
                board.undo_move(move[0], move[1])
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in valid_moves:
                board.place_marker(move[0], move[1], HUMAN_PLAYER_VALUE)
                evaluation, _ = self.minimax(board, depth - 1, True, alpha, beta)
                board.undo_move(move[0], move[1])
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval, best_move


    def get_best_move(self, board):
        _, best_move = self.minimax(board, self.depth, True)
        return best_move

    def get_valid_moves(self, board):
        moves = set()
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for x in range(board.size):
            for y in range(board.size):
                if board.board[x][y] != 0:
                    for dx, dy in directions:
                        for step in range(1, 3):
                            nx, ny = x + dx * step, y + dy * step
                            if 0 <= nx < board.size and 0 <= ny < board.size and board.board[nx][ny] == 0:
                                moves.add((nx, ny))
        return list(moves)


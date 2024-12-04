from Util.constants import HUMAN_PLAYER_VALUE, AI_PLAYER_VALUE

class AI:
    def __init__(self, difficulty="medium"):
        self.difficulty_levels = {"easy": 2, "medium": 4, "hard": 6}
        self.depth = self.difficulty_levels.get(difficulty, 4)
    def heuristic1(board):
        ai_score = sum(row.count(AI_PLAYER_VALUE) for row in board.board)
        human_score = sum(row.count(HUMAN_PLAYER_VALUE) for row in board.board)
        return ai_score - human_score
    def minimax(self, board, depth, maximizing_player, alpha=-float('inf'), beta=float('inf')):
        winner = board.check_winner()
        if winner == AI_PLAYER_VALUE:
            return 10000, None
        elif winner == HUMAN_PLAYER_VALUE:
            return -10000, None
        elif winner == 0 or depth == 0:
            return self.heuristic1(board), None
        best_move = None
        if maximizing_player:
            max_eval = -float('inf')
            for move in self.get_valid_moves(board):
                board.make_move(move[0], move[1], 1)
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
            for move in self.get_valid_moves(board):
                board.make_move(move[0], move[1], -1)
                evaluation, _ = self.minimax(board, depth - 1, True, alpha, beta)
                board.undo_move(move[0], move[1])
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval, best_move
    def get_best_move(self, depth):
        best_move = self.minimax(self.depth, float("-inf"), float("inf"), True)
        return best_move
    def get_valid_moves(self, board):
        return [(x, y) for x in range(board.size) for y in range(board.size) if board.board[x][y] == 0]
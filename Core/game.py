from board import Board
class Game:
    __HUMAN_PLAYER_VALUE = -1
    __AI_PLAYER_VALUE = 1
    def __init__(self, board_size=15, ai_difficulty="medium"):
        self.board = Board(size=board_size)
        self.current_player = self.__HUMAN_PLAYER_VALUE
        self.ai_difficulty = ai_difficulty
    def play_turn(self, x, y):
        if self.current_player == self.__HUMAN_PLAYER_VALUE:
            if self.board.make_move(x, y, self.current_player):
                self.current_player = self.__AI_PLAYER_VALUE
                return True
        else:
            move = self.get_ai_move()
            if move:
                self.board.make_move(move[0], move[1], self.current_player)
                self.current_player = self.__HUMAN_PLAYER_VALUE
                return True
        return False
    def get_ai_move(self):
        from ai import AI
        ai = AI(self.ai_difficulty)
        return ai.get_best_move(self.board)
    def is_game_over(self):
        return self.board.check_winner() is not None
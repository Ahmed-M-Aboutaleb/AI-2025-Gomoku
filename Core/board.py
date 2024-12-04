from Util.constants import DRAW_VALUE
class Board:
    def __init__(self, size=15):
        self.size = size
        self.board = [[0] * size for _ in range(size)]
    def is_valid_move(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == 0
    def place_marker(self, x, y, marker):
        if self.is_valid_move(x, y):
            self.board[x][y] = marker
            return True
        return False
    def check_winner(self, x, y, marker):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    if j + 4 < self.size and all(self.board[i][j + k] == self.board[i][j] for k in range(5)):
                        return self.board[i][j]
                    if i + 4 < self.size and all(self.board[i + k][j] == self.board[i][j] for k in range(5)):
                        return self.board[i][j]
                    if i + 4 < self.size and j + 4 < self.size and all(self.board[i + k][j + k] == self.board[i][j] for k in range(5)):
                        return self.board[i][j]
                    if i + 4 < self.size and j - 4 >= 0 and all(self.board[i + k][j - k] == self.board[i][j] for k in range(5)):
                        return self.board[i][j]
        if self.is_full():
            return DRAW_VALUE
        return None 
    def is_full(self):
        return all(self.board[i][j] != 0 for i in range(self.size) for j in range(self.size))
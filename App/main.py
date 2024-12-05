import tkinter as tk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.game import Game
from Util.constants import HUMAN_PLAYER_VALUE, AI_PLAYER_VALUE, SYMBOL_X, SYMBOL_O

class GomokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gomoku AI")
        self.game = Game()
        self.board_buttons = []
        self.create_board()

    def create_board(self):
        for i in range(self.game.board.size):
            row_buttons = []
            for j in range(self.game.board.size):
                button = tk.Button(self.root, text=" ", width=4, height=2, command=lambda row=i, col=j: self.on_move(row, col))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.board_buttons.append(row_buttons)

    def on_move(self, row, col):
        if self.game.play_turn(row, col):
            self.update_ui()
        if self.game.current_player == AI_PLAYER_VALUE:
            self.root.after(500, self.update_ui)

    def update_ui(self):
        for i in range(self.game.board.size):
            for j in range(self.game.board.size):
                if self.game.board.board[i][j] == HUMAN_PLAYER_VALUE:
                    self.board_buttons[i][j].config(text=SYMBOL_O)
                elif self.game.board.board[i][j] == AI_PLAYER_VALUE:
                    self.board_buttons[i][j].config(text=SYMBOL_X)

if __name__ == "__main__":
    root = tk.Tk()
    app = GomokuApp(root)
    root.mainloop()

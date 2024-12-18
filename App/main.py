import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Core.game import Game
from Util.constants import HUMAN_PLAYER_VALUE, AI_PLAYER_VALUE, SYMBOL_X, SYMBOL_O

class GomokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gomoku AI")

        self.difficulty = tk.StringVar(value="medium")
        self.grid_size = tk.IntVar(value=15)

        self.game = None
        self.board_buttons = []

        self.create_setup_menu()

    def create_setup_menu(self):
        setup_frame = tk.Frame(self.root)
        setup_frame.pack(pady=10)

        # Difficulty selection
        tk.Label(setup_frame, text="Select Difficulty:").grid(row=0, column=0, padx=5, pady=5)
        difficulty_menu = ttk.Combobox(setup_frame, textvariable=self.difficulty, state="readonly")
        difficulty_menu["values"] = ("easy", "medium", "hard")
        difficulty_menu.grid(row=0, column=1, padx=5, pady=5)

        # Grid size selection
        tk.Label(setup_frame, text="Select Grid Size:").grid(row=1, column=0, padx=5, pady=5)
        grid_size_entry = ttk.Spinbox(setup_frame, from_=5, to=30, textvariable=self.grid_size, width=5)
        grid_size_entry.grid(row=1, column=1, padx=5, pady=5)

        # Start button
        start_button = tk.Button(setup_frame, text="Start Game", command=self.start_game)
        start_button.grid(row=2, column=0, columnspan=2, pady=10)

    def start_game(self):
        # Clear existing widgets and reset the game
        for widget in self.root.winfo_children():
            widget.destroy()

        self.game = Game(board_size=self.grid_size.get(), ai_difficulty=self.difficulty.get())
        self.board_buttons = []
        self.create_board()

    def create_board(self):
        board_frame = tk.Frame(self.root)
        board_frame.pack(pady=10)

        for i in range(self.game.board.size):
            row_buttons = []
            for j in range(self.game.board.size):
                button = tk.Button(board_frame, text=" ", width=4, height=2, 
                                   command=lambda row=i, col=j: self.on_move(row, col))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.board_buttons.append(row_buttons)

    def on_move(self, row, col):
        if self.game.play_turn(row, col):
            self.update_ui()
            if self.game.is_game_over():
                self.display_winner()
            elif self.game.current_player == AI_PLAYER_VALUE:
                self.root.after(500, self.ai_move)

    def ai_move(self):
        self.game.play_turn(None, None)  # AI's move
        self.update_ui()
        if self.game.is_game_over():
            self.display_winner()

    def update_ui(self):
        for i in range(self.game.board.size):
            for j in range(self.game.board.size):
                if self.game.board.board[i][j] == HUMAN_PLAYER_VALUE:
                    self.board_buttons[i][j].config(text=SYMBOL_O)
                elif self.game.board.board[i][j] == AI_PLAYER_VALUE:
                    self.board_buttons[i][j].config(text=SYMBOL_X)

    def display_winner(self):
        winner = self.game.board.check_winner()
        message = "Draw!" if winner == 0 else ("AI Wins!" if winner == AI_PLAYER_VALUE else "Human Wins!")
        messagebox.showinfo("Game Over", message)
        self.root.after(2000, self.root.destroy)  # Delay before closing

if __name__ == "__main__":
    root = tk.Tk()
    app = GomokuApp(root)
    root.mainloop()

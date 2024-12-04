class Board:
    """TODO: Gomoku Board"""
    def __init__(self, size=15):
        self.size = size
    def is_valid_move(self, x, y):
        """TODO: Check if a move is valid."""
    def place_marker(self, x, y, marker):
        """TODO: Place a marker on the board."""
    def check_winner(self, x, y, marker):
        """TODO: Check if placing `marker` at `(x, y)` resulted in a win."""
    def is_full(self):
        """TODO: Check if the board is full."""
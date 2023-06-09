from dataclasses import dataclass


@dataclass
class Board:
    """
    This class wraps the original data structure representing the board, which
    is a list of integers ∈ {0, 1, 2} representing either an empty cell (0),
    a piece from player 1 (1) or a piece from player 2 (2).

    The regular size of the board is 7 rows x 6 columns, but those values are
    parametrized, but won't change during the game.

    The following is a representation of a board with its row indexes, column
    indexes and board indexes

        0   1   2   3   4   5   6
    0 [ 00, 01, 02, 03, 04, 05, 06,
    1   07, 08, 09, 10, 11, 12, 13,
    2   14, 15, 16, 17, 18, 19, 20,
    3   21, 22, 23, 24, 25, 26, 27,
    4   28, 29, 30, 31, 32, 33, 34,
    5   35, 36, 37, 38, 39, 40, 41 ]

    """
    board: list[int]
    rows: int
    columns: int

    def __getitem__(self, item):
        return self.board[item]

    def __len__(self):
        return len(self.board)


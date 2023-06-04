import unittest

from board.board_class import Board


def parse_board(nested_list: list[list[int]]) -> 'Board':
    """
    parses a board from a nested list representation
    [[0, 0, 0],
     [1, 2, 1], => Board(board=[0, 0, 0, 1, 2, 1, 2, 1, 2], rows=3, columns=3)
     [2, 1, 2]]
    """
    assert len(nested_list) > 0, '0 rows'
    first_row = nested_list[0]
    assert len(first_row) > 0, '0 columns'
    assert all(len(row) == len(first_row) for row in nested_list), 'unequal row lengths'

    rows = len(nested_list)
    columns = len(first_row)
    board_list = [value for row in nested_list for value in row]
    assert all(value in [0, 1, 2] for value in board_list), 'invalid board value'
    return Board(board_list, rows, columns)


def get_default_empty_board() -> Board:
    """
    Returns an empty 7 x 6 board

    Board indexes:
         0   1   2   3   4   5   6
    0 [ 00, 01, 02, 03, 04, 05, 06,
    1   07, 08, 09, 10, 11, 12, 13,
    2   14, 15, 16, 17, 18, 19, 20,
    3   21, 22, 23, 24, 25, 26, 27,
    4   28, 29, 30, 31, 32, 33, 34,
    5   35, 36, 37, 38, 39, 40, 41 ]
    """
    return Board([0 for _ in range(42)], columns=7, rows=6)

class TestParseBoard(unittest.TestCase):
    def test_parse_small_board(self):
        board = [[0, 0, 0],
                 [1, 0, 2],
                 [1, 1, 2]]
        expected = Board([0, 0, 0, 1, 0, 2, 1, 1, 2], 3, 3)
        actual = parse_board(board)
        self.assertEqual(expected, actual)


    def test_parse_full_sized_board(self):
        expected = get_default_empty_board()
        expected.board[35] = 1
        expected.board[28] = 1
        expected.board[39] = 2
        expected.board[40] = 2

        actual = parse_board(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 2, 2, 0]
            ]
        )

        self.assertEqual(expected, actual)

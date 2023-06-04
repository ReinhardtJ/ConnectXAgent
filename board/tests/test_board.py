import unittest

from board.interaction import add_bead
from board.navigation import get_value_at, get_row_and_col_at, get_index_at, Up, UpRight, Right, \
    DownRight, Down, DownLeft, Left, UpLeft, DownwardsDiagonal, UpwardsDiagonal, Horizontal, Vertical, TAxis, \
    all_axes
from board.tests.helpers import parse_board
from board.value_calculation import get_board_value, value_table, find_blocked_opponent_connections, find_connections


class TestBoardSpecialCases(unittest.TestCase):
    def test_board_no_except_1(self):
        board = parse_board(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 1, 0, 2]
            ]
        )
        find_connections(board, 2)

    def test_board_no_except_2(self):
        board = parse_board(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1]
            ]
        )
        get_board_value(board, 1)
        get_board_value(board, 2)


class TestBoard(unittest.TestCase):
    def test_get_value_at(self):
        board = parse_board(
            [[0, 0, 0],  # [[0, 1, 2]
             [1, 0, 0],  # [3, 4, 5]
             [0, 0, 2]]  # [6, 7, 8]]
        )
        self.assertEqual(get_value_at(board, 1, 0), 1)
        self.assertEqual(get_value_at(board, 0, 0), 0)
        self.assertEqual(get_value_at(board, 2, 2), 2)

    def test_get_row_and_column_at(self):
        board = parse_board(
            [[0, 0, 0],  # [[0, 1, 2]
             [1, 0, 0],  # [3, 4, 5]
             [0, 0, 2]]  # [6, 7, 8]]
        )
        self.assertEqual(get_row_and_col_at(board, 3), (1, 0))
        self.assertEqual(get_row_and_col_at(board, 0), (0, 0))
        self.assertEqual(get_row_and_col_at(board, 8), (2, 2))

    def test_get_row_and_column_at_2(self):
        board = parse_board(
            [
                #     0   1   2   3   4   5   6
                [0, 0, 0, 0, 0, 0, 0],  # 0   00, 01, 02, 03, 04, 05, 06,
                [0, 0, 0, 0, 0, 0, 0],  # 1   07, 08, 09, 10, 11, 12, 13,
                [0, 0, 0, 0, 0, 0, 0],  # 2   14, 15, 16, 17, 18, 19, 20,
                [0, 0, 0, 1, 0, 0, 0],  # 3   21, 22, 23, 24, 25, 26, 27,
                [0, 2, 0, 1, 0, 0, 2],  # 4   28, 29, 30, 31, 32, 33, 34,
                [0, 0, 0, 0, 0, 0, 0]  # 5   35, 36, 37, 38, 39, 40, 41 ]
            ]
        )

        self.assertEqual(get_row_and_col_at(board, 31), (4, 3))

    def test_get_index_at(self):
        board = parse_board(
            [[0, 0, 0],  # [[0, 1, 2]
             [1, 0, 0],  # [3, 4, 5]
             [0, 0, 2]]  # [6, 7, 8]]
        )
        self.assertEqual(get_index_at(board, 1, 0), 3)
        self.assertEqual(get_index_at(board, 0, 0), 0)
        self.assertEqual(get_index_at(board, 2, 2), 8)

    def test_get_board_value(self):
        board = parse_board(
            [[0, 0, 0],  # [[0, 1, 2]
             [1, 0, 0],  # [3, 4, 5]
             [1, 2, 2]]  # [6, 7, 8]]
        )
        # own: {vertical: [3, 6]} blocked: {horizontal: [7, 8], downwards_diagonal: [7]}
        self.assertEqual(2 / 6 + 3 / 6 + 1 / 6, get_board_value(board, 1))
        # own: {horizontal: [7, 8]} blocked: {vertical: [6], downwards_diagonal: [3]}
        self.assertEqual(2 / 6 + 1 / 6 + 1 / 6, get_board_value(board, 2))

    # def test_get_board_value_layout_2(self):
    #     board = parse_board(
    #         [[0, 0, 0],  # [[0, 1, 2]
    #          [0, 0, 0],  # [3, 4, 5]
    #          [0, 0, 1]]  # [6, 7, 8]]
    #     )
    #     board.get_board_value(2)

    def test_get_board_value_2(self):
        board = parse_board(
            [  # 0   1   2   3   4   5   6
                [0, 0, 0, 0, 0, 0, 0],  # 0   00, 01, 02, 03, 04, 05, 06,
                [0, 0, 0, 0, 0, 0, 0],  # 1   07, 08, 09, 10, 11, 12, 13,
                [0, 0, 0, 0, 0, 0, 0],  # 2   14, 15, 16, 17, 18, 19, 20,
                [0, 0, 0, 0, 0, 0, 0],  # 3   21, 22, 23, 24, 25, 26, 27,
                [0, 0, 0, 1, 0, 0, 0],  # 4   28, 29, 30, 31, 32, 33, 34,
                [0, 2, 0, 1, 0, 0, 2]  # 5   35, 36, 37, 38, 39, 40, 41 ]
            ]
        )
        self.assertEqual(get_board_value(board, 1), value_table[2])
        self.assertEqual(get_board_value(board, 2), 0)

    def test_add_bead(self):
        board = parse_board(
            [[1, 0, 0],  # [[0, 1, 2]
             [2, 0, 0],  # [3, 4, 5]
             [1, 0, 0]]  # [6, 7, 8]]
        )

        self.assertRaises(AssertionError, lambda: add_bead(board, 2, 0))

        board = parse_board(
            [[0, 0, 0],  # [[0, 1, 2]
             [2, 0, 0],  # [3, 4, 5]
             [1, 1, 0]]  # [6, 7, 8]]
        )
        expected_board = parse_board(
            [[0, 0, 0],  # [[0, 1, 2]
             [2, 1, 0],  # [3, 4, 5]
             [1, 1, 0]]  # [6, 7, 8]]
        )

        add_bead(board, 1, 1)
        self.assertEqual(board, expected_board)


class TestFindBlockedConnections(unittest.TestCase):
    def test(self):
        board_with_blocked_connections = parse_board(
            [[0, 0, 0, 0],  # [[00, 01, 02, 03],
             [1, 1, 2, 2],  # [04, 05, 06, 07],
             [1, 2, 1, 2],  # [08, 09, 10, 11],
             [1, 2, 2, 1]]  # [12, 13, 14, 15]]
        )
        blocked_connections = {
            Vertical: [[9, 13], [14]],
            Horizontal: [[6, 7], [13, 14], [9], [11]],
            UpwardsDiagonal: [[13], [7]],
            DownwardsDiagonal: [[9, 14], [13]]
        }
        actual = find_blocked_opponent_connections(board_with_blocked_connections, 1)
        for axis in all_axes():
            self.assertEqual(sorted(blocked_connections[axis]), sorted(actual[axis]))


class TestFindConnections(unittest.TestCase):
    def test(self):
        board_with_connections = parse_board(
            [[0, 0, 0, 0],  # [00, 01, 02, 03]
             [1, 1, 2, 0],  # [04, 05, 06, 07]
             [1, 2, 1, 2],  # [08, 09, 10, 11]
             [1, 2, 2, 1]]  # [12, 13, 14, 15]
        )
        connections_mark_1: dict[TAxis, list[list[int]]] = {
            Horizontal: [[4, 8, 12], [5], [10], [15]],
            Vertical: [[4, 5], [8], [10], [12], [15]],
            UpwardsDiagonal: [[8, 5], [4], [12], [10], [15]],
            DownwardsDiagonal: [[5, 10, 15], [4], [8], [12]]
        }

        connections_mark_2: dict[TAxis, list[list[int]]] = {
            Horizontal: [[13, 14], [6], [9], [11]],
            Vertical: [[9, 13], [6], [14], [11]],
            UpwardsDiagonal: [[9, 6], [14, 11], [13]],
            DownwardsDiagonal: [[9, 14], [6, 11], [13]]
        }

        for axis in all_axes():
            self.assertEqual(
                sorted(connections_mark_1[axis]),
                sorted(find_connections(board_with_connections, 1)[axis])
            )
            self.assertEqual(
                sorted(connections_mark_2[axis]),
                sorted(find_connections(board_with_connections, 2)[axis])
            )


class TestGetNeighborIndex(unittest.TestCase):
    def test(self):
        board = parse_board(
            [[0, 0, 0],  # [0, 1, 2]
             [0, 0, 0],  # [3, 4, 5]
             [0, 0, 0]]  # [6, 7, 8]
        )
        self.assertEqual(1, Up.get_neighbor_index(board, 4))
        self.assertEqual(2, UpRight.get_neighbor_index(board, 4))
        self.assertEqual(5, Right.get_neighbor_index(board, 4))
        self.assertEqual(8, DownRight.get_neighbor_index(board, 4))
        self.assertEqual(7, Down.get_neighbor_index(board, 4))
        self.assertEqual(6, DownLeft.get_neighbor_index(board, 4))
        self.assertEqual(3, Left.get_neighbor_index(board, 4))
        self.assertEqual(0, UpLeft.get_neighbor_index(board, 4))

        self.assertEqual(None, Up.get_neighbor_index(board, 1))
        self.assertEqual(None, UpRight.get_neighbor_index(board, 2))
        self.assertEqual(None, Right.get_neighbor_index(board, 5))
        self.assertEqual(None, DownRight.get_neighbor_index(board, 8))
        self.assertEqual(None, Down.get_neighbor_index(board, 7))
        self.assertEqual(None, DownLeft.get_neighbor_index(board, 6))
        self.assertEqual(None, Left.get_neighbor_index(board, 3))
        self.assertEqual(None, UpLeft.get_neighbor_index(board, 0))

        small_board = parse_board([[0]])
        self.assertEqual(None, Up.get_neighbor_index(small_board, 0))
        self.assertEqual(None, UpRight.get_neighbor_index(small_board, 0))
        self.assertEqual(None, Right.get_neighbor_index(small_board, 0))
        self.assertEqual(None, DownRight.get_neighbor_index(small_board, 0))
        self.assertEqual(None, Down.get_neighbor_index(small_board, 0))
        self.assertEqual(None, DownLeft.get_neighbor_index(small_board, 0))
        self.assertEqual(None, Left.get_neighbor_index(small_board, 0))
        self.assertEqual(None, UpLeft.get_neighbor_index(small_board, 0))

import unittest
from enum import Enum
from collections import deque

import attr

from funcs import update_group


class Direction(Enum):
    up = 0
    up_right = 1
    right = 2
    down_right = 3
    down = 4
    down_left = 5
    left = 6
    up_left = 7

    def is_positive(self):
        return self in [Direction.up_right,
                        Direction.right,
                        Direction.down_right,
                        Direction.down]


class Axis(Enum):
    vertical = 0
    horizontal = 1
    upwards_diagonal = 2
    downwards_diagonal = 3

    def get_directions(self) -> tuple[Direction, Direction]:
        directions = {
            Axis.vertical: (Direction.up, Direction.down),
            Axis.horizontal: (Direction.right, Direction.left),
            Axis.upwards_diagonal: (Direction.up_right, Direction.down_left),
            Axis.downwards_diagonal: (Direction.down_right, Direction.up_left)
        }
        return directions[self]

    @staticmethod
    def all_axes() -> list['Axis']:
        return [Axis.vertical, Axis.horizontal, Axis.upwards_diagonal, Axis.downwards_diagonal]


@attr.s(auto_attribs=True)
class Board:
    """
    This class wraps the original data structure representing the board, which
    is a list of integers ∈ {0, 1, 2} representing either an empty cell (0),
    a bead from player 1 (1) or a bead from player 2 (2).

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

    @staticmethod
    def parse_from_nested_list(nested_list: list[list[int]]) -> 'Board':
        """
        parses a board from a nested list representation and
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

    def get_value_at(self, row: int, col: int):
        return self.board[self.get_index_at(row, col)]

    def get_index_at(self, row: int, col: int) -> int:
        return row * self.rows + col

    def get_row_and_col_at(self, index: int) -> tuple[int, int]:
        row = int(index / self.rows)
        column = index - row * self.rows
        return row, column

    def get_board_value(self, mark: int):
        connections = self.find_connections(mark)
        value = 0
        for connection in connections:
            pass

    def find_connections(self, mark: int) -> dict[Axis, set[list[int]]]:
        """
        returns a list of indexes which are connections of a player (specified
        by mark), grouped by axis
        """
        assert mark in [1, 2]

        connections = {
            Axis.vertical: [],
            Axis.horizontal: [],
            Axis.upwards_diagonal: [],
            Axis.downwards_diagonal: []
        }
        for value in range(len(self.board)):
            if self.board[value] != mark:
                continue

            for axis in Axis.all_axes():
                connection = self._find_connection_on_axis(axis, value, mark)
                if len(connection) > 1:
                    connections = update_group(connections, axis, connection)

        return connections

    def _find_connection_on_axis(
            self,
            axis: Axis,
            value: int,
            mark: int
    ) -> list[int]:
        connection = deque([value])
        pos_direction, neg_direction = axis.get_directions()
        connection = self._find_connection_in_one_direction(value, pos_direction, connection, mark)
        connection = self._find_connection_in_one_direction(value, neg_direction, connection, mark)
        return list(connection)

    def _find_connection_in_one_direction(
            self,
            from_index: int,
            direction: Direction,
            connection: deque[int],
            mark: int
    ) -> deque[int]:
        search_queue = deque([from_index])
        while len(search_queue):
            search_index = search_queue.pop()
            neighbor_index = self.get_neighbor_index(search_index, direction)
            if neighbor_index and self.board[neighbor_index] == mark:
                search_queue.append(neighbor_index)
                if direction.is_positive():
                    connection.append(neighbor_index)
                else:
                    connection.appendleft(neighbor_index)

        return connection

    def get_neighbor_index(self, index: int, direction: Direction) -> int | None:
        row, col = self.get_row_and_col_at(index)
        if direction == Direction.up and row > 0:
            return self.get_index_at(row - 1, col)
        if direction == Direction.up_right and row > 0 and col < self.columns - 1:
            return self.get_index_at(row - 1, col + 1)
        if direction == Direction.right and col < self.columns - 1:
            return self.get_index_at(row, col + 1)
        if direction == Direction.down_right and col < self.columns - 1 and row < self.rows - 1:
            return self.get_index_at(row + 1, col + 1)
        if direction == Direction.down and row < self.rows - 1:
            return self.get_index_at(row + 1, col)
        if direction == Direction.down_left and row < self.rows - 1 and col > 0:
            return self.get_index_at(row + 1, col - 1)
        if direction == Direction.left and col > 0:
            return self.get_index_at(row, col - 1)
        if direction == Direction.up_left and col > 0 and row > 0:
            return self.get_index_at(row - 1, col - 1)
        return None


class BoardTest(unittest.TestCase):
    def get_indexed_default_board(self) -> Board:
        return Board(list(range(42)), 7, 6)

    def test_get_value_at(self):
        board = Board.parse_from_nested_list(
            [[0, 0, 0],  # [[0, 1, 2]
             [1, 0, 0],  # [3, 4, 5]
             [0, 0, 2]]  # [6, 7, 8]]
        )
        self.assertEqual(board.get_value_at(1, 0), 1)
        self.assertEqual(board.get_value_at(0, 0), 0)
        self.assertEqual(board.get_value_at(2, 2), 2)

    def test_get_row_and_column_at(self):
        board = Board.parse_from_nested_list(
            [[0, 0, 0],  # [[0, 1, 2]
             [1, 0, 0],  # [3, 4, 5]
             [0, 0, 2]]  # [6, 7, 8]]
        )
        self.assertEqual(board.get_row_and_col_at(3), (1, 0))
        self.assertEqual(board.get_row_and_col_at(0), (0, 0))
        self.assertEqual(board.get_row_and_col_at(8), (2, 2))

    def test_get_index_at(self):
        board = Board.parse_from_nested_list(
            [[0, 0, 0],  # [[0, 1, 2]
             [1, 0, 0],  # [3, 4, 5]
             [0, 0, 2]]  # [6, 7, 8]]
        )
        self.assertEqual(board.get_index_at(1, 0), 3)
        self.assertEqual(board.get_index_at(0, 0), 0)
        self.assertEqual(board.get_index_at(2, 2), 8)

    def test_get_connections(self):
        board_with_connections = Board.parse_from_nested_list(
            [[0, 0, 0, 0],  # [[00, 01, 02, 03],
             [1, 1, 2, 0],  # [04, 05, 06, 07],
             [1, 2, 1, 2],  # [08, 09, 10, 11],
             [1, 2, 2, 1]]  # [12, 13, 14, 15]]
        )
        connections_mark_1 = {
            Axis.vertical: [[4, 8, 12]],
            Axis.horizontal: [[4, 5]],
            Axis.upwards_diagonal: [[8, 5]],
            Axis.downwards_diagonal: [[5, 10, 15]]
        }

        connections_mark_2 = {
            Axis.horizontal: [[13, 14]],
            Axis.vertical: [[9, 13]],
            Axis.upwards_diagonal: [[9, 6], [14, 11]],
            Axis.downwards_diagonal: [[9, 14], [6, 11]]
        }

        for axis in Axis.all_axes():
            self.assertEqual(
                sorted(connections_mark_1[axis]),
                sorted(board_with_connections.find_connections(1)[axis])
            )
            self.assertEqual(
                sorted(connections_mark_2[axis]),
                sorted(board_with_connections.find_connections(2)[axis])
            )

    def test_parse_board(self):
        board = [[0, 0, 0],
                 [1, 0, 2],
                 [1, 1, 2]]
        expected = Board([0, 0, 0, 1, 0, 2, 1, 1, 2], 3, 3)
        actual = Board.parse_from_nested_list(board)
        self.assertEqual(expected, actual)

    def test_get_neighbor_index(self):
        board = Board.parse_from_nested_list(
            [[0, 0, 0],  # [[0, 1, 2]
             [0, 0, 0],  # [3, 4, 5]
             [0, 0, 0]]  # [6, 7, 8]]
        )
        self.assertEqual(1, board.get_neighbor_index(4, Direction.up))
        self.assertEqual(2, board.get_neighbor_index(4, Direction.up_right))
        self.assertEqual(5, board.get_neighbor_index(4, Direction.right))
        self.assertEqual(8, board.get_neighbor_index(4, Direction.down_right))
        self.assertEqual(7, board.get_neighbor_index(4, Direction.down))
        self.assertEqual(6, board.get_neighbor_index(4, Direction.down_left))
        self.assertEqual(3, board.get_neighbor_index(4, Direction.left))
        self.assertEqual(0, board.get_neighbor_index(4, Direction.up_left))

        self.assertEqual(None, board.get_neighbor_index(1, Direction.up))
        self.assertEqual(None, board.get_neighbor_index(2, Direction.up_right))
        self.assertEqual(None, board.get_neighbor_index(5, Direction.right))
        self.assertEqual(None, board.get_neighbor_index(8, Direction.down_right))
        self.assertEqual(None, board.get_neighbor_index(7, Direction.down))
        self.assertEqual(None, board.get_neighbor_index(6, Direction.down_left))
        self.assertEqual(None, board.get_neighbor_index(3, Direction.left))
        self.assertEqual(None, board.get_neighbor_index(0, Direction.up_left))

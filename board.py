import unittest
from enum import Enum
from collections import deque

import attr

from funcs import update_group


class Direction(Enum):
    """
    Represents one of eight possible directions you can traverse on the grid
    """
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
    """
    Represents one of 4 axes that opposite directions lie on
    """
    vertical = 0
    horizontal = 1
    upwards_diagonal = 2
    downwards_diagonal = 3

    @property
    def positive_direction(self) -> Direction:
        directions = {
            Axis.vertical: Direction.down,
            Axis.horizontal: Direction.right,
            Axis.upwards_diagonal: Direction.up_right,
            Axis.downwards_diagonal: Direction.down_right
        }
        return directions[self]

    @property
    def negative_direction(self) -> Direction:
        directions = {
            Axis.vertical: Direction.up,
            Axis.horizontal: Direction.left,
            Axis.upwards_diagonal: Direction.down_left,
            Axis.downwards_diagonal: Direction.up_left
        }
        return directions[self]

    @staticmethod
    def all_axes() -> list['Axis']:
        return [Axis.vertical, Axis.horizontal, Axis.upwards_diagonal, Axis.downwards_diagonal]


def _parse_board(nested_list: list[list[int]]) -> 'Board':
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


class TestParseBoard(unittest.TestCase):
    def test(self):
        board = [[0, 0, 0],
                 [1, 0, 2],
                 [1, 1, 2]]
        expected = Board([0, 0, 0, 1, 0, 2, 1, 1, 2], 3, 3)
        actual = _parse_board(board)
        self.assertEqual(expected, actual)


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

    def get_value_at(self, row: int, col: int) -> int:
        return self.board[self.get_index_at(row, col)]

    def get_index_at(self, row: int, col: int) -> int:
        return row * self.rows + col

    def get_row_and_col_at(self, index: int) -> tuple[int, int]:
        row = int(index / self.rows)
        column = index - row * self.rows
        return row, column

    def get_board_value(self, mark: int) -> float:
        assert mark in [1, 2], f'invalid value for mark: {mark}'

        value_table = {
            1: 0 / 6,
            2: 2 / 6,
            3: 4 / 6,
            4: 6 / 6
        }
        grouped_connections = _find_connections(self, mark)
        value = 0
        for axis, connections in grouped_connections.items():
            for connection in connections:
                value += value_table[len(connection)]

        blocked_value_table = {
            1: 1 / 6,
            2: 3 / 6,
            3: 5 / 6
        }
        grouped_blocked_connections = _find_blocked_opponent_connections(self, mark)
        for axis, connections in grouped_blocked_connections.items():
            for connection in connections:
                value += blocked_value_table[len(connection)]

        return value


class TestBoard(unittest.TestCase):
    def test_get_value_at(self):
        board = _parse_board(
            [[0, 0, 0],  # [[0, 1, 2]
             [1, 0, 0],  # [3, 4, 5]
             [0, 0, 2]]  # [6, 7, 8]]
        )
        self.assertEqual(board.get_value_at(1, 0), 1)
        self.assertEqual(board.get_value_at(0, 0), 0)
        self.assertEqual(board.get_value_at(2, 2), 2)

    def test_get_row_and_column_at(self):
        board = _parse_board(
            [[0, 0, 0],  # [[0, 1, 2]
             [1, 0, 0],  # [3, 4, 5]
             [0, 0, 2]]  # [6, 7, 8]]
        )
        self.assertEqual(board.get_row_and_col_at(3), (1, 0))
        self.assertEqual(board.get_row_and_col_at(0), (0, 0))
        self.assertEqual(board.get_row_and_col_at(8), (2, 2))

    def test_get_index_at(self):
        board = _parse_board(
            [[0, 0, 0],  # [[0, 1, 2]
             [1, 0, 0],  # [3, 4, 5]
             [0, 0, 2]]  # [6, 7, 8]]
        )
        self.assertEqual(board.get_index_at(1, 0), 3)
        self.assertEqual(board.get_index_at(0, 0), 0)
        self.assertEqual(board.get_index_at(2, 2), 8)

    def test_get_board_value(self):
        board = _parse_board(
            [[0, 0, 0],  # [[0, 1, 2]
             [1, 0, 0],  # [3, 4, 5]
             [1, 2, 2]]  # [6, 7, 8]]
        )
        # own: {vertical: [3, 6]} blocked: {horizontal: [7, 8], downwards_diagonal: [7]}
        self.assertEqual(2 / 6 + 3 / 6 + 1 / 6, board.get_board_value(1))
        # own: {horizontal: [7, 8]} blocked: {vertical: [6], downwards_diagonal: [3]}
        self.assertEqual(2 / 6 + 1 / 6 + 1 / 6, board.get_board_value(2))


def _find_blocked_opponent_connections(board: Board, mark: int) -> dict[Axis, list[list[int]]]:
    def _connection_is_blocked(board: Board, connection: list[int], axis: Axis, mark: int) \
            -> bool:
        """returns if the connection of the opponent of the player specified with mark
        is blocked by at least one bead from the player specified with mark"""
        positive_neighbor_index = _get_neighbor_index(board, connection[-1], axis.positive_direction)
        negative_neighbor_index = _get_neighbor_index(board, connection[0], axis.negative_direction)

        if positive_neighbor_index is None and negative_neighbor_index is None:
            return False
        if positive_neighbor_index is None:
            return board.board[negative_neighbor_index] == mark
        if negative_neighbor_index is None:
            return board.board[positive_neighbor_index] == mark
        return board.board[positive_neighbor_index] == mark and board.board[negative_neighbor_index] == mark

    opponent_mark = 2 if mark == 1 else 1
    opponent_connections = _find_connections(board, opponent_mark)
    blocked_opponent_connections = {
        Axis.vertical: [],
        Axis.horizontal: [],
        Axis.upwards_diagonal: [],
        Axis.downwards_diagonal: []
    }
    for axis, connections in opponent_connections.items():
        for connection in connections:
            if _connection_is_blocked(board, connection, axis, mark):
                blocked_opponent_connections[axis].append(connection)

    return blocked_opponent_connections


class TestFindBlockedConnections(unittest.TestCase):
    def test(self):
        board_with_blocked_connections = _parse_board(
            [[0, 0, 0, 0],  # [[00, 01, 02, 03],
             [1, 1, 2, 2],  # [04, 05, 06, 07],
             [1, 2, 1, 2],  # [08, 09, 10, 11],
             [1, 2, 2, 1]]  # [12, 13, 14, 15]]
        )
        blocked_connections = {
            Axis.vertical: [[9, 13], [14]],
            Axis.horizontal: [[6, 7], [13, 14], [9], [11]],
            Axis.upwards_diagonal: [[13], [7]],
            Axis.downwards_diagonal: [[9, 14], [13]]
        }
        actual = _find_blocked_opponent_connections(board_with_blocked_connections, 1)
        for axis in Axis.all_axes():
            self.assertEqual(sorted(blocked_connections[axis]), sorted(actual[axis]))


def _find_connections(board: Board, mark: int) -> dict[Axis, list[list[int]]]:
    """
    returns a list of indexes which are connections of a player (specified
    by mark), grouped by axis
    """

    def _find_connection_on_axis(board: Board, axis: Axis, value: int, mark: int) \
            -> list[int]:
        connection = deque([value])
        connection = _find_connection_in_one_direction(board, value, axis.positive_direction, connection, mark)
        connection = _find_connection_in_one_direction(board, value, axis.negative_direction, connection, mark)
        return list(connection)

    def _find_connection_in_one_direction(
            board: Board,
            from_index: int,
            direction: Direction,
            connection: deque[int],
            mark: int
    ) -> deque[int]:
        search_queue = deque([from_index])
        while len(search_queue):
            search_index = search_queue.pop()
            neighbor_index = _get_neighbor_index(board, search_index, direction)
            if neighbor_index and board.board[neighbor_index] == mark:
                search_queue.append(neighbor_index)
                if direction.is_positive():
                    connection.append(neighbor_index)
                else:
                    connection.appendleft(neighbor_index)

        return connection

    connections = {
        Axis.vertical: [],
        Axis.horizontal: [],
        Axis.upwards_diagonal: [],
        Axis.downwards_diagonal: []
    }
    for value in range(len(board.board)):
        if board.board[value] != mark:
            continue

        for axis in Axis.all_axes():
            connection = _find_connection_on_axis(board, axis, value, mark)
            update_group(connections, axis, connection)

    return connections


class TestFindConnections(unittest.TestCase):
    def test(self):
        board_with_connections = _parse_board(
            [[0, 0, 0, 0],  # [[00, 01, 02, 03],
             [1, 1, 2, 0],  # [04, 05, 06, 07],
             [1, 2, 1, 2],  # [08, 09, 10, 11],
             [1, 2, 2, 1]]  # [12, 13, 14, 15]]
        )
        connections_mark_1 = {
            Axis.vertical: [[4, 8, 12], [5], [10], [15]],
            Axis.horizontal: [[4, 5], [8], [10], [12], [15]],
            Axis.upwards_diagonal: [[8, 5], [4], [12], [10], [15]],
            Axis.downwards_diagonal: [[5, 10, 15], [4], [8], [12]]
        }

        connections_mark_2 = {
            Axis.horizontal: [[13, 14], [6], [9], [11]],
            Axis.vertical: [[9, 13], [6], [14], [11]],
            Axis.upwards_diagonal: [[9, 6], [14, 11], [13]],
            Axis.downwards_diagonal: [[9, 14], [6, 11], [13]]
        }

        for axis in Axis.all_axes():
            self.assertEqual(
                sorted(connections_mark_1[axis]),
                sorted(_find_connections(board_with_connections, 1)[axis])
            )
            self.assertEqual(
                sorted(connections_mark_2[axis]),
                sorted(_find_connections(board_with_connections, 2)[axis])
            )


def _get_neighbor_index(board: Board, index: int, direction: Direction) -> int | None:
    row, col = board.get_row_and_col_at(index)
    if direction == Direction.up and row > 0:
        return board.get_index_at(row - 1, col)
    if direction == Direction.up_right and row > 0 and col < board.columns - 1:
        return board.get_index_at(row - 1, col + 1)
    if direction == Direction.right and col < board.columns - 1:
        return board.get_index_at(row, col + 1)
    if direction == Direction.down_right and col < board.columns - 1 and row < board.rows - 1:
        return board.get_index_at(row + 1, col + 1)
    if direction == Direction.down and row < board.rows - 1:
        return board.get_index_at(row + 1, col)
    if direction == Direction.down_left and row < board.rows - 1 and col > 0:
        return board.get_index_at(row + 1, col - 1)
    if direction == Direction.left and col > 0:
        return board.get_index_at(row, col - 1)
    if direction == Direction.up_left and col > 0 and row > 0:
        return board.get_index_at(row - 1, col - 1)
    return None


class TestGetNeighborIndex(unittest.TestCase):
    def test(self):
        board = _parse_board(
            [[0, 0, 0],  # [[0, 1, 2]
             [0, 0, 0],  # [3, 4, 5]
             [0, 0, 0]]  # [6, 7, 8]]
        )
        self.assertEqual(1, _get_neighbor_index(board, 4, Direction.up))
        self.assertEqual(2, _get_neighbor_index(board, 4, Direction.up_right))
        self.assertEqual(5, _get_neighbor_index(board, 4, Direction.right))
        self.assertEqual(8, _get_neighbor_index(board, 4, Direction.down_right))
        self.assertEqual(7, _get_neighbor_index(board, 4, Direction.down))
        self.assertEqual(6, _get_neighbor_index(board, 4, Direction.down_left))
        self.assertEqual(3, _get_neighbor_index(board, 4, Direction.left))
        self.assertEqual(0, _get_neighbor_index(board, 4, Direction.up_left))

        self.assertEqual(None, _get_neighbor_index(board, 1, Direction.up))
        self.assertEqual(None, _get_neighbor_index(board, 2, Direction.up_right))
        self.assertEqual(None, _get_neighbor_index(board, 5, Direction.right))
        self.assertEqual(None, _get_neighbor_index(board, 8, Direction.down_right))
        self.assertEqual(None, _get_neighbor_index(board, 7, Direction.down))
        self.assertEqual(None, _get_neighbor_index(board, 6, Direction.down_left))
        self.assertEqual(None, _get_neighbor_index(board, 3, Direction.left))
        self.assertEqual(None, _get_neighbor_index(board, 0, Direction.up_left))

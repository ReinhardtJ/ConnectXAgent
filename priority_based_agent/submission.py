# standalone module of the priority-based agent
import copy
from abc import abstractmethod, ABC
from dataclasses import dataclass
from enum import Enum


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


@dataclass
class FourTuple:
    zero: int
    one: int
    two: int
    three: int

    def __getitem__(self, index: int):
        if index == 0:
            return self.zero
        elif index == 1:
            return self.one
        elif index == 2:
            return self.two
        elif index == 3:
            return self.three
        else:
            raise KeyError('key must be between 0 and 3')

    def __setitem__(self, index: int, value: int):
        if index == 0:
            self.zero = value
        elif index == 1:
            self.one = value
        elif index == 2:
            self.two = value
        elif index == 3:
            self.three = value
        else:
            raise KeyError('key must be between 0 and 3')

    def __hash__(self):
        return hash(self.zero) ^ hash(self.one) ^ hash(self.two) ^ hash(self.three)

    def __str__(self):
        return f'4-tuple({self.zero}, {self.one}, {self.two}, {self.three})'

    def __contains__(self, item: int):
        return item in [self.zero, self.one, self.two, self.three]


def invert_4_tuple(t: FourTuple) -> FourTuple:
    def invert_number(n: int):
        if n == 0: return 0
        if n == 1: return 2
        if n == 2: return 1

    return FourTuple(
        invert_number(t.zero),
        invert_number(t.one),
        invert_number(t.two),
        invert_number(t.three)
    )


def get_value_at(board: Board, row: int, col: int) -> int:
    return board.board[get_index_at(board, row, col)]


def get_index_at(board: Board, row: int, col: int) -> int:
    return row * board.columns + col


def get_row_and_col_at(board: Board, index: int) -> tuple[int, int]:
    row = index // board.columns
    column = index % board.columns
    return row, column


class _Direction(ABC):
    """
    Represents one of eight possible directions you can traverse on the grid
    """

    @staticmethod
    @abstractmethod
    def is_positive():
        pass

    @staticmethod
    @abstractmethod
    def get_neighbor_index(board: Board, index: int):
        pass


class Up(_Direction):

    @staticmethod
    def is_positive():
        return False

    @staticmethod
    def get_neighbor_index(board: Board, index: int):
        row, col = get_row_and_col_at(board, index)
        if row > 0:
            return get_index_at(board, row - 1, col)
        return None


class UpRight(_Direction):

    @staticmethod
    def is_positive():
        return True

    @staticmethod
    def get_neighbor_index(board: Board, index: int):
        row, col = get_row_and_col_at(board, index)
        if row > 0 and col < board.columns - 1:
            return get_index_at(board, row - 1, col + 1)
        return None


class Right(_Direction):
    @staticmethod
    def is_positive():
        return True

    @staticmethod
    def get_neighbor_index(board: Board, index: int):
        row, col = get_row_and_col_at(board, index)
        if col < board.columns - 1:
            return get_index_at(board, row, col + 1)
        return None


class DownRight(_Direction):

    @staticmethod
    def is_positive():
        return True

    @staticmethod
    def get_neighbor_index(board: Board, index: int):
        row, col = get_row_and_col_at(board, index)
        if col < board.columns - 1 and row < board.rows - 1:
            return get_index_at(board, row + 1, col + 1)
        return None


class Down(_Direction):
    @staticmethod
    def is_positive():
        return True

    @staticmethod
    def get_neighbor_index(board: Board, index: int):
        row, col = get_row_and_col_at(board, index)
        if row < board.rows - 1:
            return get_index_at(board, row + 1, col)
        return None


class DownLeft(_Direction):
    @staticmethod
    def is_positive():
        return False

    @staticmethod
    def get_neighbor_index(board: Board, index: int):
        row, col = get_row_and_col_at(board, index)
        if row < board.rows - 1 and col > 0:
            return get_index_at(board, row + 1, col - 1)
        return None


class Left(_Direction):
    @staticmethod
    def is_positive():
        return False

    @staticmethod
    def get_neighbor_index(board: Board, index: int):
        row, col = get_row_and_col_at(board, index)
        if col > 0:
            return get_index_at(board, row, col - 1)
        return None


class UpLeft(_Direction):
    @staticmethod
    def is_positive():
        return False

    @staticmethod
    def get_neighbor_index(board: Board, index: int):
        row, col = get_row_and_col_at(board, index)
        if col > 0 and row > 0:
            return get_index_at(board, row - 1, col - 1)
        return None


class _Axis(ABC):
    """
    Represents one of 4 axes that opposite directions lie on
    """

    @staticmethod
    @abstractmethod
    def positive_direction() -> type[_Direction]:
        pass

    @staticmethod
    @abstractmethod
    def negative_direction() -> type[_Direction]:
        pass


def all_axes() -> list[type['_Axis']]:
    return [Vertical, Horizontal, UpwardsDiagonal, DownwardsDiagonal]


class Vertical(_Axis):
    @staticmethod
    def positive_direction() -> type[_Direction]:
        return Down

    @staticmethod
    def negative_direction() -> type[_Direction]:
        return Up


class Horizontal(_Axis):
    @staticmethod
    def positive_direction() -> type[_Direction]:
        return Right

    @staticmethod
    def negative_direction() -> type[_Direction]:
        return Left


class UpwardsDiagonal(_Axis):

    @staticmethod
    def positive_direction() -> type[_Direction]:
        return UpRight

    @staticmethod
    def negative_direction() -> type[_Direction]:
        return DownLeft


class DownwardsDiagonal(_Axis):

    @staticmethod
    def positive_direction() -> type[_Direction]:
        return DownRight

    @staticmethod
    def negative_direction() -> type[_Direction]:
        return UpLeft


TAxis = type[_Axis]
TDirection = type[_Direction]


class Priority(int, Enum):
    connect_4 = 1
    prevent_4 = 2
    connect_3 = 3
    prevent_3 = 4
    connect_2 = 5
    prevent_2 = 6
    connect_1 = 7
    none = 8


@dataclass
class PriorityResult:
    priority: Priority
    four_tuple: FourTuple
    tuple_indexes: FourTuple

    def __post_init__(self):
        assert type(self.priority) == Priority
        assert type(self.four_tuple) == FourTuple
        assert type(self.tuple_indexes) == FourTuple


def get_priority_from_4_tuple(t: FourTuple, mark: int) -> Priority:
    # if the agent is player 2, we invert the tuple. That way we can always assume
    # the agent is player 1 and leave out half of the permutations
    if mark == 2:
        t = invert_4_tuple(t)

    # we have to cover the following permutations:
    # - at least one occurrence of 1
    # - all 1s need to be next to each other in the permutation
    # of the following multiset:
    # - of cardinality 4
    # - with reoccurring values
    # - values in [0, 1, 2]
    priority_map = {
        FourTuple(0, 0, 0, 0): Priority.none,
        # just one 1
        FourTuple(0, 0, 0, 1): Priority.connect_1,
        FourTuple(0, 0, 1, 0): Priority.connect_1,
        FourTuple(0, 1, 0, 0): Priority.connect_1,
        FourTuple(1, 0, 0, 0): Priority.connect_1,

        # one 1, one 2
        FourTuple(0, 0, 0, 1): Priority.connect_1,  # 1 at pos 4
        FourTuple(0, 0, 2, 1): Priority.prevent_2,
        FourTuple(0, 2, 0, 1): Priority.connect_1,
        FourTuple(2, 0, 0, 1): Priority.connect_1,

        FourTuple(0, 0, 1, 2): Priority.prevent_2,  # 1 at pos 3
        FourTuple(0, 2, 1, 0): Priority.connect_1,
        FourTuple(2, 0, 1, 0): Priority.connect_1,

        FourTuple(0, 1, 0, 2): Priority.connect_1,  # 1 at pos 2
        FourTuple(0, 1, 2, 0): Priority.connect_1,
        FourTuple(2, 1, 0, 0): Priority.prevent_2,

        FourTuple(1, 0, 0, 2): Priority.connect_1,  # 1 at pos 1
        FourTuple(1, 0, 2, 0): Priority.connect_1,
        FourTuple(1, 2, 0, 0): Priority.none,

        # one 1, two 2s
        FourTuple(0, 2, 2, 1): Priority.none,  # 1 at pos 4
        FourTuple(2, 0, 2, 1): Priority.none,
        FourTuple(2, 2, 0, 1): Priority.connect_1,

        FourTuple(0, 2, 1, 2): Priority.prevent_3,  # 1 at pos 3
        FourTuple(2, 0, 1, 2): Priority.prevent_2,
        FourTuple(2, 2, 1, 0): Priority.prevent_3,

        FourTuple(0, 1, 2, 2): Priority.prevent_3,  # 1 at pos 2
        FourTuple(2, 1, 0, 2): Priority.prevent_2,
        FourTuple(2, 1, 2, 0): Priority.prevent_3,

        FourTuple(1, 0, 2, 2): Priority.connect_1,  # 1 at pos 1
        FourTuple(1, 2, 0, 2): Priority.prevent_2,
        FourTuple(1, 2, 2, 0): Priority.prevent_3,

        # one 1, three 2s
        FourTuple(2, 2, 2, 1): Priority.prevent_4,
        FourTuple(2, 2, 1, 2): Priority.prevent_4,
        FourTuple(2, 1, 2, 2): Priority.prevent_4,
        FourTuple(1, 2, 2, 2): Priority.prevent_4,

        # just two 1s
        FourTuple(0, 0, 1, 1): Priority.connect_2,
        FourTuple(0, 1, 0, 1): Priority.connect_1,
        FourTuple(0, 1, 1, 0): Priority.connect_2,
        FourTuple(1, 0, 0, 1): Priority.connect_1,
        FourTuple(1, 0, 1, 0): Priority.connect_1,
        FourTuple(1, 1, 0, 0): Priority.connect_2,

        # two 1s, one 2
        FourTuple(0, 2, 1, 1): Priority.none,
        FourTuple(2, 0, 1, 1): Priority.connect_2,

        FourTuple(0, 1, 2, 1): Priority.prevent_2,
        FourTuple(2, 1, 0, 1): Priority.prevent_2,

        FourTuple(0, 1, 1, 2): Priority.connect_2,
        FourTuple(2, 1, 1, 0): Priority.connect_2,

        FourTuple(1, 0, 1, 2): Priority.prevent_2,
        FourTuple(1, 2, 1, 0): Priority.prevent_2,

        FourTuple(1, 1, 0, 2): Priority.connect_2,
        FourTuple(1, 1, 2, 0): Priority.connect_2,

        # two 1s, two 2s
        FourTuple(2, 2, 1, 1): Priority.prevent_3,
        FourTuple(2, 1, 2, 1): Priority.prevent_3,
        FourTuple(2, 1, 1, 2): Priority.none,
        FourTuple(1, 2, 1, 2): Priority.prevent_3,
        FourTuple(1, 1, 2, 2): Priority.prevent_3,

        # just three 1s
        FourTuple(0, 1, 1, 1): Priority.connect_3,
        FourTuple(1, 0, 1, 1): Priority.connect_2,
        FourTuple(1, 1, 0, 1): Priority.connect_2,
        FourTuple(1, 1, 1, 0): Priority.connect_3,

        # three 1s, one 2
        FourTuple(2, 1, 1, 1): Priority.connect_3,
        FourTuple(1, 2, 1, 1): Priority.connect_2,
        FourTuple(1, 1, 2, 1): Priority.connect_2,
        FourTuple(1, 1, 1, 2): Priority.connect_3,

        # 4 ones
        FourTuple(1, 1, 1, 1): Priority.connect_4,
    }
    other_t = invert_4_tuple(t)
    if t in priority_map:
        return priority_map[t]
    if other_t in priority_map:
        return Priority.none
    raise Exception(f'neither {t} nor {other_t} in priority map')


def get_4_tuple_from_indexes(board: Board, indexes: FourTuple) -> FourTuple:
    return FourTuple(
        -1 if indexes.zero == -1 else board.board[indexes.zero],
        -1 if indexes.one == -1 else board.board[indexes.one],
        -1 if indexes.two == -1 else board.board[indexes.two],
        -1 if indexes.three == -1 else board.board[indexes.three],
    )


def get_4_tuple_from_index(board: Board, index: int, axis: TAxis, mark: int) -> PriorityResult:
    """
    returns None when no tuple can be established from that index
    (e.g. at the edge of the board)
    """
    direction = axis.positive_direction()  # we only need to check in one direction
    tuple_indexes = FourTuple(index, -1, -1, -1)
    for i in range(1, 4):
        next_index = direction.get_neighbor_index(board, tuple_indexes[i - 1])
        if next_index is None:
            four_tuple = get_4_tuple_from_indexes(board, tuple_indexes)
            priority = Priority.none
            return PriorityResult(priority, four_tuple, tuple_indexes)
        tuple_indexes[i] = next_index

    four_tuple = get_4_tuple_from_indexes(board, tuple_indexes)
    priority = get_priority_from_4_tuple(four_tuple, mark)
    return PriorityResult(priority, four_tuple, tuple_indexes)


def get_best_4_tuple(board: Board, with_index: int, mark: int) -> PriorityResult:
    current_best_result = PriorityResult(Priority.none, FourTuple(-1, -1, -1, -1), FourTuple(-1, -1, -1, -1))
    for axis in all_axes():
        print(f'axis: {axis}')
        for index in range(len(board.board)):
            result = get_4_tuple_from_index(board, index, axis, mark)
            # skip when the currently examined tuple does not contain the newly added piece
            if with_index not in result.tuple_indexes: continue
            # skip when the currently examined tuple has a null-priority
            if result.priority == Priority.none: continue

            # early-return when we can connect 4
            if result.priority == Priority.connect_4:
                print(f'found winning 4-tuple {result.four_tuple} at indexes {result.tuple_indexes}')
                return result

            # track the best tuple we found so far
            if result.priority < current_best_result.priority:
                print(
                    f'{result.four_tuple} at indexes {result.tuple_indexes} wins against {current_best_result.four_tuple} at indexes {current_best_result.tuple_indexes}')
                current_best_result = result

    return current_best_result


@dataclass
class Observation:
    board: list[int]  # flattened rows x cols, starting top left
    step: int
    mark: int  # the label of our pieces


@dataclass
class Configuration:
    columns: int
    rows: int


def add_piece(board: Board, mark: int, column: int) -> int:
    """
    returns the board index of the piece added
    mutates the board
    """
    assert get_value_at(board, 0, column) == 0, 'column is full'

    # search for any pieces in this column, and place our piece on top of it
    for row in range(board.rows):
        first_piece_in_column = get_value_at(board, row, column)
        if first_piece_in_column != 0:
            index_above_piece = get_index_at(board, row - 1, column)
            board.board[index_above_piece] = mark
            return index_above_piece
    # otherwise, place it at the bottom of the column
    bottom_index = get_index_at(board, board.rows - 1, column)
    board.board[bottom_index] = mark
    return bottom_index


def act(observation: Observation, configuration: Configuration):
    print(f'state from [{observation.step + 1}] -> [{observation.step + 2}]\n')
    board = Board(observation.board, configuration.rows, configuration.columns)
    our_mark = observation.mark

    current_best_priority = Priority.none
    current_best_col = -1
    for column in range(board.columns):
        print(f'column: {column}')
        next_state_board = copy.deepcopy(board)
        try:
            added_piece_index = add_piece(next_state_board, our_mark, column)
        except AssertionError:
            continue
        result = get_best_4_tuple(next_state_board, added_piece_index, our_mark)
        if result.priority == Priority.none:
            continue
        if result.priority == Priority.connect_4:
            return column
        if result.priority < current_best_priority:
            current_best_priority = result.priority
            current_best_col = column
        print('')
    print('-------------------\n')
    return current_best_col

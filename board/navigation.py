from abc import ABC, abstractmethod

from board.board_class import Board


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

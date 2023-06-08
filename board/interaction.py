from board.board_class import Board
from board.navigation import get_value_at, get_index_at


def add_piece(board: Board, mark: int, column: int):
    """mutates the board"""
    assert get_value_at(board, 0, column) == 0, 'column is full'

    for row in range(board.rows):
        first_piece_in_column = get_value_at(board, row, column)
        if first_piece_in_column != 0:
            index_above_piece = get_index_at(board, row - 1, column)
            board.board[index_above_piece] = mark
            break

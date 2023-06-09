from board.board_class import Board
from board.navigation import get_value_at, get_index_at


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

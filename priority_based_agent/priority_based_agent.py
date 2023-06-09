import copy

from board.board_class import Board
from board.interaction import add_piece
from board.navigation import TAxis, all_axes
from data_structures import Observation, Configuration
from priority_based_agent.four_tuple import FourTuple
from priority_based_agent.priority import Priority, PriorityResult, get_priority_from_4_tuple


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
    direction = axis.positive_direction() # we only need to check in one direction
    tuple_indexes = FourTuple(index, -1, -1, -1)
    for i in range(1, 4):
        next_index = direction.get_neighbor_index(board, tuple_indexes[i-1])
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
                print(f'{result.four_tuple} at indexes {result.tuple_indexes} wins against {current_best_result.four_tuple} at indexes {current_best_result.tuple_indexes}')
                current_best_result = result

    return current_best_result

def priority_based_agent(observation: Observation, configuration: Configuration):
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

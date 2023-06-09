import copy

from board.board_class import Board
from board.interaction import add_piece
from board.value_calculation import get_board_value
from data_structures import Observation, Configuration


def random_agent(observation: Observation, configuration: Configuration):
    from random import choice
    return choice([c for c in range(configuration.columns) if observation.board[c] == 0])


def simple_reward_agent(observation: Observation, configuration: Configuration):
    board = Board(observation.board, configuration.rows, configuration.columns)
    our_mark = observation.mark
    next_state_best_board_value = 0
    next_state_best_column = -1
    for column in range(board.columns):
        next_state_board = copy.deepcopy(board)
        try:
            add_piece(next_state_board, our_mark, column)
        except AssertionError:
            continue
        next_state_value = get_board_value(next_state_board, our_mark)
        if next_state_value > next_state_best_board_value:
            next_state_best_board_value = next_state_value
            next_state_best_column = column

    # total_reward = next_state_best_board_value - board_value
    return next_state_best_column if next_state_best_column != -1 else 3



def search_based_agent(observation: Observation, configuration: Configuration):
    board = Board(observation.board, configuration.rows, configuration.columns)
    our_mark = observation.mark

    for column in range(board.columns):
        next_state_board = copy.deepcopy(board)
        try:
            add_piece(next_state_board, our_mark, column)
        except AssertionError:
            continue


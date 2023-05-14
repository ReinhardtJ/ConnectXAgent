import unittest

from data_structures import Observation, Configuration


def down(index: int) -> int | None:
    pass

def get_connections(
        board: list[int],
        mark: int
) -> list[list[int]]:
    connections = []
    board = observation.board
    # floodfill algorithm starting to search for
    for i in range(len(observation.board)):
        if board[i] != mark:
            continue
        # search for connections vertically
        vertical_connection = [i]
        search_queue = [i]
        if d := down(i):
            pass


def get_board_value(
        observation: Observation,
        configuration: Configuration,
        mark: int
):
    size_two_connections = 0
    size_three_connections = 0
    size_four_connections = 0
    blocked_size_two_connections = 0
    blocked_size_three_connections = 0
    blocked_size_four_connections = 0

    return sum([
        2 / 6 * size_two_connections,
        4 / 6 * size_three_connections,
        6 / 6 * size_four_connections,
        1 / 6 * blocked_size_two_connections,
        3 / 6 * blocked_size_three_connections,
        5 / 6 * blocked_size_four_connections,
    ])




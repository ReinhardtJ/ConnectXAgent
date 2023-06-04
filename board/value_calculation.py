from collections import deque
from typing import TypeVar

from board.board_class import Board
from board.navigation import Vertical, Horizontal, UpwardsDiagonal, DownwardsDiagonal, TAxis, \
    TDirection, all_axes

value_table = {
    1: 2**0,
    2: 2**4,
    3: 2**8,
    4: 2**12,
}

blocked_value_table = {
    1: 2**0,
    2: 2**2,
    3: 2**6,
    4: 2**10,
}

def get_board_value(board: Board, mark: int) -> float:
    assert mark in [1, 2], f'invalid value for mark: {mark}'

    grouped_connections = find_connections(board, mark)
    value_from_connections = value_from_grouped_connections(
        grouped_connections, value_table
    )

    grouped_blocked_connections = find_blocked_opponent_connections(board, mark)
    value_from_blocked_connections = value_from_grouped_connections(
        grouped_blocked_connections, blocked_value_table
    )

    return value_from_connections + value_from_blocked_connections


def value_from_grouped_connections(
        grouped_connections,
        value_table_
):
    value = 0
    for axis, connections in grouped_connections.items():
        for connection in connections:
            if len(connection) in value_table_.keys():
                value += value_table_[len(connection)]
            else:
                value += value_table_[4]

    return value



def find_blocked_opponent_connections(board: Board, mark: int) -> dict[TAxis, list[list[int]]]:
    opponent_mark = 2 if mark == 1 else 1
    opponent_connections = find_connections(board, opponent_mark)
    blocked_opponent_connections: dict[TAxis, list[list[int]]] = {
        Vertical: [],
        Horizontal: [],
        UpwardsDiagonal: [],
        DownwardsDiagonal: []
    }
    for axis, connections in opponent_connections.items():
        for connection in connections:
            if connection_is_blocked(board, connection, axis, mark):
                blocked_opponent_connections[axis].append(connection)

    return blocked_opponent_connections


def connection_is_blocked(board: Board, connection: list[int], axis: TAxis, mark: int) \
        -> bool:
    """returns if the connection of the opponent of the player specified with mark
    is blocked by at least one bead from the player specified with mark"""
    positive_neighbor_index = axis.positive_direction().get_neighbor_index(board, connection[-1])
    negative_neighbor_index = axis.negative_direction().get_neighbor_index(board, connection[0])

    if positive_neighbor_index is None and negative_neighbor_index is None:
        return False
    if positive_neighbor_index is None:
        return board.board[negative_neighbor_index] == mark
    if negative_neighbor_index is None:
        return board.board[positive_neighbor_index] == mark
    return board.board[positive_neighbor_index] == mark and board.board[negative_neighbor_index] == mark


def find_connections(board: Board, mark: int) -> dict[TAxis, list[list[int]]]:
    """
    returns a list of indexes which are connections of a player (specified
    by mark), grouped by axis
    """
    connections: dict[TAxis, list[list[int]]] = {
        Vertical: [],
        Horizontal: [],
        UpwardsDiagonal: [],
        DownwardsDiagonal: []
    }
    for value in range(len(board.board)):
        if board.board[value] != mark:
            continue

        for axis in all_axes():
            connection = _find_connection_on_axis(board, axis, value, mark)
            update_group(connections, axis, connection)

    return connections


def _find_connection_on_axis(board: Board, axis: TAxis, value: int, mark: int) \
        -> list[int]:
    connection = deque([value])
    connection = _find_connection_in_one_direction(board, value, axis.positive_direction(), connection, mark)
    connection = _find_connection_in_one_direction(board, value, axis.negative_direction(), connection, mark)
    return list(connection)

def _find_connection_in_one_direction(
        board: Board,
        from_index: int,
        direction: TDirection,
        connection: deque[int],
        mark: int
) -> deque[int]:
    search_queue = deque([from_index])
    already_seen = []
    while len(search_queue):
        search_index = search_queue.pop()
        already_seen.append(search_index)
        neighbor_index = direction.get_neighbor_index(board, search_index)
        if neighbor_index and board.board[neighbor_index] == mark:
            if neighbor_index not in already_seen:
                search_queue.append(neighbor_index)
            if direction.is_positive():
                connection.append(neighbor_index)
            else:
                connection.appendleft(neighbor_index)

    return connection


K = TypeVar('K')
V = TypeVar('V')

def update_group(grouping: dict[K, list[list[V]]], group: K, update: list[V]) \
        -> dict[K, list[list[V]]]:
    """mutates grouping"""
    assert group in grouping, f"missing group {group} in grouping {grouping} "
    values = grouping[group]
    if update not in values:
        updated_values = values + [update]
        grouping[group] = updated_values
    return grouping
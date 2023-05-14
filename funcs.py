import unittest
from typing import TypeVar

from data_structures import Observation, Configuration

K = TypeVar('K')
V = TypeVar('V')


def update_group(grouping: dict[K, list[list[V]]], group: K, update: list[V]) \
        -> dict[K, list[list[V]]]:
    assert group in grouping, f"missing group {group} in grouping {grouping} "
    values = grouping[group]
    if update not in values:
        updated_values = values + [update]
        grouping[group] = updated_values
    return grouping



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

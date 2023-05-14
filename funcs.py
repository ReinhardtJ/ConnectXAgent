from typing import TypeVar

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


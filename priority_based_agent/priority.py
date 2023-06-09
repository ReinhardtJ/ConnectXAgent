from dataclasses import dataclass
from enum import Enum

from priority_based_agent.four_tuple import FourTuple, invert_4_tuple


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
        FourTuple(0, 0, 0, 1): Priority.connect_1, # 1 at pos 4
        FourTuple(0, 0, 2, 1): Priority.prevent_2,
        FourTuple(0, 2, 0, 1): Priority.connect_1,
        FourTuple(2, 0, 0, 1): Priority.connect_1,

        FourTuple(0, 0, 1, 2): Priority.prevent_2, # 1 at pos 3
        FourTuple(0, 2, 1, 0): Priority.connect_1,
        FourTuple(2, 0, 1, 0): Priority.connect_1,

        FourTuple(0, 1, 0, 2): Priority.connect_1, # 1 at pos 2
        FourTuple(0, 1, 2, 0): Priority.connect_1,
        FourTuple(2, 1, 0, 0): Priority.prevent_2,

        FourTuple(1, 0, 0, 2): Priority.connect_1, # 1 at pos 1
        FourTuple(1, 0, 2, 0): Priority.connect_1,
        FourTuple(1, 2, 0, 0): Priority.none,

        # one 1, two 2s
        FourTuple(0, 2, 2, 1): Priority.none, # 1 at pos 4
        FourTuple(2, 0, 2, 1): Priority.none,
        FourTuple(2, 2, 0, 1): Priority.connect_1,

        FourTuple(0, 2, 1, 2): Priority.prevent_3, # 1 at pos 3
        FourTuple(2, 0, 1, 2): Priority.prevent_2,
        FourTuple(2, 2, 1, 0): Priority.prevent_3,

        FourTuple(0, 1, 2, 2): Priority.prevent_3, # 1 at pos 2
        FourTuple(2, 1, 0, 2): Priority.prevent_2,
        FourTuple(2, 1, 2, 0): Priority.prevent_3,

        FourTuple(1, 0, 2, 2): Priority.connect_1, # 1 at pos 1
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

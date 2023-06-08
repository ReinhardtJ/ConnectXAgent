from enum import Enum

import attr


class PositionState(int, Enum):
    EMPTY = 0
    ME = 1
    OPPONENT = 2


@attr.s(auto_attribs=True)
class Observation:
    board: list[int]  # flattened rows x cols, starting top left
    step: int
    mark: int  # the label of our pieces


@attr.s(auto_attribs=True)
class Configuration:
    columns: int
    rows: int

from enum import Enum
from unittest import TestCase


class Pattern(Enum):
    One: 0
    Two: 1
    Three: 2
    OneBlocked: 3
    TwoBlocked: 4
    ThreeBlocked: 5

def get_board_value(board: Board, mark: int) -> float:
    pass

def get_pattern_for_connection(connection: list[int]) -> Pattern:
    

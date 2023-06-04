import unittest

from agent import simple_reward_agent
from board.tests.helpers import parse_board
from data_structures import Observation, Configuration


class TestAgent(unittest.TestCase):
    def test_1(self):
        board = parse_board(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 2, 0, 1, 0, 0, 2]
            ]
        )
        observation = Observation(
            board.board,
            step=0,
            mark=1
        )
        configuration = Configuration(
            rows=6,
            columns=7
        )
        self.assertEqual(simple_reward_agent(observation, configuration), 3)

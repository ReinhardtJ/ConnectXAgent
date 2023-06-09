import unittest

from priority_based_agent.priority_based_agent import priority_based_agent
from board.tests.helpers import parse_board
from data_structures import Observation, Configuration


class TestPriorityBasedAgent(unittest.TestCase):
    def test_agent_tries_prevent_4_situation_1(self):
        board = parse_board(
            [
            #    0  1  2  3  4  5  6
                [0, 0, 0, 0, 0, 0, 0],  # 0   00, 01, 02, 03, 04, 05, 06,
                [0, 0, 0, 0, 0, 0, 0],  # 1   07, 08, 09, 10, 11, 12, 13,
                [0, 0, 0, 0, 0, 0, 0],  # 2   14, 15, 16, 17, 18, 19, 20,
                [0, 0, 0, 0, 0, 0, 0],  # 3   21, 22, 23, 24, 25, 26, 27,
                [0, 0, 2, 2, 0, 0, 0],  # 4   28, 29, 30, 31, 32, 33, 34,
                [0, 0, 1, 1, 1, 0, 0]   # 5   35, 36, 37, 38, 39, 40, 41
            ]
        )

        observation = Observation(board.board, 1, 2)
        configuration = Configuration(7, 6)
        result = priority_based_agent(observation, configuration)
        print(result)
        self.assertTrue(result in [1, 5])

    def test_agent_tries_prevent_4_situation_2(self):
        board = parse_board(
            [
            #    0  1  2  3  4  5  6
                [0, 0, 0, 0, 0, 0, 0],  # 0   00, 01, 02, 03, 04, 05, 06,
                [0, 0, 0, 0, 0, 0, 0],  # 1   07, 08, 09, 10, 11, 12, 13,
                [0, 0, 0, 0, 0, 0, 0],  # 2   14, 15, 16, 17, 18, 19, 20,
                [0, 0, 0, 0, 0, 0, 0],  # 3   21, 22, 23, 24, 25, 26, 27,
                [0, 0, 0, 0, 0, 0, 2],  # 4   28, 29, 30, 31, 32, 33, 34,
                [0, 0, 0, 0, 0, 1, 1]   # 5   35, 36, 37, 38, 39, 40, 41
            ]
        )

        observation = Observation(board.board, 3, 2)
        configuration = Configuration(7, 6)
        result = priority_based_agent(observation, configuration)
        print(result)
        self.assertTrue(result == 4)

    def test_agent_tries_prevent_4_situation_3(self):
        board = parse_board(
            [
            #    0  1  2  3  4  5  6
                [0, 0, 0, 0, 0, 0, 0],  # 0   00, 01, 02, 03, 04, 05, 06,
                [2, 0, 0, 0, 0, 0, 0],  # 1   07, 08, 09, 10, 11, 12, 13,
                [1, 0, 0, 0, 0, 0, 0],  # 2   14, 15, 16, 17, 18, 19, 20,
                [2, 0, 0, 0, 0, 0, 0],  # 3   21, 22, 23, 24, 25, 26, 27,
                [2, 0, 0, 0, 1, 0, 0],  # 4   28, 29, 30, 31, 32, 33, 34,
                [1, 1, 2, 1, 2, 1, 0]   # 5   35, 36, 37, 38, 39, 40, 41
            ]
        )

        observation = Observation(board.board, 9, 2)
        configuration = Configuration(7, 6)
        result = priority_based_agent(observation, configuration)
        print(result)
        self.assertEqual(result, 2)
from data_structures import Observation, Configuration


def my_agent(observation: Observation, configuration: Configuration):
    from random import choice
    return choice([c for c in range(configuration.columns) if observation.board[c] == 0])

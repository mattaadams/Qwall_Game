import torch
import random
import numpy as np
from platform_game import PlatformGame


class Agent():

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0

    def get_state(self, game):
        pass

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self, state):
        pass


def train():
    agent = Agent()
    game = PlatformGame()
    total_score = 0

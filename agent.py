import torch
import random
import numpy as np
from model import Linear_QNet
from platform_game import PlatformGame
from collections import deque

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent():

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.8
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        player = game.player
        # Player coordinates, and what the player is around (can player move left,right,up,down)
        # State of the other 'coins'
        # level (static except for 'coins')
        dir_left = 0
        dir_right = 0
        dir_up = 0
        dir_down = 0

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self, state):
        self.epsilon = 100 - self.n_games

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state)
            final_move[move] = 1
        return final_move


def train():
    agent = Agent()
    game = PlatformGame()
    total_score = 0

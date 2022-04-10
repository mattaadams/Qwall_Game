import torch
import random
import numpy as np
from model import Linear_QNet
from collections import deque
from platform_game_AI import PlatformGameAI

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
        level = game.level
        tile_list = game.level.tile_list

        state = []
        # Player coordinates, and what the player is around (can player move left,right,up,down)
        # State of the other 'coins'
        # level (static except for 'coins')
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)


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
    total_score = 0
    game = PlatformGameAI()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

if __name__ == '__main__':
    train()
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
from collections import deque
import time
import random
from tqdm import tqdm
import os
from PIL import Image
import cv2
from Wall_Game_AI import WallGameAI
from model_viz import ModifiedTensorBoard

MODEL_NAME = 'ConvNet_2x256'
env = WallGameAI()
random.seed(1)
np.random.seed(1)
tf.random.set_seed(1)


class DQNAgent():
    """The DQNAgent class

    Attributes: 
        discount: Float, scaling of future rewards
        replay_memory: Integer,How many last steps to keep for model training
        min_replay_memory: Integer, Minimum number of steps in a memory to start training
        minibatch_size: Integer,How many steps (samples) to use for training
        update_freq: Integer,Terminal states (end of episodes)
        """

    def __init__(
            self, discount=0.99, replay_memory_size=50_000, min_replay_memory_size=1_000, minibatch_size=64,
            update_freq=5):

        self.model = self.create_model()
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())
        self.replay_memory = deque(maxlen=replay_memory_size)
        self.tensorboard = ModifiedTensorBoard(log_dir="logs/{}-{}".format(MODEL_NAME, int(time.time())))
        self.target_update_counter = 0
        self.update_freq = update_freq
        self.discount = discount
        self.min_replay_memory_size = min_replay_memory_size
        self.minibatch_size = minibatch_size

    def create_model(self):
        model = Sequential()

        # OBSERVATION_SPACE_VALUES = (12, 12, 3) - our 12x12 RGB image.
        model.add(Conv2D(256, (3, 3), input_shape=env.OBSERVATION_SPACE_VALUES, activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))

        model.add(Conv2D(256, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.2))

        model.add(Flatten())
        model.add(Dense(64))

        model.add(Dense(env.ACTION_SPACE_SIZE, activation='linear'))
        model.compile(loss="mse", optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])
        return model

    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    def train(self, terminal_state, step):

        if len(self.replay_memory) < self.min_replay_memory_size:
            return

        minibatch = random.sample(self.replay_memory, self.minibatch_size)

        current_states = np.array([transition[0] for transition in minibatch])/255
        current_qs_list = self.model.predict(current_states)

        new_current_states = np.array([transition[3] for transition in minibatch])/255
        future_qs_list = self.target_model.predict(new_current_states)

        X = []
        y = []

        for index, (current_state, action, reward, new_current_state, done) in enumerate(minibatch):
            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + self.discount * max_future_q
            else:
                new_q = reward

            current_qs = current_qs_list[index]
            current_qs[action] = new_q
            X.append(current_state)
            y.append(current_qs)

        self.model.fit(np.array(X)/255, np.array(y), batch_size=self.minibatch_size, verbose=0,
                       shuffle=False, callbacks=[self.tensorboard] if terminal_state else None)

        if terminal_state:
            self.target_update_counter += 1

        if self.target_update_counter > self.update_freq:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0

    def get_qs(self, state):
        return self.model.predict(np.array(state).reshape(-1, *state.shape)/255)[0]


class QTrainer():
    """Attributes: 
        agent: object
        episodes: integer
        epsilon: float
        epsilon_decay: float,
        agg_stats_freq: integer,
        max_reward: integer, threshold for maximum reward for model to save
        min_epsilon: float, minimum value for epsilon
        """

    def __init__(self, agent=DQNAgent(), episodes=10_000, epsilon=1.0, epsilon_decay=0.99975, agg_stats_freq=20,
                 max_reward=20, min_epsilon=0.001):
        self.agent = agent
        self.episodes = episodes
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.agg_stats_freq = agg_stats_freq
        self.max_reward = max_reward
        self.min_epsilon = min_epsilon

    def run(self):
        if not os.path.isdir('models'):
            os.makedirs('models')
        self.ep_rewards = [-10]
        for episode in tqdm(range(1, self.episodes + 1), ascii=True, unit='episodes'):

            # Update tensorboard step every episode
            self.agent.tensorboard.step = episode

            # Restart episode
            episode_reward = 0
            step = 1
            current_state = env.reset()
            done = False
            while not done:

                if np.random.random() > self.epsilon:
                    action = np.argmax(self.agent.get_qs(current_state))
                else:
                    action = np.random.randint(0, env.ACTION_SPACE_SIZE)

                new_state, reward, done = env.step(action)
                episode_reward += reward
                self.agent.update_replay_memory((current_state, action, reward, new_state, done))
                self.agent.train(done, step)

                current_state = new_state
                step += 1

            # save stats
            self.ep_rewards.append(episode_reward)
            if not episode % self.agg_stats_freq or episode == 1:
                self.save_stats()

            # Decay epsilon
            if self.epsilon > self.min_epsilon:
                self.epsilon *= self.epsilon_decay
                self.epsilon = max(self.min_epsilon, self.epsilon)

            if episode == self.episodes:
                agent.model.save(f'models/model{int(time.time())}.model')

    def save_stats(self):
        average_reward = sum(self.ep_rewards[-self.agg_stats_freq:])/len(self.ep_rewards[-self.agg_stats_freq:])
        min_reward = min(self.ep_rewards[-self.agg_stats_freq:])
        max_reward = max(self.ep_rewards[-self.agg_stats_freq:])
        self.agent.tensorboard.update_stats(reward_avg=average_reward, reward_min=min_reward,
                                            reward_max=max_reward, epsilon=self.epsilon)

        # Save model only when max reward is greater or equal a set value
        if max_reward >= self.max_reward:
            agent.model.save(
                f'models/{MODEL_NAME}_{average_reward:_7.2f}avg_{int(time.time())}.model')

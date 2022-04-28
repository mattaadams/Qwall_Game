import numpy as np
from tensorflow.keras.models import load_model

from Wall_Game_AI import WallGameAI

# Runs the game with a pre-trained model

model_name_ = "model1650751087.model"
model = load_model(f'../models/{model_name_}')

game = WallGameAI()

done = False
state = game.reset()
while not done:
    pred = model.predict(np.array(state).reshape(-1, *state.shape)/255)[0]
    action = np.argmax(pred)
    state, reward, done = game.step(action)

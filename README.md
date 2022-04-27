# Q-Wall Game


## About

This project contains code to train a model that automatically avoids the wall obstacles by using pixels as the input. 
  

## Model Performance  


First Episode           |  Last Episode (10,000)
:-------------------------:|:-------------------------:
![First Episode](https://github.com/mattaadams/RL_Wall_Game/blob/master/assets/Wall_Game_Ep0.gif)  |  ![Last Episode](https://github.com/mattaadams/RL_Wall_Game/blob/master/assets/Wall_Game.gif)



Max Reward        | Loss
:-------------------------:|:-------------------------:
![First Episode](https://github.com/mattaadams/RL_Wall_Game/blob/master/assets/Max_Reward.png)  |  ![Last Episode](https://github.com/mattaadams/RL_Wall_Game/blob/master/assets/Loss.png)





## Inputs, Outputs, and Actions
  
### Inputs
 - Environment State - 12x12 RGB Image of environment

### Outputs

### Actions
 -  Up
 -  Down
 -  Do Nothing

## Rewards/Punishments
 
 -  Pass through Wall `+ 1` 
 -  Hit Wall  `- 10`
 -  Anything Else `0`
  

## Model and Policy


<img src="[drawing.jpg](https://github.com/mattaadams/RL_Wall_Game/blob/master/assets/Epsilon.png)" alt="Epsilon" width="400"/>


# Usage

## Libraries Required

- PyGame 2.1.2
- Tensorflow 2.8.0
- OpenCV2 4.4.0
- Pillow 8.0.1



# Q-Wall Game


## About

This project contains code to train a model that automatically avoids the wall obstacles by using pixels as the input. 
  

## Model Performance  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
First Episode &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
Last Episode (10,000)



<p float="left">
<img src="https://github.com/mattaadams/RL_Wall_Game/blob/master/assets/Wall_Game_Ep0.gif" align="center" height="200" width="200" >
<img src="https://github.com/mattaadams/RL_Wall_Game/blob/master/assets/Wall_Game.gif" align="center" height="200" width="200" >
</p>


Solarized dark             |  Solarized Ocean
:-------------------------:|:-------------------------:
![](https://github.com/mattaadams/RL_Wall_Game/blob/master/assets/Wall_Game.gif)  |  ![](https://github.com/mattaadams/RL_Wall_Game/blob/master/assets/Wall_Game.gif)
Max Reward


<a href="url"><img src="https://github.com/mattaadams/RL_Wall_Game/blob/master/assets/Max_Reward.png" align="center" width="300" ></a>

Loss
<a href="url"><img src="https://github.com/mattaadams/RL_Wall_Game/blob/master/assets/Loss.png" align="center" width="300" ></a>

Epsilon 
<a href="url"><img src="https://github.com/mattaadams/RL_Wall_Game/blob/master/assets/Epsilon.png" align="center" width="300" ></a>


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
  

## Model 
 
 -  


## Libraries Required

- PyGame 2.1.2
- Tensorflow 2.8.0
- OpenCV2 4.4.0
- Pillow 8.0.1



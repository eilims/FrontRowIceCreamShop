import sys
import os
path = "{}/simulator".format(os.getcwd())
sys.path.append(path)

from simulator import simulator
from gridworld import GridWorld
import numpy as np

initial_state = np.array([0,0])
gw = GridWorld()

# print(gw.get_observation(initial_state))
# print(gw.get_harmonic_mean(initial_state))
# print(gw.get_next_state(initial_state, act1))
# print(gw.get_next_state(initial_state, act2))
observation = gw.get_observation(initial_state)
sim = simulator.Simulator(gw, initial_state)
sim.run(steps=100, render=True)
exit()



"""
import numpy as np
import random
import copy
from matplotlib import pyplot as plt

actions   = [(1,0),(-1,0),(0,1),(0,-1),(0,0)]
shops     = [(2,0), (2,2)]
obstacles = [(1,1), (1,3),(2,1),(2, 3)]

def stateChange(action, state, matMap, p_e):
  newState = state.copy()
  realAction = random.choices([], weights = [10, 1, 1], k = 14))
  
  newState[0] += realAction[0]
  newState[1] += realAction[1]
  
  return newState

def genMap(size = (5,5), shops = [], obstacles = [], negRewPos = [], negRewVal = []):
  matMap = [[0 for i in range(size[1])] for j in range(size[0])]
  for shop in shops:
    matMap[shop[0]][shop[1]] = float('inf')
  for obstacle in obstacles:
    matMap[shop[0]][shop[1]] = float('inf')
    

if __name__ == "__main__":
  
"""

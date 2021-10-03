import sys
import os
path = "{}/simulator".format(os.getcwd())
sys.path.append(path)

from simulator import environment as env
from simulator import simulator
import numpy as np
from math import ceil, floor
import random

class gridword(env.Environment):
  def __init__(self):
    self._goals = [
      np.array([2, 2])
    ]
    self._actions = [
      np.array([-1, 0]),
      np.array([1, 0]),
      np.array([0, -1]),
      np.array([0, 1]),
      np.array([0, 0])
    ]
    self._obstacles = [
      np.array([1, 1]),
      np.array([1, 3]),
      np.array([2, 1]),
      np.array([2, 3])
    ]
    self._pe = .05
    self._x_max = 5
    self._y_max = 5
    return

  def draw(self, state):
    grid = [[" " for i in range(self._x_max)] for j in range(self._y_max)]
    for obs in self._obstacles:
      grid[obs[0]][obs[1]] = "O"
    for goal in self._goals:
      grid[goal[0]][goal[1]] = "S"
    grid[state[0]][state[1]] = "R"
    for row in grid:
      print(row)
    print("\n")
    return

  def in_grid(self, state):
    """
    Returns true if state is in grid
    """
    x = state[0]
    y = state[1]
    if not (0 <= x < self._x_max):
      return False
    if not (0 <= y < self._y_max):
      return False
    return True
  
  def get_harmonic_mean(self, state):
    den = []
    for goal in self._goals:
      dG = np.sqrt(np.sum(np.power(state - goal, 2)))
      den.append(1/dG)
    h = 2. / sum(den)
    prob = ceil(h) - h
    return ceil(h) if random.random() > (1-prob) else floor(h)

  def get_observation(self, state):
    new_state = [self.get_next_state(state, act) for act in self._actions]
    obs = [self.get_harmonic_mean(ns) for ns in new_state]
    return obs

  def get_best_action(self, state, observation):
    return self._actions[np.argmin(observation)]

  def get_next_state(self, state, action):
    # action is do nothing
    if np.array_equal(action, self._actions[-1]):
      return state

    # action moves into obstacle
    new_state = state + action
    for obs in self._obstacles:
      if np.array_equal(obs, new_state):
        return state

    if not self.in_grid(new_state):
      return state

    num = random.random()
    if num < self._pe:
      actions = [act for act in self._actions if not np.array_equal(act, self._actions[-1])]
      actions = [act for act in actions if not np.array_equal(act, actions)]
      pos_new_states = [state + act for act in actions]
      pos_new_states = [state for state in pos_new_states if self.in_grid(state)]
      new_states = []
      for state in new_states:
        add_state = True
        for obs in self._obstacles:
          if np.array_equal(obs, state):
            add_state = False
            break
        if add_state:
          new_states.append(add_state)
      return new_state[random.randint(0, len(new_states))]
    else:
      return state + action

initial_state = np.array([0,0])
gw = gridword()

# print(gw.get_observation(initial_state))
# print(gw.get_harmonic_mean(initial_state))
# print(gw.get_next_state(initial_state, act1))
# print(gw.get_next_state(initial_state, act2))
observation = gw.get_observation(initial_state)
sim = simulator.Simulator(gw, initial_state)
sim.run(steps=25, render=True)
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

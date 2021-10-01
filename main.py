import numpy as np
import random
import copy
from matplotlib import pyplot as plt

size      = (5,5)
actions   = [(1,0),(-1,0),(0,1),(0,-1),(0,0)]
shops     = [(2,0), (2,2)]
obstacles = [(1,1), (1,3),(2,1),(2, 3)]

def genNewState(action, state, p_e):
  allActions = [action]
  allActions.extend([act for act in actions if (act[0] != action[0] or act[1] != action[1])])
  allWeights = [1-p_e]
  allWeights.extend([p_e/4.0 for i in range(4)])
  realAction = random.choices(allActions, weights = allWeights, k = 1)[0]
  
  reached = 0
  newState = (state[0] + realAction[0], state[1] + realAction[1])
  if newState in obstacles or newState[0] < 0 or newState[0] > size[0]-1 or newState[1] < 0 or newState[1] > size[1]-1:
    newState = state
  if newState in shops:
    reached = 1
  
  return newState, reached

if __name__ == "__main__":
  action = actions[0]
  state  = (1,0)
  print(genNewState(action, state, 0.1))
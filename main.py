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

if __name__ == "__main__":
  
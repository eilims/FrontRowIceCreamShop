import sys
import os
path = "{}/simulator".format(os.getcwd())
sys.path.append(path)

from simulator import environment as env
from simulator import simulator
import numpy as np
from math import ceil, floor
import random

class GridWorld(env.Environment):
  def __init__(self):
    self._states = []
    for i in range(5):
        for j in range(5):
            self._states.append(np.array([i, j]))

    print(self._states)

    self._goals = [
      np.array([4, 4]),
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

    self._transition_probabilities = {}

    self._pe = .3
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

  def is_state_in_list(self, state, list):
    isInList = []
    for listItem in list:
        isInList.append(np.all(state == listItem))
        # Verify if the state exists in the current list in any amount
    return any(isInList)

  def get_actionable_states(self, state):
    neighborStates = []
    for action in self._actions:
        neighborStates.append(state + action)
    return neighborStates

  def get_number_of_obstacles(self, state):
    obstacleCount = 0
    for neighborState in self.get_actionable_states(state):
        if(self.is_state_in_list(neighborState, self._obstacles)):
            obstacleCount += 1
        elif(not self.in_grid(neighborState)):
            obstacleCount += 1
    return obstacleCount

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

  def init_transition_probabilites(self):
    print(len(self._states))
    for actionIndex in range(len(self._actions)):
        currentAction = self._actions[actionIndex]
        # Create new array for each action
        self._transition_probabilities[actionIndex] = []
        # While iterating through the states we use the indexes to help with generating the transition probabilities
        for currentStateIndex in range(len(self._states)):
            currentState = self._states[currentStateIndex]
            # Append new array for each current state
            self._transition_probabilities[actionIndex].append([])
            for nextStateIndex in range(len(self._states)):
                nextState = self._states[nextStateIndex]
                # Start with assumption 0
                probability = 0;

                # Verify the target state is not an obstacle
                if(not self.is_state_in_list(nextState, self._obstacles)):
                    # If the current action is to do nothing
                    if(actionIndex == 4):
                        obstacleCount = self.get_number_of_obstacles(currentState)
                        # Does the state action combo take us to the given next state
                        if(all(currentState + currentAction == nextState)):
                            probability = 1 - ((4 - obstacleCount)*(self._pe/4))
                        # The next state is not a result of our actions!
                        # Either a failure or out of reach
                        else:
                            # Is the next state the same as the current state
                            if(all(nextState == currentState)):
                                probability = (1 + obstacleCount)*(self._pe/4)
                            else:
                                # Is the next state somewhere the actions allow us to move
                                if(self.is_state_in_list(nextState, self.get_actionable_states(currentState))):
                                    probability = (self._pe/4)
                                else:
                                    probability = 0
                    # Any action other than do nothing
                    else:
                        # Does the state action combo take us to the given next state
                        if(all(currentState + currentAction == nextState)):
                            probability = 1 - (self._pe)
                        # The next state is not a result of our actions!
                        # Either a failure or out of reach
                        else:
                            obstacleCount = self.get_number_of_obstacles(currentState)
                            # Is the next state the same as the current state
                            if(all(nextState == currentState)):
                                probability = 1 - ((4 - obstacleCount)*(self._pe/4))
                            else:
                                # Is the next state somewhere the actions allow us to move
                                if(self.is_state_in_list(nextState, self.get_actionable_states(currentState))):
                                    probability = (self._pe/4)
                                else:
                                    probability = 0
                else:
                    probability = 0

                 # Append the probability of transition from the current state to the next state
                self._transition_probabilities[actionIndex][currentStateIndex].append(probability)

    # print for debug
    for actionIndex, stateMatrix in self._transition_probabilities.items():
        print(self._actions[actionIndex])
        for currentStateIndex in range(len(stateMatrix)):
            print("  " + str(self._states[currentStateIndex]))
            print("    " + str(stateMatrix[currentStateIndex]))

  def get_harmonic_mean(self, state):
    den = []
    for goal in self._goals:
      dG = np.sqrt(np.sum(np.power(state - goal, 2)))
      den.append(1/dG)
    h = 2. / sum(den)
    prob = ceil(h) - h
    return ceil(h) if random.random() > (1-prob) else floor(h)

  def get_observation(self, state):
    # new_state = [self.get_next_state(state, act) for act in self._actions]
    new_states = [
        (i, state + self._actions[i]) for i in range(len(self._actions)) if self.in_grid(state + self._actions[i])
    ]
    obs = [(ns[0], self.get_harmonic_mean(ns[1])) for ns in new_states]
    return obs

  def get_best_action(self, state, observation):
    minObs = min(observation, key = lambda x : x[1])
    return self._actions[minObs[0]]

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
      for state in pos_new_states:
        add_state = True
        for obs in self._obstacles:
          if np.array_equal(obs, state):
            add_state = False
            break
        if add_state:
          new_states.append(state)
      return new_states[random.randint(0, len(new_states)-1)]
    else:
      return state + action
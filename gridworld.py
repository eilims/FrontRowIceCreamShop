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
    self._x_max = 20
    self._y_max = 20
    self._pe = .3

    # States
    self._states_map = {}
    self._states_keys = {}
    self._state_count = 0
    for i in range(self._x_max):
        for j in range(self._y_max):
            self._states_map[self._state_count] = (i,j)
            self._states_keys[(i,j)] = self._state_count
            self._state_count+=1
    self._states = self._states_map.keys()

    # Actions
    self._actions = [[-1, 0],[1, 0],[0, -1],[0, 1],[0, 0]]
    self._actions_map = {i:a for i,a in enumerate(self._actions)}
    self._actions = np.array(list(self._actions_map.keys()))

    self._goals = np.array([[4,4]])

    # Place obstacles into map. Value does not really matter
    self._obstacles = {}
    self._obstacles[(1,1)] = 1
    self._obstacles[(1,3)] = 1
    self._obstacles[(2,1)] = 1
    self._obstacles[(2,3)] = 1
    print(self._obstacles)

    self._transition_probabilities = {}
    self.init_transition_probabilites()

    self._rewards = {}
    self._goal_reward = 1
    self._penalty = -10
    self.init_reward()
    return

  def draw(self, state):
    state = self._states_map[state]
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
        isInList.append(np.all(np.equal(state, listItem)))
        # Verify if the state exists in the current list in any amount
    return any(isInList)

  def get_actionable_states(self, state):
    neighborStates = []
    for action in self._actions_map.values():
        neighborStates.append(state + action)
    return neighborStates

  def get_number_of_obstacles(self, state):
    obstacleCount = 0
    for action in self._actions_map.values():
        neighborStateArr = state + action
        neighborState = (neighborStateArr[0], neighborStateArr[1])
        if(neighborState in self._obstacles):
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

  def init_reward(self):
    """
    Takes obstacles, states, actions and goals
    and returns dictionary with the following format:
    R = {A : matrix of rewards for states i and j for action A}
    OR
    R = {a1: [r(s1,s1), r(s1,s2) ... r(s1,sn),
              ...                            ,
              ...                            ,
              ...                            ,
              r(sn,s1), r(sn,s2) ... r(sn,sn)],
         a2: [           ... ...             ],
         ...
         ...
         an: [           ... ...             ]}
    """
    for actionIndex in self._actions:
      currentAction = self._actions_map[actionIndex]
      states_size = len(self._states)
      currentRewardMatrix = np.zeros([states_size, states_size])
      for currentStateIndex in range(states_size):
        currentState = self._states_map[currentStateIndex]
        for nextStateIndex in range(states_size):
          nextState = self._states_map[nextStateIndex]
          nextStateIsObstacle = self.is_state_in_list(nextState, self._obstacles)
          nextStateIsGoal = self.is_state_in_list(nextState, self._goals)
          probabilityDistribution = self._transition_probabilities[actionIndex][currentStateIndex]
          transitionProbability = probabilityDistribution[nextStateIndex]
          if( nextStateIsObstacle ):
            currentRewardMatrix[currentStateIndex, nextStateIndex] = 0
          elif ( transitionProbability > 0 and nextStateIsGoal ):
            currentRewardMatrix[currentStateIndex, nextStateIndex] = self._goal_reward
          else:
            currentRewardMatrix[currentStateIndex, nextStateIndex] = 0
      self._rewards[actionIndex] = currentRewardMatrix

    #for testing
    # print (self._rewards)
    # for actionIndex, stateMatrix in self._rewards.items():
    #    print(self._actions[actionIndex])
    #    for currentStateIndex in range(len(stateMatrix)):
    #        print("  " + str(self._states[currentStateIndex]))
    #        print("    " + str(stateMatrix[currentStateIndex]))

  def init_transition_probabilites(self):
    for actionIndex in self._actions:
        currentAction = np.array(self._actions_map[actionIndex])
        # Create new array for each action
        self._transition_probabilities[actionIndex] = []
        # While iterating through the states we use the indexes to help with generating the transition probabilities
        for currentStateIndex in self._states:
            currentState = np.array(self._states_map[currentStateIndex])
            # Append new array for each current state
            self._transition_probabilities[actionIndex].append([])
            for nextStateIndex in self._states:
                nextState = self._states_map[nextStateIndex]
                # Start with assumption 0
                probability = 0

                # Verify the target state is not an obstacle
                if(not nextState in self._obstacles.keys()):
                    # If the current action is to do nothing
                    if(actionIndex == 4):
                        obstacleCount = self.get_number_of_obstacles(currentState)
                        # Does the state action combo take us to the given next state
                        if(np.all(np.equal(currentState + currentAction, nextState))):
                            probability = 1 - ((4 - obstacleCount)*(self._pe/4))
                        # The next state is not a result of our actions!
                        # Either a failure or out of reach
                        else:
                            # Is the next state the same as the current state
                            if(np.all(np.equal(nextState,currentState))):
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
                        if(np.all(np.equal(currentState + currentAction, nextState))):
                            probability = 1 - (self._pe)
                        # The next state is not a result of our actions!
                        # Either a failure or out of reach
                        else:
                            obstacleCount = self.get_number_of_obstacles(currentState)
                            # Is the next state the same as the current state
                            if(np.all(np.equal(nextState, currentState))):
                                desiredNextState = currentState + currentAction
                                # If the current state and action take us into a invalid state
                                if(self.is_state_in_list(desiredNextState, self._obstacles) or not self.in_grid(desiredNextState)):
                                    probability = 1 - (4 - obstacleCount)*(self._pe/4)
                                # If the current state and action take us into a valid state
                                else:
                                    probability = (1 + obstacleCount)*(self._pe/4)
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
    # for actionIndex, stateMatrix in self._transition_probabilities.items():
    #    print(self._actions[actionIndex])
    #    for currentStateIndex in range(len(stateMatrix)):
    #        print("  " + str(self._states[currentStateIndex]))
    #        print("    " + str(stateMatrix[currentStateIndex]))

  def get_harmonic_mean(self, state):
    denInv = []
    for goal in self._goals:
      dG = np.sqrt(np.sum(np.power(state - goal, 2)))
      denInv.append(dG)
    if 0. in denInv:
      h = 0.
    else:
      h = 2. / sum([1./d for d in denInv])
    prob = ceil(h) - h
    return ceil(h) if random.random() > (1-prob) else floor(h)

  def get_observation(self, state):
    return self.get_harmonic_mean(self._states_map[state])

  def get_best_action(self, state, policy):
    return policy[state]

  def get_next_state(self, state, action):
    states = self._transition_probabilities[action][state]
    print("Transition Prob at state {}, given action {}: ".format(
      self._states_map[state],
      self._actions_map[action]), states)
    nState = random.choices(
      [i for i in range(self._state_count)], weights=states)
    print("Current State: {}, Action: {}, Next State: {}".format(
      self._states_map[state],
      self._actions_map[action],
      self._states_map[nState[0]]))
    return nState[0]
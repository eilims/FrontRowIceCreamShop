import sys
import os
path = "{}/simulator".format(os.getcwd())
sys.path.append(path)
path = "{}/mdp".format(os.getcwd())
sys.path.append(path)

from simulator import simulator
from gridworld import GridWorld
from mdp import ValueIteration
import numpy as np

initial_state = np.array([0,0])
gw = GridWorld()
gw.init_transition_probabilites()
gw.init_reward()

test_states = list(range(len(gw._states)))
test_actions = list(range(len(gw._actions)))
solver = ValueIteration(test_states, test_actions, gw._transition_probabilities, gw._rewards, -1, 0.5, 0.000001)
solver.run()
print(solver.policy)

observation = gw.get_observation(initial_state)
sim = simulator.Simulator(gw, initial_state)
sim.run(steps=10, render=True)
exit()
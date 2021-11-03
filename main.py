import os, sys
path = "{}/simulator".format(os.getcwd())
sys.path.append(path)
path = "{}/mdp".format(os.getcwd())
sys.path.append(path)

from simulator import simulator
from gridworld import GridWorld
from mdp import ValueIteration
from mdp import PolicyIteration
from bayes import state_estimation
import numpy as np

initial_state = (0,0)
gw = GridWorld()

# Run value iteration
# solver = ValueIteration(gw, -1, 0.5, 0.000001)
# solver.run()
# print("State Values: ")
# print(solver.V)
# print("Policy: ")
# print(solver.policy)
# gw._policy = solver.policy

sim = simulator.Simulator(gw, initial_state)
# sim.run(solver.policy, steps=20, render=True)

belief0 = [0 for s in range(len(gw._states_map))]
initStateNum = [key for key, state in gw._states_map.items() if state == initial_state][0]
belief0[initStateNum] = 1.0
print(state_estimation(gw, belief0, 5))

# gw.plot_policy()
exit()
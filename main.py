import os, sys
path = "{}/simulator".format(os.getcwd())
sys.path.append(path)
path = "{}/mdp".format(os.getcwd())
sys.path.append(path)
path = "{}/trajectory".format(os.getcwd())
sys.path.append(path)

from simulator import simulator
from gridworld import GridWorld
from mdp import ValueIteration
from mdp import ValueIterationApprox
from mdp import PolicyIteration
from trajectory import Trajectory
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
my_trajectory = Trajectory([3,3,3,3,1,1,1,1], sim)
my_trajectory.construct()

belief0 = [0 for s in range(len(gw._states_map))]
belief0[gw._states_keys[initial_state]] = 1.0
belief_history = state_estimation(gw, my_trajectory, belief0)
print("State Estimates ({}): {}".format(len(belief_history), [np.argmax(belief) for belief in belief_history]))

# gw.plot_policy()
exit()
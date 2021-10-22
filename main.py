import sys
import os
path = "{}/simulator".format(os.getcwd())
sys.path.append(path)
path = "{}/mdp".format(os.getcwd())
sys.path.append(path)


from simulator import simulator
from gridworld import GridWorld
from mdp import ValueIteration
from mdp import ValueIterationApprox
from mdp import PolicyIteration
import numpy as np

initial_state = (0,0)
gw = GridWorld()

# Run value iteration
solver = ValueIterationApprox(gw, 5, 0.5, 0.000001)
solver.run()
print("State Values: ")
print(solver.V)
print("Policy: ")
print(solver.policy)

gw._policy = solver.policy

sim = simulator.Simulator(gw, initial_state)
sim.run(solver.policy, steps=20, render=True)

gw.plot_policy()
exit()
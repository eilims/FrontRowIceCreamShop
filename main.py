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

initial_state = (0,0)
gw = GridWorld()

# Run value iteration
solver = ValueIteration(gw, -1, 0.5, 0.000001)
solver.run()
print("State Values: ")
print(np.reshape(solver.V, (5,5)))
print("Policy: ")
print(solver.policy)

sim = simulator.Simulator(gw, initial_state)
sim.run(solver.policy, steps=10, render=True)
exit()
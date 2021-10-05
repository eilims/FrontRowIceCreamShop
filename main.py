import sys
import os
path = "{}/simulator".format(os.getcwd())
sys.path.append(path)

from simulator import simulator
from gridworld import GridWorld
import numpy as np

initial_state = np.array([0,0])
gw = GridWorld()

observation = gw.get_observation(initial_state)
sim = simulator.Simulator(gw, initial_state)
sim.run(steps=100, render=True)
exit()
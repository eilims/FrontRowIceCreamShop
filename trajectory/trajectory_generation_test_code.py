import sys
import os
path = "../simulator"
sys.path.append(path)
path = ".."
sys.path.append(path)

from simulator import simulator
from gridworld import GridWorld
from trajectory import Trajectory

initial_state = (0,0)

# Trajectory 1: L shape down and right
gw = GridWorld()
sim = simulator.Simulator(gw, initial_state)
my_trajectory = Trajectory([1,1,1,1,3,3,3,3], sim)
my_trajectory.construct()
sim.render()

# Trajectory 2: L shape right and down
gw2 = GridWorld()
sim2 = simulator.Simulator(gw2, initial_state)
my_trajectory2 = Trajectory([3,3,3,3,1,1,1,1], sim2)
my_trajectory2.construct()
sim2.render()


exit()
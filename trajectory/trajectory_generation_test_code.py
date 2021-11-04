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
gw = GridWorld()

sim = simulator.Simulator(gw, initial_state)

my_trajectory = Trajectory([1,1,1,1,1,1,1], sim)
my_trajectory.construct()

print("History of states {}: {}".format(len(my_trajectory._state_history), my_trajectory._state_history))
print("History of actions {}: {}".format(len(my_trajectory._action_history), my_trajectory._action_history))

exit()
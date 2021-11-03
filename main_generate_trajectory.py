import sys
import os
path = "{}/simulator".format(os.getcwd())
sys.path.append(path)

from simulator import simulator
from gridworld import GridWorld
from trajectory import Trajectory

initial_state = (0,0)
gw = GridWorld()

sim = simulator.Simulator(gw, initial_state)

my_trajectory = Trajectory([1,1,1,1,1,1,1],sim)
my_trajectory.construct()

print(my_trajectory._state_history)
print(my_trajectory._action_history)


exit()
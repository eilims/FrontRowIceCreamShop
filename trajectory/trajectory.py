# Defines a class for the environment. The environment is used by the simulator
# By: Vishnu Devarakonda

class Trajectory:
    def __init__(self, action_trajectory, simulator):
        """
        A Trajectory contains a history of states, the actions we took, and the observations we took at those states
        args:
            action_trajectory: A desired set of actions to take
            initial_state: The starting state of our trajectory
            simulator: A simulator that generates our next states and observations given our desired actions

        """
        self._simulator = simulator
        self._initial_state = self._simulator._current_state
        self._state_history = [self._initial_state]
        self._action_history = action_trajectory
        self._observation_history = []
        

    def construct(self):
        """
        Generate our state and observation history using the simulator
        """
        for action in self._action_history:
            next_state = self._simulator.step(action)
            self._state_history.append(next_state) # History of states
            # self._observation_history(self._simulator._env.sample_prob_obs_(next_state)) # History of observations
            self._simulator._current_state = next_state
        


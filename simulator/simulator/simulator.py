# File contains the simulator class which runs discrete stochastic state space
# By: Vishnu Devarakonda
from simulator.environment import Environment
import copy


class Simulator:
    def __init__(self, env: Environment, initial_state) -> None:
        """
        Initialize a simulator
        args:
            env: Environment. The simulator environment.
            initial_state: numpy array.
        """
        self._env = env
        self._initial_state = self._env._states_keys[initial_state]
        self._current_state = copy.deepcopy(self._initial_state)
        self._current_observation = self.observe()
        self._current_action = self._env._actions[0] # choose any action
        self._t_step = 0

    def render(self):
        """
        Function renders
        """
        self._env.draw(self._current_state)

    def reset(self):
        """
        Function resets the environment to the initial state
        """
        self._current_state = self._initial_state.copy()
        self._t_step = 0

    def step(self, action):
        """
        Function performs an action in the environment.
        args:
            action: The action to be performed in the environment.
                The initialized environment must be able to understand the
                action.

        """
        next_state = self._env.get_next_state(self._current_state, action)
        return next_state

    def observe(self):
        """
        Function returns an observation in the environment.
        """
        return self._env.get_observation(self._current_state)


    def run(self, policy, steps: int, render : bool = False):
        """
        This function will run the simulator.
        args:
            steps: int. The number of steps to run the simulator for.
            render: Bool. If true, the function will render the environment
                after every step.
        """
        if render:
            self.render()
        while self._t_step < steps:
            self._current_action = self._env.get_best_action(self._current_state, policy)
            self._current_state = self.step(self._current_action)
            self._current_observation = self.observe()
            if render:
                self.render()
            self._t_step +=1

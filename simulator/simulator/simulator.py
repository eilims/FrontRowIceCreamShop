# File contains the simulator class which runs discrete stochastic state space
# By: Vishnu Devarakonda
from simulator.environment import Environment


class Simulator:
    def __init__(self, env: Environment, initial_state) -> None:
        """
        Initialize a simulator
        args:
            env: Object. The simulator environment.
        """
        self._env = env
        self._initial_state = initial_state
        self._current_state = self._initial_state.copy()
        self._current_observation = self.observe()
        self._current_action = None
        self._t_step = 0

    def render(self):
        """
        Function renders
        """
        self._env.draw()

    def reset(self):
        """
        Function resets the environment to the initial state
        """
        self._env.set_state(self._initial_state)
        self._t_step = 0
        return self._initial_state

    def step(self, action):
        """
        Function performs an action in the environment.
        args:
            action: The action to be performed in the environment.
                The initialized environment must be able to understand the
                action.

        """
        next_state = self._env.get_next(action)
        return next_state

    def observe(self):
        """
        Function returns an observation in the environment.
        """
        return self._env.get_observation(self._current_state)


    def run(self, steps: int, print : bool = False):
        """
        This function will run the simulator.
        args:
            steps: int. The number of steps to run the simulator for.
            print: Bool. If true, the function will render the environmnet
                after every step.
        """
        self.render()
        while self._t_step < steps:
            self._current_action = self._env.get_best_action(
                self._current_state,
                self._current_observation)
            """(
                current_state,
                current_observation,
                curret_action,
                next_state,
                t_step)"""
            self._current_state = self.step(self._current_action)
            self._current_observation = self.observe(self._current_state)
            self._t_step +=1
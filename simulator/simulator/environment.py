# Defines a class for the environment. The environment is used by the simulator
# By: Vishnu Devarakonda

class Environment:
    """
    Define an environment by subclassing. Implement this following.

    ex: class Gridworld(Environment) ....
    """
    def __init__(self) -> None:
        pass

    def draw(self, state) -> None:
        """
        Implement this function to draws the environment with the current state.
        """
        raise NotImplementedError

    def get_next_state(self, action):
        """
        Implement this function to get the next state after applying action.
        """
        raise NotImplementedError

    def get_observation(self, state):
        """
        Implement this function to get the observation given the state.
        """
        raise NotImplementedError

    def get_best_action(self, state, observation):
        """
        Implement this function to get the best action given the state and
        observation.
        """
        raise NotImplementedError
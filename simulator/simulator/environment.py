# Defines a class for the environment. The environment is used by the simulator
# By: Vishnu Devarakonda

class Environment:
    def __init__(self) -> None:
        pass

    def draw(self) -> None:
        raise NotImplementedError

    def get_next_state(self, action):
        raise NotImplementedError

    def set_state(self, state):
        raise NotImplementedError

    def get_observation(self):
        raise NotImplementedError

    def get_best_action(self):
        raise NotImplementedError
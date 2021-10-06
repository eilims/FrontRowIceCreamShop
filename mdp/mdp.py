# Defines classes for a general MDP problem and associated problem solvers.
# By: Patrick Han


class MDP:
    def __init__(self, states, actions, probabilities, rewards, horizon, gamma, epsilon):
        """
        Initialize an MDP problem
        args:
            states: All possible states
            actions: Possible actions that can be taken
            probabilities: Transition probabilities between states under some action
            rewards: Immediate rewards received for state transitions under some action
            horizon: Horizon, -1 for infinite or a positive integer for finite horizon
            gamma: Discount factor on future rewards, float [0.0, 1.0]
            epsilon: Stopping criteria, maximum change in value function for each iteration before stopping
        """
        self._states = states
        self._actions = actions
        self._probabilities = probabilities
        self._rewards = rewards
        assert horizon == -1 or (type(horizon) is int and horizon >= 0)
        self._horizon = horizon
        self._gamma = gamma
        self._epsilon = epsilon


class ValueIteration(MDP):
    def __init__(self, states, actions, probabilities, rewards, horizon, gamma, epsilon):
        """
        Initialize a Value Iteration MDP problem solver, inherits from MDP class
        args:
            states: All possible states
            actions: Possible actions that can be taken
            probabilities: Transition probabilities between states under some action
            rewards: Immediate rewards received for state transitions under some action
            horizon: Horizon, -1 for infinite or a positive integer for finite horizon
            gamma: Discount factor on future rewards, float [0.0, 1.0]
            epsilon: Stopping criteria, maximum change in value function for each iteration before stopping
        """
        MDP.__init__(self, states, actions, probabilities, rewards, horizon, gamma, epsilon)

        # Initialize the deterministic policy which is a mapping between states and actions
        # Therefore, this dictionary should have each state as a key, each with 1 action as the value
        self.policy = {}
        for state in states:
            # We can check to make sure that every state has an action later (i.e. not False), this is a really hacky way to do it for now
            self.policy[state] = False 

        # Decide if we need to solve on an infinite or finite horizon
        self.use_infinite_horizon = False
        if self._horizon == -1:
            self.infinite_horizon = True
        self.iteration = 0 # If horizon if finite, we need to check 


        # Value Iteration variables
        # TODO: self.V = np.zeros("sizeof"(S)) # Zero initialize values, this is just pseudocode for now since I don't know how S is represented


    def run(self):
        """
        Runs the Value Iteration algorithm
        """

        while(True):
            self.iteration += 1

            Vprevious = self.V.copy()


            # Apply bellman operator to current V to calculate the new V
            # TODO: Highly dependent on the representations of P and R

            # Stopping criteria
            if self.use_infinite_horizon:
                # TODO:~ if np.max(np.abs(Vprevious - self.V)) <= self._epsilon: # If the max absolute difference is less than epsilon...
                #           break
                # Also need to bound this or something so the loop doesn't run forever....
            else if self.iteration == self._horizon:
                break


# TODO: Write Policy Iteration class
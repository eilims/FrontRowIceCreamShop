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

        # Initialize a deterministic policy which is a mapping between states and actions
        self.policy = {}
        for state in self._states:
            # We can check to make sure that every state has an action later (i.e. not False), this is a really hacky way to do it for now
            self.policy[state] = False

        # Value Iteration
        self.V = np.zeros(len(self._states)) # Zero initialize values


    def bellmanBackup(self):
        """
        Applies the bellman operator T on the current value V and updates self.V and self.policy
        """
        # TODO: Highly dependent on the representations of P and R!!

        P = self._probabilities
        R = self._rewards

        # Very slow way of doing things, should be able to be vectorized but right now my brain hurts after writing this class all morning
        for i, s in enumerate(self.V):
            Q = np.zeros(len(self._actions))
            for k, a in enumerate(self._actions):
                running_sum = 0 # Sum over all s_primes (future state)
                for j, s_prime in enumerate(self._states):
                    running_sum += P[a][i][j] * (R[a][i][j] + self._gamma * self.V[i])
                Q[k] = running_sum
            
            self.V[i] = np.max(Q) # Maximize over all actions to get new V
            self.policy[s] = self._actions(np.argmax(Q)) # Argmax over all actions to update the policy
            


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


        # Decide if we need to solve on an infinite or finite horizon
        self.use_infinite_horizon = False
        if self._horizon == -1:
            self.infinite_horizon = True
        self.iteration = 0 # If horizon if finite, we need to check 


    def run(self):
        """
        Runs the Value Iteration algorithm
        """

        while(True):
            self.iteration += 1

            Vprevious = self.V.copy()

            # Apply bellman operator to update V and the policy
            self.bellmanBackup()

            # Stopping criteria
            if self.use_infinite_horizon:
                if np.max(np.abs(Vprevious - self.V)) <= self._epsilon: # If the max absolute difference is less than epsilon
                    break
            else if self.iteration == self._horizon:
                break


# TODO: Write Policy Iteration class
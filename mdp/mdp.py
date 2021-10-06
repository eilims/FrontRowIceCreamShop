# Defines classes for a general MDP problem and associated problem solvers.
# By: Patrick Han
import random

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

        # Policy maps between states and actions
        self.policy = {}

        # Value initalization
        self.V = np.zeros(len(self._states)) # Zero initialize values


    def bellmanBackup(self, update_value):
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
            
            if update_value: # Value should only be updated during Value Iteration
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

        # Initialize a deterministic policy which is a mapping between states and actions
        for state in self._states:
            # We can check to make sure that every state has an action later (i.e. not False), this is a really hacky way to do it for now
            self.policy[state] = False

    def run(self):
        """
        Runs the Value Iteration algorithm
        """

        while(True):
            self.iteration += 1

            Vprevious = self.V.copy()

            # Apply bellman operator to update V and the policy
            self.bellmanBackup(update_value = True)

            # Stopping criteria
            if self.use_infinite_horizon:
                if np.max(np.abs(Vprevious - self.V)) <= self._epsilon: # If the max absolute difference is less than epsilon
                    break
            else if self.iteration == self._horizon:
                break



class PolicyIteration(MDP):
    def __init__(self, states, actions, probabilities, rewards, horizon, gamma, epsilon):
        """
        Initialize a Policy Iteration MDP problem solver, inherits from MDP class
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

        # Initialize a randomized deterministic policy which is a mapping between states and actions
        for state in self._states:
            self.policy[state] = random.choice(self._actions)


    def run(self):
        """
        Runs the Policy Iteration algorithm
        """

        while(True):
            self.iteration += 1

            Vprevious = self.V.copy()
            policyPrevious = self.policy.copy()


            # 1. Policy Evaluation: Compute V^(pi_i) from policy_i
            num_states = len(self._states)
            P_bar = np.array((num_states, num_states))
            for m, s in enumerate(self._states): # Build P_bar, i.e. transition probabilities under the current policy
                for n, s_prime in enumerate(self._states):
                    P_bar[m][n] = self._probabilities[self.policy[s]][m][n] # The probability of going from s to s_prime under the current policy
            
            R_bar = np.array((num_states, num_states))
            for m, s in enumerate(self._states): # Build R_bar, i.e. rewards under the current policy
                for n, s_prime in enumerate(self._states):
                    R_bar[m][n] = self._rewards[self.policy[s]][m][n] # The probability of going from s to s_prime under the current policy

            D_bar = np.diag(np.matmul(P_bar, R_bar.T))
            V_bar = np.matmul(np.linalg.inv(np.eye(num_states) - self._gamma * P_bar), D_bar)


            # 2. Policy Refinement: Compute policy_(i+1) from V^(pi_i)
            self.bellmanBackup(update_value = False) # Only update self.policy


            # Stopping criteria - Either the value doesn't change between steps or policy doesn't change
            if np.max(np.abs(Vprevious - self.V)) <= self._epsilon: # If the value is unchanging
                break
            if self.policy == policyPrevious: # Dunno if this is a good idea
                break
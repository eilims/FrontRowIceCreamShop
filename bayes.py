#Implements the Bayes Filter
#By: Aaron John Sabu

def belpls(P_o, bMin, observation):
  numStates = len(P_o)
  bPls = [0.0 for s in range(numStates)]
  sumB =  0.0
  for state in range(numStates):
    for obs in range(len(P_o[state]["choices"])):
      if P_o[state]["choices"][obs] == observation:
        bPls[state] = P_o[state]["weights"][obs]*bMin[state]
        break
  sumB = sum(bPls)
  bPls = [bVal/sumB for bVal in bPls]
  # print(bPls)
  return bPls

def belmin(P_t, bPls, action):
  numStates = len(P_t[0])
  bMin = [0.0 for s in range(numStates)]
  for new_state in range(numStates):
    for state in range(numStates):
      bMin[new_state] += P_t[action][state][new_state]*bPls[state]
  return bMin

def get_next_belief(P_t, P_o, bPls, action, observation):
  bMin = belmin(P_t, bPls, action)
  bPls = belpls(P_o, bMin, observation)
  return bPls

def state_estimation(env, trajectory, b0):
  action_history, observation_history = trajectory._action_history, trajectory._observation_history
  P_t  = env._transition_probabilities
  P_o  = env._proability_obs_given_state
  bPls = get_next_belief(P_t, P_o, b0, action_history[0], observation_history[0])
  belief_history = [bPls]
  for step in range(1, len(action_history)):
    bPls = get_next_belief(P_t, P_o, bPls, action_history[step], observation_history[step])
    belief_history.append(bPls)
  return belief_history

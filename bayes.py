#Implements the Bayes Filter
#By: Aaron John Sabu

def belpls(P_o, bMin):
  numStates = len(P_o)
  bPls = [0.0 for s in range(numStates)]
  sumB =  0.0
  for state in range(numStates):
    bPls[state] = P_o[state][observation]*bMin[state]
    sumB += bPls[state]
  bPls = [bVal/sumB for bVal in bPls]
  return bPls

def belmin(P_t, bPls):
  numStates = len(P_t[0])
  bMin = [0.0 for s in range(numStates)]
  for new_state in range(numStates):
    for state in range(numStates):
      bMin[new_state] += P_t[action][state][new_state]*bPls[state]
  return bMin

def get_next_belief(P_t, P_o, bPls):
  bMin = belmin(P_t, bPls)
  bPls = belpls(P_o, bMin)
  return bPls

def state_estimation(env, b0, numIters):
  P_t  = env.init_transition_probabilites()
  P_o  = env.init_observation_distribution()
  bMin = belmin(P_t, b0)
  bPls = belpls(P_o, bMin)
  for i in range(numIters - 1):
    bMin = belmin(P_t, bPls)
    bPls = belpls(P_o, bMin)
  return bPls

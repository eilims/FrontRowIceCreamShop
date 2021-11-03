#Implements the Bayes Filter
#By: Aaron John Sabu

numIters = 5

def belpls(P_o, belMin):
  belPls = [0 for s in range(len(all_states))]
  sumBel = 0.0
  for new_state in all_states:
    belPls[state] = P_o[observation][state]*belMin[state]
    sumBel += belPls[state]
  belPls = [belVal/sumBel for belVal in belPls]
  return belPls

def belmin(P_t, belPls):
  belMin = [0 for s in range(len(all_states))]
  for new_state in all_states:
    for state in all_states:
      belMin[new_state] += P_t[new_state][state][action]*belPls[state][observation]
  return belMin

def state_estimation(initial_state):
  bel0 = [0 for i in range(len(all_states))]
  bel0[initial_state] = 1
  belMin = belmin(P_t, bel0)
  belPls = belpls(P_t, belMin)
  for i in range(numIters - 1):
    belMin = belmin(P_t, belPls)
    belPls = belpls(P_t, belMin)
import main

states  = [(0, 0),(0,1),(1,0),(4,0),(0,4),(3, 4),(4,3),(4,4),(4,4),( 3,3),(0,3),(1,2),( 3,2),(1,0),( 3,0)]
actions = [(-1,0),(1,0),(0,0),(1,0),(0,1),(0,-1),(1,0),(1,0),(0,1),(-1,0),(1,0),(1,0),(-1,0),(1,0),(-1,0)]
p_e = 0.1

for test in range(len(states)):
  print(actions[test], states[test], p_e)
  print(main.genNewState(actions[test], states[test], p_e))
  print()
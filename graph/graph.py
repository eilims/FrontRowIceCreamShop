    # Defines classes for 
# By: Patrick Han

class Graph:
    def __init__(self):
        self.G = {}
        self.action_list = [(-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1)]
        self.num_cols = 8
        for v in range(64):
            self.G[v] = []
        # actions
        # 0 : up and left
        # 1 : up and right
        # 2 : right and up
        # 3 : right and down
        # 4 : down and right
        # 5 : down and left
        # 6 : left and down
        # 7 : left and up

        # {node : [(node, action)]}
        # [0, 1, 2,  3,  4,  5 , 6,  7
        #  8, 9, 10, 11, 12, 13, 14, 15
        #  16,17,18, 19, 20, 21, 22, 23
        #  24,25,26, 27, 28, 29, 30, 31
        #  32,33,34, 35, 36, 37, 38, 39
        #  40,41,42, 43, 44, 45, 46, 47
        #  48,49,50, 51, 52, 53, 54, 55
        #  56,57,58, 59, 60, 61, 62, 63]]

        # from 2d:
        # number of cols * row_idx + col_idx
        # 8 * 4 + 5

        for row_idx in range(8):
            for col_idx in range(8):
                state_start_flat = self.num_cols * row_idx + col_idx

                for i, action in enumerate(self.action_list):
                    check_state_2d = [col_idx, row_idx]
                    check_state_2d[0] += action[0]
                    check_state_2d[1] += action[1]

                    if check_state_2d[0] >= 0 and check_state_2d[0] <= 7 and check_state_2d[1] >= 0 and check_state_2d[1] <= 7:
                        # Only a valid ending state if within bounds of the grid
                        end_state_flat = self.num_cols * check_state_2d[1] + check_state_2d[0]
                        self.G[state_start_flat].append((end_state_flat, i)) # (end_state_flat, action enumeration)
                            
        for n in range(64):
            print(self.G[n])

g = Graph()



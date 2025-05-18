import sys
import numpy as np

#get file path
path = sys.argv[1]

#read file
file = open(path, 'r')

#split line
lines = file.read().split('\n')

#get row and col
row, col = lines[0].split(' ')
row = int(row)
col = int(col)

# print(row, col)

map = np.ones((row, col), dtype = str)

for r in range(1, row + 1):
    map[r-1] = lines[r].split(' ')[:-1]

# print(map)

time = lines[row + 1]
time = int(time)
# print(time)

observed = np.zeros((time, 4), dtype = str)
for t in range(time):
    for c in range(4):
        observed[t][c] = lines[row + 2 + t][c]

# print(observed)

error_rate = lines[-1]
error_rate = float(error_rate)
# print(error_rate)

#########################################################

#number of empty positions (no obstacles)
num_state = 0
state_array = []
for r in range(row):
    for c in range(col):
        if map[r][c] == '0':
            num_state += 1
            state_array.append((r, c))

# print(num_state)
# print(state_array)

#neighbour function
def is_neighbour(pos1, pos2):
    """
    Input: 2 position of two states
    Output: True if they are neighbour
    """
    x1, y1 = pos1
    x2, y2 = pos2
    if x1 == x2 and (y1 == y2 - 1 or y1 == y2 + 1):
        return True
    if (x1 == x2 - 1 or x1 == x2 + 1) and y1 == y2:
        return True
    
    return False

#build transition matrix
transition = np.zeros((num_state, num_state))

neighbours_array = []

for state in state_array:
    neighbour = []
    for state2 in state_array:
        if is_neighbour(state, state2):
            neighbour.append(state2)
    neighbours_array.append(neighbour)

for s in range(num_state):
    prob = 0
    if len(neighbours_array[s]) != 0:
        prob = 1/len(neighbours_array[s])
    for neighbour in neighbours_array[s]:
        i = state_array.index(neighbour)
        transition[s][i] = prob

# print(transition, end='\n\n')

#build emission matrix
emission = np.zeros((num_state, time))

for r, state in enumerate(state_array):
    for c, obs in enumerate(observed):
        error = 0

        #north
        north,south,west,east = 0, 0, 0, 0
        if state[0] == 0 or map[state[0] - 1][state[1]] == 'X':
            north = 1
        else: 
            north = 0
        
        if north != int(obs[0]):
            error += 1

        #south
        if state[0] == row - 1 or map[state[0] + 1][state[1]] == 'X':
            south = 1
        else: 
            south = 0

        if south != int(obs[1]):
            error += 1

        #west
        if state[1] == 0 or map[state[0]][state[1] - 1] == 'X':
            west = 1
        else: 
            west = 0

        if west != int(obs[2]):
            error += 1

        #east
        if state[1] == col - 1 or map[state[0]][state[1] + 1] == 'X':
            east = 1
        else: 
            east = 0

        if east != int(obs[3]):
            error += 1

        emission[r][c] = ((1 - error_rate) ** (4 - error)) * (error_rate ** error)

# print(emission, end='\n\n')

#initial probability
initial = np.ones((num_state,1))
for r in range(num_state):
    initial[r][0] = 1/num_state

# print(initial)

#trellis
trellis = np.zeros((num_state, time))

#get the first column for trellis meaning t = 1
for s in range(num_state):
    trellis[s][0] = initial[s][0] * emission[s][0]

#get the second column until end meaning t = 2,3,...
for t in range(1, time):
    for s in range(num_state):
        #find the most likely prior position
        neighbours = neighbours_array[s]
        highest = 0.0
        trellis[s][t] = 0.0
        for neighbour in neighbours:
            i = state_array.index(neighbour)
            trellis[s][t] = max(trellis[s][t], trellis[i][t-1] * transition[i][s] * emission[s][t])

# for t in range(time):
#     print("Time:", t + 1)
#     for s in range(num_state):
#         print(trellis[s][t], end=' ')
#     print("")

final = []

for t in range(time):
    final_map = np.zeros((row, col), dtype = float)
    for s in range(num_state):
        x = state_array[s][0]
        y = state_array[s][1]
        final_map[x][y] = trellis[s][t]

    print("Time:", t + 1)
    print(final_map)
    final.append(final_map)

final = np.asarray(final)
np.savez("output.npz", *final)
import numpy as np

cells = [(i,j) for i in range(1,6) for j in range(1, 7)]
states = [(i,j) for i in cells for j in cells]
states += "F"

stat_d = len(states)

lookup_dict = {states[i]:i for i in range(stat_d)}

angles = [(1,1),(1,6),(5,1),(5,6)]

#states are rows/cols of transition matrixes
#5 matrices, 1 for each action of the human
#matrix 1, a="stay_still"
def row_function(row, i):
    #Get positions by row
    state = states[i]
    human_pos = state[0]
    # Final state "F" has only one value, out-of-bound access state[1]
    if human_pos=="F":
        positions = lookup_dict["F"]
        row[positions]=1
        return row
    minotaur = state[1]
    print("human: " + str(human_pos) + " minotaur: " + str(minotaur))
    #If minotaur and human have same position, games end
    if human_pos==minotaur:
        positions = lookup_dict["F"]
        row[positions]=1
        return row
    #if minotaur is on the angles can only move in 2 adjancten cells
    if minotaur==(1,1):
        #can only move to (1,2) or (2,1)
        #retrive corresponding state
        possible_states = [(human_pos,(1,2)),(human_pos,(2,1))]
        possible_states.append((human_pos, minotaur))
        positions = []
        for i in possible_states:
            positions.append(lookup_dict[i])
        assert len(positions) == 3
        row[positions] = 1/3
        return row
    elif minotaur==(1,6):
        possible_states = [(human_pos, (1, 5)), (human_pos, (2, 6))]
        possible_states.append((human_pos, minotaur))
        positions = []
        for i in possible_states:
            positions.append(lookup_dict[i])
        assert len(positions) == 3
        row[positions] = 1/3
        return row
    elif minotaur==(5,1):
        possible_states = [(human_pos, (5, 2)), (human_pos, (4, 1))]
        possible_states.append((human_pos, minotaur))

        positions = []
        for i in possible_states:
            positions.append(lookup_dict[i])
        assert len(positions) == 3
        row[positions] = 1/3
        return row
    elif minotaur==(5,6):
        possible_states = [(human_pos, (5, 5)), (human_pos, (4, 6))]
        possible_states.append((human_pos, minotaur))

        positions = []
        for i in possible_states:
            positions.append(lookup_dict[i])
        assert len(positions) == 3
        row[positions] = 1/3
        return row
    elif minotaur[0]>1 and minotaur[0]<5 and minotaur[1]>1 and minotaur[1]<6:
        min_r=minotaur[0]
        min_c=minotaur[1]
        possible_states=[(human_pos, (min_r, min_c+1)), (human_pos, (min_r, min_c-1)),
                         (human_pos, (min_r+1, min_c)),(human_pos, (min_r-1, min_c))]
        possible_states.append((human_pos, minotaur))

        positions = []
        for i in possible_states:
            positions.append(lookup_dict[i])
        assert len(positions) == 5
        row[positions] = 0.2
        return row
    else:
    # Minotaur is on the edges, but not on angles -> p = 0.33
        min_r = minotaur[0]
        min_c = minotaur[1]
        possible_states = []
        if min_r==1: #On the upper edge, no row up
            possible_states = [(human_pos, (min_r, min_c + 1)), (human_pos, (min_r, min_c - 1)),
                               (human_pos, (min_r + 1, min_c)) ]
        elif min_r==5: #Lower row, no row down
            possible_states = [(human_pos, (min_r, min_c + 1)), (human_pos, (min_r, min_c - 1)),
                               (human_pos, (min_r - 1, min_c))]
        elif min_c==1: #Left side, no col-1
            possible_states = [(human_pos, (min_r, min_c + 1)),
                               (human_pos, (min_r+1, min_c)),(human_pos, (min_r-1, min_c))]
        elif min_c==6: #Right side, no col+1
            possible_states = [(human_pos, (min_r, min_c - 1)),
                               (human_pos, (min_r + 1, min_c)), (human_pos, (min_r - 1, min_c))]
        possible_states.append((human_pos, minotaur))
        assert len(possible_states) == 4

        positions = []
        for i in possible_states:
            positions.append(lookup_dict[i])
        assert len(positions) == 4
        row[positions] = 1/4
        return row

P = np.zeros( (stat_d,stat_d) )
for row in range(stat_d):
    P[row,:] = row_function(P[row,:], row)

print(P.shape)
P.tofile("P_stay_still", sep=";")
#action: move right
import numpy as np

cells = [(i,j) for i in range(1,6) for j in range(1, 7)]
states = [(i,j) for i in cells for j in cells]
final_state = "F"
states.append(final_state)

stat_d = len(states)

lookup_dict = {states[i]:i for i in range(stat_d)}

#Is transition possible?
#(x,y) means impossible move from x to y
impossible_human_movement=[((2, 5), (3, 5)),
                           ((2, 6), (3, 6)),
                           ((4, 2), (5, 2)),
                           ((4, 3), (5, 3)),
                           ((4, 4), (5, 4)),
                           ((4, 5), (5, 5)),
                           ((5, 1), (6, 1)),
                           ((5, 2), (6, 2)),
                           ((5, 3), (6, 3)),
                           ((5, 4), (6, 4)),
                           ((5, 5), (6, 5)),
                           ((5, 6), (6, 6))
                          ]

def row_function(row, i):
    #Get positions by row
    state = states[i]
    #Since final state has a differnt sintax, cannot postpone this rule
    # P(s'=END | s=END, a=<whatever> )=1
    if state == final_state:
        positions = lookup_dict[final_state]
        row[positions] = 1
        return row

    human_position = state[0]
    minotaur_position = state[1]

    hum_row=human_position[0]
    hum_col=human_position[1]

    minotaur_row = minotaur_position[0]
    minotaur_col = minotaur_position[1]

    next_human_position = (hum_row+1, hum_col)

    ########################
    #Evaluate whether the transaction s -> s' is possible due to wall
    ########################
    if (human_position,next_human_position) in impossible_human_movement:
        #no feasible transaction
        #return row as row is already full of 0
        return row

    ###########################
    #Set Final transitions
    ##########################

    #P(s'=END | s=[(x,y),(x,y)], a=<whatever> )=1
    if human_position==minotaur_position:
        positions = lookup_dict[final_state]
        row[positions]=1
        return row

    if human_position==(5,6):
        positions = lookup_dict[final_state]
        row[positions] = 1
        return row
    #########################
    #Start deal with Minotaur
    #########################
    candidate_next_states = []
    #if minotaur is on the angles can only move in 2 adjancten cells
    if minotaur_position==(1,1):
        #can only move to (1,2) or (2,1)
        #retrive corresponding state
        candidate_next_states = [(next_human_position,(1,2)),(next_human_position,(2,1))]

    elif minotaur_position==(1,6):
        candidate_next_states = [(next_human_position, (1, 5)), (next_human_position, (2, 6))]

    elif minotaur_position==(5,1):
        candidate_next_states = [(next_human_position, (5, 2)), (next_human_position, (4, 1))]

    elif minotaur_position==(5,6):
        candidate_next_states = [(next_human_position, (5, 5)), (next_human_position, (4, 6))]

    elif minotaur_row>1 and minotaur_row<5 and minotaur_col>1 and minotaur_col<6:
        #Non edge position
        candidate_next_states=[(next_human_position, (minotaur_row, minotaur_col+1)),
                               (next_human_position, (minotaur_row, minotaur_col-1)),
                               (next_human_position, (minotaur_row+1, minotaur_col)),
                               (next_human_position, (minotaur_row-1, minotaur_col))
                              ]

    else:
    # Minotaur is on the edges, but not on angles -> p = 0.33
        if minotaur_row==1: #On the upper edge, no row up
            candidate_next_states = [(next_human_position, (minotaur_row, minotaur_col+1)),
                                     (next_human_position, (minotaur_row, minotaur_col-1)),
                                     (next_human_position, (minotaur_row+1, minotaur_col))
                                    ]
        elif minotaur_row==5: #Lower row, no row down
            candidate_next_states = [(next_human_position, (minotaur_row, minotaur_col+1)),
                                     (next_human_position, (minotaur_row, minotaur_col-1)),
                                     (next_human_position, (minotaur_row-1, minotaur_col))
                                    ]
        elif minotaur_col==1: #Left side, no col-1
            candidate_next_states = [(next_human_position, (minotaur_row, minotaur_col+1)),
                                     (next_human_position, (minotaur_row+1, minotaur_col)),
                                     (next_human_position, (minotaur_row-1, minotaur_col))
                                    ]
        elif minotaur_col==6: #Right side, no col+1
            candidate_next_states = [(next_human_position, (minotaur_row, minotaur_col-1)),
                                     (next_human_position, (minotaur_row+1, minotaur_col)),
                                     (next_human_position, (minotaur_row-1, minotaur_col))
                                    ]
    positions = []
    print("Human: {} Minotaur: {}".format(human_position, minotaur_position))
    for i in candidate_next_states:
        positions.append(lookup_dict[i])
    row[positions] = 1/len(candidate_next_states)
    return row

P = np.zeros( (stat_d,stat_d) )
for row in range(stat_d):
    P[row,:] = row_function(P[row,:], row)

print(P.shape)
P.tofile("P_down", sep=";")
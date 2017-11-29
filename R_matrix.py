import numpy as np

cells = [(i,j) for i in range(1,6) for j in range(1, 7)]
states = [(i,j) for i in cells for j in cells]
final_state = "F"
states.append(final_state)

human_actions = ["stay_still","right","down","left","up"]

stat_d = len(states)
action_d = len(human_actions)

state_lookup_dict = {states[i]:i for i in range(stat_d)}
action_lookup_dict = {human_actions[i]:i for i in range(action_d)}

winner_states = []
for i in states:
    human_position = i[0]
    if human_position == final_state: continue
    minotaur_position = i[1]
    if human_position == (5,5) and minotaur_position != (5,5):
        #i is winning state
        winner_states.append( state_lookup_dict[i] )

winner_action = action_lookup_dict["down"]

#Reward Matrix: Format (S, A)
R = np.zeros((stat_d,action_d))

R[winner_states,winner_action]=1

R.tofile("R", sep=";")
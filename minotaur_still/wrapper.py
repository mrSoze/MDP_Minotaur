import numpy as np
from mdptoolbox.mdp import FiniteHorizon as fh


P_stay_still = np.fromfile("P_stay_still", sep=";").reshape((901,901))
P_right = np.fromfile("P_right", sep=";").reshape((901,901))
P_down = np.fromfile("P_down", sep=";").reshape((901,901))
P_left = np.fromfile("P_left", sep=";").reshape((901,901))
P_up = np.fromfile("P_up", sep=";").reshape((901,901))
R = np.fromfile("R", sep=";").reshape((901,5))

P = np.array([ P_stay_still, P_right, P_down, P_left, P_up ])

mdp = fh(P, R, 1, 15)
mdp.run()

V15 = mdp.V[:,0]
policy15 = mdp.policy[:,0]

print(V15)
print(policy15)

V15.tofile("Value_at_T_15", sep="\n")
policy15.tofile("Policy_at_T_15", sep="\n")

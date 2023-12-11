import pandas as pd
import matplotlib.pyplot as plt
import random


def to_wound(stn, tghn):
    if 2*stn <= tghn:
        return 6
    elif stn < tghn:
        return 5
    elif stn == tghn:
        return 4
    elif 2*stn >= tghn:
        return 6
    else:
        return 5

def sequence(params):
    hits = 0
    wounds = 0
    failed_saves = 0
    damage = 0
    for i in range(params["attacks"]):
        if random.randrange(1,7) < params["to_hit"]:
            continue
        hits += 1
        if random.randrange(1,7) < to_wound(params["strength"],params["toughness"]):
            continue
        wounds +=1
        if random.randrange(1,7) < params["save"] + params["AP"]:
            failed_saves += 1
            damage += params["damage"]

    return {"total_attacks":params["attacks"],"hits":hits,"wounds":wounds,"failed saves":failed_saves,"damage taken":damage}



attacks = 30
to_hit = 4
strength = 4
toughness = 4
AP = 0
sv = 4
dmg = 1
sims = 5000
parameters={"toughness":toughness,
            "attacks":attacks,
            "to_hit":to_hit,
            "strength":strength,
            "AP":AP,
            "save":sv,
            "damage":dmg}
results = pd.DataFrame(columns=["total_attacks","hits","wounds","failed saves","damage taken"])

for j in range(sims):
    results.loc[len(results)] = sequence(parameters)
plt.hist(results["wounds"]/attacks,histtype="bar",range = (0,1))
plt.xlabel("#wounds in % of total attacks")
plt.ylabel("occurences")
plt.vlines(results["wounds"].mean()/attacks,ymin=0,ymax=3000,color='r')
plt.show()






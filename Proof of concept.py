import pandas as pd
import matplotlib.pyplot as plt
import random
import multiprocessing as mp







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

def roll_sequ(val,target,reroll_1,reroll_all,modifiers = 0):
    if val + modifiers >= target:
        return True
    elif val == 1 and reroll_1:
        return roll_sequ(random.randrange(1,7),target,False,False,modifiers)
    elif reroll_all:
        return roll_sequ(random.randrange(1,7),target,False,False,modifiers)
    else:
        return False

def sequence(params):
    hits = 0
    wounds = 0
    failed_saves = 0
    damage = 0
    for i in range(params["attacks"]):
        hit_roll = random.randrange(1,7)
        if not roll_sequ(hit_roll,params["to_hit"],params["rhits_1"],params["rhits_all"],params["hit_mod"]):
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
sims = 1000
rhits_1 = True
rhits_all = False
hit_mod = 0
if to_hit + hit_mod >=6: hit_mod =0
parameters={"toughness":toughness,
            "attacks":attacks,
            "to_hit":to_hit,
            "strength":strength,
            "AP":AP,
            "save":sv,
            "damage":dmg,
            "rhits_1":rhits_1,
            "rhits_all":rhits_all,
            "hit_mod":hit_mod}
results = pd.DataFrame(columns=["total_attacks","hits","wounds","failed saves","damage taken"])

for j in range(sims):
    results.loc[len(results)] = sequence(parameters)
print(results)
print(results["hits"].mean())
#plt.hist(results["wounds"]/attacks,histtype="bar",range = (0,1))
#plt.xlabel("#wounds in % of total attacks")
#plt.ylabel("occurences")
#plt.vlines(results["wounds"].mean()/attacks,ymin=0,ymax=3000,color='r')
#plt.show()






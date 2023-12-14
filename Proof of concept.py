import os

import pandas as pd
import matplotlib.pyplot as plt
import random

def simulation():
    Base_roll = Roll(attacks, to_hit, strength, hit_mods, wound_mods, AP, dmg,invulnerable_save)
    Base_roll.to_hit()
    Base_roll.wound_sequence(toughness)
    Base_roll.save_sequ(sv)
    results.loc[len(results)] = [attacks, Base_roll.no_hits, Base_roll.no_sust,
                                 Base_roll.no_lethal, Base_roll.no_wounds,
                                 Base_roll.no_crit_wounds, Base_roll.no_deva,
                                 Base_roll.fail_sv, Base_roll.tot_dmg]


class Roll:
    def __init__(self,attacks,target,strength,
                 hit_mods,wound_mods,AP,dmg,invul):
        self.attacks=attacks
        self.target = max(2,min(target - hit_mods["bon_hit"],6))
        self.strength = strength
        self.hit_mods = hit_mods
        self.wound_mods = wound_mods
        self.AP = AP
        self.dmg = dmg
        self.no_hits = 0
        self.no_wounds = 0
        self.no_sust = 0
        self.no_lethal = 0
        self.no_crit_wounds = 0
        self.no_deva = 0
        self.tot_dmg = 0
        self.fail_sv = 0
        self.invul = invul

    def wound_value(self,tghn):
        return max(2,min(6,to_wound(self.strength,tghn)-self.wound_mods["wound_mod"]))

    def to_hit(self):
        for j in range(self.attacks):
            hit_value = random.randrange(1,7)
            if hit_value >= self.target: #we need to hit
                self.no_hits += 1
                if hit_value >= self.hit_mods["crit_hit"] and \
                (self.hit_mods["sustained"] >0 or self.hit_mods["lethal"]): #we wound with a critical
                    self.no_hits += self.hit_mods["sustained"]
                    self.no_sust += self.hit_mods["sustained"]
                    self.no_lethal += self.hit_mods["lethal"]
                elif hit_value == 1 and self.hit_mods["rhits_1"]:
                    self.to_hit_reroll(random.randrange(1,7))
                elif self.hit_mods["rhits_all"]:
                    self.to_hit_reroll(random.randrange(1,7))
                else:
                    pass

    def to_hit_reroll(self,hit_value):
        if hit_value >= self.target:
            self.no_hits += 1
            if hit_value == self.hit_mods["crit_hit"] and \
            (self.hit_mods["sustained"] >0 or self.hit_mods["lethal"]):
                self.no_hits += self.hit_mods["sustained"]
                self.no_sust += self.hit_mods["sustained"]
                self.no_lethal += self.hit_mods["lethal"]

    def wound_sequence(self,toughness):
        for i in range(self.no_hits - self.no_lethal):
            wound_roll = random.randrange(1,7)
            if max(2,min(6,wound_roll + self.wound_mods["wound_mod"])) >= to_wound(self.strength,toughness):
                self.no_wounds += 1
                if wound_roll >= self.wound_mods["crit_wound"]:
                    self.no_crit_wounds += 1
                    if self.wound_mods["devastating"]:
                        self.no_deva += 1
                        self.tot_dmg += self.dmg
            elif (wound_roll == 1 and self.wound_mods["rwounds_1"]) \
            or self.wound_mods["rwounds_all"]:
                self.wound_roll_base(toughness)

    def wound_roll_base(self,toughness):
        wound_roll = random.randrange(1, 7)
        if max(2, min(6, wound_roll + self.wound_mods["wound_mod"])) >= to_wound(self.strength, toughness):
            self.no_wounds += 1
            if wound_roll >= self.wound_mods["crit_wound"]:
                self.no_crit_wounds += 1
                if self.wound_mods["devastating"]:
                    self.no_deva += 1
                    self.tot_dmg += self.dmg

    def save_sequ(self,save):
        if save + self.AP > 6 and self.invul > 6:
            self.tot_dmg = self.dmg * (self.no_wounds + self.no_lethal)
            self.fail_sv = self.no_wounds + self.no_lethal
        else:
            for i in range(self.no_wounds + self.no_lethal):
                if random.randrange(1,7) < min(self.invul,save + self.AP):
                    self.tot_dmg += self.dmg
                    self.fail_sv += 1

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


attacks = 30
to_hit = 4
strength = 4
toughness = 4
AP = 3
sv = 5
dmg = 1
sims = 100
rhits_1 = False
rhits_all = False
sustained = True
lethal = False
crit_hit = 6
crit_wound = 6
anti = 6
devastating = False
hit_mod = 0
wound_mod =0
rwounds_1 = False
rwounds_all = False
invulnerable_save = 4
hit_mods = {"rhits_1":rhits_1,
            "rhits_all":rhits_all,
            "crit_hit" :crit_hit,
            "sustained":sustained,
            "lethal":lethal,
            "bon_hit":hit_mod}

wound_mods = {"crit_wound":min(anti,crit_wound),
              "wound_mod":wound_mod,
              "devastating" : devastating,
              "rwounds_1" : rwounds_1,
              "rwounds_all" : rwounds_all}
results = pd.DataFrame(columns=["total_attacks",
                                "hits",
                                "sustained_hits",
                                "lethal hits",
                                "wounds",
                                "critical wounds",
                                "devastating wounds",
                                "failed saves","damage taken"])
if __name__ == '__main__':
    for i in range(sims):
        simulation()

    #print(results)
    #print(results["hits"].mean())
    var_to_study = results["failed saves"]/results["wounds"]
    plt.hist(var_to_study,bins = (0,0.2,0.4,0.6,0.8,1),histtype="bar",range = (0,1))
    plt.xlabel("#failed saves in % of total attacks")
    plt.ylabel("occurences")
    plt.axvline(results["failed saves"].mean()/results["wounds"].mean(),ymin=0,ymax=3000,color='r')
    plt.show()
    print(results["failed saves"].mean()/results["wounds"].mean())






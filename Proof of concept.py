import pandas as pd
import matplotlib.pyplot as plt
import random

#TODO : implement comparative analysis
#TODO : implement better graphs lmao
#TODO : implement i/o output to avoid running the simulation again

def simulation():
    Base_roll = Roll(attacks, to_hit, strength,
                     hit_mods, wound_mods,
                     AP, dmg,invulnerable_save,
                     wounds_per_model,fnp)
    Base_roll.to_hit()
    Base_roll.wound_sequence(toughness)
    Base_roll.save_sequ(sv)
    Base_roll.dmg_sequ()
    results.loc[len(results)] = [attacks, Base_roll.no_hits, Base_roll.no_sust,
                                 Base_roll.no_lethal, Base_roll.no_wounds,
                                 Base_roll.no_crit_wounds, Base_roll.no_deva,
                                 Base_roll.fail_sv, Base_roll.tot_dmg,Base_roll.models_killed]

#This class handles everything that is needed for one attack sequence
class Roll:
    def __init__(self,attacks,target,strength,
                 hit_mods,wound_mods,AP,dmg,invul,wpm,fnp):
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
        self.wpm = wpm
        self.fnp = fnp
        self.models_killed = 0
    #This makes sure that the wound roll (with modifiers) is bounded between 2 and 6
    def wound_value(self,tghn):
        return max(2,min(6,to_wound(self.strength,tghn)-self.wound_mods["wound_mod"]))
    #If an attack hits, before any rerolls (therefore includes the reroll modifiers)
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
                elif (hit_value == 1 and self.hit_mods["rhits_1"]) or self.hit_mods["rhits_all"]:
                    self.to_hit_reroll(random.randrange(1,7))
                else:
                    pass
    #This is if the reroll hits, therefore not allowing an extra reroll
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
                        self.fail_sv += 1
            elif (wound_roll == 1 and self.wound_mods["rwounds_1"]) \
            or self.wound_mods["rwounds_all"]:
                self.wound_roll_base(toughness)
    #Same as the hit roll, only in the case of a failed wound that is rerolled
    def wound_roll_base(self,toughness):
        wound_roll = random.randrange(1, 7)
        if max(2, min(6, wound_roll + self.wound_mods["wound_mod"])) >= to_wound(self.strength, toughness):
            self.no_wounds += 1
            if wound_roll >= self.wound_mods["crit_wound"]:
                self.no_crit_wounds += 1
                if self.wound_mods["devastating"]:
                    self.no_deva += 1
                    self.fail_sv += 1
    #Includes invulnerable saves
    def save_sequ(self,save):
        if save + self.AP > 6 and self.invul > 6:
            self.tot_dmg = self.dmg * (self.no_wounds + self.no_lethal)
            self.fail_sv = self.no_wounds + self.no_lethal
        else:
            for i in range(self.no_wounds + self.no_lethal):
                if random.randrange(1,7) < min(self.invul,save + self.AP):
                    self.tot_dmg += self.dmg
                    self.fail_sv += 1

    def dmg_sequ(self):
        attacks_left = self.fail_sv
        if self.fnp > 6:
            if self.dmg >= self.wpm:
                self.models_killed = attacks_left
            else:
                self.models_killed = self.dmg % self.wpm * attacks_left
        else:
            wounds_allocated = 0
            for j in range(attacks_left):
                wounds_allocated += self.feel_no_pain(self.dmg,self.fnp)
                if wounds_allocated >= self.wpm :
                    self.models_killed += 1
                    wounds_allocated = 0

    def feel_no_pain(self,dmg,value):
        failed = 0
        for i in range(dmg):
            if random.randrange(1,7) < value : failed += 1
        return failed

#Basic function to determine base wound value
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

#Parameters (will eventually be handled by the GUI)
attacks = 2
to_hit = 2
strength = 24
toughness = 12
AP = 5
sv = 2
dmg = 12
sims = 5000
rhits_1 = False
rhits_all = False
sustained = False
lethal = True
crit_hit = 6
crit_wound = 6
anti = 6
devastating = True
hit_mod = 0
wound_mod =0
rwounds_1 = False
rwounds_all = False
invulnerable_save = 7
wounds_per_model = 24
fnp = 7
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
                                "failed saves","damage taken","models killed"])
if __name__ == '__main__':
    for i in range(sims):
        simulation()

    #print(results)
    #print(results["hits"].mean())
    bins_sequ = (0,0.05,0.1,0.15,0.20,0.25,0.30,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1)
    var_to_study = results["damage taken"]
    plt.hist(var_to_study,histtype="bar")
    plt.xlabel("effective damage taken")
    plt.ylabel("occurences")
    plt.axvline(results["damage taken"].mean(),ymin=0,ymax=3000,color='r')
    plt.show()
    print(results["damage taken"].mean())






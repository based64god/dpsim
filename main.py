# kraken_damage takes a level, and a number of attacks, and returns the total damage done by the kraken, including the user's ad
def kraken_damage( level, num_attack=0, user_base_damage=0, kraken_multiplier=1):
    def kraken_proc_damage( level, kraken_multiplier=1 ):
        # if the level is less than 9, it is set to 8. this sets the minimum damage to 140.
        if level < 9:
            level = 8
        return int((140 + (17 * (level - 8))) * kraken_multiplier)
    total_damage = user_base_damage 
    if num_attack % 3 == 0:
        total_damage += kraken_proc_damage(level, kraken_multiplier)
    return total_damage

# bork_damage takes a hp value, and returns the total damage done by the blade of the ruined king, including the user's ad
def bork_damage( hp, user_base_damage=0):
    def bork_proc_damage( hp, ranged=False ):
        bork_chp_damage = 0.12
        if ranged:
            bork_chp_damage = 0.08
        return int(hp * bork_chp_damage)
    return int(max(bork_proc_damage(hp),15) + user_base_damage)

def phys_reduction(armor):
    return 100 / (100 + armor)

import argparse

parser = argparse.ArgumentParser(description='Calculate the number of autos to kill a target')
parser.add_argument('-k', '--kraken', action='store_true', help='Use kraken slayer')
parser.add_argument('-b', '--bork', action='store_true', help='Use blade of the ruined king')
args = parser.parse_args()
if not args.kraken and not args.bork:
    print("You must specify either --kraken or --bork")
    exit(1)
if args.kraken and args.bork:
    print("You cannot specify both --kraken and --bork")
    exit(1)
filename = "kraken.csv" if args.kraken else "bork.csv"
with open(filename, 'w') as f:
    f.write("hp,armor,level,ad,num_autos\n")
    max_iter = 6100
    for hp in range(100, max_iter, 100):
        print(f"{int(hp/max_iter*100)}%")
        for armor in range(0, 505, 5):
            for level in range(1, 19):
                for ad in range(0, 405, 5):
                    if args.kraken:
                        num_autos = 0
                        # auto the target until it dies
                        hp_copy = hp
                        kraken_mult = 1
                        while hp_copy > 0:
                            # attack the target
                            num_autos += 1
                            if num_autos % 3 == 0:
                                kraken_mult += 0.5
                            # calculate the damage of the auto attack, removing the damage from the target's hp, accounting for armor
                            hp_copy -= kraken_damage(level, num_attack=num_autos, user_base_damage=ad, kraken_multiplier= kraken_mult) * phys_reduction(armor)
                        f.write(f"{hp},{armor},{level},{ad},{num_autos}\n")
                    if args.bork:
                        num_autos = 0
                        # auto the target until it dies, again with blade of the ruined king
                        hp_copy = hp
                        while hp_copy > 0:
                            num_autos += 1
                            hp_copy -= bork_damage(hp_copy, user_base_damage=ad) * phys_reduction(armor)
                        f.write(f"{hp},{armor},{level},{ad},{num_autos}\n")

        
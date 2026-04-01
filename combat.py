from env import delete_file, group_by_zone
from agent import level_up

def process_combat(agents, actions):
    zones = group_by_zone()

    damage_map = {}

    # collect valid attacks (same zone only)
    for attacker in actions:
        action, target = actions[attacker]

        if action != "attack":
            continue

        if not agents[attacker]["alive"]:
            continue

        if target is None or not agents[target]["alive"]:
            continue

        # check same zone
        same_zone = False
        for z in zones:
            if attacker in zones[z] and target in zones[z]:
                same_zone = True
                break

        if not same_zone:
            continue

        if target not in damage_map:
            damage_map[target] = []

        damage_map[target].append(attacker)

    # apply damage
    for target in damage_map:
        total_damage = 0

        for attacker in damage_map[target]:
            total_damage += agents[attacker]["atk"]

        agents[target]["hp"] -= total_damage

    # handle deaths
    for file in agents:
        if agents[file]["alive"] and agents[file]["hp"] <= 0:
            agents[file]["alive"] = False
            attackers = damage_map.get(file, [])
            if len(attackers) > 0:
                print(f"{file} was killed by {attackers}")
                for attacker in attackers:
                    if agents[attacker]["alive"]:
                        level_up(agents[attacker])
            else:
                print(f"{file} died")
            delete_file(file)
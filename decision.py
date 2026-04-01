from env import group_by_zone
import random

def decide_actions(agents,storm_zones,chests):
    zones = group_by_zone()
    actions = {}

    for f in agents:
        if not agents[f]["alive"]:
            continue

        strategy = agents[f]["strategy"]

        zone = None
        for z in zones:
            if f in zones[z]:
                zone = z
                break

        if zone is None:
            actions[f] = ("idle", None)
            continue
        in_storm = zone in storm_zones
        has_chest = zone in chests and len(chests[zone]) > 0

        enemies = [x for x in zones[zone] if x != f and agents[x]["alive"]]
        possible = [f"Zone_{i}" for i in range(1,10) if f"Zone_{i}" != zone]

        # SIMPLE REFLEX
        if strategy == "simple":
            if enemies:
                actions[f] = ("attack", random.choice(enemies))
            else:
                actions[f] = ("move", random.choice(possible))

        # GREEDY
        elif strategy == "greedy":
            if enemies:
                target = min(enemies, key=lambda x: agents[x]["hp"])
                actions[f] = ("attack", target)
            else:
                actions[f] = ("move", random.choice(possible))

        # HEURISTIC
        elif strategy == "heuristic":
            if in_storm:
                actions[f]=("move",random.choice(possible))
            elif has_chest:
                actions[f]=("idle",None)
            elif agents[f]["hp"]<40:
                actions[f]=("move",random.choice(possible))
            elif enemies:
                target=min(enemies,key=lambda x:agents[x]["level"])
                actions[f]=("attack",target)
            else:
                actions[f]=("move",random.choice(possible))

        # HYBRID
        else:
            if in_storm:
                actions[f]=("move",random.choice(possible))
            elif enemies:
                weaker=[x for x in enemies if agents[x]["level"]<=agents[f]["level"]]
                if weaker:
                    target=min(weaker,key=lambda x:agents[x]["hp"])
                else:
                    target=min(enemies,key=lambda x:agents[x]["hp"])
                actions[f]=("attack",target)
            elif has_chest:
                actions[f]=("idle",None)
            else:
                actions[f]=("move",random.choice(possible))

    return actions
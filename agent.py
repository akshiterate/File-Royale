import random
from env import scan_arena, group_by_zone
def initialize_agents():
    files = scan_arena()
    agents = {}

    for file in files:
        agents[file] = {
            "hp": 100,
            "atk": 20,
            "alive": True,
            "level": 1,
            "memory": {
                "zones_visited": set(),
                "agents_seen": set(),
                "agents_levels": {}
            }
        }

    return agents


def update_memory(agents):
    zones = group_by_zone()

    for zone in zones:
        files = zones[zone]

        for file in files:
            if not agents[file]["alive"]:
                continue

            # update zones visited
            agents[file]["memory"]["zones_visited"].add(zone)

            # update agents seen
            for other in files:
                if other != file:
                    agents[file]["memory"]["agents_seen"].add(other)
                    agents[file]["memory"]["agents_levels"][other] = agents[other]["level"]

def decide_actions(agents):
    zones = group_by_zone()
    actions = {}

    for file in agents:
        if not agents[file]["alive"]:
            continue

        zone = None
        for z in zones:
            if file in zones[z]:
                zone = z
                break

        if zone is None:
            actions[file] = ("idle", None)
            continue

        files_in_zone = zones[zone]

        targets = []
        for f in files_in_zone:
            if f != file and agents[f]["alive"]:
                targets.append(f)

        if len(targets) > 0:
            target = random.choice(targets)
            actions[file] = ("attack", target)
        else:
            # no enemies → move
            possible_zones = [f"Zone_{i}" for i in range(1,10) if f"Zone_{i}" != zone]
            new_zone = random.choice(possible_zones)
            actions[file] = ("move", new_zone)

    return actions

def level_up(agent):
    agent["level"] += 1
    agent["atk"] += 20
    agent["hp"] += 40
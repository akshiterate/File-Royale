import random
from env import scan_arena,group_by_zone

def initialize_agents():
    files=scan_arena()
    agents={}
    for f in files:
        agents[f]={
            "hp":100,
            "atk":5,
            "alive":True,
            "level":1,
            "memory":{
                "zones_visited":set(),
                "agents_seen":set(),
                "agents_levels":{}
            }
        }
    return agents

def update_memory(agents):
    zones=group_by_zone()
    for z in zones:
        files=zones[z]
        for f in files:
            if not agents[f]["alive"]:
                continue
            agents[f]["memory"]["zones_visited"].add(z)
            for o in files:
                if o!=f:
                    agents[f]["memory"]["agents_seen"].add(o)
                    agents[f]["memory"]["agents_levels"][o]=agents[o]["level"]

def decide_actions(agents):
    zones=group_by_zone()
    actions={}
    for f in agents:
        if not agents[f]["alive"]:
            continue
        zone=None
        for z in zones:
            if f in zones[z]:
                zone=z
                break
        if zone is None:
            actions[f]=("idle",None)
            continue
        targets=[x for x in zones[zone] if x!=f and agents[x]["alive"]]
        if targets:
            actions[f]=("attack",random.choice(targets))
        else:
            possible=[f"Zone_{i}" for i in range(1,10) if f"Zone_{i}"!=zone]
            actions[f]=("move",random.choice(possible))
    return actions

def level_up(agent):
    agent["level"]+=1
    agent["atk"]+=10
    agent["hp"]+=80
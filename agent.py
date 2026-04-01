import random
from env import scan_arena,group_by_zone

def initialize_agents():
    files=scan_arena()
    agents={}
    for f in files:
        agents[f]={
            "hp":random.randint(90,150),
            "atk":random.randint(3,8),
            "alive":True,
            "level":1,
            "strategy": random.choice(["simple","greedy","heuristic","hybrid"]),
            "memory":{
                "zones_visited":set(),
                "agents_seen":set(),
                "agents_levels":{},
                "agents_hp": {}
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
                    agents[f]["memory"]["agents_hp"][o]=agents[o]["hp"]

def level_up(agent):
    agent["level"]+=1
    agent["atk"]+=10
    agent["hp"]+=80
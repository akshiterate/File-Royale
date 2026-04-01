from env import delete_file,group_by_zone
from agent import level_up

def process_combat(agents,actions):
    zones=group_by_zone()
    damage_map={}
    for a in actions:
        act,t=actions[a]
        if act!="attack":
            continue
        if not agents[a]["alive"]:
            continue
        if t is None or not agents[t]["alive"]:
            continue
        same=False
        for z in zones:
            if a in zones[z] and t in zones[z]:
                same=True
                break
        if not same:
            continue
        if t not in damage_map:
            damage_map[t]=[]
        damage_map[t].append(a)
    for t in damage_map:
        dmg=sum(agents[a]["atk"] for a in damage_map[t])
        agents[t]["hp"]-=dmg
    for f in agents:
        if agents[f]["alive"] and agents[f]["hp"]<=0:
            agents[f]["alive"]=False
            attackers=damage_map.get(f,[])
            if attackers:
                print(f"{f} was killed by {attackers}")
                for a in attackers:
                    if agents[a]["alive"]:
                        level_up(agents[a])
            else:
                print(f"{f} died")
            delete_file(f)
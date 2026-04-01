from env import setup,group_by_zone,move_files,get_chests_in_zone,remove_chest,spawn_chest
from agent import initialize_agents,update_memory,level_up
from combat import process_combat
import random
from decision import decide_actions

def main():
    print("Setting up arena...")
    setup()
    input("Add files to zones, then press Enter...")
    agents=initialize_agents()
    storm_zones=set()
    all_zones=[f"Zone_{i}" for i in range(1,10)]
    tick=1
    for _ in range(3):
        spawn_chest()
    while True:
        print(f"\n--- Tick {tick} ---")
        if tick==3:
            storm_zones.update(random.sample(all_zones,3))
            print("Storm expanded to:",storm_zones)

        if tick==8:
            remaining=[z for z in all_zones if z not in storm_zones]
            storm_zones.update(random.sample(remaining,4))
            print("Storm expanded to:",storm_zones)
        update_memory(agents)
        print("\nDecision Phase")
        chests=get_chests_in_zone()
        actions=decide_actions(agents,storm_zones,chests)
        print_actions(actions)
        print("\nMovement Phase")
        process_movement(actions,agents)
        process_idle(actions,agents)
        process_storm(agents,storm_zones)
        process_chests(agents)
        print("\nCombat Phase")
        process_combat(agents,actions)
        print("\nAgent States")
        print_agents(agents)
        alive=[a for a in agents if agents[a]["alive"]]
        if len(alive)<=1:
            print("\nGame Over")
            if len(alive)==1:
                print("Winner:",alive[0])
            else:
                print("No winner (all agents died)")
            break
        tick+=1
        input("\nPress Enter for next tick...")

def process_movement(actions,agents):
    for f in actions:
        act,t=actions[f]
        if not agents[f]["alive"]:
            continue
        if act=="move":
            move_files(f,t)
            agents[f]["hp"]-=1

def process_idle(actions,agents):
    for f in actions:
        act,_=actions[f]
        if not agents[f]["alive"]:
            continue
        if act=="idle":
            agents[f]["hp"]-=2

def process_chests(agents):
    zones=group_by_zone()
    chests=get_chests_in_zone()
    for z in zones:
        if z not in chests or not chests[z]:
            continue
        alive=[f for f in zones[z] if agents[f]["alive"]]
        if len(alive)==1:
            f=alive[0]
            c=chests[z][0]
            print(f"{f} opened {c} in {z}")
            level_up(agents[f])
            remove_chest(z,c)

def print_agents(agents):
    print("\nAgent States:")
    for f in agents:
        d=agents[f]
        s="Alive" if d["alive"] else "Dead"
        print(f"{f} | HP: {d['hp']} | {s} | {d['strategy']}")

def print_actions(actions):
    print("\nActions:")
    for f in actions:
        act,t=actions[f]
        if act=="attack":
            print(f"{f} -> attacks {t}")
        elif act=="move":
            print(f"{f} -> moves to {t}")
        else:
            print(f"{f} -> idle")
def process_storm(agents,storm_zones):
    zones=group_by_zone()
    for z in zones:
        if z not in storm_zones:
            continue
        for f in zones[z]:
            if agents[f]["alive"]:
                agents[f]["hp"]-=10
                print(f"{f} took storm damage in {z}")
if __name__=="__main__":
    main()
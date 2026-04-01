from env import setup,group_by_zone,move_files,get_chests_in_zone,remove_chest,spawn_chest
from agent import initialize_agents,decide_actions,update_memory,level_up
from combat import process_combat
import random

def main():
    print("Setting up arena...")
    setup()
    input("Add files to zones, then press Enter...")
    agents=initialize_agents()
    tick=1
    while True:
        print(f"\n--- Tick {tick} ---")
        update_memory(agents)
        if random.random()<0.3:
            spawn_chest()
        print("\nDecision Phase")
        actions=decide_actions(agents)
        print_actions(actions)
        print("\nMovement Phase")
        process_movement(actions,agents)
        process_idle(actions,agents)
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
            agents[f]["hp"]-=5

def process_idle(actions,agents):
    for f in actions:
        act,_=actions[f]
        if not agents[f]["alive"]:
            continue
        if act=="idle":
            agents[f]["hp"]-=10

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
        print(f"{f} | HP: {d['hp']} | {s}")

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

if __name__=="__main__":
    main()
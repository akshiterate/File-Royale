from env import setup, scan_arena, group_by_zone
from agent import initialize_agents, decide_actions ,update_memory
from combat import process_combat
from env import move_files
from env import get_chests_in_zone, remove_chest, spawn_chest
from agent import level_up
import random
def main():
    print("Setting up arena...")
    setup()

    input("Add files to zones, then press Enter...")

    agents = initialize_agents()

    tick = 1

    while True:
        print(f"\n--- Tick {tick} ---")

        update_memory(agents)
        if random.random() < 0.3:
            spawn_chest()
        print("\nDecision Phase")
        actions = decide_actions(agents)
        print_actions(actions)

        print("\nMovement Phase")
        process_movement(actions,agents)
        process_idle(actions,agents)
        
        process_chests(agents)

        print("\nCombat Phase")
        process_combat(agents, actions)

        print("\nAgent States")
        print_agents(agents)
        # check end condition
        alive_agents = [a for a in agents if agents[a]["alive"]]
        if len(alive_agents) <= 1:
            print("\nGame Over")
            if len(alive_agents) == 1:
                print("Winner:", alive_agents[0])
            elif len(alive_agents) == 0:
                print("No winner (all agents died)")
            break

        tick += 1

        input("\nPress Enter for next tick...")

def process_movement(actions, agents):
    for file in actions:
        action, target = actions[file]

        if not agents[file]["alive"]:
            continue

        if action == "move":
            move_files(file, target)
            agents[file]["hp"] -= 5
def process_idle(actions, agents):
    for file in actions:
        action, _ = actions[file]

        if not agents[file]["alive"]:
            continue

        if action == "idle":
            agents[file]["hp"] -= 10
def print_agents(agents):
    print("\nAgent States:")

    for file in agents:
        data = agents[file]

        status = "Alive" if data["alive"] else "Dead"

        print(f"{file} | HP: {data['hp']} | {status}")
def print_actions(actions):
    print("\nActions:")

    for file in actions:
        action, target = actions[file]

        if action == "attack":
            print(f"{file} -> attacks {target}")
        elif action == "move":
            print(f"{file} -> moves to {target}")
        else:
            print(f"{file} -> idle")
def process_chests(agents):
    zones = group_by_zone()
    chests = get_chests_in_zone()

    for zone in zones:
        if zone not in chests or len(chests[zone]) == 0:
            continue

        alive_agents = [f for f in zones[zone] if agents[f]["alive"]]

        # only one agent can open
        if len(alive_agents) == 1:
            agent = alive_agents[0]
            chest = chests[zone][0]

            print(f"{agent} opened {chest} in {zone}")

            level_up(agents[agent])
            remove_chest(zone, chest)
if __name__ == "__main__":
    main()
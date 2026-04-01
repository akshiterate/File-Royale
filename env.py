import os
import shutil
import random
def setup():
    if os.path.exists("ARENA"):
        shutil.rmtree("ARENA")
    os.mkdir("ARENA")
    for zone in range(1,10):
        os.mkdir(f"ARENA/Zone_{zone}")

def scan_arena():
    files = {}
    with os.scandir('ARENA/') as dirs:
        for dir in dirs:
            if dir.is_dir():
                with os.scandir(f'{dir.path}/') as zone:
                    for file in zone:
                        if file.is_file() and not file.name.endswith(".chest"):
                            files[file.name] = dir.name
    return files
def move_files(file,new_zone):
    files = scan_arena()
    zone = files[file]
    print(f"FROM: ARENA/{zone}/{file}")
    print(f"TO:   ARENA/{new_zone}/{file}")
    shutil.move(f"ARENA/{zone}/{file}",f"ARENA/{new_zone}/{file}")
def delete_file(file):
    files = scan_arena()
    zone = files[file]
    os.remove(f"ARENA/{zone}/{file}")
def group_by_zone():
    files = scan_arena()
    zones = {}
    for file, zone in files.items():
        if zone not in zones:
            zones[zone] = []
        zones[zone].append(file)
    return zones


chest_counter = 1
def spawn_chest():
    global chest_counter

    zone = f"ARENA/Zone_{random.randint(1,9)}"
    existing = get_chests_in_zone()
    zone_name = zone.split("/")[-1]
    if len(existing.get(zone_name, [])) > 0:
        return
    chest_name = f"chest_{chest_counter}.chest"

    open(f"{zone}/{chest_name}", "w").close()

    chest_counter += 1

def get_chests_in_zone():
    zones = {}

    with os.scandir('ARENA/') as dirs:
        for dir in dirs:
            if dir.is_dir():
                zones[dir.name] = []

                with os.scandir(dir.path) as files:
                    for file in files:
                        if file.is_file() and file.name.endswith(".chest"):
                            zones[dir.name].append(file.name)

    return zones
def remove_chest(zone, chest):
    os.remove(f"ARENA/{zone}/{chest}")
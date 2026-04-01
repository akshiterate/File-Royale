import os
import shutil
import random

def setup():
    if os.path.exists("ARENA"):
        shutil.rmtree("ARENA")
    os.mkdir("ARENA")
    for i in range(1,10):
        os.mkdir(f"ARENA/Zone_{i}")

def scan_arena():
    files={}
    with os.scandir("ARENA/") as dirs:
        for d in dirs:
            if d.is_dir():
                with os.scandir(d.path) as zone:
                    for f in zone:
                        if f.is_file() and not f.name.endswith(".chest"):
                            files[f.name]=d.name
    return files

def move_files(file,new_zone):
    files=scan_arena()
    zone=files[file]
    print(f"FROM: ARENA/{zone}/{file}")
    print(f"TO:   ARENA/{new_zone}/{file}")
    shutil.move(f"ARENA/{zone}/{file}",f"ARENA/{new_zone}/{file}")

def delete_file(file):
    files=scan_arena()
    zone=files[file]
    os.remove(f"ARENA/{zone}/{file}")

def group_by_zone():
    files=scan_arena()
    zones={}
    for f,z in files.items():
        if z not in zones:
            zones[z]=[]
        zones[z].append(f)
    return zones

chest_counter=1

def spawn_chest():
    global chest_counter
    zone=f"ARENA/Zone_{random.randint(1,9)}"
    existing=get_chests_in_zone()
    name=zone.split("/")[-1]
    if len(existing.get(name,[]))>0:
        return
    chest=f"chest_{chest_counter}.chest"
    open(f"{zone}/{chest}","w").close()
    chest_counter+=1

def get_chests_in_zone():
    zones={}
    with os.scandir("ARENA/") as dirs:
        for d in dirs:
            if d.is_dir():
                zones[d.name]=[]
                with os.scandir(d.path) as files:
                    for f in files:
                        if f.is_file() and f.name.endswith(".chest"):
                            zones[d.name].append(f.name)
    return zones

def remove_chest(zone,chest):
    os.remove(f"ARENA/{zone}/{chest}")
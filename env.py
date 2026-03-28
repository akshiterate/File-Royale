import os
import shutil
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
                        if file.is_file():
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


def main():
    print("hi")
    scan_arena()
    move_files("gay.pp","Zone_1")
    delete_file("man.dick")
if __name__ == "__main__":
    main()
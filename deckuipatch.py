from pathlib import Path, PurePosixPath, PureWindowsPath
from enum import Enum
import subprocess
import argparse
import platform
import os

class Systems(Enum):
    Lin: str = "Linux"
    Win: str = "Windows"
    Mac: str = "Darwin"
    Unknown: str = "Unknown"

PATCH_CONTENTS: str = "steampal_stable_9a24a2bf68596b860cb6710d9ea307a76c29a04d"
WIN_PATH = PureWindowsPath("C:", "Program Files (x86)", "Steam")
LIN_PATH = Path.home() / PurePosixPath(".steam", "steam")
LIN_FLATPAK_PATH = Path.home() / PurePosixPath(".var", "app", "com.valvesoftware.Steam", ".steam", "steam")

SYSTEM: Systems = Systems.Unknown

def os_steam_path() -> str:
    global SYSTEM 
    opsys = platform.system()
    if opsys == Systems.Lin.value:
        SYSTEM = Systems.Lin 
        return Path(LIN_PATH) 
    elif opsys == Systems.Win.value:
        SYSTEM = Systems.Win
        return Path(WIN_PATH)
    elif opsys == Systems.Mac.value:
        SYSTEM = Systems.Mac
        raise OSError("MacOS is not supported!")
    else:
        raise OSError("Unknown OS detected!")

def launch_steam(path, is_flatpak) -> None:
    os.chdir(path)
    if SYSTEM == Systems.Win: 
        subprocess.Popen(["./steam.exe", "-gamepadui"], shell=False)
        return

    if is_flatpak:
        subprocess.Popen(["flatpak", "run", "com.valvesoftware.Steam", "-gamepadui"], shell=False)
        return

    subprocess.Popen(["./steam.sh", "-gamepadui"], shell=False)
    return

def write_patch(path: Path) -> None:
    try: path.write_text(PATCH_CONTENTS)
    except IOError as e: raise IOError(e)

def read_patch(path: Path) -> str:
    try: return path.read_text()
    except IOError as e: raise IOError(e)

def remove_patch(path: Path) -> None:
    try: os.remove(path)
    except FileNotFoundError: raise FileNotFoundError("There is no existing patch file to remove!")
    except IOError as e: raise IOError(e)

def parse_args():

    parser = argparse.ArgumentParser(description="Patches the steamdeck UI into desktop steam.")
    parser.add_argument("path", type=str, default=os_steam_path(), nargs='?', help="Path to your local steam install.")
    parser.add_argument("-r", "--remove", action="store_true", required=False, help="Removes the steamdeck ui patch from steam.")
    parser.add_argument("-f", "--flatpak", action="store_true", required=False, help="Tells the patch tool to look for a flatpak install of steam.")
    parser.add_argument("-l", "--launch", action="store_true", required=False, help="Launches steam in deck mode after patch.")
    try: args = parser.parse_args()
    except argparse.ArgumentError as e: raise argparse.ArgumentError(e)

    remove, flatpak, launch = False, False, False
    if args.remove: remove = True
    if args.flatpak: flatpak = True
    if args.launch: launch = True

    return (Path(args.path), remove, flatpak, launch)

def main() -> None:

    path, remove, flatpak, launch = parse_args()

    if not os.path.isdir(path):
        raise OSError("Steam path for your operating system was not found!")

    patch_file = path / "package" / "beta"

    if remove:
        print("[INFO] Removing Patch...")
        remove_patch(patch_file)
        print("[SUCCESS] Removed Patch!")
        return

    if os.path.isfile(patch_file):
        patch_file_contents = read_patch(patch_file)
        if patch_file_contents == PATCH_CONTENTS:
            print("[INFO] Existing patch already found.")
            if launch: 
                print("[INFO] Launching Steam...")
                launch_steam(path, flatpak)
            return
        
        print("[INFO] Existing path file found was corrupted. Rewriting...")
    
    print("[INFO] Writing patch...")
    write_patch(patch_file)
    print("[SUCCESS] UI patch was written successfully")

    if launch:
        print("[INFO] Launching Steam...")
        launch_steam(path, flatpak)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: exit()
    except Exception as e:
        print(f"[ERROR] Program failed with response: {e}")

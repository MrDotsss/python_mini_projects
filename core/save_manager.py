import json
import os

save_path: str = "saves"

def save_exists(mode_name: str) -> bool:
    mode_path: str = f"{save_path}/{mode_name}.json"
    return os.path.exists(mode_path) and os.path.isfile(mode_path)

def save_state(save_object: dict, mode_name: str) -> bool:
    mode_path: str = f"{save_path}/{mode_name}.json"
    try:
        with open(mode_path, "w") as file:
            json.dump(save_object, file, indent=4)
            return True
    except PermissionError:
        print(f"Error: You do not have permission to save {mode_name} | {mode_path}")
        return False
    except IsADirectoryError:
        print(f"Error: The specified path for {mode_name} is a directory, not a file | {mode_path}")
        return False
    except OSError as e:
        print(f"System Error: Unable to write file for {mode_name}. Details: {e}")
        return False

def load_state(mode_name: str) -> tuple[bool, dict]:
    mode_path: str = f"{save_path}/{mode_name}.json"
    try:
        with open(mode_path, "r") as file:
            content = json.load(file)
            return True, content
    except FileNotFoundError:
        print(f"Error: The specified save for {mode_name} does not exist.")
        return False, {}
    except PermissionError:
        print(f"Error: You do not have permission to read this file for {mode_name}.")
        return False, {}
    except UnicodeDecodeError:
        print(f"Error: File contains characters that cannot be decoded for {mode_name}.")
        return False, {}
    except IsADirectoryError:
        print(f"Error: The path points to a directory, not a file for {mode_name}.")
        return False, {}
    except OSError as e:
        print(f"System Error: Unable to read file for {mode_name}. Details: {e}")
        return False, {}

def clear_save(mode_name: str) -> bool:
    mode_path: str = f"{save_path}/{mode_name}.json"
    try:
        os.remove(mode_path)
        return True
    except FileNotFoundError:
        print("Delete failed: The file does not exist.")
        return True
    except PermissionError:
        print("Delete failed: File is locked by another program or access is denied.")
        return True
    except IsADirectoryError:
        print("Delete failed: The path points to a folder, not a file.")
        return True
    except OSError as e:
        print(f"Delete failed due to a system error: {e}")
        return True
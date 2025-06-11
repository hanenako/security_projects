import json
import os
from datetime import datetime

SNAPSHOT_DIR = "snapshots"

def save_snapshot(hash_data: dict) -> str:
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    filename = f"{datetime.now().strftime('%Y-%m-%d_%H%M%S')}-snapshot.json"
    path = os.path.join(SNAPSHOT_DIR, filename)
    with open(path, "w") as f:
        json.dump(hash_data, f, indent=2)
    return path

def load_snapshot(file_path: str) -> dict:
    with open(file_path, "r") as f:
        return json.load(f)

def compare_snapshots(old: dict, new: dict) -> dict:
    added = {f: h for f, h in new.items() if f not in old}
    removed = {f: h for f, h in old.items() if f not in new}
    modified = {f: (old[f], new[f]) for f in old if f in new and old[f] != new[f]}
    return {
        "added": added,
        "removed": removed,
        "modified": modified
    }

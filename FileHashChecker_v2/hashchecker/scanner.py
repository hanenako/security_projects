import hashlib
from pathlib import Path

def calculate_hash(file_path: Path, method='sha256'):
    h = hashlib.new(method)
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def scan_directory(dir_path: str, method='sha256'):
    hash_dict = {}
    for path in Path(dir_path).rglob('*'):
        if path.is_file():
            hash_dict[str(path)] = calculate_hash(path, method)
    return hash_dict
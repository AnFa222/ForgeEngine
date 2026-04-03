import json

def save_text(path, data):
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)

def load_text(path, default=""):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return default


def save_binary(path, data):
    with open(path, "wb") as f:
        f.write(data)

def load_binary(path, default=b""):
    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return default
    

def save_json(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)

def load_json(path, default=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default
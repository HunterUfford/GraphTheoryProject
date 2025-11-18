# utils/json_store.py
import json

# save data to a JSON files
def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# load data from a JSON file
def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

import json
import os

STATE_DIR = "data"
STATE_FILE = os.path.join(STATE_DIR, "current_video.json")


def load_state():

    if not os.path.exists(STATE_FILE):
        return {}

    with open(STATE_FILE, "r") as file:
        return json.load(file)


def save_state(data):

    os.makedirs(STATE_DIR, exist_ok=True)

    with open(STATE_FILE, "w") as file:
        json.dump(data, file, indent=4)
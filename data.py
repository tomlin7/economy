"""
data management class
"""

import json

try:
    file = open("money.json", "r")
    data = json.load(file)
    users = data['users']
    file.close()
except FileNotFoundError:
    print("data not found")
    _data = {"users": {"default_user": {"id": 0, "score": 0}}}
    _users = _data['users']
    json.dump(_data, open("money.json", "w"), indent=4)


def sync_data():
    global file
    global data
    global users
    file = open("money.json", "r")
    data = json.load(file)
    users = data['users']
    file.close()

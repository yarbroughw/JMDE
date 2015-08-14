""" Retrieve dataset of instances for training/testing. """

import json

def instances():
    with open("../data/instances.json") as f:
        return json.load(f)

def properties(instance):
    return instance["properties"].keys()

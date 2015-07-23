import json
import random


def dropentities(category, num):
    with open("../data/flatontology.json", 'r') as f:
        flatontology = json.load(f)
    categorypath = flatontology[category]["fullpath"]

    with open("../data/" + categorypath + "fileindex.json", 'r') as f:
        fileindex = json.load(f)

    for key in random.sample(fileindex.keys(), num):
        del fileindex[key]


if __name__ == "__main__":
    dropentities("CareerStation", 10)

''' script for making directory structure of dbpedia ontology '''

from __future__ import print_function
import json
import os


def makeDirectories(ontologyDict):
    for value in ontologyDict:
        directory = "../mockdata/" + value["fullpath"]
        print("making directory", directory, " ...", end='')
        os.mkdir(directory)
        with open(directory+"/fileindex.json", 'a') as indexfile:
            d = {}
            json.dump(d, indexfile)
        print("done.")
        makeDirectories(value["children"])

with open("../data/nestedontology.json", 'r') as ontologyFile:
    ontology = json.load(ontologyFile)

makeDirectories(ontology)

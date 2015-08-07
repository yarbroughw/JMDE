
''' copy entities in owl:Thing fileindex to all
    fileindexes below
'''

from __future__ import print_function
import json


def makefileindexes(ontologyDict):
    for value in ontologyDict:
        directory = "../data/" + value["fullpath"]
        print("making fileindex", directory, " ...", end='')
        with open(directory+"/fileindex.json", 'w') as indexfile:
            d = {}
            json.dump(d, indexfile)
        print("done.")
        makefileindexes(value["children"])

with open("../data/nestedontology.json", 'r') as ontologyFile:
    ontology = json.load(ontologyFile)

makefileindexes(ontology[0]["children"])

with open("../data/owl:Thing/fileindex.json", 'r') as f:
    filedict = json.load(f)

# write each entry to appropriate fileindexes
for name, path in filedict.items():
    x = path.split('/')[:-2]
    fullpaths = ['/'.join(x[:i+1]) for i, _ in enumerate(x)][1:]
    for i, fullpath in enumerate(fullpaths):
        with open('../data/' + fullpath + '/fileindex.json', 'r') as f:
            index = json.load(f)
        index[name] = path
        with open('../data/' + fullpath + '/fileindex.json', 'w') as f:
            json.dump(index, f)
    print('wrote', name, 'to', ', '.join(x[1:]), "fileindexes")

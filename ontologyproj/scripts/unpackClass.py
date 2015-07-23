''' takes dbpedia CSV class file and splits it
    into separate, cleaned entity files
'''

from __future__ import print_function
import json
import csv
import glob
from itertools import count

ontologyprefix = "http://dbpedia.org/ontology/"
resourceprefix = "http://dbpedia.org/resource/"
itemprefix = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
with open("../data/flatontology.json", 'r') as flat:
    ontology = json.load(flat)
ontology_labels = list(ontology.keys())


def toName(url):
    return url[len(ontologyprefix):]


def csvinstances(path, skip=1):
    with open(path, 'r') as classfile:
        dicts = csv.DictReader(classfile)
        labelURIs = next(dicts)     # field label URIs
        next(dicts)     # field types      (unneeded)
        next(dicts)     # field type URIs  (unneeded)
        for i, instance in zip(count(start=0), dicts):
            if i % skip == 0:
                yield cleanCSVinstance(instance, labelURIs)


def cleanCSVinstance(instance, labeldict):
    tolist = lambda x: x[1:-1].split('|')

    newinstance = {"properties": {}}
    for key, value in instance.items():
        if labeldict[key].startswith(ontologyprefix):
            newinstance["properties"][key] = value
            if value[0] == '{':
                newinstance["properties"][key] = tolist(value)

    typelabel = "22-rdf-syntax-ns#type"
    newinstance[typelabel] = tolist(instance[typelabel])

    uri = instance["URI"]
    newinstance["URI"] = uri
    newinstance["name"] = uri[len(resourceprefix):].replace('/', '-')

    return newinstance


def writeInstances(instances, dest):
    ''' stream of all instances in file '''
    for instance in instances:
        writeEntity(instance, dest)


def writeEntity(instance, dest):
    entity = buildEntity(instance)
    if len(entity['properties']) > 2:
        deepest = getFinestOntology(entity['ontologies'])
        path = ontology[toName(deepest)]['fullpath']
        write(entity, dest, path)
        addToIndexes(entity, dest, path)


def buildEntity(instance):
    return {'URI': instance["URI"],
            'name': instance["name"],
            'properties': getProperties(instance),
            'ontologies': getOntologies(instance)}


def getProperties(instance):
    ''' returns dict of all properties in instance '''

    validproperty = lambda key, val: not key.endswith("_label") \
        and key != "wikiPageRevisionID" \
        and key != "wikiPageID" \
        and key != "wikiPageRedirects" \
        and key != "22-rdf-syntax-ns#type" \
        and key != "thumbnail" \
        and val != "NULL"

    allprops = instance["properties"]
    properties = {key: val for key, val in allprops.items()
                  if validproperty(key, val)}
    return properties


def getOntologies(instance):
    ''' construct list of ontology refs in instance '''
    ontologyrefs = instance["22-rdf-syntax-ns#type"]
    return [x for x in ontologyrefs
            if x.startswith(ontologyprefix)
            and x[len(ontologyprefix):] in ontology_labels]


def getFinestOntology(refs):
    ''' take list of ontology classes and return deepest one '''
    getdepth = lambda ref: ontology[toName(ref)]['depth']
    return max(refs, key=getdepth)


def write(entity, dest, path):
    ''' write entity to JSON file at path '''
    name = entity['name']
    fullname = dest + path + name + ".json"
    with open(fullname, 'w') as fp:
        json.dump(entity, fp)
    print("wrote", name, "...", end='')


def addToIndexes(entity, dest, path):
    paths = path.split('/')[:-2]
    fullpaths = ['/'.join(paths[:i+1]) for i, _ in enumerate(paths)]
    for p in fullpaths:
        addToIndex(entity, dest+p, path)
    print("added to parent fileindexes")


def addToIndex(entity, dest, path):
    ''' add name and filepath to file index at dest '''
    this_entity = entity['name']
    val = path + entity['name'] + ".json"

    with open(dest+"/fileindex.json", 'r') as f:
        index = json.load(f)
    index[this_entity] = val
    with open(dest+"/fileindex.json", 'w') as f:
        json.dump(index,  f,  indent=4)


def unpackAll():
    # load progress file
    with open("../data/csv/progress.json", 'r') as f:
        progress = set(json.load(f))

    files = glob.glob("../data/csv/*.csv")
    files = set(map(lambda x: x.split('/')[-1], files))

    remaining = files - progress

    for x in remaining:
        print("Unpacking", x, "...")
        instances = csvinstances("../data/csv/" + x, skip=500)
        writeInstances(instances, "../data/")
        progress.add(x)
        with open("../data/csv/progress.json", 'w') as f:
            json.dump(list(progress), f)


def unpack(x, skip=1):
    x = x + ".csv"
    instances = csvinstances("../data/csv/" + x, skip=skip)
    writeInstances(instances, "../data/")

if __name__ == "__main__":
    unpack("Food", 1)
    unpack("Sales", 1)
    unpack("Holiday", 1)
    unpack("Colour", 1)
    unpack("Biomolecule", 10)

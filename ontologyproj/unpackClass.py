''' takes dbpedia CSV class file and splits it
    into separate, cleaned entity files
'''

from __future__ import print_function
import json
import csv
from itertools import count

ontologyprefix = "http://dbpedia.org/ontology/"
resourceprefix = "http://dbpedia.org/resource/"
itemprefix = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
with open("../data/flatontology.json", 'r') as flat:
    ontology = json.load(flat)


def toName(url):
    return url[len(ontologyprefix):]


def csvinstances(path, skip=1):
    with open(path, 'r') as classfile:
        dicts = csv.DictReader(classfile)
        labelURIs = next(dicts)     # field label URIs
        next(dicts)     # field types      (unneeded)
        next(dicts)     # field type URIs  (unneeded)
        for i, instance in zip(count(), dicts):
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
    newinstance["name"] = instance["rdf-schema#label"]
    newinstance["URI"] = instance["URI"]
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
    return [x for x in ontologyrefs if x.startswith(ontologyprefix)]


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


if __name__ == "__main__":
    instances = csvinstances("/Users/will/Desktop/Brewery.csv")
    writeInstances(instances, "../mockdata/")

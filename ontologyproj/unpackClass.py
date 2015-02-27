
'''
    takes dbpedia class file (a giant JSON file)
    and splits it into separate, cleaned entity files
'''

import ijson
import json
import time

ontologyprefix = "http://dbpedia.org/ontology/"
resourceprefix = "http://dbpedia.org/resource/"
itemprefix     = "http:\/\/www.w3.org\/1999\/02\/22-rdf-syntax-ns#type"

with open("../data/flatontology.json",'r') as flat:
    ontology = json.load(flat)

def toName(url):
    return url[len(ontologyprefix):]

def main():
    speciespath = "../data/Species.json"
    splitClassFile(speciespath)

def splitClassFile(classfilepath):

    classfile = open(classfilepath,'r')

    count = 0
    for instance in ijson.items(classfile,'instances.item'):
        entity = buildEntity(instance)
        if len(entity['properties']) > 2:
            print(json.dumps(entity,indent=4))
        print(entity['ontologies'])
        deepest = getFinestOntology(entity['ontologies'])
        path = ontology[toName(deepest)]['fullpath']
        print("DEEPEST:",path)
        #write(entity,path)
        #addToDirectory(entity)
        time.sleep(0.1)
        count += 1
        if count >= 10: break

def buildEntity(instance):
    return { 'url'        : instance.keys()[0],
             'name'       : instance.keys()[0][len(resourceprefix):],
             'properties' : getProperties(instance),
             'ontologies' : getOntologies(instance) }

def getProperties(instance):
    ''' returns dict of all properties in instance '''

    validproperty = lambda key,val: key.startswith(ontologyprefix) \
                                    and not key.endswith("_label") \
                                    and val != "NULL" \
                                    and key != ontologyprefix + "wikiPageRevisionID" \
                                    and key != ontologyprefix + "wikiPageID"

    allprops = instance.values()[0]
    properties = { toName(key) : val for key,val in allprops.iteritems()
            if validproperty(key,val) }
    return properties

def getOntologies(instance):
    ''' construct list of ontology refs in instance '''
    ontologyrefs = instance.values()[0][itemprefix]
    return [ x for x in ontologyrefs if x.startswith(ontologyprefix) ]

def getFinestOntology(refs):
    ''' take list of ontology classes and return deepest one '''
    getdepth = lambda ref: ontology[toName(ref)]['depth']
    return max(refs,key=getdepth)

def write(entity,path):
    ''' write entity to JSON file at path '''
    pass

def addToDirectory(entity):
    ''' add name and filepath to entity directory '''
    pass

splitClassFile("../data/Species.json")

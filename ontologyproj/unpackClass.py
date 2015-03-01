''' takes dbpedia class file (a giant JSON file)
    and splits it into separate, cleaned entity files
'''

import ijson
import json
import time

ontologyprefix  = "http:\/\/dbpedia.org\/ontology\/"
ontologyprefix2 = "http://dbpedia.org/ontology/"
resourceprefix = "http:\/\/dbpedia.org\/resource\/"
itemprefix     = "http:\/\/www.w3.org\/1999\/02\/22-rdf-syntax-ns#type"
itemprefix2    = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"

with open("../data/flatontology.json",'r') as flat:
    ontology = json.load(flat)

with open("../data/directory.json",'r+') as f:
    directory = json.load(f)



def main():
    speciespath = "../data/Species.json"
    splitClassFile(speciespath)



def toName(url):
    return url[len(ontologyprefix):]

def toName2(url):
    return url[len(ontologyprefix2):]

def splitClassFile(classfilepath):

    classfile = open(classfilepath,'r')

    ''' stream of all instances in file '''
    for instance in ijson.items(classfile,'instances.item'):
        if not inDirectory(instance):
            toEntity(instance)

    classfile.close()

def toEntity(instance):
    entity = buildEntity(instance)
    if len(entity['properties']) > 2:
        deepest = getFinestOntology(entity['ontologies'])
        path = ontology[toName2(deepest)]['fullpath']
        write(entity,path)
        addToDirectory(entity,path)

def buildEntity(instance):
    return { 'url'        : instance.keys()[0],
             'name'       : instance.keys()[0][len(resourceprefix):],
             'properties' : getProperties(instance),
             'ontologies' : getOntologies(instance) }

def getProperties(instance):
    ''' returns dict of all properties in instance '''

    validproperty = lambda key,val: key.startswith(ontologyprefix) \
                                    and not key.endswith("_label") \
                                    and key != ontologyprefix + "wikiPageRevisionID" \
                                    and key != ontologyprefix + "wikiPageID" \
                                    and val != "NULL"

    allprops = instance.values()[0]
    properties = { toName(key) : val for key,val in allprops.iteritems()
            if validproperty(key,val) }
    return properties

def getOntologies(instance):
    ''' construct list of ontology refs in instance '''
    ontologyrefs = instance.values()[0][itemprefix]
    return [ x for x in ontologyrefs if x.startswith(ontologyprefix2) ]

def getFinestOntology(refs):
    ''' take list of ontology classes and return deepest one '''
    getdepth = lambda ref: ontology[toName2(ref)]['depth']
    return max(refs,key=getdepth)

def write(entity,path):
    ''' write entity to JSON file at path '''
    name = entity['name'].replace('/','-')
    fullname = "../data/" + path + entity['name'] + ".json"
    with open(fullname, 'wb') as fp:
        json.dump(entity, fp)
    print "wrote",entity['name'],"...",

def addToDirectory(entity,path):
    ''' add name and filepath to entity directory '''
    this_entity = entity['url']
    val = path + entity['name'].replace('/','-') + ".json"
    directory[this_entity] = val

    with open("../data/directory.json",'w+') as f:
        json.dump(directory, f)
    print "added to directory"

def inDirectory(instance):
    instance_name = instance.keys()[0]
    return instance_name in directory

if __name__ == "__main__":
    main()

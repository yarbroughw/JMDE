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

def toName(url):
    return url[len(ontologyprefix):]

def toName2(url):
    return url[len(ontologyprefix2):]

def splitClassFile(classfilepath,destination,skip=1):
    ''' stream of all instances in file '''
    classfile = open(classfilepath,'r')
    for i,instance in zip(itertools.count(),ijson.items(classfile,'instances.item')):
        if i % skip == 0:
            toEntity(instance,destination)
    classfile.close()

def toEntity(instance,dest):
    entity = buildEntity(instance)
    if len(entity['properties']) > 2:
        deepest = getFinestOntology(entity['ontologies'])
        path = ontology[toName2(deepest)]['fullpath']
        write(entity,dest,path)
        addToIndexes(entity,dest,path)

def buildEntity(instance):
    return { 'url'        : instance.keys()[0].replace('\\',''),
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

def write(entity,dest,path):
    ''' write entity to JSON file at path '''
    name = entity['name'].replace('\/','-')
    fullname = dest + path + name + ".json"
    with open(fullname, 'wb') as fp:
        json.dump(entity, fp)
    print "wrote",entity['name'],"...",

def addToIndexes(entity,dest,path):
    paths = path.split('/')
    paths = [ '/'.join(paths[:i+1]) for i,_ in enumerate(paths) ]
    for p in paths:
        addToIndex(entity,dest+p,path)
    print "added to relevant indexes"

def addToIndex(entity,dest,path):
    ''' add name and filepath to file index at dest '''
    this_entity = entity['url']
    val = path + entity['name'].replace('/','-') + ".json"

    with open(dest+"/fileindex.json",'r') as f:
        index = json.load(f)
    index[this_entity] = val
    with open(dest+"/fileindex.json",'w') as f:
        json.dump(index, f, indent=4)

def main():
    speciespath = "../data/Species.json"
    splitClassFile(speciespath,"../mockdata/")

if __name__ == "__main__":
    main()

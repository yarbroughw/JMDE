''' transforms DBpedia ontology into a dictionary '''

import json
from bs4 import BeautifulSoup

def getHtml():
    ''' retrieve DBpedia ontology (in HTML) '''
    with open("../data/Ontology.html",'r') as f:
        data = f.read()
    soup = BeautifulSoup(data)
    return soup

def getNestedOntology(ul,path='',level=0):
    ''' recursive function that makes a list of nested ul items '''
    lis = ul.findAll('li',recursive=False)
    children = []
    for li in lis:
        sublists = li.find('ul',recursive=False)
        name = li.find('a').get('name')
        child = {
                "name"     : name,
                "children" : getNestedOntology(sublists,path+name+'/',level=level+1),
                "fullpath" : path + name + '/' ,
                "depth"    : level
                }
        children.append(child)
    return children

def getFlatOntology(entities):
    flat = {}
    for entity in entities:
        name = entity.pop("name")
        children = entity.pop("children")
        flat[name] = entity
        flat.update(getFlatOntology(children))
    return flat

ontology_html = getHtml()
ul = ontology_html.find('ul')
o = getNestedOntology(ul)

with open("../data/nestedontology.json","w") as nested:
    json.dump(o,nested,indent=4)

with open("../data/flatontology.json",'w') as flat:
    json.dump(getFlatOntology(o),flat,indent=4)

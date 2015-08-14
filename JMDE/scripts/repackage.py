""" repackage.py

This script repackages the instances dataset to be more sane.
Specifically, it favors a flat structure in a single file, rather than a
complex nested directory of multiple files.

To compensate for the lack of structure in this repackaged version, the modules
that use the dataset will need to be rewritten.

Why: When I first wrote the code for my thesis, I was under the mistaken
impression that the dataset would be too big to fit in memory (which was true
of the raw, unfiltered version of the dataset). Once I realized that the
dataset could easily fit in memory, it was too late to rewrite things. Now I
have the time!
"""

import json
import os
from itertools import count

prefix = "http://dbpedia.org/ontology/"

def getFile(path):
    ''' gets the contents of a json file. '''
    with open("../../data/" + path) as f:
        return json.load(f)

def getPaths(num=None):
    ''' opens fileindex and returns paths.
    if num is set, it returns that many paths
    '''

    values = getFile("owl:Thing/fileindex.json").values()
    if not num:
        return values
    else:
        return [ path for path, i in zip(values, range(num)) ]

def clean(classname):
    ''' Remove prefix from a class name. '''
    return classname[len(prefix):]

def properties(instance):
    ''' Gets list of property labels from instance. '''
    return list(instance["properties"].keys())

def deepest_class(ontology, classes):
    ''' Returns deepest class from list of classes. '''
    depth = lambda class_: ontology[class_]["depth"]
    return max(classes, key=depth)

def simplify(ontology, instance):
    ''' Returns smaller form of instance with just
    properties and deepest subsuming class.
    '''
    return { "properties": properties(instance),
             "class"     : deepest_class(ontology, instance["classes"])
           }

def simplify_instances():
    ''' Returns instances dataset with each instance in smaller
    form, with just properties and deepest subsuming class.
    '''
    with open("../../data/flatontology.json") as f:
        ontology  = json.load(f)
    with open("../../data/instances.json") as f:
        instances = json.load(f)

    return [simplify(ontology, instance) for instance in instances]

def repackage(debug=False):
    num = 2 if debug else None

    # get paths from fileindex
    filepaths = getPaths(num)

    # get instances
    exists = lambda path: os.path.exists("../../data/" + path)
    instances = [ getFile(path) for path in filepaths if exists(path)]

    # rename and clean classes list for good measure :)
    for instance in instances:
        classes = instance.pop("ontologies")
        instance["classes"] = [ clean(class_) for class_ in classes ]

    if debug:
        print(json.dumps(instances, indent=4))
    else:
        with open("instances.json", 'w') as f:
            json.dump(instances, f)

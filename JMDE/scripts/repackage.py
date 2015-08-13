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

def main(debug=False):
    num = 2 if debug else None

    # get paths from fileindex
    filepaths = getPaths(num)

    # get instances
    exists = lambda path: os.path.exists("../../data/" + path)
    instances = [ getFile(path) for path in filepaths if exists(path)]

    print(json.dumps(instances, indent=4))

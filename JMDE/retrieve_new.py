""" Retrieve dataset of instances for training/testing. """

import json

def instances():
    ''' Loads and returns dataset of instances. '''
    with open("../data/instances.json") as f:
        return json.load(f)


def simple_instances():
    ''' Loads and returns dataset of instances, where the instances
    have been simplified to just property labels and class name.
    See the scripts/repackage.py for more details.
    '''
    with open("../data/simple_instances.json") as f:
        return json.load(f)


def dataset():
    ''' Returns tuple of feature corpus and target labels. '''
    instances = simple_instances()
    corpus = [ ' '.join(instance["properties"]) for instance in instances ]
    target = [ instance["class"] for instance in instances ]
    return corpus, target

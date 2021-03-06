from __future__ import print_function
import random
import ujson
import os


def entitygenerator(category):
    ''' generator using directory file to yield random json from class '''

    # get path of category from ontology file
    with open("../data/flatontology.json", 'r') as ontology:
        flatontology = ujson.load(ontology)
        category_path = flatontology[category]["fullpath"]

    # get child names of category
    with open("../data/nestedontology.json", 'r') as ontology:
        tree = ujson.load(ontology)[0]

    childnames = getchildnames(tree, category_path)

    # load index file from that path
    indexfile = "../data/" + category_path + "fileindex.json"
    with open(indexfile, 'r') as directory:
        filedict = ujson.loads(directory.read())

    # pick random entry in index and return associated object
    while filedict:
        randomkey = random.choice(list(filedict.keys()))
        path = filedict.pop(randomkey)
        classes = path.split('/')[:-1]

        with open("../data/" + path, 'r') as entityfile:
            entity = ujson.loads(entityfile.read())

        # class is intersection of entity's classes and subclasses of category
        entity["class"] = (childnames & set(classes)).pop()
        entity["deepest"] = classes[-1]
        entity["fullpath"] = '/'.join(classes)
        yield entity


def getchildnames(tree, path):
    ''' returns names of direct children of category in tree '''
    path = path.split('/')[:-1]
    node = tree
    while path != []:
        level = path.pop(0)
        for child in node["children"]:
            if child["name"] == level:
                node = child
    return set([child["name"] for child in node["children"]])


def progress(counter, total):
    ''' simple helper function for string of progress '''
    percentage = int(counter / total * 100)
    return '\r'+str(percentage)+"%"


def entities(amount, category):
    ''' helper function that wraps entity generator. returns up to <amount>
        entities (less if no more can be retrieved)
    '''
    g = entitygenerator(category)
    for i, entity in zip(range(amount), g):
        yield entity


def direct(amount, category):
    ''' gets entities directly from category, not category's children
    '''
    with open("../data/flatontology.json", 'r') as ontology:
        flatontology = ujson.load(ontology)
        category_path = flatontology[category]["fullpath"]

    filenames = [f for f in os.listdir("../data/" + category_path)
                 if f != "fileindex.json"
                 and os.path.isfile("../data/" + category_path + f)]

    for _, filename in zip(range(amount), filenames):
        with open("../data/" + category_path + filename, 'r') as f:
            entity = ujson.load(f)
            entity["class"] = category
            yield entity


def sets(category, trainnum, testnum):
    ''' pull random training and testing sets from disk
        if not enough entities exists at "category",
        then pull as many as possible and
    '''
    total = trainnum + testnum
    g = entities(total, category)
    xs = []

    # built trainset while printing out progress percentage
    counter = 0
    for entity in g:
        xs.append(entity)
        counter += 1
        print(progress(counter, total), "of training/test sets loaded", end='')
    print()

    split_at = int(testnum / total * len(xs) * -1)

    return xs[:split_at], xs[split_at:]

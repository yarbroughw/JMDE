import random
import ujson


def entitygenerator(category):
    ''' generator using directory file to yield random json from class '''

    # get path of category from ontology file
    with open("../data/flatontology.json", 'r') as ontology:
        category_path = ujson.load(ontology)[category]["fullpath"]

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
        classes = set(path.split('/')[:-1])

        with open("../data/" + path, 'r') as entityfile:
            entity = ujson.loads(entityfile.read())

        # class is intersection of entity's classes and subclasses of category
        entity["class"] = (childnames & classes).pop()
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
        if i == amount:
            return
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
        print(progress(counter, total), "of training/test sets loaded")
    print()

    split_at = int(testnum / total * len(xs) * -1)

    return xs[:split_at], xs[split_at:]

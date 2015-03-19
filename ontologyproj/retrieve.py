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
    indexfile = "../mockdata/" + category_path + "fileindex.json"
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
    ''' helper function that wraps entity generator '''
    g = entitygenerator(category)
    for _ in range(amount):
        yield next(g)


def sets(category, trainnum, testnum):
    ''' pull random training and testing sets from disk '''
    g = entitygenerator(category)
    trainset = []
    testset = []

    # built trainset while printing out progress percentage
    counter = 0
    for _ in range(trainnum):
        trainset.append(next(g))
        counter += 1
        print(progress(counter, trainnum), "of training set loaded", end='')
    print()

    # built testset while printing out progress percentage
    counter = 0
    for _ in range(testnum):
        testset.append(next(g))
        counter += 1
        print(progress(counter, testnum), "of test set loaded", end='')

    return trainset, testset

import sys
import random
import ujson

def entitygenerator(category):
    ''' generator using directory file to yield random json from class '''

    # get path of category from ontology file
    with open("../data/flatontology.json",'r') as ontology:
        path = ujson.load(ontology)[category]["fullpath"]

    # load index file from that path
    with open("../mockdata/" + path + "fileindex.json",'r') as directory:
        filedict = ujson.loads(directory.read())

    # pick random entry in index and return associated object
    while filedict:
        randomkey = random.choice(list(filedict.keys()))
        path = filedict.pop(randomkey)
        classname = path.split('/')[-2]

        with open("../data/" + path, 'r') as entityfile:
            entity = ujson.loads(entityfile.read())

        entity["class"] = classname
        yield entity

def progress(counter,total):
    ''' simple helper function for string of progress '''
    percentage = int(counter / total * 100)
    return '\r'+str(percentage)+"%"

def entities(amount, category):
    ''' helper function that wraps entity generator '''
    g = entitygenerator(category)
    for _ in range(amount):
        yield next(g)

def sets(category,trainnum,testnum):
    ''' pull random training and testing sets from disk '''
    g = entitygenerator(category)
    trainset = []
    testset  = []

    # built trainset while printing out progress percentage
    counter = 0
    for _ in range(trainnum):
        trainset.append(next(g))
        counter += 1
        print(progress(counter,trainnum),"of training set loaded",end='')
    print()

    # built testset while printing out progress percentage
    counter = 0
    for _ in range(testnum):
        testset.append(next(g))
        counter += 1
        print(progress(counter,testnum),"of test set loaded",end='')

    return trainset, testset

import sys
import random
import ujson

def entitygenerator():
    ''' generator using directory file to yield random json docs '''
    counter = 0

    with open("../data/directory.json",'r') as directory:
        filedict = ujson.loads(directory.read())

    while filedict:
        randomkey = random.choice(list(filedict.keys()))
        path = filedict.pop(randomkey)
        classname = path.split('/')[-2]

        with open("../data/" + path, 'r') as entityfile:
            entity = ujson.loads(entityfile.read())

        entity["class"] = classname
        counter += 1
        yield entity

def progress(counter,total):
    ''' simple helper function for string of progress '''
    percentage = int(counter / total * 100)
    return '\r'+str(percentage)+"%"

def entities(amount):
    ''' helper function that wraps entity generator '''
    g = entitygenerator()
    for _ in range(amount):
        yield next(g)

def trainAndTestSets(trainnum,testnum):
    ''' pull random training and testing sets from disk '''
    g = entitygenerator()
    trainset = []
    testset  = []

    counter = 0
    for _ in range(trainnum):
        trainset.append(next(g))
        counter += 1
        print(progress(counter,trainnum),"of training set loaded",end='')
    print()

    counter = 0
    for _ in range(testnum):
        testset.append(next(g))
        counter += 1
        print(progress(counter,testnum),"of test set loaded",end='')

    return trainset, testset

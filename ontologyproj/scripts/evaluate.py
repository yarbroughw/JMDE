import pickle
import json
import numpy as np

import retrieve
import basicclassifier
import lexicalmatcher


with open("../data/flatontology.json", 'r') as f:
    flatontology = json.load(f)


def lca(class1, class2):
    ''' least common ancestor of two classes in ontology '''
    path1 = flatontology[class1]["fullpath"].split('/')[:-1]
    path2 = flatontology[class2]["fullpath"].split('/')[:-1]

    lca = "owl:Thing"
    for a, b in zip(path1, path2):
        if a == b:
            lca = a
        else:
            break
    return lca


def distance(class1, class2):
    ''' distance between two classes in ontology '''
    if class1 == class2:
        return 0
    depth1 = flatontology[class1]["depth"]
    depth2 = flatontology[class2]["depth"]
    lca_depth = flatontology[lca(class1, class2)]["depth"]
    return depth1 + depth2 - 2*lca_depth


def getscores(entities):
    ns = [10, 100, 1000, 10000]
    scores = {"basic": [],
              "tree": [],
              "trained": [],
              "lexical": None}

    for n in ns:
        filename = "../data/classifiers/basicdump" + str(n) + ".pkl"
        with open(filename, 'rb') as f:
            bc = pickle.load(f)
        score = basicclassifier.test(bc, test_entities)
        scores["basic"].append(score)

    for n in ns:
        filename = "../data/classifiers/treedump" + str(n) + ".pkl"
        with open(filename, 'rb') as f:
            tree = pickle.load(f)
        score = tree.score(test_entities)
        scores["tree"].append(score)

    for n in ns:
        filename = "../data/classifiers/learnedtreedump" + str(n) + ".pkl"
        with open(filename, 'rb') as f:
            learnedtree = pickle.load(f)
        score = learnedtree.score(test_entities)
        scores["trained"].append(score)

    lm = lexicalmatcher.LexicalMatcher()
    score = lm.score(test_entities)
    scores["lexical"] = score

    return scores


def getdistances(entities):
    distance_averages = {"lexical": {"avg": [], "stddev": []},
                         "basic": {"avg": [], "stddev": []},
                         "tree": {"avg": [], "stddev": []},
                         "trained": {"avg": [], "stddev": []}}

    with open("../data/classifiers/basicdump10000.pkl", 'rb') as f:
        bc = pickle.load(f)
    with open("../data/classifiers/treedump10000.pkl", 'rb') as f:
        tc = pickle.load(f)
    with open("../data/classifiers/learnedtreedump10000.pkl", 'rb') as f:
        ltc = pickle.load(f)

    # avg distance for lexical's predictions
    lm = lexicalmatcher.LexicalMatcher()
    distances = []
    for entity in entities:
        distances.append(distance(entity["deepest"], lm.classify(entity)))
    distance_averages["lexical"]["avg"] = np.mean(distances)
    distance_averages["lexical"]["stddev"] = np.std(distances)

    # avg distance for basic's predictions
    bcpredictions = basicclassifier.predictions(bc, entities)
    distances = []
    for entity, predicted in zip(entities, bcpredictions):
        distances.append(distance(entity["deepest"], predicted))
    distance_averages["basic"]["avg"] = np.mean(distances)
    distance_averages["basic"]["stddev"] = np.std(distances)

    # avg distance for tree's predictions
    distances = []
    for entity in entities:
        distances.append(distance(entity["deepest"], tc.predict(entity)))
    distance_averages["tree"]["avg"] = np.mean(distances)
    distance_averages["tree"]["stddev"] = np.std(distances)

    # avg distance for learned tree's predictions
    distances = []
    for entity in entities:
        distances.append(distance(entity["deepest"], ltc.predict(entity)))
    distance_averages["trained"]["avg"] = np.mean(distances)
    distance_averages["trained"]["stddev"] = np.std(distances)

    return distance_averages


if __name__ == "__main__":
    test_entities = list(retrieve.entities(1000, "owl:Thing"))
    #with open("../data/results/scores.json", 'w') as f:
        #json.dump(getscores(test_entities), f)
    with open("../data/results/distances.json", 'w') as f:
        json.dump(getdistances(test_entities), f)

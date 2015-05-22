import pickle
import time
import json
import numpy as np

import lexicalmatcher
import basicclassifier
import retrieve

current_milli_time = lambda: time.time() * 1000


def basictime(classifier, testset):
    print("timing basic classifier over testset")
    iterations = 10
    times = []
    for n in range(iterations):
        start = current_milli_time()
        basicclassifier.predictions(classifier, testset)
        times.append(current_milli_time() - start)
    average = np.mean(times)
    stddev = np.std(times)
    return average, stddev


def classifiertime(fn, testset):
    print("timing", fn.__name__, "over testset")
    iterations = 10
    times = []
    for n in range(iterations):
        start = current_milli_time()
        fn(testset)
        times.append(current_milli_time() - start)
    average = np.mean(times)
    stddevs = np.std(times)
    return average, stddevs


times = {"lexical": {"avgs": [], "stddevs": []},
         "basic": {"avgs": [], "stddevs": []},
         "tree": {"avgs": [], "stddevs": []},
         "trained": {"avgs": [], "stddevs": []}}

with open("../data/classifiers/basicdump10000.pkl", 'rb') as f:
    bc = pickle.load(f)
with open("../data/classifiers/treedump10000.pkl", 'rb') as f:
    tc = pickle.load(f)
with open("../data/classifiers/learnedtreedump10000.pkl", 'rb') as f:
    ltc = pickle.load(f)
lm = lexicalmatcher.LexicalMatcher()
basicpredictions = lambda testset: basicclassifier.predictions(bc, testset)

for n in [10, 100, 1000, 10000]:
    testset = list(retrieve.entities(n, "owl:Thing"))

    avg, stddev = classifiertime(lm.classifyset, testset)
    times["lexical"]["avgs"].append(avg)
    times["lexical"]["stddevs"].append(stddev)

    avg, stddev = basictime(bc, testset)
    times["basic"]["avgs"].append(avg)
    times["basic"]["stddevs"].append(stddev)

    avg, stddev = classifiertime(tc.predictions, testset)
    times["tree"]["avgs"].append(avg)
    times["tree"]["stddevs"].append(stddev)

    avg, stddev = classifiertime(ltc.predictions, testset)
    times["trained"]["avgs"].append(avg)
    times["trained"]["stddevs"].append(stddev)

    print(times)

with open("../data/results/times.json", 'w') as f:
    json.dump(times, f)

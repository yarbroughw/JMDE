import retrieve
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


def getkeystrings(dataset):
    return [ ' '.join(entity["properties"]) for entity in dataset ]


def getclasslabels(dataset):
    return [ entity["deepest"] for entity in dataset ]


def train(trainset):
    corpus = getkeystrings(trainset)
    target = getclasslabels(trainset)
    return pipeline().fit(corpus, target)


def pipeline():
    return Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB())])


def evalclassifier(trainsize, testsize):
    trainset, testset = retrieve.sets("owl:Thing", trainsize, testsize)
    classifier = train(trainset)
    return test(classifier, testset)


def predictions(classifier, testset):
    testdata = getkeystrings(testset)
    predicted = classifier.predict(testdata)
    return predicted


def test(classifier, testset):
    testtargets = getclasslabels(testset)
    predicted = predictions(classifier, testset)
    return np.mean(predicted == testtargets)


if __name__ == "__main__":
    trainsize, testsize = 1000, 100

    accuracies = []
    for i in range(10):
        print("Trial", i+1)
        accuracies.append(evalclassifier(trainsize, testsize))
        print("\nAccuracy:", accuracies[-1], "\n")
    avgaccuracy = np.mean(accuracies)

    print("training set size:", trainsize)
    print("test set size:", testsize)
    print("Average accuracy:", avgaccuracy)

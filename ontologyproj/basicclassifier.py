import retrieve
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

def getkeystring(entity):
    return ' '.join(entity["properties"])

def getclasslabel(entity):
    return entity["class"]

def train(trainset):
    corpus  = list(map(getkeystring, trainset))
    target  = list(map(getclasslabel,trainset))
    return pipeline().fit(corpus,target)

def pipeline():
    return Pipeline([('vect',CountVectorizer()),
                     ('tfidf',TfidfTransformer()),
                     ('clf',MultinomialNB()),
                   ])

def evalclassifier(trainsize,testsize):
    trainset,testset = retrieve.trainAndTestSets(trainsize,testsize)
    classifier = train(trainset)

    testdata    = list(map(getkeystring, testset))
    testtargets = list(map(getclasslabel,testset))

    predicted = classifier.predict(testdata)
    return np.mean(predicted == testtargets)


if __name__ == "__main__":
    trainsize,testsize = 1000,100

    accuracies = []
    for i in range(10):
        print("Trial",i+1)
        accuracies.append(evalclassifier(trainsize,testsize))
        print("\nAccuracy:",accuracies[-1],"\n")
    avgaccuracy = np.mean(accuracies)

    print("training set size:",trainsize)
    print("test set size:",testsize)
    print("Average accuracy:",avgaccuracy)

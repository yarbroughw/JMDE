import retrieve_new

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn import cross_validation


class BasicClassifier:
    ''' Simple wrapper class for a sklearn pipeline, with
    Multinomial Naive Bayes as the final estimator.
    '''
    def __init__(self, corpus=None, target=None):
        ''' Constructs pipeline, and trains itself if corpus and
        target params are set.
        '''
        vectorizer  = ('vect',  CountVectorizer())
        transformer = ('tfidf', TfidfTransformer())
        classifier  = ('clf',   MultinomialNB())
        self.pipeline = Pipeline([vectorizer, transformer, classifier])

        if corpus is not None and target is not None:
            self.train(corpus, target)

    def train(self, corpus, target):
        ''' Fit pipeline to feature corpus and target set of labels. '''
        return self.pipeline.fit(corpus, target)

    def test(self, corpus, target):
        ''' Score pipeline using test corpus and labels. '''
        return self.pipeline.score(corpus, target)

    def predict(self, properties):
        ''' Predict the class of a single string of property names. '''
        return self.pipeline.predict([properties])[0]


def keystrings(entities):
    return  [ ' '.join(entity["properties"]) for entity in entities ]


def class_labels(instances):
    return [ instance["class"] for instance in instances ]


def split_dataset(ratio):
    corpus, target = retrieve_new.dataset()
    return cross_validation.train_test_split(corpus, target, test_size=ratio)


def evalclassifier(test_ratio):
    split = split_dataset(test_ratio)
    train_corpus, test_corpus, train_labels, test_labels = split

    print("Training size:", len(train_corpus))
    classifier = BasicClassifier(train_corpus, train_labels)

    print("Testing size: ", len(test_corpus))
    return classifier.test(test_corpus, test_labels)


def kfold_eval():
    corpus, target = retrieve_new.dataset()
    corpus, target = np.array(corpus), np.array(target)
    fold_indices = cross_validation.KFold(len(corpus), n_folds=5)

    for train, test in fold_indices:
        train_corpus, train_labels = corpus[train], target[train]
        test_corpus,  test_labels  = corpus[test],  target[test]
        classifier = BasicClassifier(train_corpus, train_labels)
        return classifier.test(test_corpus, test_labels)


def main():
    print(kfold_eval())

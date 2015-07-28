from __future__ import print_function
import json
import warnings
import pickle
import itertools
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import scipy.optimize as opt

import retrieve


class Node:
    def __init__(self, n, pipeline):
        self.name = n
        self.children = {}
        self.pipeline = pipeline
        self.threshold = 0.00

    def hasChildren(self):
        return self.children != dict()

    def getset(self, amount):
        return list(retrieve.entities(amount, self.name))

    def train(self, entities):
        if not entities:
            return
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            corpus = features(entities)
            target = labels(entities)
            self.pipeline = self.pipeline.fit(corpus, target)
            assert hasattr(self.pipeline.steps[0][1], "vocabulary_")

    def test(self):
        if not self.testset:
            print(self.name + "'s test set not initialized!")
            return
        corpus = features(self.testset)
        target = labels(self.testset)
        return self.pipeline.score(corpus, target)

    def predict(self, x):
        ''' take an entity and classify it into either a child node (if
        confident about prediction) or self (if unconfident)
        '''
        fs = features([x])
        proba = max(self.pipeline.predict_proba(fs)[0])
        if proba < self.threshold:
            label = self.name
        else:
            label = self.pipeline.predict(fs)[0]
        return label

    def isTrained(self):
        return hasattr(self.pipeline.steps[0][1], "vocabulary_")

    def distance(self, predicted, label):
        ''' error function for optimization of node thresholds.
        correct classification is a 0, withholded classification is a 1,
        and misclassification is a 2
        '''
        if predicted == label:
            return 0
        elif predicted == self.name:
            return 1
        else:
            return 2

    def score(self, threshold):
        ''' gets entities from this node and its children, to score how
            well the node classifies the entities (using "distance")
        '''
        self.threshold = threshold
        total = sum([self.distance(self.predict(e), e["class"])
                    for e in self.testset])
        return total / len(self.testset)

    def learnthreshold(self):
        print("loading test set.")
        self.testset = list(itertools.chain(retrieve.direct(100, self.name),
                                            retrieve.entities(200, self.name)))
        print("optimizing.")
        result = opt.minimize_scalar(self.score,
                                     bounds=(0.0, 1.0),
                                     method='bounded')
        print(result)
        self.threshold = result.x
        print(self.name, "threshold set to", self.threshold)


class TreeClassifier:
    def __init__(self, subclass=None):
        # make tree from nested ontology
        with open("../data/nestedontology.json", 'r') as f:
            ontology = json.load(f)[0]
        self.root = self._buildtree(ontology)
        if subclass:
            self.root = self.getsubnode(subclass)

    def getsubnode(self, classname):
        ''' returns the node in the tree that matches classname '''
        for node in iter(self):
            if node.name == classname:
                return node
        raise ValueError(classname + " is not a valid class name!")

    def _buildtree(self, json_tree):
        ''' build tree from nested json '''
        root = Node(json_tree["name"], pipeline())
        for child in json_tree["children"]:
            root.children[child["name"]] = (self._buildtree(child))
        return root

    def __iter__(self):
        ''' BFS traversal of tree '''
        queue = [self.root]
        while queue != []:
            current = queue.pop(0)
            queue.extend(list(current.children.values()))
            yield current

    def train(self, entities):
        ''' train each node's classifier '''
        for node in iter(self):
            print("Training", node.name)
            node.train(entities)

    def autotrain(self, amount):
        ''' train each node's classifier '''
        for node in iter(self):
            entities = node.getset(amount)
            node.train(entities)

    def learnthresholds(self):
        for node in iter(self):
            if node.isTrained():
                print("learning threshold for", node.name, end='. ')
                node.learnthreshold()

    def predict(self, entity):
        ''' returns predicted classes for entity.
        predicts downwards in tree from root node
        '''
        node = self.root
        while node.hasChildren() and node.isTrained():
            predicted_label = node.predict(entity)
            if predicted_label == node.name:
                break
            node = node.children[predicted_label]
        return node.name

    def predictions(self, entities):
        ''' runs predict function ovr set of entities '''
        for entity in entities:
            self.predict(entity)

    def score(self, entities):
        total = 0
        for entity in entities:
            realclass = entity["deepest"]
            predicted = self.predict(entity)
            if predicted == realclass:
                total += 1
        return total / len(entities)


def features(dataset):
    getkeystring = lambda x: ' '.join(x["properties"])
    return list(map(getkeystring, dataset))


def labels(dataset):
    getclassname = lambda x: x["class"]
    return list(map(getclassname, dataset))


def pipeline():
    return Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB())])


def dump(trainnum, testnum, filename):
    tree = TreeClassifier("owl:Thing")
    print("Tree created with", tree.root.name, "as root.")
    tree.train(trainnum, testnum)
    with open(filename, 'wb') as f:
        pickle.dump(tree, f)


def load(filename):
    with open(filename, 'rb') as f:
        tree = pickle.load(f)
    return tree


if __name__ == "__main__":
    tree = TreeClassifier()
    tree.train(1000, 10)
    entities = [e for e in retrieve.entities(10, "owl:Thing")]
    for e in entities:
        print(e["name"], e["class"], tree.predict(e))

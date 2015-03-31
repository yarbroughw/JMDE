import json
import retrieve
import pickle
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


class Node:
    def __init__(self, n, pipeline):
        self.name = n
        self.children = {}
        self.pipeline = pipeline
        self.threshold = 0.05

    def hasChildren(self):
        return self.children != dict()

    def getsets(self, trainnum, testnum):
        print(self.name, "node gathering sets.")
        trainset, testset = retrieve.sets(self.name, trainnum, testnum)
        self.trainset = trainset
        self.testset = testset

    def train(self):
        if not self.trainset:
            print(self.name + "'s training set not initialized!")
            return
        corpus = features(self.trainset)
        target = labels(self.trainset)
        self.pipeline = self.pipeline.fit(corpus, target)

    def test(self):
        if not self.testset:
            print(self.name + "'s test set not initialized!")
            return
        corpus = features(self.testset)
        target = labels(self.testset)
        return self.pipeline.score(corpus, target)

    def predict(self, x):
        ''' take an entity and classify it into child nodes '''
        fs = features([x])
        prediction = {"label": self.pipeline.predict(fs)[0],
                      "proba": max(self.pipeline.predict_proba(fs)[0])}
        return prediction

    def confidence(self, entity):
        getkeystring = lambda x: ' '.join(x["properties"])
        vector = getkeystring(entity)
        return np.amax(self.pipeline.predict_proba(vector))

    def emptychildren(self):
        ''' returns list of untrained children '''
        empties = []
        for name, child in self.children.items():
            if not hasattr(child.pipeline.steps[0][1], "vocabulary_"):
                empties.append(name)
        return empties

    def trained(self):
        return hasattr(self.pipeline.steps[0][1], "vocabulary_")

    def distance(self, predicted, label):
        ''' distance function for optimization of node thresholds.
        correct classification is a 1, withholded classification is a 0,
        and misclassification is a -1
        '''
        if predicted == label:
            return 1
        elif predicted == self.name:
            return 0
        else:
            return -1

    def score(self):
        # TODO: add files from class
        entities = retrieve.entities(100, self.name)
        return sum([self.distance(self.predict(e), e["class"])
                    for e in entities])

    def learnthreshold(self):
        self.threshold = 0
        current = self.score()
        rightscore = current - 1

        # move right until going right is worse (TODO: debug?)
        while rightscore > current:
            self.threshold += 0.05
            current = rightscore
            rightscore = self.score()
        self.threshold -= 0.05


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

    def train(self, trainnum, testnum):
        ''' train each node's classifier '''
        for node in iter(self):
            print("Training", node.name)
            node.getsets(trainnum, testnum)
            node.train()
            node.trainset = []
        self.emptynodes = [marked for node in iter(self)
                           for marked in node.emptychildren()]

    def learnthresholds(self):
        for node in iter(self):
            node.learnthreshold()

    def predict(self, entity):
        ''' returns predicted classes for entity.
        predicts downwards in tree from root node
        '''
        node = self.root
        print(entity["name"], "actually is a", entity["fullpath"])
        while node.hasChildren() and node.trained():
            prediction = node.predict(entity)
            if prediction["proba"] < node.threshold:
                break
            print(entity["name"], "is a", prediction["label"],
                  prediction["proba"])
            node = node.children[prediction["label"]]


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

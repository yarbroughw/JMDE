import json
import retrieve

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

class Node:
    def __init__(self,n,pipeline):
        self.name     = n
        self.children = []
        self.pipeline = pipeline

    def hasChildren(self):
        return self.children != []

    def getsets(self,trainnum,testnum):
        trainset,testset = retrieve.sets(self.name,trainnum,testnum)
        self.trainset = trainset
        self.testset  = testset

    def train(self):
        if not self.trainset:
            print(self.name + "'s training set not initialized!")
            return
        corpus = features(self.trainset)
        target = labels(self.trainset)
        self.pipeline = self.pipeline.fit(corpus,target)

    def test(self):
        if not self.testset:
            print(self.name + "'s test set not initialized!")
            return
        corpus = features(self.testset)
        target = labels(self.testset)
        return self.pipeline.score(corpus,target)

    def confidence(self,entity):
        vector = getkeystring(entity)
        return self.pipeline.predict_proba(vector)

class TreeClassifier:
    def __init__(self,subclass=None):
        self.pipeline  = pipeline()
        self.threshold = 0.05

        # make tree from nested ontology
        with open("../data/nestedontology.json",'r') as f:
            ontology = json.load(f)[0]
        self.root = self._buildtree(ontology)
        if subclass: self.root = self.getsubnode(subclass)

    def getsubnode(self,classname):
        ''' returns the node in the tree that matches classname '''
        for node in iter(self):
            if node.name == classname:
                return node
        raise ValueError(classname + " is not a valid class name!")

    def _buildtree(self,json_tree):
        ''' build tree from nested json '''
        root = Node(json_tree["name"],self.pipeline)
        for child in json_tree["children"]:
            root.children.append(self._buildtree(child))
        return root

    def __iter__(self):
        ''' BFS traversal of tree '''
        queue = [self.root]
        while queue != []:
            current = queue.pop(0)
            queue.extend(current.children)
            yield current

    def train(self,trainnum,testnum):
        ''' train each node's classifier '''
        for node in iter(self):
            print("Training",node.name)
            node.getsets(trainnum,testnum)
            node.train()

    def predict(self,entity):
        ''' predict downwards in tree from root node '''
        node = self.root
        while node.hasChildren() and node.confidence(entity) > self.threshold:
            node = node.predict(entity)
        return node.name

def features(dataset):
    getkeystring = lambda x: ' '.join(x["properties"])
    return list(map(getkeystring, dataset))

def labels(dataset):
    getclassname = lambda x: x["class"]
    return list(map(getclassname, dataset))

def pipeline():
    return Pipeline([('vect',CountVectorizer()),
                     ('tfidf',TfidfTransformer()),
                     ('clf',MultinomialNB()),
                   ])

if __name__ == "__main__":
    tree = TreeClassifier()

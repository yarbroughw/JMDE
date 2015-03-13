class Node:
    def __init__(self,n,classifier):
        self.name       = n
        self.children   = []
        self.classifier = classifier

    def hasChildren(self):
        return self.children != []

    def train(trainnum,testnum):
        trainset,testset = retrieve.sets(category.name)
        corpus = list(map(getkeystring,  trainset))
        target = list(map(getclasslabel, testset))
        self.classifier = pipeline().fit(corpus,target)

    def condfidence(self,entity):
        # TODO
        pass


class TreeClassifier:
    def __init__(self):
        # make tree from nested ontology
        self.threshold = 0.05

    def train(trainnum,testnum):
        ''' train each node's classifier '''
        for node in iter(self):
            node.train(trainnum,testnum)

    def predict(entity):
        ''' predict downwards in tree from root node '''
        #TODO: flesh out
        node = self.root
        # predict down in tree
        while node.hasChildren() and node.confidence(entity) > self.threshold:
            node = node.predict(entity)

def getkeystring(entity):
    return ' '.join(entity["properties"])

def getclasslabel(entity):
    return entity["class"]

def pipeline():
    return Pipeline([('vect',CountVectorizer()),
                     ('tfidf',TfidfTransformer()),
                     ('clf',MultinomialNB()),
                   ])


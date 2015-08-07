import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
import pickle

# import treeclassifier
import retrieve

with open("../data/classifiers/treedump10000.pkl", 'rb') as f:
    tree = pickle.load(f)


def plot_confusion_matrix(labelset, cm, name, title='Confusion matrix',
                          cmap=plt.cm.OrRd):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(labelset))
    plt.xticks(tick_marks, labelset, rotation=30)
    plt.yticks(tick_marks, labelset)
    plt.tight_layout(pad=1.4, w_pad=0.0, h_pad=0.0)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    # plt.savefig("../output/cms/" + name + ".png")
    plt.show()


def retrieve_children(amount, node):
    entities = []
    keys = node.children.keys()
    amount = amount // len(keys)
    for childname in node.children.keys():
        entities.extend(retrieve.direct(amount, childname))
    return entities


def cm_from_testset(node, test_set):
    predictions = [node.predict(x) for x in test_set]
    labels = list(map(lambda x: x["class"], test_set))
    print(*zip(predictions, labels))
    labelset = list(set(labels))
    # if node.name != "owl:Thing":
        # labelset.append(node.name)
    title = 'Confusion Matrix of Classifications in \"' + node.name + '\" node'
    plot_confusion_matrix(labelset,
                          metrics.confusion_matrix(labels, predictions),
                          node.name,
                          cmap=plt.cm.winter,
                          title=title)

node = tree.getsubnode("AnatomicalStructure")
test_set = retrieve_children(100, node)
cm_from_testset(node, test_set)

node = tree.getsubnode("Device")
test_set = retrieve_children(100, node)
cm_from_testset(node, test_set)

node = tree.getsubnode("SportsEvent")
test_set = retrieve_children(100, node)
cm_from_testset(node, test_set)

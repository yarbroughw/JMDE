from __future__ import print_function
import treeclassifier
import basicclassifier
import retrieve
import pickle


ns = [10, 100, 1000, 10000]

for n in ns:
    print("making treeclassifier with trainsize of", n, "...")
    tree = treeclassifier.TreeClassifier()
    tree.autotrain(n)
    tree.learnthresholds()
    print("saving.")
    filename = "../data/treesaves/learnedtreedump" + str(n) + ".pkl"
    with open(filename, 'wb') as f:
        pickle.dump(tree, f)

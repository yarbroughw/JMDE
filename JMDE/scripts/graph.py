from __future__ import print_function
import json
import matplotlib.pyplot as plt
import numpy as np

with open("../data/results/scores.json", 'r') as f:
    scores = json.load(f)
with open("../data/results/distances.json", 'r') as f:
    distances = json.load(f)
with open("../data/results/times.json", 'r') as f:
    times = json.load(f)

print(scores)
print(distances)
print(times)


def scorelines():
    ''' line plot of learned classifier's scores (x = ns, y = accuracy) '''
    ns = [10, 100, 1000, 10000]
    fig, ax = plt.subplots()
    ax.plot(ns, scores["basic"], marker='o', linestyle='-', color='r',
            label='Basic')
    ax.plot(ns, scores["tree"], marker='s', linestyle='-', color='b',
            label='Tree')
    ax.plot(ns, scores["trained"], marker='^', linestyle='-', color='g',
            label='Learned Thresholds')
    ax.set_xlabel('Size of Training Set')
    ax.set_ylabel('Average Accuracy over Test Set')
    title = 'Learning-based Classifier Accuracy by Size of Training Set'
    ax.set_title(title)
    ax.set_xscale('log')
    ax.set_xlim(7, 14000)
    ax.set_ylim(0.0, 1.0)
    ax.set_yticklabels(["0%", "20%", "40%", "60%", "80%", "100%"])
    plt.legend(loc=2)
    plt.tight_layout()
    plt.savefig("../output/linechart_scores.png")


def scorebars():
    ''' bar chart of classifier's scores by classifier type (y = accuracy) '''
    scorelist = [scores["lexical"], scores["basic"][-1], scores["tree"][-1],
                 scores["trained"][-1]]
    N = 4
    offset = 0.125
    ind = np.arange(N)  # the x locations for the groups
    width = 0.75        # the width of the bars

    fig, ax = plt.subplots()
    ax.bar(ind+offset, scorelist, width, alpha=0.40, color='r')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Average Accuracy')
    ax.set_title('Classification Accuracy by Classifier Type')
    ax.set_xticks(ind+width/2+offset)
    ax.set_xticklabels(('Lexical Matcher',
                        'Basic Classifier',
                        'Tree Classifier',
                        'Learned Thresholds'))
    ax.set_ylim(0.0, 1.0)
    ax.set_yticklabels(["0%", "20%", "40%", "60%", "80%", "100%"])
    plt.tight_layout()
    plt.savefig("../output/barchart_scores.png")


def distancebars():
    ''' bar chart of classifier's distances by category (y = accuracy) '''
    distancelist = [distances["basic"], distances["tree"],
                    distances["trained"]]
    N = 3
    offset = 0.125
    ind = np.arange(N)  # the x locations for the groups
    width = 0.75        # the width of the bars

    fig, ax = plt.subplots()
    ax.bar(ind+offset, distancelist, width, alpha=0.40, color='b')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Average Distance')
    ax.set_title('Average Distance of Predictions by Classifier Type')
    ax.set_xticks(ind+width/2+offset)
    ax.set_xticklabels(('Basic Classifier', 'Tree Classifier',
                        'Tree w/ Learned Thresholds'))
    ax.set_ylim(0.0, 1.0)
    # ax.set_yticklabels(["0%", "20%", "40%", "60%", "80%", "100%"])
    plt.tight_layout()
    plt.savefig("../output/barchart_distances.png")


def timelines():
    ''' line plot of learned classifier's times (x = ns, y = ms) '''
    ns = [10, 100, 1000, 10000]
    fig, ax = plt.subplots()

    ax.errorbar(ns, times["lexical"]["avgs"], yerr=times["lexical"]["stddevs"],
                marker='*', linestyle='-', color='y', label='Lexical')

    ax.errorbar(ns, times["basic"]["avgs"], yerr=times["basic"]["stddevs"],
                marker='o', linestyle='-', color='r', label='Basic')

    ax.errorbar(ns, times["tree"]["avgs"], yerr=times["tree"]["stddevs"],
                marker='s', linestyle='-', color='b', label='Tree')

    ax.errorbar(ns, times["trained"]["avgs"], yerr=times["trained"]["stddevs"],
                marker='^', linestyle='-', color='g',
                label='Learned Thresholds')

    ax.set_xlabel('Size of Test Set')
    ax.set_ylabel('Time to Classify Test Set (ms)')
    ax.set_title('Classifier Execution Times (ms) by Size of Test Set')
    ax.set_xscale('log')
    #ax.set_yscale('log')
    ax.set_xlim(7, 14000)
    # ax.set_ylim(0.0, 1.0)
    # ax.set_yticklabels(["0%", "20%", "40%", "60%", "80%", "100%"])
    plt.legend(loc=2)
    plt.tight_layout()
    plt.show()
    #plt.savefig("../output/linechart_times.png")


if __name__ == "__main__":
    #scorelines()
    #scorebars()
    #distancebars()
    timelines()

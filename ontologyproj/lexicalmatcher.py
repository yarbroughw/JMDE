import json
import retrieve


def distance(inputprops, targetprops):
    if not targetprops:
        return 0
    matches = [x for x in inputprops if x in targetprops]
    return (len(matches) / len(targetprops))


class LexicalMatcher:
    def __init__(self):
        with open("../data/properties.json") as f:
            self.properties = json.load(f)

    def closestclass(self, properties):
        maxdist = 0
        bestclass = None
        for k, v in self.properties.items():
            if distance(properties, v) > maxdist:
                bestclass = k
        return bestclass

    def classify(self, document):
        properties = list(document.keys())
        return self.closestclass(properties)

    def classifyset(self, entities):
        for entity in entities:
            self.classify(entity["properties"])

    def score(self, documents):
        total = 0
        for entity in documents:
            props = entity["properties"]
            guessed = self.classify(props)
            if guessed == entity["deepest"]:
                total += 1
        return total / len(documents)


if __name__ == "__main__":
    print("testing matcher for 1000 entities")
    matcher = LexicalMatcher()
    entities = retrieve.entities(1000, "owl:Thing")
    matcher.score(list(entities))

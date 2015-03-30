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


if __name__ == "__main__":

    entitycount = 1000

    matcher = LexicalMatcher()
    entities = retrieve.entities(entitycount, "owl:Thing")
    total = 0

    for entity in entities:
        props = entity["properties"]
        print("checking", entity["name"])
        guessed = matcher.classify(props)
        if guessed == entity["class"]:
            total += 1

    correctratio = total / entitycount
    print(correctratio, "of the entities guessed correctly.")

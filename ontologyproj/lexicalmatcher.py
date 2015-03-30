import json
import retrieve


def distance(inputprops, targetprops):
    matches = [x for x in inputprops if x in targetprops]
    return (len(matches) / len(targetprops))


class LexicalMatcher:
    def __init__(self):
        with open("../data/allproperties.json") as f:
            self.properties = json.load(f)

    def closestclass(self, properties):
        maxdist = 0
        for k, v in self.properties:
            if distance(properties, v) > maxdist:
                bestclass = k
        return bestclass

    def classify(self, document):
        properties = list(document.keys())
        return self.closestclass(properties)


if __name__ == "__main__":

    matcher = LexicalMatcher()
    entities = retrieve.entities(100, "owl:Thing")
    total = 0

    for entity in entities:
        props = entity["properties"]
        guessed = matcher.classify(props)
        if guessed == entity["Class"]:
            total += 1

    correctratio = total / len(entities)
    print(correctratio, "of the entities guessed correctly.")

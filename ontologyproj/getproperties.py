import json
import time
from SPARQLWrapper import SPARQLWrapper, JSON

PREFIX = "http://dbpedia.org/ontology/"
toName = lambda x: x[len(PREFIX):]


def classproperties(sparql, class_):
    time.sleep(2)
    sparql.setQuery("""
    select distinct ?property where {
        ?property <http://www.w3.org/2000/01/rdf-schema#domain>
        <http://dbpedia.org/ontology/""" + class_ + """> .
    }
    """)
    print(class_, end=' ')
    x = sparql.query().convert()["results"]["bindings"]
    x = [prop["property"]["value"] for prop in x]
    return x


with open("../data/flatontology.json", 'r') as f:
    flatontology = json.load(f)
with open("../data/properties.json", 'r') as f:
    properties = json.load(f)

a = set([k for k, v in flatontology.items()])
b = set([k for k, v in properties.items()])
classes = a - b
n = len(classes) - 1

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)

for i, class_ in enumerate(classes):
    print(i, "of", n, end=": ")
    x = list(map(toName, classproperties(sparql, class_)))
    print(x)
    properties[class_] = x
    with open("../data/properties.json", 'w') as f:
        json.dump(properties, f)

props = {}
for class_ in [k for k, v in properties.items()]:
    parents = flatontology[class_]["fullpath"].split('/')[:-1]
    props[class_] = [prop for p in parents for prop in properties[p]]
    print(props[class_])

    with open("../data/allproperties.json", 'w') as f:
        json.dump(props, f)

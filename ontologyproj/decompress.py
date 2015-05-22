import json
import shutil
import os.path


with open("../data/flatontology.json", 'r') as f:
    ontology = json.load(f)

filenames = [k for k, v in ontology.items() if v["depth"] == 1]
filenames = map(lambda x: x + ".csv.gz", filenames)

for filename in filenames:
    if os.path.isfile("../data/csvgz/" + filename):
        shutil.move("../data/csvgz/" + filename,
                    "../data/csv/" + filename)

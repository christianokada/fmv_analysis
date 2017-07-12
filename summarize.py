import os, json
import pandas as pd

path = 'data/'
json_files = [pos_json for pos_json in os.listdir(path) if pos_json.endswith('.json')]
print json_files  # for me this prints ['foo.json']
print "\n"

description = []

for js in json_files:
    with open(os.path.join(path, js)) as json_file:
        # do something with your json; I'll just print
        data = json.load(json_file)
        if "description" in data:
            text = data["description"]["captions"][0]["text"]
            if (len(description) < 1):
                description.append(text)
            if (len(description) > 0 and text != description[len(description) - 1]):
                description.append(text)
            # print (data["description"]["captions"][0]["text"])
        # print json.load(json_file)

for d in description:
    print d

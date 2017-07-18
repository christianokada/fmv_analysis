import os, json
import pandas as pd

# get all json files
path = 'data/'
json_files = [pos_json for pos_json in os.listdir(path) if pos_json.endswith('.json')]

def parse_json_name(text):
    filename = text.split(".")
    return filename[0] + ".jpg"

description = []
images = []
count = 0 

for js in json_files:
    with open(os.path.join(path, js)) as json_file:
        # print timestamp : image description
        data = json.load(json_file)
        if "description" in data:
            text = data["timestamp"] + " " + data["description"]["captions"][0]["text"]
            if (len(description) < 1):
                description.append(text)
                images.append(parse_json_name(json_files[count]))
            if (len(description) > 0 and text[6:] != description[len(description) - 1][6:]):
                description.append(text)
                images.append(parse_json_name(json_files[count]))\
        # print json.load(json_file)
        count += 1

for d in description:
    print d
    
def parse_json_name(text):
    filename = text.split(".")
    return filename[0] + ".jpg"

index1 = open("index1.txt", "r")
index2 = open("index2.txt", "r")
html = index1.read()
html_images = []

for x in range (0, len(images)):
    html += '<a class="gallery-item" href="single.html"><img src="analyze/'+ images[x] + '" alt="" width="100%" height="auto"><span class="overlay"><h2>'+ description[x] + '</h2></span></a>'
    x += 1

html += index2.read()

index = open("index.html", "w")
index.write(html)
index.close()
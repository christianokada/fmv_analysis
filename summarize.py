import os, json
import pandas as pd

# get all json files
path = 'data/'
json_files = [pos_json for pos_json in os.listdir(path) if pos_json.endswith('.json')]

def parse_json_name(text, ext):
    filename = text.split(".")
    return filename[0] + ext

description = []
images = []
tags = [] # add tags to image pages
count = 0 

for js in json_files:
    with open(os.path.join(path, js)) as json_file:
        # print timestamp : image description
        data = json.load(json_file)
        if "description" in data:
            text = data["timestamp"] + " " + data["description"]["captions"][0]["text"]
            if (len(description) < 1):
                description.append(text)
                images.append(parse_json_name(json_files[count], ".jpg"))
            if (len(description) > 0 and text[6:] != description[len(description) - 1][6:]):
                description.append(text)
                images.append(parse_json_name(json_files[count], ".jpg"))\
        # print json.load(json_file)
        count += 1

for d in description:
    print d

single1 = open("web/single1.txt", "r").read()
single2 = open("web/single2.txt", "r").read()

# create individual image pages
pages = []
for x in range (0, len(images)):
    name = parse_json_name(json_files[x], ".html")
    pages.append(name)
    page = open("pages/"+name, "w")
    text = single1 + '<div class="fh5co-narrow-content animate-box fh5co-border-bottom" data-animate-effect="fadeInLeft"><h2 class="fh5co-heading" ></span></h2><p><p>' + description[x] + '</p></p><div class="row"><div class="col-md-12"><figure><img src="../analyze/' + images[x] + '" alt="" width="75%" height="auto" class="img-responsive"></figure></div></div></div>' + single2
    # text +=  add tags here
    page.write(text)

index1 = open("web/index1.txt", "r")
index2 = open("web/index2.txt", "r")

html = index1.read()
html_images = []

# create index page
for x in range (0, len(images)):
    html += '<a class="gallery-item" href="pages/' + pages[x] + '"><img src="analyze/'+ images[x] + '" alt="" width="100%" height="auto"><span class="overlay"><h2>'+ description[x] + '</h2></span></a>'
    x += 1

html += index2.read()

index = open("index.html", "w")
index.write(html)
index.close()

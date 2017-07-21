import os, json
import pandas as pd
from bs4 import BeautifulSoup as Soup

# get all json files
path = 'data/'
json_files = [pos_json for pos_json in os.listdir(path) if pos_json.endswith('.json')]

def parse_json_name(text, ext):
    filename = text.split(".")
    return filename[0] + ext

description = [] # CV description
images = [] # image file names
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
                tags.append(data["description"]["tags"])
                images.append(parse_json_name(json_files[count], ".jpg"))
            if (len(description) > 0 and text[6:] != description[len(description) - 1][6:]):
                description.append(text)
                tags.append(data["description"]["tags"])
                images.append(parse_json_name(json_files[count], ".jpg"))\
        # print json.load(json_file)
        count += 1

for d in description:
    print d

json_list = []
for img in images:
    json_list.append(parse_json_name(img, ""))

data_json = open("images.json", "w")
data_json.write(json.dumps(json_list))
data_json.close()

#create individual images pages
pages = []
for x in range (0, len(images)):
    name = parse_json_name(json_files[x], ".html")
    pages.append(name)
    page = open("pages/"+name, "w")
    base = open("web/base_single.txt")
    soup = Soup(base, "html.parser")
    loc = soup.find("div", { "id" : "image-loc" })
    element = soup.new_tag('div')
    element['class'] = 'fh5co-narrow-content animate-box fh5co-border-bottom'
    element['data-animate-effect'] = 'fadeInLeft'
    h2 = soup.new_tag('h2')
    h2['class'] = 'fh5co-heading'
    p = soup.new_tag('p')
    p.insert(1, description[x])
    div = soup.new_tag('div')
    div['class'] = 'row'
    sub_div = soup.new_tag('div')
    sub_div['class'] = 'col-md-12'
    figure = soup.new_tag('figure')
    img = soup.new_tag('img')
    img['class'] = 'img-responsive'
    img['src'] = '../analyze/' + images[x]
    img['width'] = '75%'
    img['height'] = 'auto'
    
    figure.insert(1, img)
    sub_div.insert(1, figure)
    div.insert(1, sub_div)

    element.insert(1, h2)
    element.insert(2, p)
    element.insert(3, div)

    # add tags below
    tags_element = soup.new_tag('div')
    h2 = soup.new_tag('h2')
    h2['class'] = 'tags_h2'
    # h2.insert(1, 'Tags')
    div = soup.new_tag('div')
    div['class'] = 'tags_list'
    ul = soup.new_tag('ul')
    ul['id'] = 'menu'
    ul['style'] = 'list-style-type:none'

    # put tags in unordered list
    for t in range (0, len(tags[x])):
        li = soup.new_tag('li')
        li.insert(t, tags[x][t])
        ul.insert(t, li)

    # insert tag number
    tag_num_loc = soup.find("div", { "class" : "col-md-4 text-center" })
    tag_num = soup.new_tag('span')
    tag_num['class'] = 'fh5co-counter js-counter'
    tag_num['data-from'] = '0'
    tag_num['data-to'] = len(tags[x])
    tag_num['data-speed'] = '1500'
    tag_num['data-refresh-interva'] = '50'

    # insert nested tags
    div.insert(1, ul)
    tags_element.insert(1, h2)
    tags_element.insert(2, div)

    # add html after selected location
    loc.insert_after(tags_element)
    loc.insert_after(element)
    tag_num_loc.insert_after(tag_num)

    #write to file
    page.write(str(soup))
    page.close()

# create index.html
html_index = open("web/base.txt")
soup = Soup(html_index, "html.parser")
gallery = soup.find("div", { "class" : "image-gallery" })

# table = soup.new_tag('table')
# table['id'] = 'table'

# iterate backwards and add images
for x in range(len(images) - 1, -1, -1):
####################
    # tr = soup.new_tag('tr')
    # tr['class'] = 'table_header'
    # td = soup.new_tag('td')
####################
    element = soup.new_tag('a')
    element['class'] = 'gallery-item'
    element['href'] = 'pages/' + pages[x]
    element['id'] = json_list[x]
    image = soup.new_tag('img')
    image['src'] = 'analyze/'+ images[x]
    image['width'] = '100%'
    image['height'] = 'auto'
    span = soup.new_tag('span')
    span['class'] = 'overlay'
    h2 = soup.new_tag('h2')

    # insert nested tags
    h2.insert(1, description[x])
    span.insert(1, h2)
    element.insert(1, image)
    element.insert(2, span)
##############
    # td.insert(1, element)
    # tr.insert(1, td)
    # table.insert(1, tr)

    # gallery.insert_after(tr)
##############
    # insert html at specified location (gallery)
    gallery.insert_after(element)

# write to file
index = open("index.html", "w")
index.write(str(soup))
index.close()

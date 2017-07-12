# Source: https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts/python

########### Python 2.7 #############
import httplib, urllib, base64, json
import os

# from tf_idf import sortedTfIdfLists
import json
from pprint import pprint
###############################################
#### Update or verify the following values. ###
###############################################
# Replace the subscription_key string value with your valid subscription key.
subscription_key = 'b9140559a8fd44b981f7e6c906151a53'

# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your subscription keys.
# For example, if you obtained your subscription keys from the westus region, replace
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
# a free trial subscription key, you should not need to change this region.
uri_base = 'westcentralus.api.cognitive.microsoft.com'


# Program has two options:
# 1) analyzing locally stored images
# 2) analyzing image from URL
# Uncomment/comment code accordingly

def main():
    params = urllib.urlencode({
        # Request parameters. All of them are optional.
        'visualFeatures': 'Categories,Description,Color',
        'language': 'en',
    })
    localImages(params) # Uncomment if you want to analyze all images inside ./analyze/ directory
    # urlImages(params) # Uncomment if you want to analyze URL defined in urlImages method

    with open('data.json') as data_file:    
        data = json.load(data_file)

    currentPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data") # ./analyze
    for file in os.listdir(currentPath):
        try:
            if file.endswith(".json"):
                with open(file) as data_file:
                    data = json.load(data_file)
                pprint(data)
                
        except Exception:
            print "Error with reading json files"
    

####################################################################
#### Two ways to run this program, analyze localImages or urlImages
####################################################################
# Used if you want to analyze all images stored on ./analyze/ directory
def localImages(params):
    headers = headersForLocalImages()
    analyzeLocalImages(params, headers)

# Used if you want to analyze an image from a URL, does not store JSON data in ./data/ directory
def urlImages(params):
    headers = headersForURLImage()
    data = "{'url':'http://dabblesandbabbles.com/wp-content/uploads/2013/07/I_Spry_1a.jpg'}"
    analyzeImageData(params, data, headers)

#####################################################################
#### Methods for different header values
####################################################################
# header value for URL images, uses application/json
def headersForURLImage():
    headers = {
        # Request headers.
        'Content-Type': 'application/json', # Used if you want to enter URL
        'Ocp-Apim-Subscription-Key': subscription_key,
    }
    return headers

# header value for local images, uses application/octet-stream
def headersForLocalImages():
    headers = {
        # Request headers.
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }
    return headers

#####################################################################
#### Methods for analyzing either locally stored images, or images from URL
#####################################################################
# for locally stored images, looks in ./analyze folder for images of type
# png, jpg, or bmp. analyze each one individually, print and store data in data directory
def analyzeLocalImages(params, headers):
    # directory of images to analyze
    currentPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analyze") # ./analyze
    for file in os.listdir(currentPath):
        try:
          # check for png, jpg, or bmp
          # file = image.jpg
          if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".bmp"):
              img_name = os.path.splitext(os.path.basename(file))[0] # img_name = image
              img_fullPath = os.path.join(currentPath, file) # img_fullPath = .\analyze\image.jpg
          else:
              continue

        except Exception as e:
          print("Error with File: " + img_fullPath)
          print(e)

        # get raw binary image data, run through analyzeImageData()
        with open (img_fullPath, 'rb') as f:
            data = f.read()

        jsonData = analyzeImageData(params, data, headers)
        storeData(jsonData, img_name)

# used for both locally stored images and image from URL
# locally stored images get the data from f.read(), URL gets data from the URL
def analyzeImageData(params, data, headers):
    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection(uri_base)
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, data, headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        jsonData = json.loads(data)
        print ("Response:")
        print (json.dumps(jsonData, sort_keys=True, indent=2))
        conn.close()

        return jsonData

    except Exception as e:
        print('Error:')
        print(e)

# Used in analyzeLocalImages, stores json data in ./data directory
# location: ./data/img_name.json
def storeData(jsonData, img_name):
    # store data in data directory
    with open('data\\' + img_name + ".json", 'w') as fp:
        json.dump(jsonData, fp, sort_keys=True, indent=2)

if __name__ == "__main__":
    main()

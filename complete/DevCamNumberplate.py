import requests
import json
import time
import re, sys, os

mode = "URL" # default mode
# Azure access point
APIURL = 'https://westeurope.api.cognitive.microsoft.com/vision/v2.0/recognizeText?mode=Printed'

# key to Azure Cloud
key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
imageBaseURL = 'https://raw.githubusercontent.com/volkerhielscher/netnei/master/complete/images/'
localImagesPath = './images/'

headersURL = { 
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': key }
headersLocal = { 
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': key }

jsonData = {"url": imageBaseURL + "bild1.jpg"}

# contains every file in the specified path
directory = os.listdir(localImagesPath)

def getText (url):
    time.sleep(3) # give Azure time to compute
    try:
        i = 0
        # get the response of the image recognition
        request2 = requests.get(url, headers=headersLocal)
        print ('STATUSTEXT: ')
        print (request2.text)
        # test, if Azure needs more computing time
        while(request2.json()['status'] == 'Running' or request2.json()['status'] == 'Not started'):
            print ('STATUSTEXT: ' + request2.text)
            print ("Loop "+str(i))
            i += 1
            try:
                request2 = requests.get(url, headers=headersLocal)
            except requests.exceptions.RequestException as e:
                print (e)
            time.sleep(2)
        # lines is a array that holds all the recognized text
        for line in request2.json()['recognitionResult']['lines']:
            # remove small o's as they are misrecognized circles
            text = re.sub('o', '', line['text'])
            # search for german number plate via regular expression
            match = re.search("[A-ZÖÜÄ]{1,3}[ |-][A-ZÖÜÄ]{1,2}[ |-][0-9]{1,4}[E|H]?", text)
            if (match):
                print("Plate: "+ text)
            else:
                print('Not a plate: '+text)

    except requests.exceptions.RequestException as e:
        print (e)
    except Exception as e:
        print ('Error in getText():')
        print (e)

def postToCloud (mode, file):
    # check how to access files
    try:

        if mode == 'local':
            # open image as binary and post it to the Azure Cloud 
            data = open( localImagesPath + file, 'rb').read()
            print("File opened")
            request = requests.post(APIURL, headers=headersLocal, data=data, timeout=10)    
        elif mode == 'URL':
            # use images from the github remote repository
            jsonData = {"url": imageBaseURL + file}
            request = requests.post(APIURL, headers=headersURL, json=jsonData, timeout=10)        
        else:
            print ('Error: PostToCloud() was called with wrong mode')
            return

    except Exception as e:
        print ('Error in postToCloud():')
        print (e)
        return    

    # call getText() to get the result from Azure. The desired URL is sent as part of the headers.
    try:
        reqHeader = request.headers
        url = reqHeader['Operation-Location']
        getText(url)
    except Exception as e:
        print ('Error in postToCloud():')
        print (e)

def uploadIMG():
    print ("Mode: " + mode)
    print ("Args: "+ str(len(sys.argv)))
    # how was the script called? If only one argument was given, is it mode or imagename?
    if len(sys.argv) < 2 or (len(sys.argv) == 2 and (sys.argv[1] == 'local' or sys.argv[1] == 'URL')):
        # if no image was specified, loop over every image in the project folder (localImagesPath)
        for file in directory:
            if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg') or file.endswith('.bmp'):
                print (file + ' :------------------------------------------------------------------')
                postToCloud(mode, file)      
    # if only image was specified, but not mode, post specified image with default mode       
    elif (len(sys.argv) == 2 and sys.argv[1] != 'local' and sys.argv[1] != 'URL'):
        postToCloud(mode, sys.argv[1])
    # else corresponds to script call with 2 arguments, where mode is the first and image is the second
    else:
        postToCloud(mode, sys.argv[2])

# set mode
if(len(sys.argv) > 1 and (sys.argv[1] == 'local' or sys.argv[1] == 'URL')):
    mode = sys.argv[1]

uploadIMG()

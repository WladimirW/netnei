import requests
import json
import time
import re, sys, os

mode = "URL" # default mode
azureEndpoint = 'https://westcentralus.api.cognitive.microsoft.com/vision/v2.0'
# Azure access point consists your endpoint + the specific service to use
azureURL = azureEndpoint + '/recognizeText?mode=Printed'
# Access Point to check, if number plate is allowed
permitURL = 'https://kbamock.rg02.diconium.cloud/plate/'
# key to Azure Cloud
key = 'XXXXXXXXXXXXXXXXXXXXXX' #FIXME change Xs to your personal Azure resource key.
imageBaseURL = 'https://raw.githubusercontent.com/volkerhielscher/netnei/master/complete/images/'


headersURL = { 
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': key }
headersLocal = { 
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': key }

jsonData = {"url": imageBaseURL + "bild1.jpg"}

localImagesPath = './images/'
# contains every file in the specified path
directory = os.listdir(localImagesPath)



def getEntryPermit(numberPlate):
    '''checks if number plate is allowed in Stuttgart by contacting a service.

    Argument:
    numberPlate -- number plate of a car as String given by getPlate()
    '''
    fullPermitURL = permitURL + numberPlate
    # the requests module automatically encodes URLs before sending the request.
    # e.g. 'https://www.google.com/this is a test' -> 'https://www.google.com/this%20is%20a%20test'
    request3 = requests.get(fullPermitURL)
    print ('Send GET request to ' + request3.url)
    print (request3.text)
    print ('')
    brand = request3.json()['Brand']
    model = request3.json()['Modell']
    isAllowed = request3.json()['StuttgartEntry']
    if isAllowed:
        print (brand + ' ' + model + ' with number plate ' + numberPlate + ' is allowed to enter Stuttgart.')
    else:
        print (brand + ' ' + model + ' with number plate ' + numberPlate + ' is forbidden to enter Stuttgart.')


def getPlate (url):
    '''Get response of posted image and parses it to access number plate text.
    It uses a regular expression to filter received text for german number plates.

    Argument: 
    url -- url to send the Get Request to. Obtained by posting image to Azure Cloud.
    '''
    time.sleep(3) # give Azure time to compute
    try:
        i = 0
        # get the response of the image recognition
        request2 = requests.get(url, headers=headersURL)
        print ('STATUSTEXT: ')
        print (request2.text)
        # test, if Azure needs more computing time
        while(request2.json()['status'] == 'Running' or request2.json()['status'] == 'Not started'):
            print ('STATUSTEXT: ' + request2.text)
            print ("Loop "+str(i))
            i += 1
            try:
                request2 = requests.get(url, headers=headersURL)
            except requests.exceptions.RequestException as e:
                print (e)
            time.sleep(2)
        # lines is an array that holds all the recognized text
        for line in request2.json()['recognitionResult']['lines']:
            # remove small o's as they are misrecognized circles
            text = re.sub('o', '', line['text'])
            # search for german number plate via regular expression
            match = re.search("[A-ZÖÜÄ]{1,3}[ |-][A-ZÖÜÄ]{1,2}[ |-][0-9]{1,4}[E|H]?", text)
            if (match):
                print('')
                print("Plate: "+ text)
                print('')
                getEntryPermit(text)
            else:
                print('Not a plate: '+text)

    except requests.exceptions.RequestException as e:
        print (e)
    except Exception as e:
        print ('Error in getPlate():')
        print (e)


def postToCloud (mode, file):
    '''Post image to Azure cloud and calls getPlate() to get response text.

    Arguments:
    mode -- specifies in which mode the post request is done ('local', 'URL')
    file -- specifies which file to post (*.jpg, *.jpeg, *.bmp, *.png)

    Parameters:
    data -- file in binary, used for local access
    jsonData -- requestbody in json format ({"url": "imageURL"})
    request -- request object of post request. Used to access its headers (request.headers)
    '''
    # check how to access files
    try:

        if mode == 'local':
            # open image as binary and post it to the Azure Cloud 
            data = open( localImagesPath + file, 'rb').read()
            print("File opened")
            request = requests.post(azureURL, headers=headersLocal, data=data, timeout=10)    
        elif mode == 'URL':
            # use images from the github remote repository
            jsonData = {"url": imageBaseURL + file}
            request = requests.post(azureURL, headers=headersURL, json=jsonData, timeout=10)        
        else:
            print ('Error: PostToCloud() was called with wrong mode')
            return

    except Exception as e:
        print ('Error in postToCloud():')
        print (e)
        return    

    # call getPlate() to get the result from Azure. The desired URL is sent as part of the headers.
    try:
        
        url = request.headers['Operation-Location']
        getPlate(url)
    except Exception as e:
        print ('Error in postToCloud():')
        print (request.text)
        print (e)


def main(mode):
    '''the main function checks, how the script was called and calls postIntoCloud()
    with the correct arguments. This function is the access point of the script.

    Parameters:
    mode -- specifies in which mode to operate ('local', 'URL')
    file -- file in directory ('*.jpg', '*png', '*.jpeg', '*.bmp')
    sys.argv -- contains arguments from command line. sys.argv[0] is the name of the script.
    '''
    # set mode
    if(len(sys.argv) > 1 and (sys.argv[1] == 'local' or sys.argv[1] == 'URL')):
        mode = sys.argv[1]
    # how was the script called? If only one argument was given, is it mode or imagename?
    if len(sys.argv) < 2 or (len(sys.argv) == 2 and (sys.argv[1] == 'local' or sys.argv[1] == 'URL')):
        # if no image was specified, loop over every image in the project folder (localImagesPath)
        for file in directory:
            if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg') or file.endswith('.bmp'):
                print (file + ' :------------------------------------------------------------------')
                postToCloud(mode, file)      
    # if only image was specified, but not mode, post specified image with default mode       
    elif (len(sys.argv) == 2 and sys.argv[1] != 'local' and sys.argv[1] != 'URL'):
        if sys.argv[1].endswith('.jpg') or sys.argv[1].endswith('.png') or sys.argv[1].endswith('.jpeg') or sys.argv[1].endswith('.bmp'):
            postToCloud(mode, sys.argv[1])
    # else corresponds to script call with 2 arguments, where mode is the first and image is the second
    else:
        postToCloud(mode, sys.argv[2])
    print ("Mode: " + mode)

main(mode)
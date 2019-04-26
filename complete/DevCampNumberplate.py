import requests
import time, re
import sys, os

mode = "URL" # default mode
azureEndpoint = 'https://westcentralus.api.cognitive.microsoft.com/vision/v2.0' #TODO replace with your endpoint if needed
# Azure access point consists your endpoint + the specific service to use
azureURL = azureEndpoint + '/recognizeText?mode=Printed'
# key to Azure Cloud
key = 'e139df45703c4af6bb2da983b0c6636f' #FIXME change Xs to your personal Azure resource key.
imageBaseURL = 'https://raw.githubusercontent.com/volkerhielscher/netnei/master/complete/images/'
# Headers for URL call
headersURL = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': key }
headersLocal = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': key }

localImagesPath = '../complete/images/'
# contains every file in the specified path
directory = os.listdir(localImagesPath)

# Access Point to check, if number plate is allowed
permitURL = 'https://kbamock.rg02.diconium.cloud/plate/'

def isMode(argument):
    '''support function that checks wether an argument is a supported mode.
    '''
    if (argument == 'local' or argument == 'URL'):
        return True
    else:
        return False

def isImage(file):
    '''support function that checks, if a file name is actually ending with an image extension.
    '''
    if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg') or file.endswith('.bmp'):
        return True
    else:
        return False

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

def postToCloud(mode, file):
    '''Post image to Azure cloud and calls getPlate() to get response text.

    Arguments:
    mode -- specifies in which mode the post request is done ('local', 'URL')
    file -- specifies which file to post (*.jpg, *.jpeg, *.bmp, *.png)

    Parameters:
    data -- file in binary, used for local access
    jsonData -- requestbody in json format ({"url": "imageURL"})
    request -- request object of post request. Used to access its headers (request.headers)
    '''
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
    try:
        reqHeader = request.headers
        url = reqHeader['Operation-Location']
        print ('Accessing ' + url + ':')
        getPlate(url)
    except Exception as e:
        print ('Exception:')
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
    if(len(sys.argv) > 1 and isMode(sys.argv[1])):
        mode = sys.argv[1]
    # how was the script called? If only one argument was given, is it mode or imagename?
    if len(sys.argv) < 2 or (len(sys.argv) == 2 and isMode(sys.argv[1])):
        # if no image was specified, loop over every image in the project folder (localImagesPath)
        for file in directory:
            if isImage(file):
                print (file + ' :------------------------------------------------------------------')
                postToCloud(mode, file)
            else:
                print (file + ' :------------------------------------------------------------------')
                print ("The specified file is no supported image. Please use .jpg, .png, .jpeg or .bmp files")
    # if only image was specified, but not mode, post specified image with default mode
    elif (len(sys.argv) == 2 and isImage(sys.argv[1])):
            postToCloud(mode, sys.argv[1])
    # if there are atleast 2 extra arguments, set first as mode and second as image
    elif len(sys.argv) > 2 and isMode(sys.argv[1]) and isImage(sys.argv[2]):
        postToCloud(sys.argv[1], sys.argv[2])
    else:
        print ('Error: The arguments were not given correctly. Please use either mode or image as single argument or put mode as first and image as second argument.')

main(mode)
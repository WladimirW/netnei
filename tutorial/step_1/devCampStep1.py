import requests
# -----------------------------------------------
import time, re
# -----------------------------------------------

mode = "URL" # default mode
azureEndpoint = 'https://westcentralus.api.cognitive.microsoft.com/vision/v2.0'
# Azure access point consists your endpoint + the specific service to use
azureURL = azureEndpoint + '/recognizeText?mode=Printed'
# key to Azure Cloud
key = 'XXXXXXXXXXXXXXXXXXXXXX' #FIXME change Xs to your personal Azure resource key.
imageBaseURL = 'https://raw.githubusercontent.com/volkerhielscher/netnei/master/complete/images/'
# Headers for URL call
headersURL = { 
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': key }
# -----------------------------------------------
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

            else:
                print('Not a plate: '+text)
    except requests.exceptions.RequestException as e:
        print (e)
    except Exception as e:
        print ('Error in getPlate():')
        print (e)                
# -----------------------------------------------
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
            # Done in a later step.
            print ()
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
        # -----------------------------------------------
        reqHeader = request.headers
        url = reqHeader['Operation-Location']
        print ('Accessing ' + url + ':')
        getPlate(url)
        # -----------------------------------------------
    except Exception as e:
        print ('Exception:')
        print (request.text)
        print (e)
    

postToCloud(mode, 'bild1.jpg')
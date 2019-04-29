import requests


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
        print (request.headers['Operation-Location'])
    except Exception as e:
        print ('Exception:')
        print (request.text)
        print (e)
    

postToCloud(mode, 'bild1.jpg')
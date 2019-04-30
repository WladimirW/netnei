import requests
import logging

mode = "URL" # default mode
azureEndpoint = 'https://westeurope.api.cognitive.microsoft.com/vision/v2.0' #FIXME replace with your endpoint
# Azure access point consists your endpoint + the specific service to use
azureURL = azureEndpoint + '/recognizeText?mode=Printed'
# key to Azure Cloud
key = 'df27acc978b14118aa250116dab58f7c' #FIXME change Xs to your personal Azure resource key.

imageBaseURL = 'https://raw.githubusercontent.com/volkerhielscher/netnei/master/complete/images/'

# Headers for URL call
headersURL = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': key }



def recognizeTextFromImage(mode, file):
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
            # complete this in a later step
            print () # only for now
        elif mode == 'URL':
            # use images from the github remote repository
            jsonData = {"url": imageBaseURL + file}
            request = requests.post(azureURL, headers=headersURL, json=jsonData, timeout=10)
        else:
            loggerMain.error ('recognizeTextFromImage() was called with wrong mode')
            return
    except requests.exceptions.RequestException as e:
        loggerMain.critical ('Can\'t access Azure services')
        loggerMain.exception (e)
    except Exception as e:
        loggerMain.critical ('undefinded problem in recognizeTextFromImage')
        loggerMain.exception (e)
    try:
        result = request.headers['Operation-Location']
        loggerMain.debug (result)
        return result
    except Exception as e:
        loggerMain.error ('Exception:')
        loggerMain.error (request.text)
        loggerMain.exception (e)

loggerRequests = logging.getLogger('requests')
loggerMain = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(name)s:\t %(message)s')

recognizeTextFromImage(mode, 'bild1.jpg')
import requests
import json
import time
import re, sys, os

mode = "URL"
APIURL = 'https://westeurope.api.cognitive.microsoft.com/vision/v2.0/recognizeText?mode=Printed'
key = 'd9bb988b597f47b18602ca2f2701aa68'
imageBaseURL = 'https://raw.githubusercontent.com/volkerhielscher/netnei/master/complete/images/'
localImagesPath = './images/'

headersURL = { 
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': key }
headersLocal = { 
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': key }

jsonData = {"url": imageBaseURL + "bild1.jpg"}
    
directory = os.listdir(localImagesPath)


def getText (url):
    time.sleep(3)
    try:
        i = 0
        request2 = requests.get(url, headers=headersLocal)
        print ('STATUSTEXT: ')
        print (request2.text)
        while(request2.json()['status'] == 'Running' or request2.json()['status'] == 'Not started'):
            print ('STATUSTEXT: ' + request2.text)
            print ("Loop "+str(i))
            i += 1
            try:
                request2 = requests.get(url, headers=headersLocal)
            except requests.exceptions.RequestException as e:
                print (e)
            time.sleep(2)
        for line in request2.json()['recognitionResult']['lines']:
            text = re.sub('o', '', line['text'])
            match = re.search("[A-ZÖÜÄ]{1,3}[ |-][A-ZÖÜÄ]{1,2}[ |-][0-9]{1,4}[E|H]?", text)
            if (match):
                print("Plate: "+ text)
            else:
                print('Not a plate: '+text)

    except requests.exceptions.RequestException as e:
        print (e)

def uploadIMG():
    try:
        print ("Mode: " + mode)
        if(mode == 'local'):
            if(len(sys.argv) <= 2):
                for file in directory:
                    print(file + ' :')
                    try:    
                        data = open( localImagesPath + file, 'rb').read()
                        print("File opened")
                        request = requests.post(APIURL, headers=headersLocal, data=data, timeout=10)
                        reqHeader = request.headers
                        url = reqHeader['Operation-Location']
                        getText(url)
                    except Exception as e:
                        print(e)
                        
            else:
                try:
                    data = open (localImagesPath + sys.argv[2], 'rb').read()
                    print ('File opened')
                except Exception as e:
                    print(e)
                request = requests.post(APIURL, headers=headersLocal, data=data, timeout=10)
                reqHeader = request.headers
                url = reqHeader['Operation-Location']
                getText(url)
        else:
            if (len(sys.argv) < 2 ):
                for file in directory:
                    print (file + ' :------------------------------------------------------------------')
                    try:
                        jsonData = {"url": imageBaseURL + file}
                        request = requests.post(APIURL, headers=headersURL, json=jsonData, timeout=10)
                        reqHeader = request.headers
                        url = reqHeader['Operation-Location']
                        getText(url)
                    except Exception as e:
                        print ('EXCEPTION:')
                        print(e)
            elif (len(sys.argv) == 2 and sys.argv[1] != 'local' and sys.argv[1] != 'URL'):
                jsonData = {"url": imageBaseURL + sys.argv[1]}
                request = requests.post(APIURL, headers=headersURL, json=jsonData, timeout=10)
                reqHeader = request.headers
                url = reqHeader['Operation-Location']
                getText(url)
            else:
                jsonData = {"url": imageBaseURL + sys.argv[2]}
                request = requests.post(APIURL, headers=headersURL, json=jsonData, timeout=10) 
                reqHeader = request.headers
                url = reqHeader['Operation-Location']
                getText(url)

    except requests.exceptions.RequestException as e:
        print ("RequestException: ")
        print(e)
    except Exception as e:
        print ("Exception: ")
        print(e)


if(len(sys.argv) > 1):
    if(sys.argv[1] == 'local'):
        mode = 'local'


uploadIMG()
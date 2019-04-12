import requests
import json
import time

def getTextFromIMG():
    print ("In getTextFromIMG")
    headers = { 
        'Content-Type': 'application/octet-stream',
        #'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'd9bb988b597f47b18602ca2f2701aa68' }
    jsonData = {"url":"https://bilder.bild.de/fotos-skaliert/bald-nicht-mehr-in-westeuropa-erhaeltlich-autos-von-nissans-nobeltochter-infiniti-wie-dieser-qx30-200922576-60641586/2,w=993,q=high,c=0.bild.jpg"}
    
    try:    
        data = open('./images/bild6.jpg', 'rb').read()
        print("File opened")
    except Exception as e:
        print(e)
    url = 'https://westeurope.api.cognitive.microsoft.com/vision/v2.0/recognizeText?mode=Printed'

    try:
        print ("In getTextFromIMG Try")
        request = requests.post(url, headers=headers, data=data)#json=jsonData)    
        print ("Request posted")
        rheader = request.headers
        print (request.text)
        print (rheader)
        boolean = True
    except requests.exceptions.RequestException as e:
        print ("RequestExc: ")
        print(e)
        boolean = False
    except Exception as e:
        print ("Exc: ")
        print(e)
        boolean = False
    
    if (boolean):
        url2 = rheader['Operation-Location']
        print ("In getTextFromIMG 2")
        time.sleep(2)
        try:
            i = 0
            request2 = requests.get(url2, headers=headers)
            while(request2.json()['status'] == 'Running'):
                
                print ("Loop "+str(i))
                i += 1
                try:
                    request2 = requests.get(url2, headers=headers)
                except requests.exceptions.RequestException as e:
                    print (e)
                time.sleep(2)
            text = request2.json()['recognitionResult']['lines'][0]['text']
            print (text)
        except requests.exceptions.RequestException as e:
            print (e)

getTextFromIMG()
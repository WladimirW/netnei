# DevCamp 2019 diconium
## Step 1: Send Get Request to the Azure Cloud and get the response text.
*If something in this step went wrong for you or if you're unsure where to put something, devCampStep1.py contains the code from the completed step 1 tutorial*  

After creating the script in Step 0 and sending the first Request to the cloud, you can now start getting the actual response.  
Azure's *recognizeText* works in 2 parts. Firstly you need to post the image to the cloud as done in Step 0.  
From this request you get an URL. That was the printed part of the script in Step 0.  
This URL is the location, where Azure stores the result of the text recognition after computing is done.  
This result is easily accessible by sending a GET request with your key in the request header.  

To do this, you can implement a new function **getPlate()**:
Simply add the code below into your script between 

    headersURL = { 
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': key }
        
    # INSERT CODE BELOW HERE    
        
    def postToCloud(mode, file):
    
```python
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
```

The new function will not be called as of right now, so let's make a few quick adjustments to change that.

In the postToCloud() function, change 
```python
print (request.headers['Operation-Location'])
```
to
```python
reqHeader = request.headers
        url = reqHeader['Operation-Location']
        getPlate(url)
```
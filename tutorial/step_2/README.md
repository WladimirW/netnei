# DevCamp 2019 diconium

## Step 2: Send recognized plates to service, get the final result and add console parameters

*If something in this step went wrong for you or if you're unsure where to put something, devCampStep2.py contains the code from the completed step 2 tutorial.*
 *'#-------' lines mark inserted parts*

*After receiving the recognized Text from a picture and filtering it for number plates, we will now send these plates to a service to check, if they are allowed in Stuttgart.*  
Now that you've worked with requests in Python, this step will be very easy to do.
We implement a new function, that allows us to **send a simple GET request to our service**. We have to append the URL with the number plate text, because that is how our service can use the plate.  

We call this new function **getEntryPermitFromImage()**. First we **add the basic request**:  
Start by assigning the new variable **permitURL**, that contains the URL of the service access point.  

Put the following code somewhere **below the imports** and **above the functions**:

```python
# Access Point to check, if number plate is allowed
permitURL = 'https://kbamock.rg02.diconium.cloud/plate/'
```

After this is done, we can start with the actual function (**add above** your **getGermanPlatesFromResult()** function):  

```python
def getEntryPermitFromPlate(numberPlate):
    '''checks if number plate is allowed in Stuttgart by contacting a service.

    Argument:
    numberPlate -- number plate of a car as String given by getPlate()
    '''
    fullPermitURL = permitURL + numberPlate
    # the requests module automatically encodes URLs before sending the request.
    # e.g. 'https://www.google.com/this is a test' -> 'https://www.google.com/this%20is%20a%20test'
    request3 = requests.get(fullPermitURL)
    loggerMain.debug ('Response: ' + request3.text)
```

First we build the URL we need to access the service as store it in fullPermitURL.
Then we make a simple GET request to our mock service and log the response body.  
Now we need to call this function. Add the **two lines marked** to the **bottom of the script as shown** .  
 **Don't copy the whole following block**:

```python
result = recognizeTextFromImage(mode, 'bild1.jpg')
if result:
    plates = getGermanPlatesFromResult(result)
    for plate in plates:                        #<-------- ADD THIS
        getEntryPermitFromPlate(plate)          #<-------- AND THIS
```

So after we get the result of the recognition service, we call the new getEntryPermitFromPlate function for every recognized plate.  
We can now **run the script** to see whats going on:  

    cd c:\Users\user\remaining\path\To\Your\Repository\tutorial\

    python devCamp_numberplate.py

When everything worked, the output should look something like this:  

```
DEBUG urllib3.connectionpool:    Starting new HTTPS connection (1): westeurope.api.cognitive.microsoft.com
DEBUG urllib3.connectionpool:    https://westeurope.api.cognitive.microsoft.com:443 "POST /vision/v2.0/recognizeText?mode=Printed HTTP/1.1" 202 0
DEBUG __main__:  https://westeurope.api.cognitive.microsoft.com/vision/v2.0/textOperations/34071a3a-80bb-48f5-a259-4149539215a4
DEBUG urllib3.connectionpool:    Starting new HTTPS connection (1): westeurope.api.cognitive.microsoft.com
DEBUG urllib3.connectionpool:    https://westeurope.api.cognitive.microsoft.com:443 "GET /vision/v2.0/textOperations/34071a3a-80bb-48f5-a259-4149539215a4 HTTP/1.1" 200 339
DEBUG __main__:  STATUSTEXT: {"status":"Succeeded","recognitionResult":{"lines":[{"boundingBox":[146,305,273,337,265,367,138,335],"text":"K QX 1025","words":[{"boundingBox":[146,306,166,311,158,341,139,336],"text":"K"},{"boundingBox":[178,314,211,322,204,352,170,344],"text":"QX","confidence":"Low"},{"boundingBox":[211,322,273,336,266,368,204,352],"text":"1025"}]}]}}
INFO __main__:   Plate: K QX 1025
DEBUG __main__:  returned plates: ['K QX 1025']
DEBUG urllib3.connectionpool:    Starting new HTTPS connection (1): kbamock.rg02.diconium.cloud
DEBUG urllib3.connectionpool:    https://kbamock.rg02.diconium.cloud:443 "GET /plate/K%20QX%201025 HTTP/1.1" 200 131
DEBUG __main__:  Response: {"plate":"K QX 1025","Brand":"Porsche","Modell":"Cayenne","Diesel":false,"Euronorm":4,"StuttgartEntry":true,"DatabaseLookup":false}
```

As you can see in the last three lines in the output, we sent a GET request to our service and its response contains several attributes of the car, thats connected to the license plate.  
The interesting value for us is the value for "StuttgartEntry", as that's the purpose of our script.  
To access the "StuttgartEntry" key we add a little more code **to the end of getEntryPermitFromPlate**:  

```python
    brand = request3.json()['Brand']
    model = request3.json()['Modell']
    isAllowed = request3.json()['StuttgartEntry']
    if isAllowed:
        loggerMain.info (brand + ' ' + model + ' with number plate ' + numberPlate + ' is allowed to enter Stuttgart.')
    else:
        loggerMain.info (brand + ' ' + model + ' with number plate ' + numberPlate + ' is forbidden to enter Stuttgart.')
    return isAllowed
```

This code stores the **brand**, **model** and **StuttgartEntry** values in variables and logs them as easily human-readable text to the console.  
The main objective of this script is hereby achieved. We can get a number plate from an image of a car and can get additional information by contacting another service.  
You can call the script again to see a nicer output and to check, if everything worked with indents etc.  
*Note that we also return the isAllowed variable. We don't actually need the value in our script, but it's good practice, if we want to enhance the script at a later point in time.  

**Back to Step 1**:  
[Step 1](https://github.com/volkerhielscher/netnei/blob/master/tutorial/step_1/)  

**Continue with Step 3**:  
[Step 3](https://github.com/volkerhielscher/netnei/blob/master/tutorial/step_3/)

*If something in this step went wrong for you or if you're unsure where to put something, devCampStep2.py contains the code from the completed step 2 tutorial.*
 *'#-------' lines mark inserted parts*
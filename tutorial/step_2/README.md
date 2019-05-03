# DevCamp 2019 diconium

## Step 2: Send recognized plates to service, get the final result and add console parameters

*If something in this step went wrong for you or if you're unsure where to put something, devCampStep2.py contains the code from the completed step 2 tutorial.*

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

First we build the URL we need to access the service and store it in fullPermitURL.
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

**make sure the indents are correct**  
After we get the result of the recognition service, we call the new getEntryPermitFromPlate function for every recognized plate.  
We can now **run the script** to see whats going on:  

    cd c:\Users\user\remaining\path\To\Your\Repository\tutorial\

    python devCamp_numberplate.py

When everything worked, the output should look something like this:  

```
__main__(DEBUG): https://westeurope.api.cognitive.microsoft.com/vision/v2.0/textOperations/fdbdd253-9a3b-45ee-a38e-ccebf3b6fe0d
__main__(DEBUG): STATUSTEXT: {"status":"Succeeded","recognitionResult":{"lines":[{"boundingBox":[274,226,363,228,363,245,273,243],"text":"S.OY 5024","words":[{"boundingBox":[279,227,319,228,319,244,279,243],"text":"S.OY","confidence":"Low"},{"boundingBox":[322,228,360,229,360,245,322,244],"text":"5024"}]}]}}
__main__(DEBUG): Group1:S Group2:OY Group3:5024
__main__(DEBUG): Group1:S Group2:OY Group3:5024
__main__(INFO): Plate: S OY 5024
__main__(DEBUG): returned plates: ['S OY 5024']
__main__(DEBUG): Response: {"plate":"S OY 5024","Brand":"Porsche","Modell":"Cayenne","Diesel":false,"Euronorm":4,"StuttgartEntry":true,"DatabaseLookup":false}
```

As you can see in the last line in the output, we get a response containing several attributes of the car, thats connected to the license plate.  
*Remember that our service is only a mock service and therefor gives random values back. Posting the same plate twice can get you different results*  
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
**The main objective of this script is hereby achieved**. We can get a number plate from an image of a car and can get additional information by contacting another service.  
You can call the script again to see a nicer output and to check, if everything worked with indents etc.  

The log should look like this:  

```
__main__(DEBUG): https://westeurope.api.cognitive.microsoft.com/vision/v2.0/textOperations/77258a1d-390c-456d-af75-3ad554564476
__main__(DEBUG): STATUSTEXT: {"status":"Succeeded","recognitionResult":{"lines":[{"boundingBox":[274,226,363,228,363,245,273,243],"text":"S.OY 5024","words":[{"boundingBox":[279,227,319,228,319,244,279,243],"text":"S.OY","confidence":"Low"},{"boundingBox":[322,228,360,229,360,245,322,244],"text":"5024"}]}]}}
__main__(DEBUG): Group1:S Group2:OY Group3:5024
__main__(DEBUG): Group1:S Group2:OY Group3:5024
__main__(INFO): Plate: S OY 5024
__main__(DEBUG): returned plates: ['S OY 5024']
__main__(DEBUG): Response: {"plate":"S OY 5024","Brand":"Audi","Modell":"Q5","Diesel":true,"Euronorm":4,"StuttgartEntry":false,"DatabaseLookup":false}
__main__(INFO): Audi Q5 with number plate S OY 5024 is forbidden to enter Stuttgart.
```

**Back to Step 1**:  
[Step 1](https://github.com/volkerhielscher/netnei/blob/master/tutorial/step_1/)  

**Continue with Step 3**:  
[Step 3](https://github.com/volkerhielscher/netnei/blob/master/tutorial/step_3/)

*If something in this step went wrong for you or if you're unsure where to put something, devCampStep2.py contains the code from the completed step 2 tutorial.*
# DevCamp 2019 diconium

## Step 2: Send recognized plates to service, get the final result and add console parameters

*If something in this step went wrong for you or if you're unsure where to put something, devCampStep2.py contains the code from the completed step 2 tutorial.*
 *'#-------' lines mark inserted parts*

*After receiving the recognized Text from a picture and filtering it for number plates, we will now send these plates to a service to check, if they are allowed in Stuttgart.*  
Now that you've worked with requests in Python, this step will be very easy to do.
We implement a new function, that allows us to **send a simple GET request to our service**. We have to append the URL with the number plate text, because that is how our service can use the plate.  

We call this new function **getEntryPermit()**. First we **add the basic request**:  
Start by assigning the new variable **permitURL**, that contains the URL of the service access point:  
Put the following code somewhere **below the imports** and **above the functions**:

```python
# Access Point to check, if number plate is allowed
permitURL = 'https://kbamock.rg02.diconium.cloud/plate/'
```

After this is done, we can start with the actual function (add the function above your getPlate() function):  

```python
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

```

Now we need to call this function. Add **getEntryPermit(text)** to the **getPlate()** function **don't copy the whole following block**:

```python
            if (match):
                print('')
                print("number plate: "+ text)
                print('')
                getEntryPermit(text)  #<------------ add this line
```

We put it at this position, so we call the service for every valid recognized number plate.  
We can now run the script to see whats going on:  

    cd c:\Users\user\remaining\path\To\Your\Repository\tutorial\

    python devCamp_numberplate.py

When everything worked, the output should look something like this:  

```
Accessing https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/textOperations/38c09c57-92c5-4222-9866-d2feec95ec68:
STATUSTEXT:
{"status":"Succeeded","recognitionResult":{"lines":[{"boundingBox":[146,305,273,337,265,367,138,335],"text":"K QX 1025","words":[{"boundingBox":[146,306,166,311,158,341,139,336],"text":"K"},{"boundingBox":[178,314,211,322,204,352,170,344],"text":"QX","confidence":"Low"},{"boundingBox":[211,322,273,336,266,368,204,352],"text":"1025"}]}]}}

Plate: K QX 1025

Send GET request to https://kbamock.rg02.diconium.cloud/plate/K%20QX%201025
{"plate":"K QX 1025","Brand":"Mercedes Benz","Modell":"C-200","Diesel":false,"Euronorm":5,"StuttgartEntry":true,"DatabaseLookup":false}
```

As you can see in the last two lines in the output, we sent a GET request to our service and its response were several attributes of the car, thats connected to the license plate.  
The interesting value for us is the value for "StuttgartEntry", as that's the purpose of our script.  
To access the "StuttgartEntry" key we add a little more code **to the end of our getEntryPermit function**:

```python
    brand = request3.json()['Brand']
    model = request3.json()['Modell']
    isAllowed = request3.json()['StuttgartEntry']
    if isAllowed:
        print (brand + ' ' + model + ' with number plate ' + numberPlate + ' is allowed to enter Stuttgart.')
    else:
        print (brand + ' ' + model + ' with number plate ' + numberPlate + ' is forbidden to enter Stuttgart.')
```

This code stores the **brand**, **model** and **StuttgartEntry** values in variables and outputs them in human-readable text in the console.  
The main objective of this script is hereby achieved. We can get a number plate from an image of a car and can get additional information by contacting another service.  
You can call the script again to see a nicer output.

**Continue with Step 3**:  
[Step 3](https://github.com/volkerhielscher/netnei/blob/master/tutorial/step_3/)

*If something in this step went wrong for you or if you're unsure where to put something, devCampStep2.py contains the code from the completed step 2 tutorial.*
 *'#-------' lines mark inserted parts*
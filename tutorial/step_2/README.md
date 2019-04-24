# DevCamp 2019 diconium

## Step 2: Send recognized plates to service, get the final result and add terminal parameters

*If something in this step went wrong for you or if you're unsure where to put something, devCampStep2.py contains the code from the completed step 2 tutorial.*
 *'#-------' lines mark inserted parts*

After receiving the recognized Text from a picture and filtering it for numberplates, we can now send these plates to a service to check, if they are allowed in Stuttgart.  
Now that you've worked with requests in Python, this step will be very easy to do.
We implement a new function, that allows us to send a simple GET request to the server of our service. We have to append the URL with the number plate text, because that is how our service can use the plate.  

We call this new function **getEntryPermit()**. First we add the basic request:
Start by assigning the new variable *permitURL*, that contains the URL of the service access point:
Put the following code somewhere below the imports and above the functions:

```python
# Access Point to check, if number plate is allowed
permitURL = 'https://kbamock.rg02.diconium.cloud/plate/'
```

After this is done, we can start with the actual function (add the function above your getPlate() function):  

```python
def getEntryPermit(numberPlate):
    fullPermitURL = permitURL + numberPlate
    # the requests module automatically encodes URLs before sending the request.
    # e.g. 'https://www.google.com/this is a test' -> 'https://www.google.com/this%20is%20a%20test'
    request3 = requests.get(fullPermitURL)
    print (fullPermitURL.url) # to see, if the encoding works
    print (request3.text) # to check, how the response by the service looks like

```

Now we need to call this function. Add *getEntryPermit(text)* to the getPlate() function:

```python
            if (match):
                print('')
                print("number plate: "+ text)
                print('')
                getEntryPermit(text)  #<--- add this line

```

We put it at this position, so we call the service for every valid recognized number plate.  


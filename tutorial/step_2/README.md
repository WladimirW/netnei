# DevCamp 2019 diconium

## Step 2: Send recognized plates to service, get the final result and add console parameters

*If something in this step went wrong for you or if you're unsure where to put something, devCampStep2.py contains the code from the completed step 2 tutorial.*
 *'#-------' lines mark inserted parts*

After receiving the recognized Text from a picture and filtering it for numberplates, we will now send these plates to a service to check, if they are allowed in Stuttgart.  
Now that you've worked with requests in Python, this step will be very easy to do.
We implement a new function, that allows us to send a simple GET request our service. We have to append the URL with the number plate text, because that is how our service can use the plate.  

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
    print (request3.url) # to see, if the encoding works
    print (request3.text) # to check, how the response by the service looks like

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

    python c:\Users\user\remaining\path\To\Your\Repository\tutorial\devCamp_numberplate.py

When everything worked, the output should look something like this:  

```
Accessing htt<i></i>ps://westcentralus.api.cognitive.microsoft.com/vision/v2.0/textOperations/3bf43fcc-23b6-4f18-9677-dbceca4ff0fb:
STATUSTEXT:
{"status":"Succeeded","recognitionResult":{"lines":[{"boundingBox":[146,305,273,337,265,367,138,335],"text":"K QX 1025","words":[{"boundingBox":[146,306,166,311,158,341,139,336],"text":"K"},{"boundingBox":[178,314,211,322,204,352,170,344],"text":"QX","confidence":"Low"},{"boundingBox":[211,322,273,336,266,368,204,352],"text":"1025"}]}]}}

number plate: K QX 1025

Send GET request to htt<i></i>ps://kbamock.rg02.diconium.cloud/plate/K%20QX%201025
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
The main objective of this script is achieved. We can get a number plate from an image of a car and can get additional information by contacting another service.  
Obviously we cant always use only one predefined image that is uploaded to the github repository, so let's make our script more flexible.  
Let's add the ability to access local images. In a previous script we added the **postToCloud** function. Part of it was the following code:  

```python
        if mode == 'local':
            # Done in a later step.
            print ()
```

It's time to finally make it useful. To do this, we **replace** the **previous** code with the code below:  

```python
        if mode == 'local':
            # open image as binary and post it to the Azure Cloud
            data = open( localImagesPath + file, 'rb').read()
            print("File opened")
            request = requests.post(azureURL, headers=headersLocal, data=data, timeout=10)
```

We simply open the local file as read binary (therefor the *'rb'*) and send a POST request like before to our endpoint. The only
difference is that we use the keyword data, as the data we send isn't in the json format anymore. also we need to use a different header
so change complete the change from json to binary.
Right now we don't have the headersLocal variable, so let's add it **at the top below the headersURL variable**:  

```python
headersLocal = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': key }
```

'application/octet-stream' is the content type we use with the binary-read file. Other than that it's the same as the calls with URL.  
The remaining work, we have to do, is to change the script, so it can read arguments given via console and use them.  
For the script to work with console arguments, we need to import the sys module. Also while we're at it, we will import the os module for later use. We can do this by adding the following code **to our other imports**:  

```python
import sys, os
```

Now that we can access system arguments, we can finally build our last function. First **delete** the following function call, as we don't need it anymore (It's at the bottom):  

```python
postToCloud(mode, 'bild1.jpg')
```

After removing the call, we can now add the function main(mode) **at the bottom** of the script:  

```python
def main(mode):
    '''the main function checks, how the script was called and calls postIntoCloud()
    with the correct arguments. This function is the access point of the script.

    Parameters:
    mode -- specifies in which mode to operate ('local', 'URL')
    file -- file in directory ('*.jpg', '*png', '*.jpeg', '*.bmp')
    sys.argv -- contains arguments from command line. sys.argv[0] is the name of the script.
    '''
    # set mode
    if(len(sys.argv) > 1 and (sys.argv[1] == 'local' or sys.argv[1] == 'URL')):
        mode = sys.argv[1]
```

We want to give our mode variable to it so it can use the default mode if needed. In this first part, we test, if there were
extra arguments given to the script. sys.argv contains all arguments given to the script in an array. in position 0 of this array the name of the script is stored by default.
That means, that if the array contains more than 1 entry, we gave it extra arguments via console.
If that's the case, we also want to know, if the first given argument is either 'local' or 'URL' as these are the supported modes. If that's the case, we want to store its value in a mode variable for later use.  
The second test we do, is a test for either less than 2 arguments (which means no extra arguments given) or for only one extra argument, that's either 'local' or 'URL'.
In this case we want to loop through all the files in the local directory. For this to work we add the following code:  

```python
    # how was the script called? If only one argument was given, is it mode or imagename?
    if len(sys.argv) < 2 or (len(sys.argv) == 2 and (sys.argv[1] == 'local' or sys.argv[1] == 'URL')):
        # if no image was specified, loop over every image in the project folder (localImagesPath)
        for file in directory:
            if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg') or file.endswith('.bmp'):
                print (file + ' :------------------------------------------------------------------')
                postToCloud(mode, file)
```

After the if clause follows the loop. It loops through all files in the directory and posts all of them to Azure and so on. Obviously we need to know which directory to use.
For this we **add** two new variables **below our imports** called directory and localImagesPath:

```python
localImagesPath = '../complete/images/'
# contains every file in the specified path
directory = os.listdir(localImagesPath)
```

localImagesPath is the relative path to the images folder. As the images are stored in devcamp/complete/images and this script is in devcamp/tutorial, we have to go back one folder and then go to complete/images. os.listdir() lists the names of every file in the directory. In our case we store these names in the directory array.  
Now we can go back to our main method and continue working on it. We want to be able to only give an image name and using the default mode to post this image. We can do this by adding the following code at the end:  

```python
    # if only image was specified, but not mode, post specified image with default mode       
    elif (len(sys.argv) == 2 and sys.argv[1] != 'local' and sys.argv[1] != 'URL'):
        if sys.argv[1].endswith('.jpg') or sys.argv[1].endswith('.png') or sys.argv[1].endswith('.jpeg') or sys.argv[1].endswith('.bmp'):
            postToCloud(mode, sys.argv[1])
    # else corresponds to script call with 2 arguments, where mode is the first and image is the second
    else:
        postToCloud(mode, sys.argv[2])
    print ("Mode: " + mode)
```

******************CONTINUE HERE

This whole job of our main function is to see how the script was called. This first part tests, if there is an additional argument. If there is an additional argument, it tests, if the argument is trying to change the access mode

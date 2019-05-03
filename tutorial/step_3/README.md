# DevCamp 2019 diconium

## Step 3: Add console parameters for more convenient use

*If something in this step went wrong for you or if you're unsure where to put something, devCampStep3.py contains the code from the completed step 3 tutorial.*
**Note that this script won't work when executed, because localImages is relative to the tutorial directory. Copy the code into your normal tutorial script, if problems occured**

*After finishing the main functionality of the script in step 2, we can now make the usage more convenient.*
Obviously we cant always use only one predefined image that is uploaded to the github repository, so let's make our script more flexible.  
Let's add the ability to access local images. In a previous script we added the **recognizeTextFromImage** function. Part of it was the following code:  

```python
        if mode == 'local':
            # complete this in a later step
            print () # only for now
```

It's time to finally make it functional. To do this, we **replace** the **previous** code with the code below:  
**ignore shown syntax errors for this action** *They get resolved in the next 2 blocks of code*.  

```python
        if mode == 'local':
            # open image as binary and post it to the Azure Cloud
            data = open( localImagesPath + file, 'rb').read()
            loggerMain.debug("File opened")
            request = requests.post(azureURL, headers=headersLocal, data=data, timeout=10)
```

We simply open the local file as read binary (therefor the *'rb'*) and send a POST request to our endpoint like before. The only
difference is that we use the keyword data, because the data we send isn't in json format anymore. also we need to use a different header
to complete the change from json to binary.  

Right now we don't have the headersLocal variable, so let's add it **at the top of the script below the headersURL variable**:  

```python
# Headers for call with binary data
headersLocal = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': key }
```

'application/octet-stream' is the content type we use with the binary-read file. Other than that it's the same as the calls with URL.  
The remaining work, we have to do, is to change the script, so that it can read arguments given via console and use them.  
We also don't have the localImagesPath variable, yet, so let's add it as well. You can put it **below the previously added code** (headersLocal variable):
*We also add the directory variable as we'll need it later*  

```python
localImagesPath = '../complete/images/'
# contains every file in the specified path
directory = os.listdir(localImagesPath)
```

localImagesPath simply stores the relative path to our images folder as the name suggests. 'directory' is an array, that stores the name of every file in the specified path.
For the directory variable we need the os module.  
To access the arguments from the command line, we'll also need the sys module, so let's import both modules by adding the following code **below our other imports**:  

```python
import sys, os
```

Now that we can access system arguments, we want to create a little support function first.  
**Add** it **below the recognizeTextFromImage function** and **above** the **'# create logger'-line**:  

```python
def getEntryPermitFromImage(mode, image):
    '''This function calls the other functions to post an image to the Azure cloud
    and then analyze the resulting text via re for plates. In the end it gets the
    information for a plate from the mock service. This function is only needed to 
    improve modularity.
    '''
    result = recognizeTextFromImage(mode, image)
    if result:
        plates = getGermanPlatesFromResult(result)
        for plate in plates:
            getEntryPermitFromPlate(plate)
```

As you can see, it does pretty much, what we did with the last 5 lines of our script. The only **difference** is that we don't give 'bild1.jpg' to the function,
but rather use a variable for it, so we can change the image name.  
Now we can **delete** the function calls we used earlier.  
**Delete** the following code from the **bottom of the script**:  

```python
result = recognizeTextFromImage(mode, 'bild1.jpg')
if result:
    plates = getGermanPlatesFromResult(result)
    for plate in plates:
        getEntryPermitFromPlate(plate)
```

We also want to add two support functions for later use.  
**Add** the following code **below the global variables** and **above getEntryPermitFromPlate**:  

```python
def isMode(argument):
    '''support function that checks wether an argument is a supported mode.
    '''
    if (argument == 'local' or argument == 'URL'):
        return True
    else:
        return False

def isImage(file):
    '''support function that checks, if a file name is actually ending with an image extension.
    '''
    if file.lower().endswith('.jpg') or file.lower().endswith('.png') or file.lower().endswith('.jpeg') or file.lower().endswith('.bmp'):
        return True
    else:
        return False
```

These 2 newly added functions will be used to determine the type of argument given. isMode checks, if the argument is one of our 2 supported modes ('local', 'URL') and if so returns True.
*Note that the check is case sensitive*  
isImage checks for a file with supported suffix (.jpg, .jpeg, .bmp, .png) and if so returns True.  
With the help of these newly added helper functions we can now finally implement our main function:  
We do so by **adding** the following function **below** the new **getEntryPermitFromImage** function and **above** the **'# create logger'-line**:  

```python
def main(mode):
    '''the main function checks, how the script was called and calls recognizeTextFromImage()
    with the correct arguments. This function is the access point of the script.

    Parameters:
    mode -- specifies in which mode to operate ('local', 'URL')
    file -- file in directory ('*.jpg', '*png', '*.jpeg', '*.bmp')
    sys.argv -- contains arguments from command line. sys.argv[0] is the name of the script.
    '''
    # set mode
    if(len(sys.argv) > 1 and isMode(sys.argv[1])):
        mode = sys.argv[1]
```

First we want to set the mode, if it's given as system argument.  
Continue by **adding** the following code **below** the previous code:  

```python
    # how was the script called? If only one argument was given, is it mode or imagename?
    if len(sys.argv) < 2 or (len(sys.argv) == 2 and isMode(sys.argv[1])):
        # if no image was specified, loop over every image in the project folder (localImagesPath)
        for file in directory:
            loggerMain.debug('------------------------------------------------------------')
            if isImage(file):
                getEntryPermitFromImage(mode, file)
            else:
                loggerMain.warn ("The specified file is no supported image. Please use .jpg, .png, .jpeg or .bmp files")
```

This part loops through every file in the directory and calls the getEntryPermitFromImage function for it.
It only does so, if there are no system arguments ('if len(sys.argv) < 2') or if there's one extra argument, that's also a mode.  
Continue by **adding** the following code **below the previous code**:  

```python
    # if only image was specified, but not mode, post specified image with default mode
    elif (len(sys.argv) == 2 and isImage(sys.argv[1])):
        getEntryPermitFromImage(mode, sys.argv[1])
    # if there are atleast 2 extra arguments, set first as mode and second as image
    elif len(sys.argv) > 2 and isMode(sys.argv[1]) and isImage(sys.argv[2]):
        getEntryPermitFromImage(sys.argv[1], sys.argv[2])
    else:
        loggerMain.error('The arguments were not given correctly.')
        loggerMain.error('Usage: ' + sys.argv[0] + ' [mode] [imageName] , where mode is [local,URL] and imageName a name from imagePath')
```

As the in-code comments suggest we check for **one extra** argument that's also **an image** first. If so we call getEntryPermitFromImage with the default mode and
the **first extra system argument as image**. The next check is for **more than one extra argument** and also if the **first argument** is a **mode** and the **second** is an **image**.  
These are our supported ways of giving arguments to the script, so if anything else happens, the script logs an error.  
To finish our endeavors we now simply add the function call to make our script do anything.  
**Add** the following code **at the end of your script** (*as always make sure the indent level is correct*):  

```python
# start
main(mode)
```

That's it. The script is now fully functional. Call it like before or change it up a little bit like in the following example:  

```
    cd c:\Users\user\remaining\path\To\Your\Repository\tutorial\

    python devCamp_numberplate.py local IMG_0702.JPG
```

The result looks like this:  

```
__main__(DEBUG): File opened
__main__(DEBUG): https://westeurope.api.cognitive.microsoft.com/vision/v2.0/textOperations/4818cc0d-fcbd-497b-aa25-33b3d85b5c41
__main__(DEBUG): STATUSTEXT: {"status":"Succeeded","recognitionResult":{"lines":[{"boundingBox":[48,27,80,32,77,55,44,50],"text":"BAR","words":[{"boundingBox":[45,25,78,30,74,54,41,49],"text":"BAR","confidence":"Low"}]},{"boundingBox":[423,203,431,202,433,214,425,215],"text":"D","words":[{"boundingBox":[423,202,431,201,432,213,424,214],"text":"D"}]},{"boundingBox":[438,189,541,178,544,203,441,214],"text":"SoKY 249","words":[{"boundingBox":[440,189,498,184,500,208,443,215],"text":"SoKY","confidence":"Low"},{"boundingBox":[500,184,542,179,544,204,502,208],"text":"249"}]}]}}
__main__(DEBUG): Not a plate: BAR
__main__(DEBUG): Not a plate: D
__main__(DEBUG): Group1:S Group2:KY Group3:249
__main__(DEBUG): Group1:S Group2:KY Group3:249
__main__(INFO): Plate: S KY 249
__main__(DEBUG): returned plates: ['S KY 249']
__main__(DEBUG): Response: {"plate":"S KY 249","Brand":"Audi","Modell":"Q5","Diesel":true,"Euronorm":4,"StuttgartEntry":false,"DatabaseLookup":false}
__main__(INFO): Audi Q5 with number plate S KY 249 is forbidden to enter Stuttgart.
```

The images to test have to be in the *repository/complete/images* folder.

**Back to Step 2**:  
[Step 2](https://github.com/volkerhielscher/netnei/blob/master/tutorial/step_2/)

*If something in this step went wrong for you or if you're unsure where to put something, devCampStep3.py contains the code from the completed step 3 tutorial.*
**Note that this script won't work when executed, because localImages is relative to the tutorial directory. Copy the code into your normal tutorial script, if problems occured**
# DevCamp 2019 diconium

## Step 3: Add console parameters for more convenient use

*If something in this step went wrong for you or if you're unsure where to put something, devCampStep3.py contains the code from the completed step 3 tutorial.*
 *'#-------' lines mark inserted parts*

****HERE
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

We simply open the local file as read binary (therefor the *'rb'*) and send a POST request to our endpoint like before. The only
difference is that we use the keyword data, because the data we send isn't in json format anymore. also we need to use a different header
to complete the change from json to binary.
Right now we don't have the headersLocal variable, so let's add it **at the top below the headersURL variable**:  

```python
headersLocal = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': key }
```

'application/octet-stream' is the content type we use with the binary-read file. Other than that it's the same as the calls with URL.  
The remaining work, we have to do, is to change the script, so it can read arguments given via console and use them.  
We also don't have the localImagesPath variable, so let's add it as well. You can put it **below the previously added code**:
*We also add the directory variable as we'll need it later*  

```python
localImagesPath = '../complete/images/'
# contains every file in the specified path
directory = os.listdir(localImagesPath)
```

localImagesPath simply stores the relative path to our images folder as the name suggests. 'directory' is an array, that stores the name of every file in the specified path.
For the directory variable we need the os module. To access the arguments from the command line, we'll need the sys module, so let's import both modules by adding the following code
**below our other imports**:  

```python
import sys, os
```

Now that we can access system arguments, we can finally build our last function. First **delete** the following function call, as we don't need it anymore (It's at the bottom of the script):  

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
    if(len(sys.argv) > 1 and isMode(sys.argv[1])):
        mode = sys.argv[1]
```

In this first part, we check wether there were extra arguments given to the script. sys.argv contains all arguments given to the script in an array. In position 0 of this array the name of the script is stored by default. That means, that if the array contains more than 1 entry, we gave it extra arguments via console.
If so, we also want to know wether the first given argument is a supported mode. If so, we want to store its value in a mode variable for later use.
Obviously we don't yet have a **isMode()** function, therefor we have to create one. we also create a **isImage()** function while we're at it for later use. Add the below code **directly above the getEntryPermit()** function:  

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
    if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg') or file.endswith('.bmp'):
        return True
    else:
        return False
```

These functions literally only check wether the given Strings are in the correct format.  
After the support functions are added, let's get back to the **main()** function.  
The second if clause we use in **main()** checks for either less than 2 arguments (which means no extra arguments given) or for only one extra argument, that's either 'local' or 'URL'.
In this case we want to loop through all the files in the local directory. For this to work we **add** the following code **at the end of the main function**:  

```python
    # how was the script called? If only one argument was given, is it mode or imagename?
    if len(sys.argv) < 2 or (len(sys.argv) == 2 and isMode(sys.argv[1])):
        # if no image was specified, loop over every image in the project folder (localImagesPath)
        for file in directory:
            if isImage(file):
                print (file + ' :------------------------------------------------------------------')
                postToCloud(mode, file)
            else:
                print (file + ' :------------------------------------------------------------------')
                print ("The specified file is no supported image. Please use .jpg, .png, .jpeg or .bmp files"))
```

After the if clause follows the loop. It loops through all files in the directory and posts all of them to Azure.  
Now we can go back to our main method and continue working on it. We want to be able to only give an image name and using the default mode to post this image. We can do this by **adding**
the following code **at the end**:  

```python
    # if only image was specified, but not mode, post specified image with default mode
    elif (len(sys.argv) == 2 and isImage(sys.argv[1])):
            postToCloud(mode, sys.argv[1])
```

the elif clause checks wether we have an extra argument, that's not changing the mode and also wether it's really an image, If so, we post this one image to Azure in the default mode.  
This clause is followed by the last needed piece of code to get everything working. **Add** it **below** the previous code:  

```python
    # if there are atleast 2 extra arguments, set first as mode and second as image
    elif len(sys.argv) > 2 and isMode(sys.argv[1]) and isImage(sys.argv[2]):
        postToCloud(sys.argv[1], sys.argv[2])
    else:
        print ('Error: The arguments were not given correctly. Please use either mode or image as single argument or put mode as first and image as second argument.')
    print ("Mode: " + mode)
```

This last check we do is for more than two arguments (more than one extra argument) and we also check, if the first extra argument is a supported mode and the second argument is in a
supported image format. In this case, the specified image will be accessed in the specified mode and posted to Azure.  
After the if clauses are done, we want to tell via console, if a script call went wrong, so we added the else block, that prints, if the call was not successful and how to make a
successful call.  
The last line of code is the new entry point of the script. Previously we always called the postToCloud function. We deleted that call and we'll now want to call our new main function.
**Add** the following code **at the end of your script** (*as always make sure the indent level is correct):  

```python
main(mode)
```

*If something in this step went wrong for you or if you're unsure where to put something, devCampStep3.py contains the code from the completed step 3 tutorial.*
 *'#-------' lines mark inserted parts*
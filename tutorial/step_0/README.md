# DevCamp 2019 diconium

## Step 0: Setup Azure, setup Python and run a small Python script

### 1. Create Microsoft Account and start "Computer Vision" Trial

Go to [Azure](https://azure.microsoft.com/en-us/try/cognitive-services/?api=computer-vision)  
Press **Get API Key** for **"Computer Vision"** (make sure **not** to accidentally get your key for "Face").  
Start your *7-day trial* and follow the steps to login.
After your login you will see the following screen:  

![image1](https://raw.githubusercontent.com/volkerhielscher/netnei/master/tutorial/step_0/TutorialImages/KeysTrial.jpg)  

The endpoint with '/v2.0' and atleast one of the keys will be used later on.
If you accidentally closed your browser, you can always find your keys [here](https://azure.microsoft.com/en-us/try/cognitive-services/)  

### 2. Get Python and pip

Go to [Python for Windows](https://www.python.org/downloads/windows/) (use the executable installer, if your're unsure)  
[Python for MAC](https://www.python.org/downloads/mac-osx/) (use the 64-bit/32-bit installer, if you're unsure)  
[Python for Linux](https://www.python.org/downloads/source/)  
Download the latest Python version 3.\*.\* .  

**ATTENTION** In the Installer for Windows, there is a check box to **add Python to PATH** as seen here:  
![image2](https://raw.githubusercontent.com/volkerhielscher/netnei/master/tutorial/step_0/TutorialImages/python.jpg)  
**Check this box to avoid trouble later on**  

Install Python via the downloaded executable and install the requests package via writing

    python -m pip install requests  

into the terminal (*Win-R*, write **cmd** and press *Return*)  

*If 'python' is not recognized by your command window, you can add python to your path as described [here](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/) or [here (german)](https://bodo-schoenfeld.de/umgebungsvariablen-in-windows-10-bearbeiten/)*  
*Also you can specify the whole path to your python.exe file instead of just writing python:*  
*The above code is equal to the following if 'python' is not recognized as a Path variable:*

    C:\Users\yourUsername\AppData\Local\Programs\Python\yourPythonVersionFolder\python.exe -m pip install requests

### 3. Create a script

There is a file named **'devCamp_numberplate.py'** in the tutorial folder of the cloned/downloaded repository. This is the script, you'll be working with **throughout this tutorial**.  
At first this script is completely empty. To give it some life, **add the following code**:  
**if you're not familiar with Python as a programming language, it's important to keep all the indents as they are part of the syntax**  

```python
import requests
import logging

mode = "URL" # default mode
azureEndpoint = 'https://westeurope.api.cognitive.microsoft.com/vision/v2.0' #FIXME replace with your endpoint
# Azure access point consists your endpoint + the specific service to use
azureURL = azureEndpoint + '/recognizeText?mode=Printed'
# key to Azure Cloud
key = 'XXXXXXXXXXXXXXXXXXXXXX' #FIXME change Xs to your personal Azure resource key.

imageBaseURL = 'https://raw.githubusercontent.com/volkerhielscher/netnei/master/complete/images/'

# Headers for URL call
headersURL = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': key }
```

The code simply imports the requests and logging modules, so that we can do make web requests to several servers and also use the log functions instead of only printing to console. It also adds a few variables for later use. Change the key variable and set it to one of your personal keys (you can find them [here](https://azure.microsoft.com/en-us/try/cognitive-services/)). Also make sure, AzureURL uses your Azure endpoint (**compare to the v2 endpoint**).  
Change it, if you need to.
The 'mode' variable refers to the mode in which to access the images. For now it stays in its default mode. Later we add the functionality to upload local images to the Azure Cloud.  
'imageBaseURL' stores the base URL to access our example images in the github repository. 'headersURL' stores the headers for the request.  
After importing this code, we'll need to actually enable logging in our script.  
**Add** the following code **below the previous code**.  

```python
# create logger
loggerMain = logging.getLogger(__name__)
# default log settings
logging.basicConfig(format='%(name)s(%(levelname)s): %(message)s',level=logging.ERROR)
# loglevel DEBUG
loggerMain.setLevel(logging.DEBUG)
```

This part is getting the logger object of the main script. It also sets the default logging level to **ERROR**, the logging level of the main logger to **DEBUG** and formats the log, so that it prints the name of the logger followed by the log level of the log entry. In the end it puts in the log message. We'll keep the main logger logging level at DEBUG in this tutorial.  
After you've imported the logging code into your script, it's time to actually begin defining the function.  
Add the following code **directly above the the previous code**:  

```python
def recognizeTextFromImage(mode, file):
    '''Post image to Azure cloud and calls getPlate() to get response text.

    Arguments:
    mode -- specifies in which mode the post request is done ('local', 'URL')
    file -- specifies which file to post (*.jpg, *.jpeg, *.bmp, *.png)

    Parameters:
    data -- file in binary, used for local access
    jsonData -- requestbody in json format ({"url": "imageURL"})
    request -- request object of post request. Used to access its headers (request.headers)
    '''
    try:
        if mode == 'local':
            # complete this in a later step
            print () # only for now
        elif mode == 'URL':
            # use images from the github remote repository
            jsonData = {"url": imageBaseURL + file}
            request = requests.post(azureURL, headers=headersURL, json=jsonData, timeout=10)
        else:
            loggerMain.error ('recognizeTextFromImage() was called with wrong mode')
            return
    except requests.exceptions.RequestException as e:
        loggerMain.critical ('Can\'t access Azure services')
        loggerMain.exception (e)
    except Exception as e:
        loggerMain.critical ('undefinded problem in recognizeTextFromImage')
        loggerMain.exception (e)
```

This function asks in which mode to work. This is done by accessing the 'mode' variable. As our 'mode' doesn't change yet the function will only operate in "URL" mode for now.  
The URL to our test image is stored in 'jsonData'. It uses the following syntax: {"url": URLOfImage}. This will be the whole body of our request and only contains the address of the image, that needs to be analyzed by the Azure Cloud. We also log several exceptions and an error, if they occur. As you can see the syntax for log entires is loggerMain.loglevel('message'). loggerMain is the name of our logger and loglevel is the level at which to log the message. debug is the least important level. debug log entries only show with default logging level = DEBUG. The logging levels with increasing importance are: **DEBUG, INFO, WARNING, ERROR, CRITICAL**  
Now that were done with the request, we need to do something with the response. In the next tutorial step, we will actively use the information, for now we will only log it to the console.
To do this we first add the following code **at the end of our function**:  

```python
    try:
        response = request.headers['Operation-Location']
        loggerMain.debug (response)
        return response
    except Exception as e:
        loggerMain.error ('Exception:')
        loggerMain.error (request.text)
        loggerMain.exception (e)

```

This will make the function print the 'Operation-Location' part of the response header into the console.  
Operation-Location is the key to the value, we need to access.  
The whole Azure recognizeText service works in two parts. The first part is the posting of the image as we've done above.
The second part is accessing the information we get from Azure. These information are stored at a specific URL. This URL is exactly the value of the 'Operation-Location' key we get as a response to our post request from above.  
So if everything worked up to this point, we log an URL into the console, when we call our function. To call the function, simply add the following code **at the end of your script**:  

```python
recognizeTextFromImage(mode, 'bild1.jpg')
```

The image we send to the cloud is the following:  
![image1](https://raw.githubusercontent.com/volkerhielscher/netnei/master/complete/images/bild1.jpg)  
**Save the script** and continue  

Open the terminal (*Win-R*, write **cmd** and press *Return* for Windows Users) and execute **each** of the following lines by pressing **return**:  

    cd c:\Users\user\remaining\path\To\Your\Repository\tutorial\

    python devCamp_numberplate.py

If everything worked as intended, you should now see something, that looks like  

```
__main__(DEBUG): https://westeurope.api.cognitive.microsoft.com/vision/v2.0/textOperations/3968e003-e492-470b-902d-2ae8270d6e23
```

The two lines at the top are log entries, that the requests module creates. The line below is our created log. You can see the source of the log after the capslocked log level.
Also there's obviously only log entries on debug level as we didn't do any others.  
Now that we received the URL to get the result from we can continue with actually getting the result.  
This result is easily accessible by **sending a GET request** with your key in the request header.  

To do this, we first import two new modules by **adding** the following code **below the already existing *import logging* line**:  

```python
import time, re
```

We need the time module to use a sleep timer and we need the re module to filter all the text in a picture for number plates.
re is the abbreviation for 'regular expressions'.  

New global variables aren't needed in this step, so we can go right to making a new function. **Add it above the recognizeTextFromImage function from the previous step**:  

```python
def getResult(url):
    '''get result of recognizeTextFromImage() request
    '''
    time.sleep(3) # give Azure time to compute

```

First we want to give Azure a little time to compute. Three seconds usually do the trick.  

**Add** the next part right **below the previous one** (**make sure to keep all the indents, as they are needed**):  

```python
    try:
        i = 0
        # get the response of the image recognition
        request2 = requests.get(url, headers=headersURL)
        loggerMain.debug ('STATUSTEXT: ' + request2.text)
```

Again we do a request, but this time we only **need information** and dont need to post anything, so we're going with a **GET request**.  
We use the same headers as before, because we still need the authorization with our key and the key is part of the header. We also **log the response body** into the console to see, what's happening.  

In this next part we want to check, if Azure is done computing.  
Simply **add** it **below the previous** code:  

```python
        # test, if Azure needs more computing time. Break the loop after 10 tries
        while((request2.json()['status'] == 'Running' or request2.json()['status'] == 'Not started') and i <= 9):
            time.sleep(2)
            loggerMain.debug ('STATUSTEXT in loop: ' + request2.text)
            loggerMain.debug ("Loop iteration :"+str(i))
            i += 1
            try:
                request2 = requests.get(url, headers=headersURL)
            except requests.exceptions.RequestException as e:
                loggerMain.exception ('RequestException in while loop: ' + e)
            # log unusual behaviour
            if i == 5:
                loggerMain.warn('Azure computing needs longer than usual.')
            if i == 9:
                loggerMain.error('Break loop after trying to get result for 20 seconds' )
```

This part tests, if the status of the request is **'Running'** or **'Not started'**, because then Azure is not done with computing and we can't move on.
After every request the loop sleeps for 2 seconds to not spam requests while Azure is still computing.
It logs the current status into the console and breaks the loop, if Azure is ready for us to continue.  
We also check the loop iterations and log warnings/errors, if it takes longer than usual.  
After the loop is done, we want to **return the response body**.  
**Add** the following code **below your previously added code**:

```python
        result = request2.json()
        return result
    except requests.exceptions.RequestException as e:
                loggerMain.critical ('RequestException: ')
                loggerMain.exception (e)
                return
    except Exception as e:
        loggerMain.critical ('Miscellaneous exception: ')
        loggerMain.exception (e)
        return
```

The exception handling blows the code up a bit, but the core functionality is simply storing the response body in the result variable and returning it.  
As getResult is only working for jsons in the Azure format, we want to directly **call** it **from the recognizeTextFromImage** function.  
To do this, we **replace** the following code **in recognizeTextFromImage**:  

```python
    try:
        response = request.headers['Operation-Location']
        loggerMain.debug (response)
        return response
```

with **this**:  

```python
    try:
        response = request.headers['Operation-Location']
        loggerMain.debug (response)
        result = getResult (response)
        return result
```

Instead of returning the response of the post request we give this response to the new getResult function and return the result we get from it.  

It should look like this:  

```
__main__(DEBUG): https://westeurope.api.cognitive.microsoft.com/vision/v2.0/textOperations/5200a3a1-3a21-4106-b79d-0907a864b562
__main__(DEBUG): STATUSTEXT: {"status":"Succeeded","recognitionResult":{"lines":[{"boundingBox":[274,226,363,228,363,245,273,243],"text":"S.OY 5024","words":[{"boundingBox":[279,227,319,228,319,244,279,243],"text":"S.OY","confidence":"Low"},{"boundingBox":[322,228,360,229,360,245,322,244],"text":"5024"}]}]}}
```

The interesting parts of the result are the "lines" and also the "bounding boxes", that correspond to the "text" parts. The lines contain the recognized "text" and also the location of it as "bounding box". We won't use the bounding box in this tutorial, but it could used e.g. to frame the recognized text or censor it. Also note, that the recognized number plate contains a dot. This sometimes happens with the Azure recognition service, but we'll handle it in the next tutorial step.  

**Continue with Step 1**:  
[Step 1](https://github.com/volkerhielscher/netnei/blob/master/tutorial/step_1/)

# DevCamp 2019 diconium

## Step 0: Setup Azure, setup Python and run a small Python script

### 1. Create Microsoft Account and start "Computer Vision" Trial

Go to [Azure](https://azure.microsoft.com/en-us/try/cognitive-services/?api=computer-vision)  
Press **Get API Key** for **"Computer Vision"** (make sure not to accidentally get your key for "Face").  
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

mode = "URL" # default mode
azureEndpoint = 'https://westcentralus.api.cognitive.microsoft.com/vision/v2.0' #TODO replace with your endpoint if needed
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

The code simply imports the requests module, that we need to make web requests to several servers. It also adds a few variables for later use.
You can change the key variable and set it to one of your personal keys (you can find them [here](https://azure.microsoft.com/en-us/try/cognitive-services/)). Also make sure, AzureURL uses your Azure endpoint (**compare to the v2 endpoint**).  
Change it, if you need to.
The 'mode' variable refers to the mode in which to access the images. For now it stays in its default mode. Later we add the functionality to upload local images to the Azure Cloud.  
'imageBaseURL' stores the base URL to access our example images in the github repository. 'headersURL' stores the headers for the request.  
After you've imported the above code into your script, it's time to actually begin defining the function.  
Add the following code **right below the previous code**:  

```python
def postToCloud(mode, file):
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
            # Done in a later step.
            print ()
        elif mode == 'URL':
            # use images from the github remote repository
            jsonData = {"url": imageBaseURL + file}
            request = requests.post(azureURL, headers=headersURL, json=jsonData, timeout=10)
        else:
            print ('Error: PostToCloud() was called with wrong mode')
            return
    except Exception as e:
        print ('Error in postToCloud():')
        print (e)
        return
```

This function asks in which mode to work. This is done by accessing the 'mode' variable. As our 'mode' doesn't change yet the function will only operate in "URL" mode for now.  
The URL to our test image is stored in 'jsonData'. It uses the following syntax: {"url": URLOfImage}. This will be the whole body of our request and only contains the address of the image, that needs to be analyzed by the Azure Cloud.  
Now that were done with the request, we need to do something with the response. In the next tutorial step, we will actively use the information, for now we will only print it to the console.
To do this we first add the following code **at the end of our function**:  

```python
    try:
        print (request.headers['Operation-Location'])
    except Exception as e:
        print ('Exception:')
        print (request.text)
        print (e)

```

This will literally make the function print a part of the response header into the console.  
Operation-Location is the key to the value, we need to access.  
The whole Azure recognizeText service works in two parts. The first part is the posting of the image as we've done above.  
The second part is accessing the information we get from Azure. These information are stored at a specific URL. This URL is exactly the value of the 'Operation-Location' key we get as a response to our post request from above.  
So if everything worked up to this point, we print an URL into the console, when we call our function. To call the function, simply add the following code **at the end of your script**:  

```python
postToCloud(mode, 'bild1.jpg')
```

The image we send to the cloud is the following:  
![image1](https://raw.githubusercontent.com/volkerhielscher/netnei/master/complete/images/bild1.jpg)  
**Save the script** and continue with **4. Run the script**

### 4. Run the script

Open the terminal (*Win-R*, write **cmd** and press *Return* for Windows Users) and execute **each** of the following lines by pressing **return**:  

    cd c:\Users\user\remaining\path\To\Your\Repository\tutorial\

    python devCamp_numberplate.py

If everything worked as intended, you should now see an URL, that looks like  
*https://<i></i>westeurope.api.cognitive.microsoft.com/vision/v2.0/textOperations/XXXXXXXX-XXXX-...*  

**Continue with Step 1**:  
[Step 1](https://github.com/volkerhielscher/netnei/blob/master/tutorial/step_1/)

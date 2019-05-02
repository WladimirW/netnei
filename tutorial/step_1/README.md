# DevCamp 2019 diconium

## Step 1: Send Get Request to the Azure Cloud and get the response text

*If something in this step went wrong for you or if you're unsure where to put something, devCampStep1.py contains the code from the completed step 1 tutorial.*
 *'#-------' lines mark inserted parts*

*After creating the script in Step 0 and sending the first Request to the cloud, you can now start getting the actual response.*  
Azure's *recognizeText* works in 2 parts. At the beginning you need to **post the image** to the cloud as done in Step 0.  
From this request you get an URL in the response header. That was the printed part of the script in Step 0.  
This URL is the location, where Azure stores the result of the text recognition after computing is done.  
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
From this result we want to get a list of all the german number plates:  
**Add** the following code **below the global variables and above your previously added function**:  

```python
def getGermanPlatesFromResult(result):
    '''parse for text in json object and check lines for german number plates and
    returns a list that contains the correct ones.
    '''
    # list to store the regEx results in
    plates = []
    # lines is an array that holds all the recognized text
    for line in result['recognitionResult']['lines']:
        # remove small o's as they are misrecognized circles
        text = re.sub('o', '', line['text'])
        # search for german number plate via regular expression
        match = re.search("[A-ZÖÜÄ]{1,3}[ |-][A-ZÖÜÄ]{1,2}[ |-][0-9]{1,4}[E|H]?", text)
```

In this part we check every by-Azure-found text line for being a german number plate. We do so by firstly eliminating all small 'o's as there no lower case letters in german number plates
and also the recognition software sometimes misrecognizes circles as lower case 'o's. After that we match against a regular expression. Explaining regular expressions as a whole is too much for this tutorial,
but if you're interested in it, you can read about it [here](https://docs.python.org/3/library/re.html). Simply put matches re.search(re, text) the text against the regular expression and returns true, if its a match or false, if it isn't. We store this boolean result in the variable match.  
To continue **add** the following code **below your previously added code**:  

```python
        if (match):
            loggerMain.info("Plate: " + text)
            plates.append(text)
        else:
            loggerMain.info('Not a plate: '+text)
    loggerMain.debug('returned plates: ' + str(plates))
    return plates
```

This part adds the text to our plates list, if the text matches the regular expression. This happens for every found line of text. If all the lines are done, we return the whole list.  
The function should be working now, but we need to call it. To do this we have to add a call.  
**Replace** the following code (*at the bottom of your script*):  

```python
recognizeTextFromImage(mode, 'bild1.jpg')
```

with this code:  

```python
result = recognizeTextFromImage(mode, 'bild1.jpg')
if result:
    plates = getGermanPlatesFromResult(result)
```

Obviously we can only call getGermanPlatesFromResult, if there actually is a result and it's not empty.  
This step is done, so let's test it by calling it from the console:  

```
cd c:\Users\user\remaining\path\To\Your\Repository\tutorial\

python devCamp_numberplate.py
```

The output should look like this:  

```
DEBUG urllib3.connectionpool:    Starting new HTTPS connection (1): westeurope.api.cognitive.microsoft.com
DEBUG urllib3.connectionpool:    https://westeurope.api.cognitive.microsoft.com:443 "POST /vision/v2.0/recognizeText?mode=Printed HTTP/1.1" 202 0
DEBUG __main__:  https://westeurope.api.cognitive.microsoft.com/vision/v2.0/textOperations/1aec53aa-6cb4-498b-9f6a-ff9c9535cc7a
DEBUG urllib3.connectionpool:    Starting new HTTPS connection (1): westeurope.api.cognitive.microsoft.com
DEBUG urllib3.connectionpool:    https://westeurope.api.cognitive.microsoft.com:443 "GET /vision/v2.0/textOperations/1aec53aa-6cb4-498b-9f6a-ff9c9535cc7a HTTP/1.1" 200 339
DEBUG __main__:  STATUSTEXT: {"status":"Succeeded","recognitionResult":{"lines":[{"boundingBox":[146,305,273,337,265,367,138,335],"text":"K QX 1025","words":[{"boundingBox":[146,306,166,311,158,341,139,336],"text":"K"},{"boundingBox":[178,314,211,322,204,352,170,344],"text":"QX","confidence":"Low"},{"boundingBox":[211,322,273,336,266,368,204,352],"text":"1025"}]}]}}
INFO __main__:   Plate: K QX 1025
DEBUG __main__:  returned plates: ['K QX 1025']
```

We added a log entry on info level, so now you can also see the line, that starts with *INFO*. We see it,
because the INFO level is above the DEBUG level in importance and we're currently operating on the DEBUG level.  
You can see the recognized plate in the INFO line. If the recognized text is not in plate format, we log it as "Not a plate: ". You also get the whole response body logged to console. There you can see the position of the text in the image as "bounding boxes". We don't need it, but different applications could make use of it.  
The supplied image is this one:  
![image1](https://raw.githubusercontent.com/volkerhielscher/netnei/master/complete/images/bild1.jpg)  

**Back to Step 0**:  
[Step 0](https://github.com/volkerhielscher/netnei/blob/master/tutorial/step_0/)  

**Continue with Step 2**:  
[Step 2](https://github.com/volkerhielscher/netnei/blob/master/tutorial/step_2/)  

*If something in this step went wrong for you or if you're unsure where to put something, devCampStep1.py contains the code from the completed step 1 tutorial.*
 *'#-------' lines mark inserted parts*

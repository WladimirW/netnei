# DevCamp 2019 diconium

## Step 1: Send Get Request to the Azure Cloud and get the response text

*If something in this step went wrong for you or if you're unsure where to put something, devCampStep1.py contains the code from the completed step 1 tutorial.*
 *'#-------' lines mark inserted parts*

*After creating the script in Step 0 and sending the first Request to the cloud, you can now start getting the actual response.*  
Azure's *recognizeText* works in 2 parts. At the beginning you need to **post the image** to the cloud as done in Step 0.  
From this request you get an URL in the response header. That was the printed part of the script in Step 0.  
This URL is the location, where Azure stores the result of the text recognition after computing is done.  
This result is easily accessible by **sending a GET request** with your key in the request header.  

To do this, we first import two new modules by **adding** the following code **below the already existing *import requests* line**:  

```python
import time, re
```

We need the time module to use a sleep timer and we need the re module to filter all the text in a picture for number plates.
re is the abbreviation for 'regular expressions'.  
Global variables aren't needed in this step, so we can go right to making a new function. **Add it above the postToCloud function from the previous step**:  

```python
def getPlate (url):
    '''Get response of posted image and parses it to access number plate text.
    It uses a regular expression to filter received text for german number plates.

    Argument:
    url -- url to send the Get Request to. Obtained by posting image to Azure Cloud.
    '''
    time.sleep(3) # give Azure time to compute

```

First we want to give Azure a little time to compute. Three seconds usually do the trick.  
**Add** the next part right **below** the previous one (**make sure to keep all the indents, as they are needed**):  

```python
    try:
        i = 0
        # get the response of the image recognition
        request2 = requests.get(url, headers=headersURL)
        print ('STATUSTEXT: ')
        print (request2.text)
```

Again we do a request, but this time we only **need information** and dont need to post anything, so we're going with a **GET request**.  
We use the same headers as before, because we still need the authorization with our key and the key is part of the header. We also **print the response body** into the console to see, what's happening.  

In the next part we want to check, if Azure is done computing. Simply **add** it **below** the previous code:  

```python
        # test, if Azure needs more computing time
        while(request2.json()['status'] == 'Running' or request2.json()['status'] == 'Not started'):
            print ('STATUSTEXT: ' + request2.text)
            print ("Loop "+str(i))
            i += 1
            try:
                request2 = requests.get(url, headers=headersURL)
            except requests.exceptions.RequestException as e:
                print (e)
            time.sleep(2)
```

This part tests, if the status of the request is **'Running'** or **'Not started'**, because then Azure is not done with computing and we can't move on.
After every request the loop sleeps for 2 seconds to not spam requests while Azure is still computing.
It prints the current status to the console and breaks the loop, if Azure is ready for us to continue.  

After the loop is done, we want to **continue with the response**.  
Add the following code **below your previously added code**:  

```python
        # lines is an array that holds all the recognized text
        for line in request2.json()['recognitionResult']['lines']:
            # remove small o's as they are misrecognized circles
            text = re.sub('o', '', line['text'])
            # search for german number plate via regular expression
            match = re.search("[A-ZÖÜÄ]{1,3}[ |-][A-ZÖÜÄ]{1,2}[ |-][0-9]{1,4}[E|H]?", text)
            if (match):
                print('')
                print("Plate: "+ text)
                print('')

            else:
                print('Not a plate: '+text)

```

This part cycles through all the recognized text lines. The recognized lines are all stored in the response body as 'lines'.  
We **delete** all **small 'o's**, as they are misinterpreted circles (there are no lower case letters in number plates) and **match** the result against a **regular expression** to see, if they are in german number plate format.  
To **finish up** our previously started **Try block**, we need to **catch** the possibly **thrown errors** in **except block**. Simply **add** the following code **below the previous code**.  
**Keep track of the indents. the following except lines need to be on the same indent level as the try block from above**

```python
    except requests.exceptions.RequestException as e:
        print (e)
    except Exception as e:
        print ('Error in getPlate():')
        print (e)
```

The function should be working, but we need to call it. To do this, simply **replace the following code** from the **postToCloud()** function

```python
    try:
        print (request.headers['Operation-Location'])
```

with **this** code:  

```python
    try:
        reqHeader = request.headers
        url = reqHeader['Operation-Location']
        print ('Accessing ' + url + ':')
        getPlate(url)

```

This new part gets the url we printed to the console in the last step and hands it over to the new function.  
Let's test the functionality by **running the script** again with the **following commands** via console:  

```
    cd c:\Users\user\remaining\path\To\Your\Repository\tutorial\

    python devCamp_numberplate.py
```

The output should look something like this:  

```
Accessing https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/textOperations/94b4e808-8110-481a-81a1-1cbd4d6113e0:
STATUSTEXT:
{"status":"Succeeded","recognitionResult":{"lines":[{"boundingBox":[146,305,273,337,265,367,138,335],"text":"K QX 1025","words":[{"boundingBox":[146,306,166,311,158,341,139,336],"text":"K"},{"boundingBox":[178,314,211,322,204,352,170,344],"text":"QX","confidence":"Low"},{"boundingBox":[211,322,273,336,266,368,204,352],"text":"1025"}]}]}}

Plate: K QX 1025
```

If the recognized text is not in plate format, we print it to the console as "Not a plate: ". You also get the whole response body printed to console. There you can also see the position of the text as "bounding boxes". We don't need it, but different applications could make use of it.  
The supplied image is this one:  
![image1](https://raw.githubusercontent.com/volkerhielscher/netnei/master/complete/images/bild1.jpg)  

**Continue with Step 2**:  
[Step 2](https://github.com/volkerhielscher/netnei/blob/master/tutorial/step_2/)

*If something in this step went wrong for you or if you're unsure where to put something, devCampStep1.py contains the code from the completed step 1 tutorial.*
 *'#-------' lines mark inserted parts*
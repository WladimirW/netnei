# DevCamp 2019 diconium

## Step 1: Filter result for plates

*If something in this step went wrong for you or if you're unsure where to put something, devCampStep1.py contains the code from the completed step 1 tutorial.*
 *'#-------' lines mark inserted parts*

*After creating the script in Step 0 and sending the first Request to the cloud,  you can now start getting the actual response.*  
  
From this result we want to get a list of all the german number plates:  
**Add** the following code **below the global variables and above the getResult() function**:  

```python
def getGermanPlatesFromResult(result):
    '''parse for text in json object and check lines for german number plates and
    returns a list that contains the correct ones.
    '''
    # list to store the regEx results in
    plates = []
    # lines is an array that holds all the recognized text
    for line in result['recognitionResult']['lines']:
        text = line['text']
        # search for german number plate via regular expression
        match = re.search("([A-Za-zÖÜÄ0]{1,3})[ |-|o|\.|\,|:]([A-Za-zÖÜÄ0]{1,2})[ |-|o|\.|\,|:]([0-9Oo]{1,4}[E|H]?)", text)
```

In this part we check every by-Azure-found text line for being a german number plate. To do this we match against a regular expression. This regular expression also has build-in fault tolerance, that also accepts most lower case letters and similar stuff, that's misrecognized by Azure. Obviously you could shift the tolerance level to a stricter level, if your application needs it, but then you'll miss some plates. For this tutorial we are handling fault tolerance very casually.  
Explaining regular expressions as a whole is too much for this tutorial, but if you're interested in it, you can read about it [here](https://docs.python.org/3/library/re.html). Simply put, re.search(re, text) matches the text against the regular expression and returns true, if its a match or false, if it isn't. We can also access the groups we made in the regular expression individually. (A group is a part of the expression in parenthesis) We have to do so to replace several characters after a match is found.
To continue **add** the following code **below your previously added code**:  

```python
        if (match):
            match1 = str(match.group(1))
            match2 = str(match.group(2))
            match3 = str(match.group(3))

            loggerMain.debug ("Group1:" + match1 + " Group2:" + match2 + " Group3:" + match3)

            # replace town: read misrecognized number (0) with letter
            match1 = re.sub('0', 'O', match1).upper()
            # replace middle part: read misrecognized number (0) with letter
            match2 = re.sub('0', 'O', match2).upper()
            # replace number: read misrecognized letters (O, o) with number
            match3 = re.sub('o', '0', re.sub('O', '0', match3))


            loggerMain.debug ("Group1:" + match1 + " Group2:" + match2 + " Group3:" + match3)
            text = match1 + " " + match2 + " " + match3
            loggerMain.info("Plate: " + text)
            plates.append(text)
        else:
            loggerMain.debug('Not a plate: '+text)
    loggerMain.debug('returned plates: ' + str(plates))
    return plates
```

This part adds the text to our plates list, if the text matches the regular expression. This happens for every found line of text. It also replaces '0' with 'O' for the two first groups (as they can't contain numbers). We put these groups into upper case as license plates can't be in lower case, but Azure sometimes misrecognizes letters for their lower case counterpart. In the last group all 'O's and 'o's get replaced by '0's(as it can't contain letters). This obviously isn't the perfect solution, but until the recognition service improves, there's little to do. If all the lines are done, we return the whole list.  
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
__main__(DEBUG): https://westeurope.api.cognitive.microsoft.com/vision/v2.0/textOperations/45dc92e3-da48-445f-adc9-2b74f21a7d6b
__main__(DEBUG): STATUSTEXT: {"status":"Succeeded","recognitionResult":{"lines":[{"boundingBox":[274,226,363,228,363,245,273,243],"text":"S.OY 5024","words":[{"boundingBox":[279,227,319,228,319,244,279,243],"text":"S.OY","confidence":"Low"},{"boundingBox":[322,228,360,229,360,245,322,244],"text":"5024"}]}]}}
__main__(DEBUG): Group1:S Group2:OY Group3:5024
__main__(DEBUG): Group1:S Group2:OY Group3:5024
__main__(INFO): Plate: S OY 5024
__main__(DEBUG): returned plates: ['S OY 5024']
```

We added a log entry on info level, so now you can also see the info level log. We see it,
because the INFO level is above the DEBUG level in importance and we're currently operating on DEBUG level on the main logger.  
You can see the recognized plate in the INFO line. If the recognized text is not in plate format, we log it as "Not a plate: ". You also get the whole response body logged to console.  
The supplied image is this one:  
![image1](https://raw.githubusercontent.com/volkerhielscher/netnei/master/complete/images/bild1.jpg)  

**Back to Step 0**:  
[Step 0](https://github.com/volkerhielscher/netnei/blob/master/tutorial/step_0/)  

**Continue with Step 2**:  
[Step 2](https://github.com/volkerhielscher/netnei/blob/master/tutorial/step_2/)  

*If something in this step went wrong for you or if you're unsure where to put something, devCampStep1.py contains the code from the completed step 1 tutorial.*
 *'#-------' lines mark inserted parts*

# DevCamp 2019 diconium

## Step 0: Setup Azure, setup Python and run a small Python script

### 1. Create Microsoft Account and start "Computer Vision" Trial

Go to [Azure](https://azure.microsoft.com/en-us/try/cognitive-services/?api=computer-vision)  
Press **Get API Key** for **"Computer Vision"** (make sure not to accidentally get your key for "Face").  
Start your 7-day trial and follow the steps to login.
After your login you will see the following screen:  

![image1](https://raw.githubusercontent.com/volkerhielscher/netnei/master/tutorial/step_0/TutorialImages/KeysTrial.jpg)  

The endpoint with '/v2.0' and atleast one of the keys will be used later on.
If you accidentally closed your browser, you can always find your keys [here](https://azure.microsoft.com/en-us/try/cognitive-services/)  

### 2. Get Python and pip

Go to [Python for Windows](https://www.python.org/downloads/windows/)  
[Python for MAC](https://www.python.org/downloads/mac-osx/)  
[Python for Linux](https://www.python.org/downloads/source/)  
Download the latest Python version 3.\*.\* .  

**ATTENTION** In the Installer for Windows, there is a check box to add Python to PATH as seen here:  
![image2](https://raw.githubusercontent.com/volkerhielscher/netnei/master/tutorial/step_0/TutorialImages/python.jpg)
**Check this box to avoid trouble later on**  

Install Python via the downloaded executable and install the requests package via writing

    python -m pip install requests  

into the terminal (*Win-R*, write **cmd** and press *Return*)  

*If 'python' is not recognized by your command window, you can add python to your path as described [here](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/) or [here (german)](https://bodo-schoenfeld.de/umgebungsvariablen-in-windows-10-bearbeiten/)*  
*Also you can specify the whole path to your python.exe file instead of just writing python:*  

    python -m pip install requests

*is equal to the following if 'python' is not recognized as a Path variable:*

    C:\Users\yourUsername\AppData\Local\Programs\Python\yourPythonVersionFolder\python.exe -m pip install requests

### 3. Create a script

Create a file named "devCamp2019.py"
and copy the content of "devCampStep0.py" into it to make your first script functional.  
The only things to change is the value of the key variable and possibly the Azure URL. Simply change the Xs from the key variable to your personal key and save the file.
To get the correct Azure URL, change the 'westeurope' part of 'AzureURL' to the one, you got as a endpoint for your 7-day Trial previously. (e.g. westcentralus)
You can find it [here](https://azure.microsoft.com/en-us/try/cognitive-services/) if you don't remember.

### 4. Run the script

Open the terminal (*Win-R*, write **cmd** and press *Return* for Windows Users) and execute the script.

    python c:\Users\user\remaining\path\To\Your\Script\devCampStep0.py

If everything worked as intended, you should now see an URL, that looks like  
*https://<i></i>westeurope.api.cognitive.microsoft.com/vision/v2.0/textOperations/XXXXXXXX-XXXX-...*  

Continue with Step 1:  
[Step 1](https://github.com/volkerhielscher/netnei/blob/master/tutorial/step_1/)

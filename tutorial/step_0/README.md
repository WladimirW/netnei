# DevCamp 2019 diconium
## Step 0: Setup Azure, setup Python and run a small Python script
### 1. Create Azure Account and start "Computer Vision" Trial ###  
Go to *https://azure.microsoft.com/*  
Sign up via "Free account" button in the top right corner  
Follow the directions. Ready your phone and credit card to identify.  
After your account is set up, go to *https://portal.azure.com* and log in.  
##### Click on *Create a resource*   
![image1](https://raw.githubusercontent.com/volkerhielscher/netnei/master/tutorial/step_0/TutorialImages/createRes.jpg)  
##### Choose KI + Machine Learning  
![image2](https://raw.githubusercontent.com/volkerhielscher/netnei/master/tutorial/step_0/TutorialImages/createRes2.jpg)  
Enter a name and choose F0 for your pricing option. (F0 is the free version, S1 is the paid version with more requests/second)  
*Create new element* at the resource group field and select it afterwards.  
Every field should be filled in now and you're ready to create your resource.
After waiting a few seconds, you get a notification, that Azure is ready and you can access your resource.  
To do that, click on *All resources*, select your newly created resource and click on *Keys*.  
There you can find your subscription keys. You need one of them to access your Azure resource later.  
 
### 2. Get Python and pip  
Go to https://www.python.org/downloads/ for the Windows version.  
https://www.python.org/downloads/mac-osx/ for MAC  
https://www.python.org/downloads/source/ for LINUX  
Download the latest Python version 3.\*.\* .  
Install Python via the downloaded executable and install the requests package via writing

    python -m pip install requests  

into the terminal (*Win-R*, write **cmd** and press *Return*)  


*If python is not recognized by your command window, you can add python to your path as described [here](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/) or here in [german](https://bodo-schoenfeld.de/umgebungsvariablen-in-windows-10-bearbeiten/)*  
*Also you can specify the whole path to your python.exe file instead of just writing python:*  

    python -m pip install requests
	
*is the following without working path variables:*

    C:\Users\yourUsername\AppData\Local\Programs\Python\yourPythonVersionFolder\python.exe -m pip install requests




### 3. Create a script  
Create a file named "devCamp2019.py"
and copy the content of "devCampStep0.py" into it to make your first script functional.  
The only thing to change is the value of the key variable. Simply change the Xs to your personal key and save the file.
*If you forgot where to find the key, look at the end of* *1. Create Azure Account and start "Computer Vision" Trial*
### 4. Run the script  
Open the terminal (*Win-R*, write **cmd** and press *Return* for Windows Users) and execute the script.

    python c:\Users\user\remaining\path\To\Your\Script\devCampStep0.py

If everything worked as intended, you should now see an URL, that looks like  
*https://<i></i>westeurope.api.cognitive.microsoft.com/vision/v2.0/textOperations/XXXXXXXX-XXXX-...*  

Continue with Step 1:  
[Step 1](https://github.com/volkerhielscher/netnei/blob/master/tutorial/step_1/)

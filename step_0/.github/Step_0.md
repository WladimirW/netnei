# DevCamp 2019 diconium
## Step 0: Setup Azure, setup Python and run a small Python script
** 1. Create Azure Account and start "Computer Vision" Trial **  
Go to *https://azure.microsoft.com/*  
Sign up via "Free account" button in the top right corner  
Follow the directions. Ready your phone and credit card to identify.  
After your account is set up, go to *https://portal.azure.com* and log in.  
Click on *Create a resource*   
--PICTURE--  
Choose KI + Machine Learning  
--PICTURE--  
Enter a name and choose F0 for your pricing option. (F0 is the free version, S1 is the paid version with more requests/second)  
create new element for the resource group and select it afterwards.  
Every field should be filled in now and you're ready to create your resource.
After waiting a few seconds, you get a notification, that Azure is ready and you can access your resource.  
To do that, click on *All resources*, select your newly created resource and click on *Keys*.  
There you can find your subscription keys. You need them to access your Azure resource.  
 
** 2. Get Python and pip **  
Go to https://www.python.org/downloads/ for the Windows version.  
https://www.python.org/downloads/mac-osx/ for MAC  
https://www.python.org/downloads/source/ for LINUX  
Download the latest Python version 3.\*.\* .  
Install Python via the downloaded executable and install the requests package via writing

    python -m pip install requests  

into the terminal (Win-R)  

** 3. Create a script **  
Create a file named "devCamp2019.py"
and copy the content of "devCampStep0.py" into it to get your first script functional.  
** 4. Run the script **  
Open the terminal (Win-R for Windows users) and execute the script.

    python c:\Users\user\remaining\path\To\Your\Script\devCampStep0.py

If everything worked as intended, you should now see an URL, that looks like  
*https://westeurope.api.cognitive.microsoft.com/vision/v2.0/textOperations/XXXXXXXX-XXXX-...*
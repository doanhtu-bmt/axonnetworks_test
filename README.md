This project is based on python programming language

Test Rquirements:  
    Weather tools Use case: 
    1. Use https://www.accuweather.com 
    2. Select Daily menu -> Page will display weather information for 30 days 
    + Example: At the top of page say: November 8 - December 22. And there are summary of weather information of each day 
    3. For each day, retrieve following information 
    Day value: 
    + Example: Thursday, November 8 
    Day (Morning or Afternoon)/Night (Evening or Overnight) information: 
    - Temperature value: 
    + Example: 88F 
    - Main weather of the day: 
    + Example: Cloudy 
    - Day's real feel: 
    + Example: RealFeel®101° 
    - Humidity (Morning/Afternoon) : 70% 
    4. Retrieve temperature in Fahrenheit and validate the value with temperature in Celsius. 
    5. The test should be supported to execute at least every 1 hour in a day. 
    6. To save in a file all information retrieved. 
    7. Create a summary report. 
    Submit the code with script, all required libraries, readme file, test run and sample report. 

Installation and setup:
 - Install python > 3.6
 - Install selenium for python:
        pip install selenium
        pip install selenium-page-factory

 - Build/install psutil Python package
        pip install --no-binary :all: psutil
        - Note:
            When you install psutil through pip on Windows, sometimes you may encounter this error:
            error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
            This means the library you're installing has code written in other languages and needs additional tools to install. To install these tools, follow the following steps: (Requires 6GB+ disk space)
            1. Open https://visualstudio.microsoft.com/visual-cpp-build-tools/.
            2. Click Download Build Tools >. A file named vs_BuildTools or vs_BuildTools.exe should start downloading. If no downloads start after a few seconds, click click here to retry.
            3. Run the downloaded file. Click Continue to proceed.
            4. Choose C++ build tools and press Install. You will need a reboot after the installation.
            5. Try installing the library via pip again.

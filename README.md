# assignment_1

This assignment is to perform greenhouse monitoring using Raspberry Pi. This assignment is required to perform on following task:
1) Write monitorAndNotify.py3 to read temperature and humidity range from config.json. The python file need to log the current time, temperature and humidity to a database every minute. The script need to scheduled to automatically run when the Pi boots. After saving the data, if the reading is outside the configuration range and if so, send a notification using Pushbullet per day.   
2) Write createReport.py3 to create report.csv file. This csv file contains each days’ data that retrieve from the database. If the data is within the configured temperature and humidity range then the status of OK is applied, otherwise the label of BAD is applied with an appropriate message detailing the error(s) is included. 
3) Create greenhouseBluetooth.py3 using bluetooth to detect nearby devices. Send PushBullet message stating the current temperature, humidity and if the reading fall within the configured range. The script need to schedule to automatically run when the Pi boots.
4) Use 2 different Python data visualisation libraries to create 2 images. Create a python file called analytics.py3 to create the image. Analytics.txt file will be used to document the question and the comparison of the techniques.
5) The python coding must be writing in object-oriented method and fulfill PEP8 style guide.

Json setting file
1) config.json
	This json file is use to record the minimum value of temperature, maximum value of temperature, minimum value of humidity, and maximum value of temperature.

2) setting.json 
	This json file is ued to record info on database name, pushBullet access token, pushBullet greeting name, and bluetooth pairing device name.  

Execution
1) analytics.py3
	This python file is for running the analytic libraries and perform the visualization of the data.

2) createReport.py3
	This python file is for create the csv report file.
	
3) greenhouseBluetooth.py3
	This python file is for bluetooth detect the device and send the message using PushBullet.

4) monitorAndNotify.py3
	This python file is to run the greenhouse monitoring process and capture the data that save in the database. If notification is need to be send, the message is send using pushBullet.  

Module
1) jasonReader.py
	This module is use for reading json configuration file.
	
2) generateLinePlot.py
	This module is use to generate line plot graph.
	
3) generateScatterPlot.py
	This module is use to generate line plot graph.

4) pyCurlBullet.py
	This module is use to send message using PushBullet.
	
5) senseHatOp.py
	This module is use to define customize SenseHat operation that using SenseHat library.   

6) sqlite.py
	This module is the base sqlite library that ready for other class or object usage. 

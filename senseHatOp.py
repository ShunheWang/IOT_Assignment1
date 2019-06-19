import os
import datetime
from sense_hat import SenseHat
from pytz import timezone
from datetime import datetime

#customise SenseHat class
class senseHat:
    # constructor
    def __init__(self):
        self.__temperature = 0
        self.__humidity = 0
        self.__timeStamp = 0

    # retrieve data from SenseHat
    def retrieveData(self):
        sense = SenseHat()
        self.__temperature = self.__calibrateTemperature()
        self.__humidity = sense.get_humidity()
        self.__timeStamp = self.__changeTime()    
        if (self.__temperature <= 0 or self.__humidity <= 0):  
            self.retrieveData()  
    
    # change utc to Melbourne timezone
    def __changeTime(self):
        mel_zone=timezone('Australia/Melbourne')
        return datetime.now(mel_zone).strftime('%Y-%m-%d %H:%M:%S')
     
    # reference from lecture coding
    # get CPU tempeerature
    def __getCPUTemperature(self):
        res = os.popen("vcgencmd measure_temp").readline()
        return float(res.replace("temp=","").replace("'C\n",""))

    # reference from lecture coding  
    # calibrate the temperature and the relative temperature      
    def __calibrateTemperature(self):
        sense = SenseHat()
        t1 = sense.get_temperature_from_humidity()
        t2 = sense.get_temperature_from_pressure()
        t_cpu = self.__getCPUTemperature()
        t = (t1 + t2) / 2
        t_corr = t - ((t_cpu - t) / 1.5)
        t_corr = round(t_corr,1)
        return t_corr

    # getter function for temperature
    def getTemperatture(self):
        return self.__temperature

    # getter function for humidity
    def getHumidity(self):
        return self.__humidity 

    # getter function for timestamp
    def getTimeStamp(self):
        return self.__timeStamp
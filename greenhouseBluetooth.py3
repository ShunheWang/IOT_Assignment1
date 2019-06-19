import bluetooth
from jasonReader import settingReader, configReader
from sense_hat import SenseHat
from senseHatOp import senseHat
from pyCurlBullet import pyCurlBullet
 
#Reference from lecture code
class blueToothDevice:
    def __init__(self):
        self.__username = ""
        self.__device = ""
        self.__configFile = "config.json"
        self.__settingFile = "setting.json"

    #Run method to start execution
    def run(self):
        jConfig = configReader(self.__configFile)
        jSetting = settingReader(self.__settingFile)
                
        self.__username = jSetting.getGreetName()
        self.__device = jSetting.getPhoneName()
        #Get min and max temperature, min and max humidity from configuration file
        minTemperature = jConfig.getMinTemperature()
        maxTemperature = jConfig.getMaxTemperature()
        minHumidity = jConfig.getMinHumidity()
        maxHumidity = jConfig.getMaxHumidity()
        
        while True:
            deviceAddress = None
            devices = bluetooth.discover_devices()

            for row in devices:
                if self.__device == bluetooth.lookup_name(row, timeout = 5):
                    deviceAddress = row
                    break    

            if self.__device is not None:
                print("Hi {}! Your device ({}) has the MAC address: {}".format(self.__username, self.__device, deviceAddress))
                senhat = senseHat()
                senhat.retrieveData()
                #Get current temperature and humidity
                temperature = round(senhat.getTemperatture(),2)
                humidity = round(senhat.getHumidity(),2)

                message = ""
                
                #If temperature and humidity in the range
                if (temperature <= maxTemperature and temperature >= minTemperature and humidity <= maxHumidity and humidity >= minHumidity):
                    message = "Hi {}! Current temperature is {} *C & humidity is {}. ".format(self.__username, temperature, humidity) 
                    jSetting = settingReader(self.__settingFile)
                    token = jSetting.getAccessToken()
                    pyCurlB = pyCurlBullet(token, message)
                    pyCurlB.run()
                    break
                else: 
                    message = "reading outside range!"   
                    sense = SenseHat()
                    sense.show_message(message, scroll_speed=0.05)      

bd = blueToothDevice()
bd.run()

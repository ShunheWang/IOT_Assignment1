import json 
from pathlib import Path

# base class for json reader 
class jasonReader(object):
    # constructor
    def __init__(self, filename):
        self.__filename = filename

    # check json file
    def checkFileExist(self):
        config = Path(self.__filename)
        if config.is_file():
            return True
        else:
            return False
    
    # load file
    def loadFile(self):
        try:
            config = open(self.__filename, encoding = "utf-8")
            data = json.load(config)
            return data
        except:
            raise Exception("File loading error!")

# configuration json file reader
class configReader(jasonReader):
    # constructor
    def __init__(self, filename):
        jasonReader.__init__(self, filename)
        self.__minTemperature = -100 
        self.__maxTemperature = -100
        self.__minHumidity = -100
        self.__maxHumidity = -100
        check = jasonReader.checkFileExist(self)
        if check == True:
            data = jasonReader.loadFile(self)
            try:
                self.__minTemperature = data['min_temperature'] 
                self.__maxTemperature = data['max_temperature']
                self.__minHumidity = data['min_humidity']
                self.__maxHumidity = data['max_humidity']
            except:
                raise Exception("loading data error!")    
        else:
            raise Exception("File not found!")

    # getter function for minimum temperature
    def getMinTemperature(self):
        return self.__minTemperature

    # getter function for maximum temperature
    def getMaxTemperature(self):
        return self.__maxTemperature

    # getter function for minimum humidity
    def getMinHumidity(self):
        return self.__minHumidity  

    # getter function for maximum humidity
    def getMaxHumidity(self):
        return self.__maxHumidity             

# class to read setting json file
class settingReader(jasonReader):
    # constructor
    def __init__(self, filename):
        jasonReader.__init__(self, filename)
        self.__dbName = -100 
        self.__accessToken = -100
        self.__greetName = "" 
        self.__phoneName = ""
        check = jasonReader.checkFileExist(self)
        if check == True:
            data = jasonReader.loadFile(self)
            try:
                self.__dbname = data['dbname'] 
                self.__accessToken = data['accessToken']
                self.__greetName = data['greetName']
                self.__phoneName = data['phoneName']
            except:
                raise Exception("loading data error!")     
        else:
            raise Exception("File not found!")

    # getter function for database name
    def getDbName(self):
        return self.__dbname

    # getter function for Access Token
    def getAccessToken(self):
        return self.__accessToken 

    # getter function for Greeting Name
    def getGreetName(self):
        return self.__greetName   

    # getter function for Phone Name
    def getPhoneName(self):
        return self.__phoneName             
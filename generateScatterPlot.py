import numpy as np
import matplotlib.pyplot as plt
from sqlite import sqlite
from jasonReader import settingReader, configReader

#splite class to get data from database
class sqliteGra(sqlite):
    def __init__(self, dbName):
        sqlite.__init__(self, dbName)
    
    def getReadingData(self):
        conn = sqlite.createConnection(self)
        curs = conn.cursor()
        #check have table or not
        try:
            curs.execute("select * from MONITOR_DATA")
            rows = curs.fetchall()
            conn.close()
            return rows
        except Exception as e:
            conn.close()
            print(e)
            raise Exception("Get data fail!")   

#Graph class to generate graph
class scatterGraph:
    def __init__(self):
        self.__configFile = "config.json"
        self.__settingFile = "setting.json"
        self.jConfig = configReader(self.__configFile)
        self.tempGourp=[]
        self.humGourp=[]

    #init data for graph
    def initGraphData(self):
        jSetting = settingReader(self.__settingFile)
        dbName=jSetting.getDbName()
        db=sqliteGra(dbName)
        temp=db.getReadingData()
        #Separate data into different list
        for num in temp:
            self.tempGourp.append(float(num[1]))
            self.humGourp.append(float(num[2]))
    
    #Get minimum value for minimun edge value
    def initMinGraphEdgeValue(self,data):
        self.temp=data[0]
        for value in data:
            if(self.temp>value):
                self.temp=value
        return self.temp

    #Get maximum value for maximum edge value
    def initMaxGraphEdgeValue(self,data):
        self.temp=data[0]
        for value in data:
            if(self.temp<value):
                self.temp=value
        return self.temp

    #Create graph
    def createGrph(self):
        self.initGraphData()
        #Get data from configuration file
        minTemperature = self.jConfig.getMinTemperature()
        maxTemperature = self.jConfig.getMaxTemperature()
        minHumidity = self.jConfig.getMinHumidity()
        maxHumidity = self.jConfig.getMaxHumidity()

        self.pointColor=np.arctan2(self.tempGourp,self.humGourp)#for color value
        plt.scatter(self.tempGourp,self.humGourp,s=75,c=self.pointColor,alpha=0.5)
        #Generate min and max edge value
        self.minX=self.initMinGraphEdgeValue(self.tempGourp)-5
        self.maxX=self.initMaxGraphEdgeValue(self.tempGourp)+10
        self.minY=self.initMinGraphEdgeValue(self.humGourp)-5
        self.maxY=self.initMaxGraphEdgeValue(self.humGourp)+10
        plt.xlim((self.minX,self.maxX))
        plt.ylim((self.minY,self.maxY))

        #Edge definition
        plt.xlabel("temperature")
        plt.ylabel("humidity")

        #Generate functions to display data range
        plt.axvline(minTemperature,ls="--",color="r")
        plt.axvline(maxTemperature,ls="--",color="r")

        plt.axhline(minHumidity,ls="--",color="r")
        plt.axhline(maxHumidity,ls="--",color="r")

        #plt.show()
        plt.savefig("temp.png")

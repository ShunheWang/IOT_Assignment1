import datetime
import time
from jasonReader import settingReader, configReader
from sqlite import sqlite
from senseHatOp import senseHat
from datetime import datetime
from pyCurlBullet import pyCurlBullet

from sense_hat import SenseHat

# sqlite class for greenhouse monitor
class sqliteMon(sqlite):
    # constructor
    def __init__(self, dbName):
        sqlite.__init__(self, dbName)
    
    #check monitor data table for insertReadingData
    def checkAndCreateMonitorDataTable(self):
        conn = sqlite.createConnection(self)
        curs = conn.cursor()
        try:
            curs.execute("create table if not exists MONITOR_DATA (TIMESTAMP varchar(20),TEMPERATURE varchar(20), HUMIDITY varchar(20))")
            conn.commit()
            conn.close()
        except Exception as e:
            conn.close()
            print(e)
            raise Exception("Create table fail")

    #check notification data table for insertReadingData
    def checkAndCreateNotificationTable(self):
        conn = sqlite.createConnection(self)
        curs = conn.cursor()
        try:
            curs.execute("create table if not exists NOTIFICATION_DATA (DATESTAMP varchar(20), TIMESTAMP varchar(20))")
            conn.commit()
            conn.close()
        except Exception as e:
            conn.close()
            print(e)
            raise Exception("Create table fail")
           
    # insert monitor reading data
    def insertReadingData(self, reading):
        conn = sqlite.createConnection(self)
        curs = conn.cursor()
        #check have table or not
        try:
            #curs.execute("insert into test1(id,name) values (?, ?)", (reading[0]))
            curs.execute("insert into MONITOR_DATA(TIMESTAMP, TEMPERATURE, HUMIDITY) values (?, ?, ?)", (reading[0]))
            print("insert successfully!")
            conn.commit()
            conn.close()
        except Exception as e:
            conn.close()
            print(e)
            raise Exception("Insert data fail!") 

    # insert notification data
    def insertNotificationData(self, data):
        conn = sqlite.createConnection(self)
        curs = conn.cursor()
        try:
            curs.execute("insert into NOTIFICATION_DATA(DATESTAMP, TIMESTAMP) values (?, ?)", (data[0]))
            conn.commit()
            conn.close()
        except Exception as e:
            conn.close()
            print(e)
            raise Exception("Insert data fail!")   

    # check notification data
    def checkNotification(self, data):
        conn = sqlite.createConnection(self)
        curs = conn.cursor() 
        try:
            curs.execute("select DATESTAMP, TIMESTAMP from NOTIFICATION_DATA where DATESTAMP = ?", (data,))
            rows = curs.fetchall()
            conn.close()
            rValue = False
            if len(rows) != 0:
                rValue = True
            return rValue
        except Exception as e:
            conn.close()
            print(e)
            raise Exception("read data fail!")

class monitorAndNotify(object):
    # constructor
    def __init__(self):
        self.__configFile = "config.json"
        self.__settingFile = "setting.json"
        self.__frequency = 2 # time in second

    # execution of the monitor process
    def run(self):
        sense = SenseHat()
        sense.show_message('monitorAndNotify start', scroll_speed=0.02)
        
        jConfig = configReader(self.__configFile)
        jSetting = settingReader(self.__settingFile)

        minTemperature = jConfig.getMinTemperature()
        maxTemperature = jConfig.getMaxTemperature()
        minHumidity = jConfig.getMinHumidity()
        maxHumidity = jConfig.getMaxHumidity()

        dbname = jSetting.getDbName()
        token=jSetting.getAccessToken()
        sqlite3 = sqliteMon(dbname)
        senhat = senseHat()

        for i in range(0, 60):
            senhat.retrieveData()

            temperature = round(senhat.getTemperatture(),2)
            humidity = round(senhat.getHumidity(),2)
            timeStamp = senhat.getTimeStamp()

            reading = [(timeStamp, temperature, humidity)]
            dbname = jSetting.getDbName()

            sqlite3.checkAndCreateMonitorDataTable()
            sqlite3.insertReadingData(reading)

            d = datetime.today()
            dtime = d.strftime('%y-%m-%d')

            sqlite3.checkAndCreateNotificationTable()
            check = sqlite3.checkNotification(dtime)

            message = ""

            if (check == False) :
                sendFlag = False
                if (temperature <= maxTemperature and temperature >= minTemperature):
                    pass
                else:
                    if (temperature > maxTemperature):
                        message = message + str(temperature) + " *C above maximum temperature. "
                   
                    if (temperature < minTemperature):
                        message = message + str(temperature) + " *C below minimum temperature. "
                    
                    sendFlag = True   

                if (humidity <= maxHumidity and humidity >= minHumidity):
                    pass
                else:
                    if (humidity > maxHumidity):
                        message = message + str(humidity) + " above maximum humidity. "
                    
                    if (humidity < minHumidity):
                        message = message + str(humidity) + " below minimum humidity. "
                    sendFlag = True

                if (sendFlag == True):
                    #add info into notification database
                    notificationData=[(dtime,timeStamp)]
                    # send info to bulletpush
                    pyCurlB = pyCurlBullet(token, message)
                    pyCurlB.run()    
                    sqlite3.insertNotificationData(notificationData)
            time.sleep(self.__frequency)
            sense.show_message('monitorAndNotify end', scroll_speed=0.02)

mon = monitorAndNotify()
mon.run()
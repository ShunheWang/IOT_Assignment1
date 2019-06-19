import csv
import os
from jasonReader import settingReader, configReader
from sqlite import sqlite


# sqlite operation
class sqliteMon(sqlite):
    def __init__(self, dbName):
        sqlite.__init__(self, dbName)

    # Read data from database
    def readMonitorData(self):
        conn = sqlite.createConnection(self)
        curs = conn.cursor()
        try:
            curs.execute("select date(TIMESTAMP)," +
                         "avg(TEMPERATURE), avg(HUMIDITY)" +
                         "from MONITOR_DATA group by date(TIMESTAMP)")
            rows = curs.fetchall()
            conn.close()
            return rows
        except Exception as e:
            conn.close()
            print(e)
            raise Exception("read data fail!")


# Create analysis report
class csvReport:
    def __init__(self, filename):
        self.__filename = filename
        self.__configFile = "config.json"
        self.__settingFile = "setting.json"

    # Check exist file
    def checkFile(self):
        if os.path.exists(self.__filename):
            pass
        else:
            open(self.__filename, "w+")

    # Write first line in analysis report
    def writeHeader(self, header1, header2):
        with open(self.__filename, 'w',
                  encoding='utf-8', newline='') as csvFile:
            self.checkFile()
            writeCsv = csv.writer(csvFile)
            writeCsv.writerow([header1, header2])

    # Write all data into analysis report
    def writeRecord(self, date, info):
        with open(self.__filename, 'a',
                  encoding='utf-8', newline='') as csvFile:
            writeCsv = csv.writer(csvFile)
            writeCsv.writerow([date, info])

    # Main run function
    def run(self):
        jConfig = configReader(self.__configFile)
        jSetting = settingReader(self.__settingFile)

        dbname = jSetting.getDbName()
        sqlite3 = sqliteMon(dbname)
        rows = sqlite3.readMonitorData()

        # Get data from json file
        minTemperature = jConfig.getMinTemperature()
        maxTemperature = jConfig.getMaxTemperature()
        minHumidity = jConfig.getMinHumidity()
        maxHumidity = jConfig.getMaxHumidity()

        report = csvReport(self.__filename)
        report.writeHeader("Date", "Status")

        for rec in rows:
            recTime = rec[0]
            recTemperature = int(rec[1])
            recHumidity = int(rec[2])

            message = ""

            # Check current data in or out the range
            if (recTemperature <= maxTemperature and recTemperature >= minTemperature and recHumidity <= maxHumidity and recHumidity >= minHumidity):
                report.writeRecord(recTime, "ok")
            else: 
                message = "BAD: "
                if (recTemperature > maxTemperature):
                    temp = recTemperature - maxTemperature
                    message = message + str(temp) + " *C above maximum temperature. "
                    
                if (recTemperature < minTemperature):
                    temp = minTemperature - recTemperature
                    message = message + str(temp) + " *C below minimum temperature. "

                if (recHumidity > maxHumidity):
                    temp = recHumidity - maxHumidity
                    temp = (temp/maxHumidity) * 100
                    message = message + str(temp) + " % above maximum humidity. "
                    
                if (recHumidity < minHumidity):
                    temp = minHumidity - recHumidity
                    temp = (temp/minHumidity) * 100
                    message = message + str(temp) + " % below minimum humidity. "  
            report.writeRecord(recTime, message)


cr = csvReport("dataReport.csv")
cr.run()

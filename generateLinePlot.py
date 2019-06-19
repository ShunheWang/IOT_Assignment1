from pyecharts import Line
from sqlite import sqlite
from jasonReader import settingReader, configReader


class sqliteGra(sqlite):
    def __init__(self, dbName):
        sqlite.__init__(self, dbName)

    # Get average data from database based on the timestamp
    def readMonitorData(self):
        conn = sqlite.createConnection(self)
        curs = conn.cursor()
        try:
            curs.execute("select date(TIMESTAMP), avg(TEMPERATURE), "
                         + "avg(HUMIDITY) "
                         + "from MONITOR_DATA group by date(TIMESTAMP)")
            rows = curs.fetchall()
            conn.close()
            return rows
        except Exception as e:
            conn.close()
            print(e)
            raise Exception("read data fail!")


class lineGraph:
    def __init__(self):
        self.__configFile = "config.json"
        self.__settingFile = "setting.json"
        self.jConfig = configReader(self.__configFile)
        self.aveTemp = []
        self.aveHum = []
        self.every = []

    # init all data for graph
    def initGraphData(self):
        jSetting = settingReader(self.__settingFile)
        dbName = jSetting.getDbName()
        db = sqliteGra(dbName)
        temp = db.readMonitorData()

        # Store all data into different list
        for num in temp:
            self.every.append(num[0])
            self.aveTemp.append(round(num[1], 2))
            self.aveHum.append(round(num[2], 2))

    # Generate graph
    def createGrph(self):
        self.initGraphData()
        # Graph title
        line = Line("Average T and H")
        # Temperature line and min and max point
        line.add("Temperature", self.every, self.aveTemp,
                 mark_point=["max", "min"])
        # Humidity line and and max and average point
        line.add("Humidity", self.every, self.aveHum,
                 is_smooth=True, mark_line=["max", "average"])
        # Generate html file
        line.render("pyechart.html")

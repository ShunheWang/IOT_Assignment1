import sqlite3
# sqlite base class
class sqlite:
    # constructor
    def __init__(self, dbName):
        self.__dbName = dbName

    #create connection to the database
    def createConnection(self):
        try:
            conn = sqlite3.connect(self.__dbName)
            return conn
        except Exception as e:
            print(e)
            raise Exception("Database connection error!")    
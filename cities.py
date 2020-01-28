import logging
import db_handler

# ---------------------------------------------------------
# Class to hold all the cities for the website
# --------------------------------------------------------
class Cities(object):
    def __init__(self):
        self.cities_offline = ['Tel-Aviv', 'Haifa', 'Ashdod', 'Beijing', 'Tokyo'] #list of offline cities
        self.DbHandler = db_handler.DbHandler()
        self.cities = [] #to be the list of the DB cities

# ---------------------------------------------------------
# returns all offline cities 
# --------------------------------------------------------    
    def getCities(self):
        return self.cities

# ---------------------------------------------------------
# returns all cities that appear in the DB
# --------------------------------------------------------    
    def getCitiesFromDb(self):
        self.DbHandler.connectToDb()
        cursor = self.DbHandler.getCursor()
        sql = "select distinct o_city from dogOwner;" #all cities used by owners
        cursor.execute(sql)
        records = cursor.fetchall()
        for record in records:
            self.cities.append(record[0])
        self.DbHandler.disconnectFromDb()
        return self.cities
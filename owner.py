import db_handler
import datetime
import google.appengine.api
import time
import MySQLdb
import logging


# ---------------------------------------------------------
# Class to handle a dog OWNER object
# --------------------------------------------------------
class Owner():
    def __init__(self):
        self.o_DbHandler = db_handler.DbHandler()
        self.o_email=""
        self.o_name = ""
        self.o_city = ""
        self.o_bday = ""
        self.o_telephone = ""
        self.o_age = ""
        
# ---------------------------------------------------------
# inserts a dog owner to the DB
# --------------------------------------------------------
    def insertToDb(self):
        now = datetime.datetime(2009, 5, 5)
        try:
            self.o_DbHandler.connectToDb()
            cursor=self.o_DbHandler.getCursor()
            sql1 = "INSERT INTO dogOwner(o_name,o_email,o_telephone,o_city,o_bday) Values (%s,%s,%s,%s,%s)"
            cursor.execute(sql1,(self.o_name,self.o_email,self.o_telephone,self.o_city,self.o_bday))
            self.o_DbHandler.commit()
        except MySQLdb.IntegrityError:
            logging.warn("failed to insert values")
        finally:
		    self.o_DbHandler.disconnectFromDb()

        

import db_handler
import datetime
import google.appengine.api
import time
import MySQLdb
import logging


# ---------------------------------------------------------
# Class to handle a dog TRIP object
# --------------------------------------------------------
class Trip():
    def __init__(self):
        self.t_DbHandler = db_handler.DbHandler()
        self.dogID=""
        self.d_name = ""
        self.t_date = ""
        self.d_breed = ""
        self.d_age = ""
        self.t_fromHome = False
        self.t_day = ""
        self.w_email = ""
        
# ---------------------------------------------------------
# inserts a dog trip to the DB
# --------------------------------------------------------
    def insertToDb(self):
        week_days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        formattedDate = datetime.datetime.strptime(self.t_date, '%Y-%m-%d')
        self.t_day = week_days[int(formattedDate.strftime('%w'))]
        try:
            self.t_DbHandler.connectToDb()
            cursor=self.t_DbHandler.getCursor()
            sql1 = "INSERT INTO trip(t_day,t_date,w_from_home,dogID,w_email) Values (%s,%s,%s,%s,%s)"
            cursor.execute(sql1,(self.t_day,self.t_date,self.t_fromHome,self.dogID,self.w_email))
            self.t_DbHandler.commit()
        except MySQLdb.IntegrityError:
            logging.warn("failed to insert values")
        finally:
		    self.t_DbHandler.disconnectFromDb()

        

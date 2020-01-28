import db_handler
import datetime
import google.appengine.api
import logging

# ---------------------------------------------------------
# Class to handle a dog walker object
# --------------------------------------------------------
class Walker():
    def __init__(self):
        self.w_DbHandler = db_handler.DbHandler()
        self.w_email = ""
        self.w_name = ""
        self.w_telephone = ""
        self.w_city = ""
        self.w_breeds = []
        self.w_days = []
        self.w_price = {'sun': None, 'mon': None, 'tue': None,
                        'wed': None, 'thu': None, 'fri': None, 'sat': None} # price for eavery week day
        self.w_dog_num = {'sun': None, 'mon': None, 'tue': None,
                          'wed': None, 'thu': None, 'fri': None, 'sat': None} # dog capacity for each day of week

# ---------------------------------------------------------
# Insert a new dog walker to the db
# --------------------------------------------------------
    def insertToDb(self):
        try:
            self.w_DbHandler.connectToDb()
            cursor = self.w_DbHandler.getCursor()


            sql1 = "INSERT INTO dogWalker(w_name,w_email,w_telephone, w_city) Values (%s,%s,%s,%s)"
            cursor.execute(sql1, (self.w_name, self.w_email,
                                self.w_telephone, self.w_city))
            self.w_DbHandler.commit()

            for breed in self.w_breeds:
                self.insertSingleBreed(self.w_email, breed, cursor)

            for day in self.w_days:
                if self.w_price[day] != {} and self.w_dog_num[day] != {}: #checks if price or dog capacity are not null
                    logging.error(day)
                    logging.error(self.w_dog_num)
                    self.insertSingleDay(
                        self.w_email, self.convertToFullDay(day), self.w_price[day], self.w_dog_num[day],cursor)
                else:
                    logging.error('error in walker insert to db')
        finally:
            self.w_DbHandler.disconnectFromDb()

# ---------------------------------------------------------
# Insert a new DAY object to the DB
# --------------------------------------------------------
    def insertSingleDay(self, email, day, price, dog_num, cur):
        sql = "INSERT INTO week_day(w_email, day_name, price, maxDogs) Values (%s,%s,%s,%s)"
        cur.execute(sql, (email, day, price, dog_num))
        self.w_DbHandler.commit()

# ---------------------------------------------------------
# Insert a new BREED object to the DB
# --------------------------------------------------------
    def insertSingleBreed(self, email, breed, cur):
        sql = "INSERT INTO breed(w_email, d_breed) Values (%s,%s)"
        cur.execute(sql, (email, breed))
        self.w_DbHandler.commit()
        
    def convertToFullDay(self, day):
        weekDays = {'sun':'sunday', "mon":"monday","tue":"tuesday","wed":"wednesday", "thu":"thursday","fri":"friday","sat":"saturday"}
        return weekDays[day]
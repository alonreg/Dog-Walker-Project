# -------------------------------------------------------------------------------
# Message
# -------------------------------------------------------------------------------
# A class to manage the Messages - create and save in the DB
# -------------------------------------------------------------------------
# Author:       Tomer Lev
# Last updated: 04.10.2019
# -------------------------------------------------------------------------

# import logging so we can write messages to the log
import logging

import db_handler

# ---------------------------------------------------------
# Class designed to hold a dog object
# --------------------------------------------------------
class Dog(object):
    def __init__(self):
        self.d_DbHandler = db_handler.DbHandler()
        self.d_id = 0
        self.d_name = ""
        self.d_gender = ""
        self.d_age = ""
        self.d_o_email = ""
        self.d_breed = ""


# ---------------------------------------------------------
# Insert the new dog to the DB
# --------------------------------------------------------
    def insertToDb(self):
        self.d_DbHandler.connectToDb()
        cursor = self.d_DbHandler.getCursor()
        sql = "INSERT INTO dog(dogID,o_email,d_name,d_gender,d_age,d_breed) SELECT MAX(dogID)+1 ,%s,%s,%s,%s,%s FROM dog"
        cursor.execute(sql, (self.d_o_email, self.d_name,
                             self.d_gender, self.d_age, self.d_breed))
        self.d_DbHandler.commit()
        self.d_DbHandler.disconnectFromDb()
        return

import db_handler
import webapp2
from google.appengine.api import users
import logging


# ---------------------------------------------------------
# Permissions - returns what types of permissions the current user has
# --------------------------------------------------------
class Permissions():
    def __init__(self):
        self.p_DbHandler=db_handler.DbHandler()
        self.p_owner = ""
        self.p_walker = ""


# ---------------------------------------------------------
# input: email for user
# output: array of permissions where [0] is for walker, [1] is for owner
# --------------------------------------------------------
    def getPermissions(self, email):
        self.p_DbHandler.connectToDb()
        cursor=self.p_DbHandler.getCursor()
        cursor.execute("SELECT EXISTS (select w_email from dogWalker where w_email = %s) , EXISTS (select o_email from dogOwner where o_email = %s )", (email,email)) #checks the IAM of the current user
        user_records = cursor.fetchall()
        for user_record in user_records:
            self.p_walker = user_record[0]
            self.p_owner = user_record[1]
        self.p_DbHandler.disconnectFromDb()
        return [self.p_walker, self.p_owner]
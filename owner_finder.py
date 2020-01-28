import db_handler
import owner
from google.appengine.api import users
from datetime import datetime, date
import logging

# ---------------------------------------------------------
# Class to perform queries on Dog Owners from DB
# --------------------------------------------------------
class OwnerFinder(object):
    def __init__(self):
        self.o_DbHandler=db_handler.DbHandler()
        self.o_RetrievedOwnersList=[]
        
    # ---------------------------------------------------------
    # INPUT: city, minimal age, maximal age, email of user, viewall- weather to show all the results?
    # OUTPUT: a list of owners that have those parameters, pulled from the DB
    # --------------------------------------------------------
    def getAllOwners(self, city, minAge, maxAge, email, viewAll):
        self.o_DbHandler.connectToDb()
        cursor=self.o_DbHandler.getCursor()
        minAge = int(minAge)
        maxAge = int(maxAge) + 1
        minDate = self.getDateOfAge(minAge)
        maxDate = self.getDateOfAge(int(maxAge))
        sql_all = '''select distinct dogOwner.* , dog.d_name, dogWalker.w_email
                    from dogOwner 
                    join dog on dog.o_email = dogOwner.o_email
                    join trip on trip.dogID = dog.dogID
                    join dogWalker on dogWalker.w_email = trip.w_email
                    where dogWalker.w_email = '%s';''' % (email,)
                    
        sql_by_age = '''select distinct dogOwner.* , dog.d_name, dogWalker.w_email
                        from dogOwner 
                        join dog on dog.o_email = dogOwner.o_email
                        join trip on trip.dogID = dog.dogID
                        join dogWalker on dogWalker.w_email = trip.w_email
                        where dogWalker.w_email = '%s' and o_bday <= '%s' and o_bday >= '%s';''' % (email, minDate,maxDate)
                        
        sql_by_age_city = '''select distinct dogOwner.* , dog.d_name, dogWalker.w_email
                        from dogOwner 
                        join dog on dog.o_email = dogOwner.o_email
                        join trip on trip.dogID = dog.dogID
                        join dogWalker on dogWalker.w_email = trip.w_email
                        where dogWalker.w_email = '%s' and o_bday <= '%s' and o_bday >= '%s' and o_city = '%s';''' % (email, minDate,maxDate, city)
                        
        if city == "All Cities" or city == "All": #If the user chose "all cities, we show him all of the cities", and check by age
            cursor.execute(sql_by_age)
            logging.error(sql_by_age)
        elif viewAll == False: #if a user chose not to view all the results, and not all-cities, we show him results by age and city
            logging.error(sql_by_age_city)
            cursor.execute(sql_by_age_city)
        else: #if the user chose view all, we search for all owners that have buisness with this walker
            logging.error(sql_all)
            cursor.execute(sql_all)
        owner_records=cursor.fetchall()
        for owner_record in owner_records:
            current_owner = owner.Owner()
            current_owner.o_email = owner_record[0]
            current_owner.o_telephone = owner_record[1]
            current_owner.o_city = owner_record[2]
            current_owner.o_name = owner_record[3]
            current_owner.o_age = self.calculateAge(owner_record[4])
            self.o_RetrievedOwnersList.append(current_owner)
        self.o_DbHandler.disconnectFromDb()
        return self.o_RetrievedOwnersList

# ---------------------------------------------------------
# INPUT: age
# OUTPUT: date of birth if the birthday was today
# --------------------------------------------------------
    def getDateOfAge(self,age):
        d = datetime.today()
        d = d.replace(year=d.year-age)
        return d.strftime('%Y-%m-%d')
        
# ---------------------------------------------------------
# INPUT: date of birth
# OUTPUT: the age of the person
# --------------------------------------------------------
    def calculateAge(self,born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
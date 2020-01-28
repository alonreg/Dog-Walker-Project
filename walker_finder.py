import db_handler
import walker
from google.appengine.api import users
from datetime import timedelta, date, datetime
import logging
# ---------------------------------------------------------
# Class to perform queries on walker
# --------------------------------------------------------


class WalkerFinder(object):
    def __init__(self):
        self.w_DbHandler = db_handler.DbHandler()
        self.w_RetrievedWalkers = {}


# ---------------------------------------------------------
# Returns all walkers that answer to the query bellow
# --------------------------------------------------------

    def getAllWalkers(self, weekDays, startDate, endDate, dog_id, email):
        if startDate == "" or endDate == "":
            return {}
        self.w_DbHandler.connectToDb()
        cursor = self.w_DbHandler.getCursor()
        if weekDays != []:
            self.daterange(datetime.strptime(startDate, '%Y-%m-%d'), datetime.strptime(endDate, '%Y-%m-%d'), weekDays, email, dog_id, cursor) #creates a datarange iteration to run on
        logging.error(self.w_RetrievedWalkers)
        self.w_DbHandler.disconnectFromDb()
        return self.w_RetrievedWalkers

# ---------------------------------------------------------
# Iterates over a range of dates, starting from STARTDATE and ending at ENDDATE, for each one runs a query
# --------------------------------------------------------    
    def daterange(self, start, end, weekDaysFromUser, email, dog_id, cursor):
        delta = timedelta(days=1)
        week_days = ['su', 'mo', 'tu', 'we', 'th', 'fr', 'sa']
        while start <= end:
            if week_days[int(start.strftime('%w'))] == weekDaysFromUser[int(start.strftime('%w'))]:
                logging.error(start)
                self.w_RetrievedWalkers[start.strftime('%Y-%m-%d')] = [] #week_days[int(start.strftime('%w'))]
                self.queryDate(start, email, dog_id, cursor)
            start += delta
# ---------------------------------------------------------
# Runs a query on a specific date, checks weather the user
#  has enough dog capacity for this time, and gets the relevant data
# --------------------------------------------------------
    def queryDate(self, date, email, dog_id, cursor):
        
        sql_get_walkers = '''select dogWalker.w_email, dogWalker.w_telephone,dogWalker.w_name, week_day.price, week_day.day_name , breed.d_breed,  week_day.maxDogs
                        from dogWalker join week_day on dogWalker.w_email=week_day.w_email join breed on breed.w_email = dogWalker.w_email join dog on dog.dogID = %s
                        where breed.d_breed = (select dog.d_breed from dog where dogID = %s) and week_day.day_name = dayname('%s') and dogWalker.w_email IN 
                        (select distinct week_day.w_email
                        from week_day
                        where day_name LIKE dayname('%s'));''' % (dog_id, dog_id, date, date)
        logging.error(sql_get_walkers)                
        cursor.execute(sql_get_walkers)
        walker_records = cursor.fetchall()
        logging.error(date)
        date_list = self.w_RetrievedWalkers[date.strftime('%Y-%m-%d')]
        
        for walker_record in walker_records:
            current_walker = walker.Walker()
            logging.error(walker_record)
            current_walker.w_email = walker_record[0]
            current_walker.w_telephone = walker_record[1]
            current_walker.w_name = walker_record[2]
            current_walker.w_price = walker_record[3]
            current_trips = self.check_dog_capacity(date, current_walker.w_email, cursor)
            if current_trips ==-1 or current_trips < current_walker.w_price == walker_record[6]:
                date_list.append(current_walker)
            else:
                logging.error(current_walker.w_email)
                logging.error(walker_record[6])
        return self.w_RetrievedWalkers

# ---------------------------------------------------------
# Check if the user has enough dog capacity,
# wether he's taking too many dogs out
# --------------------------------------------------------
    def check_dog_capacity(self, date,email, cursor):
        
        sql_get_trips = '''select count(dogWalker.w_email)
                from dogWalker join trip on dogWalker.w_email = trip.w_email
                where trip.t_date = '%s' and dogWalker.w_email = '%s'
                group by dogWalker.w_email;''' % (date,email)
        cursor.execute(sql_get_trips)
        walker_records = cursor.fetchall()
        if walker_records:
            record = walker_records[0]
            return record[0]
        else:
            return -1 #we return -1 to indicate that this user doesn't have any trips
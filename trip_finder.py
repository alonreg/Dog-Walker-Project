import db_handler
import trip
from google.appengine.api import users
from datetime import datetime, date, timedelta #for working with time and date
import logging

# ---------------------------------------------------------
# Class to perform queries on trips 
# --------------------------------------------------------
class TripFinder(object):
    def __init__(self):
        self.t_DbHandler = db_handler.DbHandler()
        self.t_RetrievedTripsList = []


# ---------------------------------------------------------
# Returns all trips that answer to the query bellow
# --------------------------------------------------------
    def getAllTrips(self, email):
        self.t_DbHandler.connectToDb()
        cursor = self.t_DbHandler.getCursor()
        sql = '''select trip.dogID, t_date, dog.d_name, dog.d_breed, dog.d_age, trip.w_from_home
        from_home from trip join dog on dog.dogID = trip.dogID  
        where trip.w_email = '%s'; ''' % (email,)
        logging.error(sql)
        cursor.execute(sql)
        trip_records = cursor.fetchall()
        for trip_record in trip_records:
            current_trip = trip.Trip()
            current_trip.d_name = trip_record[2]
            current_trip.t_date = trip_record[1]
            current_trip.t_fromHome = 'Yes' if trip_record[5] == 1 else 'No' #if the value is 1, the user wants a trip from home

            current_trip.dogID = trip_record[0]
            current_trip.d_age = trip_record[4]
            current_trip.d_breed = trip_record[3]

            self.t_RetrievedTripsList.append(current_trip)
        self.t_DbHandler.disconnectFromDb()
        return self.t_RetrievedTripsList


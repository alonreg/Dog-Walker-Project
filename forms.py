import webapp2
from google.appengine.api import users
import logging
import jinja2
import os
import dog_finder
import dog
import walker
import owner
import datetime

# Load Jinja
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader
                                       (os.path.dirname(__file__)))

# ---------------------------------------------------------
# FORMS.PY handles all forms and inputs from forms 
# --------------------------------------------------------


# ---------------------------------------------------------
# walker data handles all the incoming walkers from the register walker page
# --------------------------------------------------------
class WalkerData(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()

        if self.request.get('telephone') == '': #check that telephone is not null
            parameters_for_template = {
                'message': 'Seems like you didn\'t set a phone number. Please go back, and try again.'}
            template = jinja_environment.get_template('error_page.html')
            self.response.write(template.render(parameters_for_template))
            return
        if user == None: #check that user is not null
            parameters_for_template = {
                'message': 'Seems like your\'e logged out of a Google account. Please login, and try again.'}
            template = jinja_environment.get_template('error_page.html')
            self.response.write(template.render(parameters_for_template))
            return
        if self.request.get('name') == None: #check that name is not null
            parameters_for_template = {
                'message': 'Seems like you didn\'t enter your name. Please go back, and try again.'}
            template = jinja_environment.get_template('error_page.html')
            self.response.write(template.render(parameters_for_template))
            return

        walker_data = walker.Walker()
        walker_data.w_email = str(user.email())
        walker_data.w_name = str(self.request.get('name'))
        walker_data.w_city = str(self.request.get('city'))
        walker_data.w_telephone = str(self.request.get('telephone'))

        walker_data.w_breeds = self.get_breeds()

        week_days_result = self.get_week_days()

        if week_days_result:
            walker_data.w_days = week_days_result[0]
            walker_data.w_dog_num = week_days_result[1]
            walker_data.w_price = week_days_result[2]
        else:
            parameters_for_template = {
                'message': 'Seems like you enter a wrong price or maximal dog number (they both have to be positive). Please go back, and try again.'}
            template = jinja_environment.get_template('error_page.html')
            self.response.write(template.render(parameters_for_template))
            return
        walker_data.insertToDb()
        self.redirect('/walker-home')

    
    
# ---------------------------------------------------------
#  returns all the week days where the walker is working, also adding
#  the price and max dogs for each day
# --------------------------------------------------------
    def get_week_days(self):
        days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
        working_days = []
        dog_num = {'sun': None, 'mon': None, 'tue': None,
                   'wed': None, 'thu': None, 'fri': None, 'sat': None}
        prices = {'sun': None, 'mon': None, 'tue': None,
                  'wed': None, 'thu': None, 'fri': None, 'sat': None}

        for day in days:
            if self.request.get(day) and self.request.get(day+'_num') > 0 and int(self.request.get(day+'_price')) >= 0:
                logging.error(int(self.request.get(day+'_price')))
                logging.error(int(self.request.get(day+'_num')))
                prices[day] = int(self.request.get(day+'_price'))
                dog_num[day] = int(self.request.get(day+'_num'))
                working_days.append(day)
            elif self.request.get(day) and self.request.get(day+'_num') <= 0 and int(self.request.get(day+'_price')) < 0:
                return None
            logging.error(int(self.request.get(day+'_price')))
            logging.error(int(self.request.get(day+'_num')))
        return [working_days, dog_num, prices]

# ---------------------------------------------------------
# returns the breeds which the walker works with
# --------------------------------------------------------
    def get_breeds(self):
        breeds = ["Poodle", "Chihuahua", "Husky", "Golden", "SnoopDog"]
        my_breeds = []
        for breed in breeds:
            if self.request.get(breed):
                my_breeds.append(breed)
        logging.error(my_breeds)
        return my_breeds


# ---------------------------------------------------------
# Owner data handles all the incoming data from the register owners page
# --------------------------------------------------------
class OwnerData(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if self.request.get('bday') != '': #make sure that the birthday exists
            bday = datetime.datetime.strptime(
                self.request.get('bday'), '%Y-%m-%d')
        else:
            parameters_for_template = {
                'message': 'Seems like you didn\'t set your birthday. Please go back, and try again.'}
            template = jinja_environment.get_template('error_page.html')
            self.response.write(template.render(parameters_for_template))
            return
        if bday > datetime.datetime.now(): #check that the birthday is not in the future
            parameters_for_template = {
                'message': 'Seems like your birthday is in the future. Please go back, and try again.'}
            template = jinja_environment.get_template('error_page.html')
            self.response.write(template.render(parameters_for_template))
            return
        if self.request.get('telephone') == '': #check if telephone is not null
            parameters_for_template = {
                'message': 'Seems like you didn\'t set a phone number. Please go back, and try again.'}
            template = jinja_environment.get_template('error_page.html')
            self.response.write(template.render(parameters_for_template))
            return
        if user == None: #check if user logged in
            parameters_for_template = {
                'message': 'Seems like your\'e logged out of a Google account. Please login, and try again.'}
            template = jinja_environment.get_template('error_page.html')
            self.response.write(template.render(parameters_for_template))
            return
        if self.request.get('name') == None: #check if the name is not null
            parameters_for_template = {
                'message': 'Seems like you didn\'t enter your name. Please go back, and try again.'}
            template = jinja_environment.get_template('error_page.html')
            self.response.write(template.render(parameters_for_template))
            return
        owner_data = owner.Owner()
        owner_data.o_name = str(self.request.get('name'))
        owner_data.o_email = str(user.email())
        owner_data.o_telephone = str(self.request.get('telephone'))
        owner_data.o_city = str(self.request.get('city'))
        owner_data.o_bday = bday
        owner_data.insertToDb()
        self.redirect('/owner-home')


# ---------------------------------------------------------
# walker data handles all the incoming dogs from the 'add dog' page
# --------------------------------------------------------
class DogData(webapp2.RequestHandler):
    def post(self):
        dog_data = dog.Dog()
        dog_data.d_o_email = users.get_current_user().email()
        dog_data.d_name = str(self.request.get('name'))
        dog_data.d_age = int(self.request.get('age'))
        dog_data.d_gender = str(self.request.get('gender'))
        dog_data.d_breed = str(self.request.get('breed'))
        dog_data.insertToDb()
        self.redirect('/owner-home')

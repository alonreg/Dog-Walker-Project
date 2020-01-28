# ------------------------------------------------------
# Dog Walker Website
# ------------------------------------------------------
# This website is designed to accomodate dog owners and
# dog walkers, and provide them with matching services.
# Using our website, dog owners can find dog walkers in their
# area, and save precious time on dog walking. Meanwhile, dog
# walkers can use this magnificent website to earn some extra cash,
# while riding the gig economy wave. We hope you enjoy our 
# service, and user experience.
# ------------------------------------------------------
# Author       - Alon Regensteiner, Maxim pomerantz
# Last updated - 26.01.2020
# ------------------------------------------------------


import webapp2
from google.appengine.api import users
import logging
import jinja2
import os
import dog_finder #Class to find all dogs of an owner
import dog #class that describes a dog
import forms #class for aggregating data from forms and inserting to DB
import permissions #class to retrieve a user's permissions (walker, owner, none)
from cities import Cities #class to hold all the supported cities in our app in one place
import owner_finder #class to find  owners
import walker_finder #class to find walkers
import trip_finder #class to find all trips of walker
import trip #class to handle a trip object

# Load Jinja
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader
                                       (os.path.dirname(__file__)))



# routing
#####################################################################################################


# ---------------------------------------------------------
# Login redirection - creates a google login form
# Handles /login
# --------------------------------------------------------
class Login(webapp2.RequestHandler):
    def get(self):
        self.redirect(users.create_login_url('/'))

# ---------------------------------------------------------
# Logout - creates a logout from google
# Handles /logout
# --------------------------------------------------------
class Logout(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect(users.create_logout_url('/'))
        else:
            self.redirect('/')

# ---------------------------------------------------------
# Root - redirects user according to user type
# Handles /
# --------------------------------------------------------
class Root(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            p_obj = permissions.Permissions()
            userTypes = p_obj.getPermissions(user.email())

            if userTypes[0] == 1 and userTypes[1] == 1:
                logging.error(userTypes[1])
                logging.error(userTypes[1])
                self.redirect('/walker-home')
            elif userTypes[0] == 1 and userTypes[1] == 0:
                logging.error('in walker')
                self.redirect('/walker-home')
            elif userTypes[0] == 0 and userTypes[1] == 1:
                logging.error('in walker')
                self.redirect('/owner-home')
            else:
                logging.error(  userTypes[0])
                self.redirect('/register')
        else:
            self.redirect('/splash-screen')

# ---------------------------------------------------------
# Splash screen - welcomes users, lets them log in
# Handles /splash-screen
# --------------------------------------------------------
class SplashScreen(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template(
            'splash_screen.html')  
        parameters_for_template = {}
        self.response.write(template.render(parameters_for_template))
        
# register
#####################################################################################################

# ---------------------------------------------------------
# Register Navigation - a screen to direct user to their wanted registeration process (walkers, owners)
# Handles /register
# --------------------------------------------------------
class RegisterNavigation(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logging.error(user.email())
        template = jinja_environment.get_template(
            'register_navigation.html') 
        parameters_for_template = {'user': user}
        self.response.write(template.render(parameters_for_template))

# ---------------------------------------------------------
# Register walker - register as a walker
# Handles /register-walker
# --------------------------------------------------------
class RegisterWalker(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        p_obj = permissions.Permissions()
        userTypes = p_obj.getPermissions(user.email())
        if userTypes[0] == 1:
            self.redirect('/walker-home')
            return
        template = jinja_environment.get_template(
            'register_walker.html')  
        cities_obj = Cities()
        my_cities = cities_obj.getCitiesFromDb()
        parameters_for_template = {'user': user, 'cities':  my_cities}
        self.response.write(template.render(parameters_for_template))

# ---------------------------------------------------------
# Register Owner - register as a dog owner
# Handles /register-owner
# --------------------------------------------------------
class RegisterOwner(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        p_obj = permissions.Permissions()
        userTypes = p_obj.getPermissions(user.email())
        if userTypes[1] == 1:
            self.redirect('/owner-home')
            return
        template = jinja_environment.get_template(
            'register_owner.html')  
        cities_obj = Cities()
        my_cities = cities_obj.getCitiesFromDb()
        parameters_for_template = {'user': user, 'cities': my_cities}
        self.response.write(template.render(parameters_for_template))

# ---------------------------------------------------------
# Add dog - lets user sign up their dog to the service
# Handles /register-dog
# --------------------------------------------------------        
class RegisterDog(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = jinja_environment.get_template(
            'register_dog.html')  
        parameters_for_template = {'user': user, 'breeds': ["Poodle","Chihuahua","Husky","Golden Retriever", "SnoopDog"]}
        self.response.write(template.render(parameters_for_template))
       

# website
#####################################################################################################

# ---------------------------------------------------------
# Walker Home Screen - show links to - view owners
# --------------------------------------------------------
class WalkerHome(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        parameters_for_template = {'user': user ,'list_of_dogs': []}
        template = jinja_environment.get_template(
            'walker_home.html')
        self.response.write(template.render(parameters_for_template))

# ---------------------------------------------------------
# Owner Home - show links to - Show status, login and logout
# Handles /owner-home
# --------------------------------------------------------
class OwnerHome(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        parameters_for_template = {'user': user ,'list_of_dogs': []}
        user = users.get_current_user()
        template = jinja_environment.get_template(
            'owner_home.html') 
        self.response.write(template.render(parameters_for_template))

# ---------------------------------------------------------
# Filter Walkers - Get walkers list according to parameters, shows all walkers
# Handles /filter-walkers
# --------------------------------------------------------
class FilterWalkers(webapp2.RequestHandler):
    def get(self):
        my_dog_finder = dog_finder.DogFinder()
        user = users.get_current_user()
        dogs = my_dog_finder.getAllDogs(user.email())
        p_obj = permissions.Permissions()
        userTypes = p_obj.getPermissions(user.email())
        if userTypes[1] != 1:
            parameters_for_template = {'message': 'You don\'t have permissions to this page. Please try again later'}
            template = jinja_environment.get_template('error_page.html')
            self.response.write(template.render(parameters_for_template))
        if len(dogs) == 0:
            parameters_for_template = {'message': 'You have to add dogs before scheduling a walker. Go back and try again.'}
            template = jinja_environment.get_template('error_page.html')
            self.response.write(template.render(parameters_for_template))
        else:
            parameters_for_template = {'user': user ,'dogs': dogs, 'walkers': {},"dogID":""}
            template = jinja_environment.get_template('filter_walkers.html')
            self.response.write(template.render(parameters_for_template))

# ---------------------------------------------------------
# Filter owners - Get owners list according to parameters, shows all owners
# Handles /filter-owners
# --------------------------------------------------------
class FilterWalkersResults(webapp2.RequestHandler):
    def get(self):
        my_dog_finder = dog_finder.DogFinder()
        user = users.get_current_user()
        dogs = my_dog_finder.getAllDogs(user.email())
        p_obj = permissions.Permissions()
        userTypes = p_obj.getPermissions(user.email())
        if userTypes[1] != 1:
            parameters_for_template = {'message': 'You don\'t have permissions to this page. Please try again later'}
            template = jinja_environment.get_template('error_page.html')
            self.response.write(template.render(parameters_for_template))
        if len(dogs) == 0:
            parameters_for_template = {'message': 'You have to add dogs before scheduling a walker. Go back and try again.'}
            template = jinja_environment.get_template('error_page.html')
            self.response.write(template.render(parameters_for_template))
        else:
            weekDays = [self.request.get('su'),self.request.get('mo'),self.request.get('tu'),self.request.get('we'),self.request.get('th'),self.request.get('fr'),self.request.get('sa')]
            logging.error(self.request.get('startDate'))
            startDate = self.request.get('startDate')
            endDate = self.request.get('endDate')
            dog_id = self.request.get('dog')
            
            my_walker_finder = walker_finder.WalkerFinder()
            walkers = my_walker_finder.getAllWalkers(weekDays, startDate, endDate, dog_id, user.email())
            logging.error(walkers)
            parameters_for_template = {'user': user ,'dogs': dogs, "dates":walkers, "dogID":dog_id}
            template = jinja_environment.get_template('filter_walkers.html')
            self.response.write(template.render(parameters_for_template))
            
            
# ---------------------------------------------------------
# View Trips- Get Trips list according to walker email
# Handles /trips
# --------------------------------------------------------
class Trips(webapp2.RequestHandler):
    def get(self):
        my_trip_finder = trip_finder.TripFinder()
        user = users.get_current_user()
        trips = my_trip_finder.getAllTrips(user.email())
        p_obj = permissions.Permissions()
        userTypes = p_obj.getPermissions(user.email())
        if userTypes[0] != 1:
            parameters_for_template = {'message': 'You don\'t have permissions to this page. Please try again later'}
            template = jinja_environment.get_template('error_page.html')
            self.response.write(template.render(parameters_for_template))
        if len(trips) == 0:
            parameters_for_template = {'message': 'Oops! You dont have any trips yet!'}
            template = jinja_environment.get_template('error_page.html')
            self.response.write(template.render(parameters_for_template))
        else:
            parameters_for_template = {'user': user ,'trips': trips}
            template = jinja_environment.get_template('my_trips.html')
            self.response.write(template.render(parameters_for_template))
            
# ---------------------------------------------------------
# Filter Walkers Result page - Same as the last one but twiked to show the results instead of all the walkers
# Handles /filter-ownerss/*
# --------------------------------------------------------            
class FilterOwners(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        p_obj = permissions.Permissions()
        userTypes = p_obj.getPermissions(user.email())
        if userTypes[0] != 1: #UPDATE TO CHECK IN DB
            parameters_for_template = {'message': 'You don\'t have permissions to this page. Please try again later'}
            template = jinja_environment.get_template('error_page.html')
            self.response.write(template.render(parameters_for_template))
        else:
            cities_obj = Cities()
            my_owner_finder = owner_finder.OwnerFinder()
            my_cities = cities_obj.getCitiesFromDb()
            owners = my_owner_finder.getAllOwners('', 0, 0, user.email(),True)
            parameters_for_template = {'user': user ,'cities': my_cities, 'owners': owners}
            template = jinja_environment.get_template('filter_owners.html')
            self.response.write(template.render(parameters_for_template))
            
# ---------------------------------------------------------
# Filter Walkers Result page - Same as the last one but twiked to show the results instead of all the walkers
# Handles /filter-walkers/*
# --------------------------------------------------------
class FilterOwnersResults(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        p_obj = permissions.Permissions()
        userTypes = p_obj.getPermissions(user.email())
        if userTypes[0] != 1:
            parameters_for_template = {'message': 'You don\'t have permissions to this page. Please try again later'}
            template = jinja_environment.get_template('error_page.html')
            self.response.write(template.render(parameters_for_template))
        else:
            city = self.request.get('city')
            minAge = self.request.get('minAge')
            maxAge = self.request.get('maxAge')
            viewAll = True if self.request.get('all') == 'on' else False
            logging.error(viewAll)
            my_owner_finder = owner_finder.OwnerFinder()
            if viewAll:
                owners = my_owner_finder.getAllOwners('', 0, 0, user.email(),viewAll)
            else:
                owners = my_owner_finder.getAllOwners(city, minAge, maxAge, user.email(),viewAll)

        logging.error(owners)
        cities_obj = Cities()
        my_cities = cities_obj.getCitiesFromDb()
        my_cities.insert(0,'All Cities')
        parameters_for_template = {'cities': my_cities,'user': user,'owners': owners}
        template = jinja_environment.get_template('filter_owners.html')
        self.response.write(template.render(parameters_for_template))
        
        
# ---------------------------------------------------------
# Schedules a dog walking session with a dog walker
# Handles /schedule.*
# --------------------------------------------------------
class Schedule(webapp2.RequestHandler):
    def get(self):
        my_trip = trip.Trip()
        my_trip.t_date = self.request.get('date')
        my_trip.w_email = self.request.get('w_email')
        my_trip.dogID = self.request.get('dogID')
        my_trip.insertToDb()
        user = users.get_current_user()
        if user: 
            parameters_for_template = {"user":user}
            template = jinja_environment.get_template('/owner_home.html')
            self.response.write(template.render(parameters_for_template))

# ---------------------------------------------------------
# Abous Us - Learn more about whose behind this cool service
# Handles /about-us
# --------------------------------------------------------
class AboutUs(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template(
            'about_us.html')  # sign up for dog walker
        parameters_for_template = {}
        self.response.write(template.render(parameters_for_template))

# --------------------------------------------------
# Routing
# --------
# '/' - Main screen, directs you to your correct home screen according to your user type
# '/splash-screen' - Unregistered users start their journey here, where we direct them to the google signin
# '/register' - navigation for registering either to be a dog walker or a dog owner
# '/register-walker' - dog walker registeration
# '/register-owner' - dog owner registeration
# '/register-dog' - add a new dog to an owner
# '/walker-home' - the main page for a dog walker
# '/owner-home' - the main page for a dog owner
# '/login' - directs you to the google login
# '/logout' - directs you to the google logout
# '/submit-walker' - submit the walker registeration form
# '/submit-dog' - submit the dog addition form
# '/filter-owners' - get specific dog owners / clients
# '/filter-walkers' - get specific dog walkers and schedule 
# '/submit-owner' - submit the owner registeration form
# '/submit-owner-filter.*' - see the results of the 'view owners' screen
# '/submit-walker-filter.*' - see the results of the 'view walkers' screen
# '/trips' - shows a walker all of his trips
# '/Schedule' - Set an apppointment with dog walker for your dog
# '/about-us', AboutUs - Learn more about our buisness and who runs it. Meow.

# --------------------------------------------------
app = webapp2.WSGIApplication([('/', Root),
                               ('/splash-screen', SplashScreen),
                               ('/register', RegisterNavigation),
                               ('/register-walker', RegisterWalker),
                               ('/register-owner', RegisterOwner),
                               ('/register-dog', RegisterDog),
                               ('/walker-home', WalkerHome),
                               ('/owner-home', OwnerHome),
                               #('/show-walkers', ShowWalkers),
                               #('/show-owners', ShowOwners),
                               #('/show-dogs', ShowDogs),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/submit-walker', forms.WalkerData),
                               ('/submit-dog', forms.DogData),
                               ('/filter-owners', FilterOwners),
                               ('/filter-walkers', FilterWalkers),
                               ('/submit-owner', forms.OwnerData),
                               ('/submit-owner-filter.*', FilterOwnersResults),
                               ('/submit-walker-filter.*', FilterWalkersResults),
                               ('/trips', Trips),
                               ('/schedule.*', Schedule),
                               ('/about-us', AboutUs)
                               ],
                              debug=True)
 
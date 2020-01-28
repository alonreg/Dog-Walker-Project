import db_handler
import dog


# ---------------------------------------------------------
# Class to perform queries on Dog, and pull dogs from DB
# --------------------------------------------------------
class DogFinder():
    def __init__(self):
        self.d_DbHandler=db_handler.DbHandler()
        self.d_RetrievedDog = dog.Dog()
        self.d_RetrievedDogsList=[]

# ---------------------------------------------------------
# INPUT: user email
# OUTPUT: all the dogs of this user
# --------------------------------------------------------
    def getAllDogs(self, email):
        self.d_DbHandler.connectToDb()
        cursor=self.d_DbHandler.getCursor()
        cursor.execute("SELECT * FROM dog WHERE o_email LIKE %s;", (email,))
        dog_records=cursor.fetchall()
        for dog_record in dog_records:
            current_dog = dog.Dog()
            current_dog.d_id = dog_record[0]
            current_dog.d_name = dog_record[2]
            current_dog.d_ownerEmail = dog_record[1]
            self.d_RetrievedDogsList.append(current_dog)
        self.d_DbHandler.disconnectFromDb()
        return self.d_RetrievedDogsList
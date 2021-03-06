from pymodm import connect
from pymodm import MongoModel, fields
import datetime
import numpy as np

connect("mongodb://localhost:27017/bme590") # connect to database
#connect("mongodb://vcm-3738.vm.duke.edu:27017/bme590")
class User(MongoModel):

    """ class creates user for Mongo Database

    :param email: email of user
    :param age: age of user
    :param heart_rate: heart rate of user
    :heart rate times: prints time of entry
    """
    email = fields.EmailField(primary_key=True)
    age = fields.IntegerField()
    heart_rate = fields.ListField(field=fields.IntegerField())
    heart_rate_times = fields.ListField()

def user_exist(email):

    """ function to check if user exists, if exist returns true

    :param email: email of user
    :returns real_state: state of user id, true= exists
    :raises ValueError: if user does not exist
    """

    try:
        exist = User.objects.raw({"_id": email}).first()
        print("user exists")
        real_state = True
    except:
        print("User DNE")
        real_state = False

    return real_state


def create_new_user(email, age, heart_rate, time):

    """ function to create new user and save entry in database

    :param email: email of user
    :param age: user age
    :param heart_rate: heart rate of user
    :param time: timestamps of entries
    """

    u = User(email, age, [],[])
    u.heart_rate.append(heart_rate)
    u.heart_rate_times.append(time)
    u.save()
    print('user created')

def add_heart_rate(email, heart_rate, time):
    
    """function to append data to existing user and saves in database
 
    :param email: email of user
    :param heart_rate: added heart rate of user
    :param time: added timestamp of entry
    """

    u = User.objects.raw({"_id": email}).first() # Get the first user where _id=email
    u.heart_rate.append(heart_rate) # Append the heart_rate to the user's list of heart rates
    u.heart_rate_times.append(time) # append the current time to the user's list of heart rate times
    u.save() # save the user to the database

def return_all_hr(email):
   
    """function returns all heart rates

    :param email: user email
    :returns u.heart_rate: list of heart rates
    """
 
    u = User.objects.raw({"_id": email}).first()
    return u.heart_rate
 
def return_all_times(email):

    """ function returns list of timestamps

    :param email: user email
    :returns u.heart_rate_times: list of heart rate timestamps
    """
    u = User.objects.raw({"_id": email}).first() 
    return u.heart_rate_times

def return_user_age(email):
    """ function returns users age

    :param email: user email
    :returns u.age: user age
    """
    u = User.objects.raw({"_id": email}).first()
    return u.age
 
def return_avg_hr(email, heart_rate_values):
 
    """ function returns average of all heart rates
 
    :param email: user email
    :param heart_rate_values: list of heart rate values
    :returns hr_avg: returns hr avg for all heart rate values
    """
 
    hr_avg = np.mean(heart_rate_values)
    return hr_avg    
    

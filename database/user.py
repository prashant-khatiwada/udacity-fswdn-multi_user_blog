from google.appengine.ext import db
from utils import *


class User(db.Model):
    firstname = db.StringProperty(required=True)
    lastname = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    # decorator funciton to call user via user_id key
    def by_id(cls, user_id):
        # Alternate method is to make a key and then call it
        # user_key = db.Key.from_path('User', int(user_id), parent=users_key())
        # post = db.get(user_key)
        return User.get_by_id(user_id, parent=users_key())

    @classmethod  # THIS MAKES THE MEDTHOD STATIC
    # decorator funciton - to call user via user_name key
    # This is the third method to access the database
    def by_name(cls, name):
        # return User.get_by_id(name, parent=users_key())
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    # Takes in multiple object and creates a user object
    # Doesn't actually stores in the Database, just creates it
    def register(cls, firstname, lastname, name, pw, email=None):
        # Creates a password Hash first
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(),
                    firstname=firstname,
                    lastname=lastname,
                    name=name,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    # For Login Funciton
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u

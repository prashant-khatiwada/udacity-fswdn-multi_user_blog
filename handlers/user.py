from utils import *
from google.appengine.ext import db
from handlers.handler import Handler
from database.user import User
from database.post import Post
from database.comment import Comment

# Signup Handler


class Signup(Handler):

    def get(self):
        # Render Signup FORM
        self.render("signup.html")

    def post(self):
        have_error = False
        firstname = self.request.get('firstname')
        lastname = self.request.get('lastname')
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username=username,
                      email=email)

        # Check to see if the input is valid or not, and present error
        if not valid_firstname(firstname):
            params['error_firstname'] = "That's not a valid Name."
            have_error = True

        if not valid_lastname(lastname):
            params['error_lastname'] = "That's not a valid Last Name."
            have_error = True

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('signup.html', **params)
        else:
            # look up if the username already exists
            # alternate code??## = User.get_by_id(user, parent=users_key())
            u = User.by_name(username)
            if u:
                message = 'Username already exists, choose different username'
                self.render('signup.html', error_username=message)
            else:
                # Resister the User
                u = User.register(
                    firstname,
                    lastname,
                    username,
                    password,
                    email)
                # Put the user Object
                u.put()
                # Call the Login Function - - Sets the Cookie function
                self.login(u)
                self.redirect('/welcome')


# Login Handler
class Login(Handler):

    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/welcome')
        else:
            msg = 'Invalid Login'
            self.render('login.html', error=msg)

# Logout Handler


class Logout(Handler):

    def get(self):
        self.logout()
        self.redirect('/')


class Welcome(Handler):

    def get(self):
        # Checks if Self.User is present, send it to front page
        if self.user:
            self.render('welcome.html', username=self.user.name)
        else:
            # Else, send it to signup
            self.redirect('/signup')

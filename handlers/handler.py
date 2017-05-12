import os
import webapp2
from utils import *
from database.user import User


class Handler(webapp2.RequestHandler):
    # easy and shorter method to write out.

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

        # takes in parameters (dictionary within it) to put it in template
    def render_str(self, template, **params):
        return render_str(template, **params)

    # calls write and render_str to print out the template
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    # More funcitons for user properties
    # Funtion sets a cookie, name and a value, and stores in a cookie
    # Cookie header name - Set-Cookie
    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        # one can also inclusde expire time [not here]
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    # Reads for the cookie
    # give it a name, if the cookie exists, it returns
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    # Function for Login
    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    # Function for Logout
    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    # Special function [Important]
    # This checks everytime you have a request
    # Checks for user cookie called user-id, if it exists, it stores
    def initialize(self, *a, **kw):
        # Runs on all the request, everytime
        webapp2.RequestHandler.initialize(self, *a, **kw)
        # checks for user cookie - called 'user_id'
        uid = self.read_secure_cookie('user_id')
        # If the cookie is there, store it in self.user as an object
        # Why?
        self.user = uid and User.by_id(int(uid))

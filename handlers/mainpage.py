from google.appengine.ext import db
from handlers.handler import Handler
from database.user import User
from utils import *


# MainPage Handler
class MainPage(Handler):

    def get(self):
        self.render("front.html")

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

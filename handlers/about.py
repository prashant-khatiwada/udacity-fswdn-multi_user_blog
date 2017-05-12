from google.appengine.ext import db
from handlers.handler import Handler
from database.user import User
from utils import *


class About(Handler):

    def get(self):
        if self.user:
            x = "ogout"
            self.render('about.html', userstatus=x)
        else:
            x = "ogin"
            self.render('about.html', userstatus=x)

from utils import *
from google.appengine.ext import db
from handlers.handler import Handler
from database.user import User


class PostPage(Handler):

    def get(self, post_id):
        """ First make a key to the specific post
        @post_id - passed in from the URL as a string
        @parent=blog_key - since we created a parent structure
        Second - look up particular item through db.get and store it in "post"
        """
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if post:
            self.render("permalink.html", post=post)
        else:
            self.error(404)
            return

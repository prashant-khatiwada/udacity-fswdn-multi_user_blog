from google.appengine.ext import db
from utils import *


class Comment(db.Model):
    author = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    postid = db.StringProperty(required=True)
    created_time = db.DateTimeProperty(auto_now_add=True)
    modified_time = db.DateTimeProperty(auto_now=True)

    def render(self):
        self.__render_text = self.content.replace('\n', '<br>')
        return render_str("comment.html", c=self)

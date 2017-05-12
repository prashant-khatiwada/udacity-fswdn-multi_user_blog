from google.appengine.ext import db
from utils import *
from database.user import User


class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created_time = db.DateTimeProperty(auto_now_add=True)
    modified_time = db.DateTimeProperty(auto_now=True)
    # Extra Entities
    author = db.StringProperty()
    like_count = db.IntegerProperty(default=0)
    # Array containing all users who have liked a post
    user_like = db.StringListProperty()

    def render(self):
        # automated creation of new lines on content
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p=self)

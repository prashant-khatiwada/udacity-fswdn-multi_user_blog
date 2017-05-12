from utils import *
from google.appengine.ext import db
from handlers.handler import Handler
from database.user import User
from database.post import Post
from database.comment import Comment


class LikePost(Handler):

    def post(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)

            if not post:
                self.error(404)
                return

            # User Authorization Check
            if self.user.name != post.author:
                if self.user.name in post.user_like:
                    # self.write("you can only like a post once")
                    post.user_like.remove(self.user.name)
                    post.like_count -= 1
                    post.put()
                    time.sleep(0.2)
                    self.redirect('/blog/postcomment/%s' % post_id)
                else:
                    post.user_like.append(self.user.name)
                    post.like_count += 1
                    post.put()
                    # Putting a Time Delay in Python Script
                    time.sleep(0.2)
                    self.redirect('/blog/postcomment/%s' % post_id)
            if self.user.name == post.author:
                self.write("You cannot like your own post.")

        else:
            self.redirect("/login")

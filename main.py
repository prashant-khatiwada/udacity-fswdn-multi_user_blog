
import os
import re
from string import letters
import random
import hmac
import hashlib
import webapp2
import jinja2
import time

from utils import *
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)


# Database
from database.user import User
from database.post import Post
from database.comment import Comment


# General Class for Handling page/post
from handlers.handler import Handler
from handlers.mainpage import MainPage
from handlers.about import About

# Handlers Related to Post
from handlers.post import PostPage
from handlers.blog import BlogFront
from handlers.blog import NewPost
from handlers.blog import EditPost
from handlers.blog import DeletePost

# Handlers Related to Like/s
from handlers.like import LikePost


# Handlers Related to Comment/s
from handlers.comment import PostComment
from handlers.comment import EditComment


# User Signup, Login and Logout
from handlers.user import Signup
from handlers.user import Login
from handlers.user import Logout
from handlers.user import Welcome


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/about', About),
                               # User Login and Signup
                               ('/signup', Signup),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/welcome', Welcome),
                               # Blog Related
                               ('/blog/?', BlogFront),
                               ('/blog/editpost/([0-9]+)', EditPost),
                               ('/blog/deletepost/([0-9]+)', DeletePost),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               # Blog Related Extra Features
                               ('/blog/([0-9]+)/like', LikePost),
                               ('/blog/postcomment/([0-9]+)', PostComment),
                               ('/blog/editcomment/([0-9]+)', EditComment),
                               ], debug=True)

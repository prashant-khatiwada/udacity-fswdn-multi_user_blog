import os
import re
from string import letters
import random
import hmac
import hashlib
import webapp2
import jinja2
import time

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)

# User Validation
FIRST_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")


def valid_firstname(firstname):
    return firstname and FIRST_RE.match(firstname)

LAST_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")


def valid_lastname(lastname):
    return lastname and LAST_RE.match(lastname)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")


def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")


def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')


def valid_email(email):
    return not email or EMAIL_RE.match(email)


# Solution for multiple blog groups, or multiple user group


def users_key(group='default'):
    """Creates the Ancestral element of the database to store user in groups"""
    return db.Key.from_path('users', group)


def blog_key(name='default'):
    """function to store data within a parent (for multiple blog function)"""
    return db.Key.from_path('blogs', name)

# Creating Global funtions


def render_str(template, **params):
    """defining global render_str that takes in global params and template"""
    t = jinja_env.get_template(template)
    return t.render(params)


def render_post(response, post):
    """defining how post is rendered with subject and content"""
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

# User Related Security
"""creating a secret text (Usually not kept in the same file)"""
secret = 'du.Udslkjfd(98273klksdjf_)sdlkfsdf0ksjdfsdf)ssflk99'


def make_salt(length=5):
    """function to make salt (makes a string of five letters)"""
    return ''.join(random.choice
                   (letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    """takes in username, password, and salt, and returns (salt, hash version of all 3)"""
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, password, h):
    # Taking Hash from the Database
    salt = h.split(',')[0]
    # Matching user input
    return h == make_pw_hash(name, password, salt)


def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())


def check_secure_val(secure_val):
    # first split the string(secure_val) and take the first fragment
    val = secure_val.split('|')[0]
    # compare
    if secure_val == make_secure_val(val):
        return val

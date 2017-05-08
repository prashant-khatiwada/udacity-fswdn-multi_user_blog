
import os
import re
from string import letters

import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
	loader = jinja2.FileSystemLoader(template_dir),
    autoescape = True)

# defining global render_str that takes in global params and template
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

# Class for Handling page/post write and rendering
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

# defining how post is rendered with subject and content
def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

### MainPage and About
class MainPage(Handler):
  def get(self):
      self.render("front.html")

class About(Handler):
	def get(self):
		self.render("about.html")

### Database Related Stuff
# Blog Defination and Class
# function to store data within a parent (for multiple blog function)
def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

### defining different database entities and its property

# Database for Blog Post 
class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created_time = db.DateTimeProperty(auto_now_add = True)
    modified_time = db.DateTimeProperty(auto_now = True)

    def render(self):
        # automated creation of new lines on content
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)

### Blog Pages, Post and NewPost
# Class for Blog Front Page which shows given number of blog entry
class BlogFront(Handler):
    def get(self):
        posts = db.GqlQuery(
        	"select * from Post order by created_time desc limit 5")
        self.render('blog.html', posts = posts)

# Class for Posting a Blog Entry (Handler for rendering post)
class PostPage(Handler):
    def get(self, post_id):
        """ First make a key to the specific post
        	 @post_id - passed in from the URL as a string
        	 @parent=blog_key - since we created a parent structure
        	 Second - we look up a particular item through db.get and store it in "post"
        """
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if post:
        	self.render("permalink.html", post = post)
        else:
            self.error(404)
            return

        

# Handler Class for Handling New Post
class NewPost(Handler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(
            	parent = blog_key(), 
            	subject = subject, 
            	content = content)
            p.put()

            #making a string that identifies each post
            post_link_store = str(p.key().id())
            self.redirect('/blog/%s' % post_link_store)
        else:
            error = "Subject and Content, please!"
            self.render(
            	"newpost.html", 
            	subject=subject, 
            	content=content, 
            	error=error)

# Handler Class for Editing Specific Post
class EditPost(Handler):
    def get(self, post_id):
    	### Something similar to def(get) from PostPage 
    	key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if post:
        	self.render("editpost.html", post = post)
        else:
            self.error(404)
            return

    def post(self, post_id):
        subject = self.request.get('subject')
        content = self.request.get('content')
    
        if "update" in self.request.POST:
            if subject and content:
                # make key that retreives the entity/row from the Database
                update_value = Post.get_by_id(int(post_id), parent=blog_key())
                if update_value:
                    # modifying the properties of the entity
                    update_value.subject = subject
                    update_value.content = content
                    # storing it back
                    update_value.put()
                    # redirecting to the newly updated page
                    self.redirect('/blog/%s' % str(update_value.key().id()))
                else:
                    return self.error(404)
            else:
                error = "Update your subject and content, please"
                key = db.Key.from_path('Post', int(post_id), parent=blog_key())
                post = db.get(key)
                self.render("editpost.html", post = post)
        if "cancel" in self.request.POST:
            update_value = Post.get_by_id(int(post_id), parent=blog_key())   
            self.redirect('/blog/%s' % str(update_value.key().id()))


# Handler Class for Deleting Specific Post
class DeletePost(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if post:
            self.render("deletepost.html", post = post)
        else:
            self.error(404)
            return

    def post(self, post_id):
        if "delete-post" in self.request.POST:
            delete_value = Post.get_by_id(int(post_id), parent=blog_key())
            if delete_value:
                delete_value.delete()
                return self.redirect("/blog")
            else:
                return self.error(404)

        if "cancel-delete" in self.request.POST:
            return self.redirect("/blog")



### User Validation
# Valid Username
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)
# Valid Password
PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)
# Valif Email
EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)


### User Related - signup, login, and welcome screen
class Signup(Handler):

    def get(self):
        self.render("signup.html")

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
                      email = email)

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
            self.redirect('welcome?username=' + username)

class Welcome(Handler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/signup')

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/about', About),
                               # User Login and Signup
                               ('/signup', Signup),
                               # Blog Related
                               ('/welcome', Welcome),
                               ('/blog/?', BlogFront),
                               ('/blog/editpost/([0-9]+)', EditPost),
                               ('/blog/deletepost/([0-9]+)', DeletePost),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ],debug=True)


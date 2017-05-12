from utils import *
from google.appengine.ext import db
from handlers.handler import Handler
from database.user import User
from database.post import Post
from database.comment import Comment


class BlogFront(Handler):

    def get(self):
        # Checks if Self.User is present, send it to front page
        if self.user:
            posts = db.GqlQuery(
                "select * from Post order by created_time desc limit 10")
            self.render('blog.html', posts=posts, username=self.user.firstname)
        else:
            # Else, send it to signup
            self.redirect('/login')


class NewPost(Handler):

    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):

        author = self.user.name
        subject = self.request.get('subject')
        content = self.request.get('content')
        user_like = []

        # User Authorization Check for Frist Time
        if self.user:
            self.render("newpost.html")
            if subject and content:
                p = Post(
                    parent=blog_key(),
                    subject=subject,
                    content=content,
                    author=author)
                p.put()

                # making a string that identifies each post
                post_link_store = str(p.key().id())
                self.redirect('/blog/%s' % post_link_store)
            else:
                error = "Subject and Content, please!"
                self.render(
                    "newpost.html",
                    subject=subject,
                    content=content,
                    error=error)
        else:
            self.redirect("/login")


class EditPost(Handler):

    def get(self, post_id):
        if self.user:
            # Something similar to def(get) from PostPage
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            if self.user.name == post.author:
                if post:
                    self.render("editpost.html", post=post)
                else:
                    self.error(404)
                    return
            else:
                self.write("You cannot Edit other User's posts!")
        else:
            return self.redirect('/login')

    def post(self, post_id):
        if not self.user:
            return self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        # User Authorization Check
        if self.user.name == post.author:
            if "update" in self.request.POST:
                if subject and content:
                    # make key that retreives the entity/row from the Database
                    update_value = Post.get_by_id(
                        int(post_id), parent=blog_key())
                    if update_value:
                        # modifying the properties of the entity
                        update_value.subject = subject
                        update_value.content = content
                        # storing it back
                        update_value.put()
                        # redirecting to the newly updated page
                        self.redirect('/blog/%s' %
                                      str(update_value.key().id()))
                    else:
                        return self.error(404)
                else:
                    error = "Update your subject and content, please"
                    key = db.Key.from_path(
                        'Post', int(post_id), parent=blog_key())
                    post = db.get(key)
                    self.render("editpost.html", post=post)
            if "cancel" in self.request.POST:
                update_value = Post.get_by_id(int(post_id), parent=blog_key())
                self.redirect('/blog/%s' % str(update_value.key().id()))
        else:
            self.write("You cannot Edit other User's posts!")


class DeletePost(Handler):

    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            if self.user.name == post.author:
                if post:
                    self.render("deletepost.html", post=post)
                else:
                    self.error(404)
                    return
            else:
                self.write("You cannot Delete other User's posts!")
        else:
            return self.redirect('/login')

    def post(self, post_id):
        # User Login Check
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            # Author Check
            if self.user.name == post.author:
                # Post Check
                if post:
                    if "delete-post" in self.request.POST:
                        delete_value = Post.get_by_id(
                            int(post_id), parent=blog_key())
                        if delete_value:
                            delete_value.delete()
                            time.sleep(0.2)
                            return self.redirect("/blog")
                        else:
                            return self.error(404)
                    if "cancel-delete" in self.request.POST:
                        return self.redirect("/blog")
                else:
                    self.error(404)
                    return
            else:
                self.write("You cannot Delete other User's posts!")
        else:
            return self.redirect('/login')

from utils import *
from google.appengine.ext import db
from handlers.handler import Handler
from database.user import User
from database.post import Post
from database.comment import Comment


class PostComment(Handler):

    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)

            if not post:
                return self.error(404)

            comments = db.GqlQuery(
                "SELECT * FROM Comment WHERE postid =:1", str(post_id)
            )
            self.render(
                "postcomment.html",
                post=post,
                comments=comments
            )
        else:
            self.redirect('/login')

    def post(self, post_id):
        if not self.user:
            return self.redirect('/blog')

        if "submit" in self.request.POST:
            content = self.request.get('content')
            author = self.user.name

            if content:
                c = Comment(
                    postid=post_id,
                    content=content,
                    author=author
                )
                c.put()
                time.sleep(0.1)
                return self.redirect('/blog/postcomment/%s' % post_id)
        if "cancel" in self.request.POST:
            return self.redirect("/blog/%s" % str(post_id))

# Comment Edit and Deleted Handler


class EditComment(Handler):

    def get(self, comment_id):
        if self.user:
            key = db.Key.from_path('Comment', int(comment_id))
            comment = db.get(key)
            if not comment:
                return self.error(404)

            if self.user.name == comment.author:
                self.render("editcomment.html", comment=comment)
            else:
                self.write("You can't edit other User's comments!")
        else:
            self.redirect("/login")

    def post(self, comment_id):
        if not self.user:
            return self.redirect("/blog")

        content = self.request.get('content')
        commentVal = Comment.get_by_id(int(comment_id))
        key = db.Key.from_path('Comment', int(comment_id))
        comment = db.get(key)
        # User Authorization Check
        if self.user.name == comment.author:
                # Update Comment
            if "update" in self.request.POST:
                if content:
                    commentVal.content = content
                    commentVal.put()
                    time.sleep(0.1)
                    return self.redirect(
                        "/blog/postcomment/%s" % str(commentVal.postid)
                    )
            # Delete Comment
            if "delete" in self.request.POST:
                if content:
                    commentVal.content = content
                    commentVal.delete()
                    time.sleep(0.1)
                    return self.redirect(
                        "/blog/postcomment/%s" % str(commentVal.postid)
                    )
            # Cancel Comment Editiong/Deleteing
            if "cancel" in self.request.POST:
                if content:
                    time.sleep(0.1)
                    return self.redirect(
                        "/blog/postcomment/%s" % str(commentVal.postid)
                    )
        else:
            self.write("You can't edit other User's comments!")

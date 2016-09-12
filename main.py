import webapp2
import cgi
import jinja2
import os
import re
from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape=True)
# Using autoescape so I don't have to manually do CGI escape

class Post(db.Model): #This is where I am defining the Post (database).
    title = db.StringProperty(required = True)
    post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
    """ A base RequestHandler class for the site.
        The other handlers inherit form this one.
    """
    def renderError(self, error_code):
        """ Sends an HTTP error code and a generic "oops!" message to the client. """
        self.error(error_code)
        self.response.write("Oops! Something went wrong.")

class Index(Handler):
    def get(self):
        welcome_message = "Welcome! But you need to visit the " + "<a href='/blog'>blog</a>" + " page!"
        self.response.write(welcome_message)

class MainHandler(Handler):
    """ Handles request to the main page of the blog. So '/blog' page
    """
    def get(self):
        #posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")
        t = jinja_env.get_template("frontpage.html")
        response = t.render()#posts = posts)
        self.response.write(response)

class NewEntry(Handler):
    """ Handles request to the new post writing of the blog. So '/blog/newpost' page.
    """

    def get(self):
        t = jinja_env.get_template("newpost.html")
        response = t.render()
        self.response.write(response)

    def post(self):
        title = self.request.get("title")
        post = self.request.get("post")

        if title and post:
            new_entry = Post(title = title, post = post)
            new_entry.put()
            self.redirect('/blog/%s' % str(new_entry.key().id()))
        else:
            error = "be sure to enter title and post!"
            t = jinja_env.get_template("newpost.html")
            response = t.render(title = title, post = post, error = error)
            self.response.write(response)

class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id):
        self.response.write(id)

app = webapp2.WSGIApplication([
    ('/',Index),
    ('/blog', MainHandler),
    ('/blog/newpost', NewEntry), webapp2.Route('/blog/<id:\d+>', ViewPostHandler)],
    debug=True)

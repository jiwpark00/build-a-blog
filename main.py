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
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

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
        unwatched_movies = db.GqlQuery("SELECT * FROM Post where watched = False")
        t = jinja_env.get_template("frontpage.html")
        response = t.render(
                        movies = unwatched_movies,
                        error = self.request.get("error"))
        self.response.write(response)

# class Latest5Blog(Handler):
#     def get(self):
#         posts = db.GqlQuery("SELECT * FROM Post ")


app = webapp2.WSGIApplication([
    ('/',Index),
    ('/blog', MainHandler)
], debug=True)

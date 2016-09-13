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

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Post(db.Model): #This is where I am defining the Post (database).
    title = db.StringProperty(required = True)
    post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
    """ A base RequestHandler class for the site.
        The other handlers inherit form this one.
    """
    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)

    def render_str(self,template,**params):
        return render_str(template,**params)

    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

class Index(Handler):
    def get(self):
        welcome_message = "Welcome! But you need to visit the " + "<a href='/blog'>blog</a>" + " page!"
        self.response.write(welcome_message)

class MainHandler(Handler):
    """ Handles request to the main page of the blog. So '/blog' page
    """
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")
        
        self.render('frontpage.html',posts=posts)

class NewEntry(Handler):
    """ Handles request to the new post writing of the blog. So '/blog/newpost' page.
    """

    def get(self):
        self.render("newpost.html")

    def post(self):
        title = self.request.get("title")
        post = self.request.get("post")

        if title and post:
            new_entry = Post(title = title, post = post)
            new_entry.put()
            self.redirect('/blog/%s' % str(new_entry.key().id()))
        else:
            error = "Be sure to enter title and post!"
            self.render("newpost.html",title=title,post=post,error=error)

class ViewPostHandler(Handler):
    def get(self, id):
        entry = Post.get_by_id(int(id))

        if not entry:
            error = "<h3>Not a valid post ID! Return to <a href='/blog'>Main</a></h3>"
            self.response.write(error)
            return

        self.render("permalink.html",entry=entry)

app = webapp2.WSGIApplication([
    ('/',Index),
    ('/blog', MainHandler),
    ('/blog/newpost', NewEntry),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)],
    debug=True)

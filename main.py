import os
import random
import string
import hmac
import webapp2
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

class Order(db.Model):
    customer = db.StringProperty(required=True)
    amount = db.IntegerProperty(required=True)
    flavor = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    state = db.StringProperty(required=True)

class User(db.Model):
    username = db.StringProperty(required=True)
    password_hash = db.StringProperty(required=True)

all_flavors = {'mixed', 'lypa', 'flower', 'buckwheat'}

def jinja2_render(template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

class AuthorizedHandler(webapp2.RequestHandler):
    def cond_call(self, f):
        userid = self.request.cookies.get('userid')
        if userid and id_valid_cookie(userid):
            f()
        else:
            self.redirect('/login')

    def post(self):
        self.cond_call(self.auth_post)

    def get(self):
        self.cond_call(self.auth_get)

    def auth_post(self):
        self.error(405)

    def auth_get(self):
        self.error(405)

class CreateOrderHandler(AuthorizedHandler):
    def auth_post(self):
        values = dict(map(lambda x: (x, self.request.get(x)), ['customer', 'amount', 'flavor']))

        c = values['customer']
        a = values['amount']
        f = values['flavor']

        if c and a and a.isdigit() and f and f in all_flavors:
            values['state'] = 'bcc'
            values['amount'] = int(a)
            order = Order(**values)
            order.put()
            self.redirect('/')
        else:
            self.response.write('bad order')

class OrdersHandler(AuthorizedHandler):
    def auth_get(self):
        all_orders = Order.all()
        self.response.write(jinja2_render('orderlist.html', orders=all_orders, flavors=all_flavors))

def pw_new_salt():
    return ''.join(random.choice(string.letters) for i in xrange(5))

def pw_new_hash(pw, salt):
    return '%s|%s' % (hmac.new(salt, pw).hexdigest(), salt)

def pw_match(pwhash, pw):
    salt = pwhash.split('|')[1].encode('ascii', 'ignore')
    return pwhash == pw_new_hash(pw, salt)

def id_secret():
    return '123qwe'

def id_new_cookie(userid):
    return '%s|%s' % (userid, hmac.new(id_secret(), userid).hexdigest())

def id_valid_cookie(cookie):
    parts = cookie.split('|')
    return len(parts) == 2 and cookie == id_new_cookie(parts[0])

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(jinja2_render('login.html'))

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        e = None

        if username and password:
            u = User.all().filter('username =', username).get()
            if u and pw_match(u.password_hash, password):
                userid = str(u.key().id())
                userid_hash = id_new_cookie(userid)
                self.response.headers.add_header('Set-Cookie', 'userid=%s' % userid_hash)
                self.redirect('/')
            else:
                e = 'incorrect user or password'
        else:
            e = 'enter username and password'

        if e:
            self.response.write(jinja2_render('login.html', error=e))

class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'userid=')
        self.redirect('/login')

app = webapp2.WSGIApplication([
    ('/', OrdersHandler),
    ('/new_order', CreateOrderHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler)],
    debug=True)

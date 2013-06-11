import os
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

all_flavors = {'mixed', 'lypa', 'flower', 'buckwheat'}

def jinja2_render(template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

class CreateOrderHandler(webapp2.RequestHandler):
    def post(self):
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

class OrdersHandler(webapp2.RequestHandler):
    def get(self):
        all_orders = Order.all()
        self.response.write(jinja2_render('orderlist.html', orders=all_orders, flavors=all_flavors))

app = webapp2.WSGIApplication([('/', OrdersHandler), ('/new_order', CreateOrderHandler)], debug=True)

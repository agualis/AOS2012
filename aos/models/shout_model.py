from google.appengine.ext import db

class Shout(db.Model):
    title = db.StringProperty(required=True)
    text = db.TextProperty(required=True)
    phone = db.PhoneNumberProperty(required=True)
    quantity = db.IntegerProperty(required = True)
    mtime = db.DateTimeProperty(auto_now_add=True) 
    user = db.StringProperty()
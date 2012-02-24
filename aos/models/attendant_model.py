from google.appengine.ext import db

class Attendant(db.Model):
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty()
    email = db.EmailProperty(required=True)
    city = db.StringProperty()
    catering = db.BooleanProperty()

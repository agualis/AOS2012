from google.appengine.ext import db


class Attendant(db.Model):
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    city = db.StringProperty(required=True)
    catering = db.BooleanProperty(required=True)

    # http://stackoverflow.com/questions/843580/writing-a-init-function-to-be-used-in-django-model
    def create(first_name, last_name, email, city, catering):
	return Attendant(key_name=email,
			 first_name=first_name,
			 last_name=last_name,
			 email=email,
			 city=city,
			 catering=catering)
    create = staticmethod(create)

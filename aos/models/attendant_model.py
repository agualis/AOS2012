from google.appengine.ext import db
from google.appengine.api import urlfetch

class Attendant(db.Model):
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    twitter_id = db.StringProperty(default='')
    twitter_avatar = db.BlobProperty()
    city = db.StringProperty(required=True)
    catering = db.BooleanProperty(required=True)
    
    
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    # http://stackoverflow.com/questions/843580/writing-a-init-function-to-be-used-in-django-model
    def create(first_name, last_name, email, city, catering):
        return Attendant(key_name=email,
    			 first_name=first_name,
    			 last_name=last_name,
    			 email=email,
    			 city=city,
    			 catering=catering)
    
    create = staticmethod(create)

    def fetch_twitter_avatar(self):
        # TODO: test with the url fetch api
        url = 'http://api.twitter.com/1/users/profile_image/' + self.twitter_id + '.json'
        response = urlfetch.fetch(url)
        if response.status_code == 200:
            self.twitter_avatar = response.content
            self.put()

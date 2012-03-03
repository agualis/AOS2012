from google.appengine.ext import db
from django.core.validators import email_re
from google.appengine.api import urlfetch

class Attendant(db.Model):
    first_name = db.StringProperty(verbose_name='Nombre', required=True)
    last_name = db.StringProperty(verbose_name='Apellidos',required=True)
    email = db.EmailProperty(required=True)
    twitter_id = db.StringProperty(verbose_name='Twitter',default='')
    twitter_avatar = db.BlobProperty()
    city = db.StringProperty(verbose_name='Ciudad',required=True)
    catering = db.BooleanProperty(default=False)
    
    
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    # http://stackoverflow.com/questions/843580/writing-a-init-function-to-be-used-in-django-model
    @classmethod
    def create(cls,first_name, last_name, email, city, catering):
        if cls.is_valid_email(email):
            return Attendant(key_name=email,
    			 first_name=first_name,
    			 last_name=last_name,
    			 email=email,
    			 city=city,
    			 catering=catering)
        else:
            raise ExMailError('mail is not valid')

    @classmethod
    def is_valid_email(cls,email):
    #    return True if email_re.match(email) else False
        return email_re.match(email)

    def fetch_twitter_avatar(self):
        # TODO: test with the url fetch api
        url = 'http://api.twitter.com/1/users/profile_image/' + self.twitter_id + '.json'
        response = urlfetch.fetch(url)
        if response.status_code == 200:
            self.twitter_avatar = response.content
            self.put()
            
class ExMailError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)



from google.appengine.ext import db
from aos.lib.common_utils.json_utils import Serializable
from django.core.validators import email_re
from google.appengine.api import urlfetch
from aos.models.user_model import User

class Attendant(db.Model, Serializable):
    first_name = db.StringProperty(verbose_name='Nombre', required=True)
    last_name = db.StringProperty(verbose_name='Apellidos',required=True)
    email = db.EmailProperty(required=True)
    twitter_id = db.StringProperty(verbose_name='Twitter',default='')
    twitter_avatar = db.BlobProperty()
    city = db.StringProperty(verbose_name='Ciudad',required=True)
    catering = db.BooleanProperty(default=False)
    user = db.ReferenceProperty(reference_class= User, collection_name='attendant')
    speaker = db.BooleanProperty(default=False)
    
    json_excluded = ['user']
    
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
            
    def create_user(self):
        user = User.create_web_user(self.email, 'patata')
        self.user = user
        return user
    
    def set_as_speaker(self):
        if not self.user:
            self.create_user()
        self.user.set_as_speaker()
        self.user.put()
        self.speaker = True

            
class ExMailError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)



from google.appengine.ext import db
from google.appengine.api import memcache

from django.http import HttpResponse, HttpResponseForbidden

from common_utils.db import insert_with_random_key
import common_utils

from datetime import datetime, timedelta
from random import choice
import logging, time
import traceback
from common_utils import decode_client_data
import hashlib


from google.appengine.api import mail


class Error(Exception):
    pass

def fetch_token(request):
    cookie = request.COOKIES.get('tok')    
    if not cookie:
        raise Error('Token missing')
    token = Token.get(cookie)
    
    if not (token and (token.expires > datetime.utcnow())): 
        raise Error('Token expired')
    request.token = token
    return token
 
ALL_CHARS = "0123456789abcdefghijkmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"    
 
class Token(db.Expando):
#    pos_key_name = db.StringProperty(required=True)
#    operator_key_name = db.StringProperty(required=True)
#    roles = db.StringListProperty(default=[], indexed=False)
#    device_id = db.StringProperty(required=True)
    secret= db.StringProperty(required=True)
    expires = db.DateTimeProperty(required=True)
    
    @classmethod
    def create(cls, validity_in_minutes=120, cache=True, **kwargs):
        validity = timedelta(minutes=validity_in_minutes)
        token = cls(secret=''.join([choice(ALL_CHARS) for i in range(32)]),
                    expires=datetime.utcnow()+validity)
        
        #now add dynamic/optional attributes
        for key, value in kwargs.iteritems():
            setattr(token, key, value)
        insert_with_random_key(token)
        
        if cache:
            token.cache()
        return token
        
    @classmethod
    def get(cls, key_name):
        token = memcache.get('tok_%s' % key_name)
        if not token:
            token = Token.get_by_key_name(key_name)
            if token:
                now = datetime.utcnow()  
                if now >= token.expires:
                    token = None
                    logging.warning('Attempt to use expired token %s', key_name)
                else:
                    token.pos_key = db.Key.from_path('PointOfSale', token.pos_key_name)
                    token.operator_key = db.Key.from_path('Operator', token.operator_key_name, parent=token.pos_key)
                    token.cache()
                    logging.info('Reloaded token %s into cache' % token.key().name())
        return token

    def refresh(self, validity_in_minutes=120):
        """If this token is still valid reset its validity and update the cache"""
        now = datetime.utcnow()
        if self.expires < now:
            raise Error('Token expired')
        validity = timedelta(minutes=validity_in_minutes)
        token.expires=datetime.utcnow()+validity
        
    def cache(self):
            memcache.set('tok_%s' % self.key().name(), self, (self.expires - datetime.utcnow()).seconds)        

    def as_json(self):
        return {'tok': self.key().name(),
                'exp': common_utils.xml_time(self.expires),
                'sec': self.secret}
    
def purge(request):
    ''' 
    Remove expired tokens from the db and the cache.
    '''
    now = datetime.utcnow()
    expired_tokens=db.Query(Token).filter('expires <', now).fetch(20)
    if expired_tokens:
        if not memcache.delete_multi([token.key().name() for token in expired_tokens], key_prefix='tok_'):
            logging.warning("Not all expired tokens were removed from the cache")
        try:
            db.delete(expired_tokens)
        except db.Error, e:
            logging.warning(e)
        logging.info("Purged %d expired tokens" % len(expired_tokens))
    return HttpResponse('OK')

    
class FormToken(object):
    """FormTokens are simple memory only, short-lived tokens to use in forms.
    
    FormTokens save the ip-address and creation time. Forms and scripts should
    be setup so that the token identifier is included in the form data. 
    The ip address of the submission should match the ip address of the token.
    """ 
    pass

WEB_EXPIRATION_MILLISECONDS = 120000 #(20 minutes)

class InvalidToken(Error):
    pass

def get_form_token(request):
    token = FormToken()
    token.ip = request.META.get('REMOTE_ADDR')
    token.time = time.time()
    key = common_utils.get_random_identifier(12, 'FTok')
    memcache.add(key, token, WEB_EXPIRATION_MILLISECONDS)
    return key

def validate(request, token=None):
    """
        It takes the token data from the request and validates it against the memcache FormToken.
        This method is just called in login process. It should be called in authorize too.
    """
    if not token:
        raise InvalidToken()
    tok = memcache.get(token) 
    if not tok:
        raise InvalidToken('Token %s not found' % token)
    if time.time() - tok.time > WEB_EXPIRATION_MILLISECONDS:
        raise InvalidToken('Token %s expired' % token)
    if not tok.ip == request.META.get('REMOTE_ADDR'):
        raise InvalidToken('Token ip (%s) does not match request from (%s)' % (tok.ip, request.META.get('REMOTE_ADDR')))
    return True
from django.http import HttpResponse, HttpResponseServerError
from django.utils import simplejson as json

import time
import os
from datetime import datetime, timedelta
from calendar import timegm
from random import choice, randint
from StringIO import StringIO
import gzip
from settings import DEBUG
import logging

import traceback
from google.appengine.api import app_identity

ALL_CHARS = "0123456789abcdefghijkmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def get_random_identifier(length=6, prefix=''):
    """
        Returns random identifier with given length (default 6) and optional prefix
    """
    return prefix + ''.join([choice(ALL_CHARS) for i in range(length - len(prefix))])
        
class TextPlainResponse(HttpResponse):
    def __init__(self, object=None, content_type='text/plain; charset=UTF-8', **kwargs):
        super(TextPlainResponse, self).__init__(
            content=object, content_type=content_type, **kwargs)         
 
def is_secure(request):
    return request.is_secure() or DEBUG == True   


    


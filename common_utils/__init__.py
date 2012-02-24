from django.http import HttpResponse, HttpResponseServerError
from django.utils import simplejson as json

import pyDes

import base64
import time
import os
from datetime import datetime, timedelta
from calendar import timegm
from random import choice, randint
from StringIO import StringIO
import gzip
import base64
from settings import DEBUG
import logging

import traceback
from google.appengine.api import app_identity

ALL_CHARS = "0123456789abcdefghijkmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def decode_client_data(request_object):
    if(request_object.META.get('HTTP_CONTENT_ENCODING',None)!=None):
        return decompress_data(request_object.raw_post_data)
    else:
        logging.warning("NOT ZIPPED REQUEST!!!")
        if request_object.raw_post_data.startswith('H4'):
            logging.info("Starting with H4")
            return decompress_data(request_object.raw_post_data)
        else:
            return request_object.raw_post_data
        
def decompress_data(raw_data):
    gzip_string = base64.standard_b64decode(str(raw_data))
    url_file_handle=StringIO(gzip_string)
    gzip_file_handle = gzip.GzipFile(fileobj=url_file_handle)
    decompressed_data = gzip_file_handle.read()
    gzip_file_handle.close()
    return decompressed_data

def get_string_from_datetime(dt):
    '''
        Returns a formated string representing a datetime with format 2010-12-02 08:12:23.1234
    '''
    return dt.strftime("%Y-%m-%d %H:%M:%S.") + str(dt.microsecond)

def get_random_identifier(length=6, prefix=''):
    """
        Returns random identifier with given length (default 6) and optional prefix
    """
    return prefix + ''.join([choice(ALL_CHARS) for i in range(length - len(prefix))])
        
class TextPlainResponse(HttpResponse):
    def __init__(self, object=None, content_type='text/plain; charset=UTF-8', **kwargs):
        super(TextPlainResponse, self).__init__(
            content=object, content_type=content_type, **kwargs)

_crypter = None
_crypt_secret = 'frogtek!' #must be exactly 8 chars long
def encrypt(str):
    global _crypter
    if not _crypter:
        _crypter = pyDes.des(_crypt_secret)
    return base64.b16encode(_crypter.encrypt(str, padmode=pyDes.PAD_PKCS5))

def decrypt(str):
    global _crypter
    if not _crypter:
        _crypter = pyDes.des(_crypt_secret)
    return _crypter.decrypt(base64.b16decode(str), padmode=pyDes.PAD_PKCS5)           
 
def is_secure(request):
    return request.is_secure() or DEBUG == True   


        
def is_in_list(element, list):
    try:
        list.index(element)
        return True
    except: 
        return False
    
def merge_dicts(dict1,dict2):
    dict3 = dict(dict1)
    for key, value in dict2.items():
        if dict3.has_key(key):
            dict3[key] = dict3[key] + value
        else:
            dict3[key] = value
    return dict3

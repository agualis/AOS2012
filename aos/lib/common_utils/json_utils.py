import logging
from django.http import HttpResponse
from django.utils import simplejson as json
from datetime import datetime, date
from google.appengine.ext import db
import traceback
from datetime import time

class JsonResponse(HttpResponse):
    def __init__(self, object=None, content_type='application/json', **kwargs):
        super(JsonResponse, self).__init__(
            content=json.dumps(object), content_type=content_type, **kwargs)
        
class Serializable():

    def to_json(self):
        result = {}
        props = [key for key in getattr(self, '_properties').iterkeys()]
        props += [key for key in getattr(self, '_dynamic_properties', {}).iterkeys()]
        for attr in props:
            if attr.startswith('_') or attr in self.get_excluded_fields():
                pass
            else:
                try:
                    value = getattr(self, attr)
                    if isinstance(value, time):
                        result[attr] = str(value.hour) + ':' + str(value.minute)
                    elif isinstance(value, db.Blob):
                        pass 
                    elif isinstance(value, db.Model):
                        result[attr] = value.to_json()
                    elif isinstance(value, date):
                        result[attr] = value.isoformat()
                    elif value <> None:
                        result[attr] = value
                except AttributeError, e:
                    traceback.print_exc()
                    logging.error('AttributeError: %s' % e)
        return result 
    
    def get_excluded_fields(self):
        if hasattr(self, 'json_excluded'):
            return self.json_excluded
        else:
            return []
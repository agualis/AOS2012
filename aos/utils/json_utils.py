import logging
from django.http import HttpResponse
from django.utils import simplejson as json
from datetime import datetime

class JsonResponse(HttpResponse):
    def __init__(self, object=None, content_type='application/json', **kwargs):
        super(JsonResponse, self).__init__(
            content=json.dumps(object), content_type=content_type, **kwargs)
        
class Serializable():
    def to_json(self, map={}, exclude=[]):
        """Return a dictionary with the attributes of the instance mapped to json-able values 
        
        Include key, value pairs of the given map but exclude the listed attributes.
        """ 
        result = {}
        result.update(map)
        props = [key for key in getattr(self, '_properties').iterkeys()]
        props += [key for key in getattr(self, '_dynamic_properties', {}).iterkeys()]
        for attr in props:
            if attr in map or attr.startswith('_') or attr in exclude:
                pass
            else:
                try:
                    value = getattr(self, attr)
                    if isinstance(value, datetime):
                        result[attr] = str(value)[:26]
                    elif value <> None:
                        result[attr] = value
                except AttributeError, e:
                    logging.error('AttributeError: %s' % e)
        return result 
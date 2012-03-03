from google.appengine.ext import db
from django.utils import simplejson as json 
from google.appengine.ext.db import BadValueError
from google.appengine.api import datastore
from aos.lib.common_utils import get_random_identifier


class Error(Exception):
    def type(self):
        return self.__class__.__name__
    
    def __str__(self):
        return "%s: %s" % (self.type(), super(Error, self).__str__())

class ExistingObject(Error):
    pass
class MissingElementError(Error):
    pass

def get_random_key(instance, key_length=6, prefix=''):
    while not instance.is_saved():
        key_name = get_random_identifier(key_length, prefix)
        key = db.Key.from_path(instance.__class__.kind(), key_name, parent=instance.parent_key())
        existing = db.get(key)
        if not existing: 
            instance._key_name = key_name
            instance.put()
        return
    
def normalize_key(key):    
    keys, multiple = datastore.NormalizeAndTypeCheckKeys(key)
    return keys[0].name()
      
                    
def insert_with_random_key(db_model_instance, length=6, prefix=''):
    
    return db.run_in_transaction(get_random_key, db_model_instance, length, prefix)

class JsonProperty(db.TextProperty):

    data_type = object

    def get_value_for_datastore(self, model_instance):
        return db.Text(json.dumps(super(JsonProperty, self).get_value_for_datastore(model_instance)))

    def make_value_from_datastore(self, value):
        if value is None:
            return None
        return json.loads(super(JsonProperty, self).make_value_from_datastore(value))
    
    def validate(self, value):
        try:
            json.dumps(value)
            return value
        except Exception, e:
            raise BadValueError("%s is not JSON serializable" % self.name)

    def empty(self, value):
        return not value
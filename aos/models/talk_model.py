from google.appengine.ext import db
import common_utils

class Serializable():
    def to_json(self):
        return common_utils.to_json(self)
      
class Room(db.Model, Serializable):
    name = db.StringProperty(required=True)

class Talk(db.Model, Serializable):
    title = db.StringProperty(required=True)
    schedule= db.StringProperty(required=True)
    room = db.ReferenceProperty(reference_class= Room, collection_name='talks')

    
    
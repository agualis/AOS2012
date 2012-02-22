from google.appengine.ext import db
from aos.utils.json_utils import Serializable

class Room(db.Model, Serializable):
    name = db.StringProperty(required=True)
    #talks
    
    def __unicode__(self):
        return self.name

    room_names = ['sala1', 'sala2', 'sala3', 'sala4']
    @classmethod
    def init_rooms(cls):
        if not cls.all().count(1) > 0:
            for room_name in cls.room_names:
                Room(name = room_name).put()
            
    @classmethod
    def get_rooms(cls):
        return Room.all().fetch(1000)

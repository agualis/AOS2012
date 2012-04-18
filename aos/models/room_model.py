from google.appengine.ext import db
from aos.lib.common_utils.json_utils import Serializable
import logging

class Room(db.Model, Serializable):
    name = db.StringProperty(required=True)
    #talks
    
    def __unicode__(self):
        return self.name
    
    room_names = ['sala1', 'sala2', 'sala3', 'sala4']
    @classmethod
    def create_room(cls, room_id, room_name):
        return Room(key_name = room_id, name = room_name)

    @classmethod
    def init_rooms(cls):
        i = 1
        if not cls.all().count(1) > 0:
            for room_name in cls.room_names:
                cls.create_room(str(i), room_name).put()
                i += 1
            
    @classmethod
    def get_rooms(cls):
        return Room.all().fetch(1000)

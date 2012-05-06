from google.appengine.ext import db
from aos.lib.common_utils.json_utils import Serializable
from aos.models.room_model import Room
from aos.models.attendant_model import Attendant
from datetime import time, date
    
class Talk(db.Model, Serializable):
    title = db.StringProperty(required=True)
    date = db.DateProperty(default=date(2012, 06, 23))
    session = db.IntegerProperty(choices=[1,2,3,4,5,6])
    duration = db.IntegerProperty(default=1)
    room = db.ReferenceProperty(reference_class= Room, collection_name='talks')
    speaker = db.ReferenceProperty(reference_class= Attendant, collection_name='talks')
    description = db.StringProperty(default="")
    
    def set_room(self, room_key):
        self.room = room_key
        return self

    @classmethod
    def get_talk_sessions(cls):
        sessions = []
        for i in range(1, 7):
            sessions.append(i) 
        return sessions  
        
    @classmethod
    def create_talk(cls, title, attendant_key_name, session = None, minute = 0, description=""):
        talk = Talk(title = title, session = session, speaker = attendant_key_name, description = description)
        return talk
    
    @classmethod
    def add_room_to_talk(cls, talk_id, room_key):
        talk = Talk.get_by_id(talk_id)
        talk.set_room(room_key)
        talk.put()
        return talk

    @classmethod
    def get_talks_from_room(cls, key_name):
        return Talk.all().filter('room', key_name).fetch(1000)
    
    @classmethod
    def get_talks_during_session(self, session):
        return Talk.all().filter('session', session).fetch(1000)
        
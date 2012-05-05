from google.appengine.ext import db
from aos.lib.common_utils.json_utils import Serializable
from aos.models.room_model import Room
from aos.models.attendant_model import Attendant
from datetime import time, date
    
class Talk(db.Model, Serializable):
    title = db.StringProperty(required=True)
    date = db.DateProperty(default=date(2012, 06, 23))
    time= db.TimeProperty()
    hour = db.IntegerProperty(choices=[9,10,11,12])
    duration = db.IntegerProperty(default=1)
    room = db.ReferenceProperty(reference_class= Room, collection_name='talks')
    speaker = db.ReferenceProperty(reference_class= Attendant, collection_name='talks')
    description = db.StringProperty(default="")
    
    def set_room(self, room_key):
        self.room = room_key
        return self

    def set_time(self, time):
        self.time = time
        self.hour = time.hour
        return self
    
    @classmethod
    def get_talk_hours(cls):
        hours = []
        for i in range(9, 13):
            hours.append(i) 
        return hours  
        
    @classmethod
    def create_talk(cls, title, attendant_key_name, hour = None, minute = 0, description=""):
        if hour:
            talk_time = time(hour, minute)
        else:
            talk_time = None
        talk = Talk(title = title, time = talk_time, speaker = attendant_key_name, description = description)
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
    def get_talks_during_hour(self, hour):
        return Talk.all().filter('hour', hour).fetch(1000)
    
    @classmethod
    def add_time_to_talk(cls, talk_id, hour, minute):
        talk = Talk.get_by_id(talk_id)
        talk.set_time(time(hour, minute))
        talk.put()
        return talk

    
    
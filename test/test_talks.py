import unittest
from aos.models.talk_model import Room, Talk
from common_utils.test import TestBedInitializer
from aos.models.attendant_model import Attendant
from datetime import time

class TalksTestCase(unittest.TestCase, TestBedInitializer):

    def setUp(self):
        self.init_testbed_for_datastore_tests()
        self.init_django_settings()
      
        self.attendant_key = Attendant(key_name = 'at1@gmail.com' , first_name='Ponente1', email= 'at1@gmail.com').put()
        self.room1 = Room(name = "sala1")
        self.room2 = Room(name = "sala2")
        room_key1 = self.room1.put()
        room_key2 = self.room2.put()
        self.attendant_key = Attendant(key_name = 'at1@gmail.com' , first_name='Ponente1', email= 'at1@gmail.com').put()
        Talk(title = 'Titulo1', speaker = self.attendant_key, room = room_key1).put()
        Talk(title = 'Titulo2', speaker = self.attendant_key, room = room_key2).put()
        Talk(title = 'Titulo3', speaker = self.attendant_key, room = room_key1).put()
        self.talk_key_4 = Talk(title = 'Titulo4',  speaker = self.attendant_key).put()
        
    def test_search_unexisting_attendant(self):
        attendant = Attendant.all().filter('name', 'PonenteN').fetch(1000)
        self.assertFalse(attendant)

    def test_fetch_talks_from_attendant(self):
        attendant = Attendant.all().filter('first_name', 'Ponente1').get()
        self.assertEquals('Titulo1', attendant.talks[0].title)
        self.assertEquals('Titulo2', attendant.talks[1].title)
        
    def test_create_talk(self):
        talk = Talk.create_talk('Titulo5', self.attendant_key)
        self.assertEquals('at1@gmail.com', talk.speaker.email)
        
    def test_add_room_to_talk(self):
        talk = Talk.add_room_to_talk(self.talk_key_4.id(), self.room1.key())
        self.assertEquals('sala1', talk.room.name)
        
    def test_add_time_to_talk(self):
        talk = Talk.add_time_to_talk(self.talk_key_4.id(), 17, 30)
        self.assertEquals(17, talk.time.hour)
        
    def test_get_talks_from_room(self):
        talks = Talk.get_talks_from_room(self.room1.key())
        self.assertEqual('Titulo1Titulo3', talks[0].title + talks[1].title)
        
    def test_get_talks_during_hour(self):
        talk= Talk.create_talk('Charla1', self.attendant_key)
        talk2= Talk.create_talk('Charla2', self.attendant_key)
        talk.set_time(time(20)).put()
        talk2.set_time(time(20)).put()
        talks = Talk.get_talks_during_hour(20)
        self.assertEquals("Charla1Charla2", talks[0].title + talks[1].title)
        

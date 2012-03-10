import unittest
from aos.lib.common_utils.test_utils import TestBedInitializer
from aos.models.talk_model import Room, Talk
from aos.models.attendant_model import Attendant
from datetime import time
import logging

class TalksTestCase(unittest.TestCase, TestBedInitializer):

    def setUp(self):
        self.init_testbed_for_datastore_tests()
        self.init_django_settings()
        self.room1 = Room(name = "sala1")
        self.room2 = Room(name = "sala2")
        room_key1 = self.room1.put()
        room_key2 = self.room2.put()
        self.attendant_key = Attendant.create('Ponente1', 'Apellido1', 'asistente1@aos.com', 'Zaragoza', False).put()
        self.talk1 = Talk(title = 'Titulo1', speaker = self.attendant_key, room = room_key1)
        self.talk1.time = time(9,0)
        self.talk1.put()
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
        self.assertEquals('asistente1@aos.com', talk.speaker.email)
        
    def test_add_room_to_talk(self):
        talk = Talk.add_room_to_talk(self.talk_key_4.id(), self.room1.key())
        self.assertEquals('sala1', talk.room.name)
        
    def test_add_time_to_talk(self):
        talk = Talk.add_time_to_talk(self.talk_key_4.id(), 11, 30)
        self.assertEquals(11, talk.time.hour)
        
    def test_get_talks_from_room(self):
        talks = Talk.get_talks_from_room(self.room1.key())
        self.assertEqual('Titulo1Titulo3', talks[0].title + talks[1].title)
        
    def test_get_talks_during_hour(self):
        talk= Talk.create_talk('Charla1', self.attendant_key)
        talk2= Talk.create_talk('Charla2', self.attendant_key)
        talk.set_time(time(11)).put()
        talk2.set_time(time(11)).put()
        talks = Talk.get_talks_during_hour(11)
        self.assertEquals("Charla1Charla2", talks[0].title + talks[1].title)
        
    def test_serialize_to_json(self):
        expected = {'room': {'name': u'sala1'}, 'title': 'Titulo1', 'duration': 1, 'speaker': {'city': u'Zaragoza', 'first_name': u'Ponente1', 'last_name': u'Apellido1', 'twitter_id': u'', 'catering': False, 'speaker': False, 'email': u'asistente1@aos.com'}, 'time': '9:0', 'date': '2012-06-23'}  
        logging.error("Talk json:  %s " %  self.talk1.to_json())
        self.assertEqual(expected, self.talk1.to_json())
        
        
        
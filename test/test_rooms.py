import unittest

from aos.lib.common_utils.test_utils import TestBedInitializer
from aos.models.talk_model import Room, Talk
import logging
from datetime import time

class TalksTestCase(unittest.TestCase, TestBedInitializer):

    def setUp(self):
        self.init_testbed_for_datastore_tests()
        self.init_django_settings()
        self.room1 = Room.create_room('1', 'sala1')
        room_key1 = self.room1.put()
        room_key2 = Room.create_room('2', 'sala2').put()
        Talk(title = 'Titulo1',  session = 1, room = room_key1).put()
        Talk(title = 'Titulo2',  session = 2, room = room_key1).put()
        Talk(title = 'Titulo3',  session = 3, room = room_key2).put()

    def test_fetch_talks_from_room(self):
        room = Room.all().filter('name', 'sala1').get()
        self.assertEquals('Titulo1', room.talks[0].title)
        self.assertEquals('Titulo2', room.talks[1].title)

    def test_filter_by_talk_name(self):
        talk = self.room1.talks.filter('title', 'Titulo2').get()
        self.assertEquals(2, talk.session)
        
    def test_serialize_to_json(self):
        logging.error("Talk json:  %s " %  self.room1.talks[0].to_json())
        self.assertEqual({'name': 'sala1'}['name'] , self.room1.to_json()['name'])

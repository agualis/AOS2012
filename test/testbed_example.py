import unittest
from google.appengine.ext import db
from aos.users.authentication import authorize_web_access
from aos.models.talk_model import Room, Talk
from django.http import HttpResponse
import logging
from common_utils.test import TestBedInitializer


class TalksTestCase(unittest.TestCase, TestBedInitializer):

    def setUp(self):
        self.init_testbed_for_datastore_tests()
        self.init_django_settings()
        self.room1 = Room(key_name = 'sala1', name = "sala1")
        room_key1 = self.room1.put()
        room_key2 = Room(key_name = 'sala2', name = "sala2").put()
        Talk(title = 'Titulo1',  schedule = '18:30', room = room_key1).put()
        Talk(title = 'Titulo2',  schedule = '19:30', room = room_key1).put()
        Talk(title = 'Titulo3',  schedule = '20:30', room = room_key2).put()

    #@authorize_web_access()
    def test_fetch_talks_from_room(self):
        room = Room.all().filter('name', 'sala1').get()
        self.assertEquals('Titulo1', room.talks[0].title)
        self.assertEquals('Titulo2', room.talks[1].title)

    def test_filter_by_talk_name(self):
        talk = self.room1.talks.filter('title', 'Titulo2').get()
        self.assertEquals('19:30', talk.schedule)
        
    def test_serialize_to_json(self):
        logging.error("AG:  %s " %  self.room1.to_json())
        logging.error("AG:  %s " %  self.room1.talks[0].to_json())
        

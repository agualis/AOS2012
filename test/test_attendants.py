import unittest
from google.appengine.ext import db
from aos.users.authentication import authorize_web_access
from aos.models.talk_model import Room, Talk
from django.http import HttpResponse
import logging
from common_utils.test import TestBedInitializer


class Attendant(db.Model):
	first_name = db.StringProperty(required=True)
	last_name = db.StringProperty(required=True)
	email = db.EmailProperty(required=True)
	city = db.StringProperty(required=True)
	catering = db.BooleanProperty(required=True)

	
class AttendantTestCase(unittest.TestCase, TestBedInitializer):

    def setUp(self):
        self.init_testbed_for_datastore_tests()
        self.init_django_settings()
        

    def test_create_attendance(self):
	attendant = Attendant(email='asistente@aos.com',
							key_name='asistente@aos.com',
							last_name='Apellido',
							first_name='Asistente',
							city='Zaragoza',
							catering=True)
	attendant.put()
	db_attendant = Attendant.get_by_key_name('asistente@aos.com')
	self.assertEquals('asistente@aos.com',db_attendant.email)
	self.assertEquals('Asistente',db_attendant.first_name)
	self.assertEquals('Apellido',db_attendant.last_name)
	self.assertEquals('Zaragoza',db_attendant.city)
	self.assertEquals(True,db_attendant.catering)
        

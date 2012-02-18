import unittest
from google.appengine.ext import db
from aos.models.attendant_model import Attendant
from django.http import HttpResponse
import logging
from aos.models import attendant_model


from common_utils.test import TestBedInitializer



	
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
        

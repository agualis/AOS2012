import unittest

from common_utils.test import TestBedInitializer
from google.appengine.ext import db
from aos.models.attendant_model import Attendant
from django.http import HttpResponse
import logging
from aos.models import attendant_model

class AttendantTestCase(unittest.TestCase, TestBedInitializer):

    def setUp(self):
        self.init_django_settings()
        self.init_testbed_for_datastore_tests()

    def test_create_attendance_constructor(self):
    	attendant = Attendant.create(
    			'Asistente2',
    			'Apellido2',
    			'asistente2@aos.com',
    			'Zaragoza2',
    			False)
    	attendant.put()
    	db_attendant = Attendant.get_by_key_name('asistente2@aos.com')
    	self.assertEquals('asistente2@aos.com',db_attendant.email)
    	self.assertEquals('Asistente2',db_attendant.first_name)
    	self.assertEquals('Apellido2',db_attendant.last_name)
    	self.assertEquals('Zaragoza2',db_attendant.city)
    	self.assertEquals(False,db_attendant.catering)

    def test_create_attendance_constructor_named(self):
    	attendant = Attendant.create(email='asistente3@aos.com',
       				     last_name='Apellido3',
    				     first_name='Asistente3',
    				     city='Zaragoza3',
    				     catering=True)
    	attendant.put()
    	db_attendant = Attendant.get_by_key_name('asistente3@aos.com')
    	self.assertEquals('asistente3@aos.com',db_attendant.email)
    	self.assertEquals('Asistente3',db_attendant.first_name)
    	self.assertEquals('Apellido3',db_attendant.last_name)
    	self.assertEquals('Zaragoza3',db_attendant.city)
    	self.assertEquals(True,db_attendant.catering)

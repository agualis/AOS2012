import unittest

from aos.lib.common_utils.test_utils import TestBedInitializer
from aos.models.attendant_model import Attendant
from aos.models import attendant_model

class AttendantTestCase(unittest.TestCase, TestBedInitializer):

    def setUp(self):
        self.init_django_settings()
        self.init_testbed_for_datastore_tests()
        self.init_for_url_fetch_tests()
        
        self.attendant = Attendant.create(email='billgates@microsoft.com', last_name='Gates', first_name='Bill', city='Zaragoza3', catering=True)
        self.attendant.twitter_account = "@Billgates"
        self.attendant.put()

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
	
    def test_create_attendance_constructor_error_mail(self):
        self.assertRaises(attendant_model.ExMailError, Attendant.create,
                    'AsistenteError',
                    'ApellidoError',
                    'pepillo.com',
                    'ZaragozaError',
                    False)

    def test_fetch_twitter_avatar(self):
        attendant = Attendant.create(email='asistente3@aos.com',
                            last_name='Apellido3',
                         first_name='Asistente3',
                         city='Zaragoza3',
                         catering=True)
        attendant.twitter_id = '@gualison'
        attendant.fetch_twitter_avatar()
        self.assertIsNotNone(attendant.twitter_avatar)
        
    def test_to_json(self):
        expected = {'city': 'Zaragoza3', 'first_name': 'Bill', 'last_name': 'Gates', 'twitter_id': '', 'catering': True, 'email': u'billgates@microsoft.com', 'speaker': False}
        self.assertEquals(expected, self.attendant.to_json())
        
    def test_create_user(self):
        self.attendant.create_user()
        self.assertEquals(self.attendant.email, self.attendant.user.user_id)
        
    def test_set_as_speaker(self):
        self.attendant.set_as_speaker()
        self.assertTrue(self.attendant.speaker)
        self.assertTrue(self.attendant.user.is_speaker())
        
        
        
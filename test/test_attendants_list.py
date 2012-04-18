import unittest

from aos.lib.common_utils.test_utils import TestBedInitializer
from aos.models.attendant_model import Attendant
from aos.models import attendant_model
import logging

class AttendantTestCase(unittest.TestCase, TestBedInitializer):

    def setUp(self):
        self.init_django_settings()
        self.init_testbed_for_datastore_tests()
        self.attendant = Attendant.create(email='isabel@folcloricas.es', last_name='Pantoja', first_name='Isabel', city='Sevilla', catering=False)
        self.attendant.twitter_id = "@pantoja"
        self.attendant.put()
        self.attendant2 = Attendant.create(email='willsmith@hollywood.com', last_name='Smith', first_name='Will', city='Los Angeles', catering=True)
        self.attendant2.put()
        
    def test_get_mail_selection_json(self):
        self.assertEqual({ 'value': u'isabel@folcloricas.es', 'label': u'isabel@folcloricas.es', 'category': "Email" }, self.attendant.get_mail_selection_json())
        
    def test_get_name_selection_json(self):
        self.assertEqual({ 'value': u'isabel@folcloricas.es', 'label': "Isabel Pantoja", 'category': "Nombre" }, self.attendant.get_name_selection_json())
 
    def test_get_blank_twitter_selection_json(self):
        self.assertEqual(None, self.attendant2.get_twitter_selection_json())
 
    def test_get_twitter_selection_json(self):
        self.attendant2.twitter_id = "@freshprince"
        self.attendant2.put()
        self.assertEqual({ "value": "willsmith@hollywood.com", 'label': "@freshprince", 'category': "Twitter" }, self.attendant2.get_twitter_selection_json())
 
    def test_get_selection_array(self):
        expected = [{"category": "Nombre", "value": "isabel@folcloricas.es", "label": "Isabel Pantoja"},
                     {"category": "Nombre", "value": "willsmith@hollywood.com", "label": "Will Smith"}, 
                     {"category": "Email", "value": "isabel@folcloricas.es", "label": "isabel@folcloricas.es"},
                     {"category": "Email", "value": "willsmith@hollywood.com", "label": "willsmith@hollywood.com"}, 
                     {"category": "Twitter", "value": "isabel@folcloricas.es", "label": "@pantoja"}]
        self.assertEqual(expected, Attendant.get_selection_array())
        
        
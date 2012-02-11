import unittest
from google.appengine.ext import testbed, db
import logging
from common_utils.test import TestBedInitializer

class Person(db.Model):
    name = db.StringProperty(required=True)
    age = db.IntegerProperty(default=18)

    def is_old(self):
        return self.age >= 80
    
class TestPerson(unittest.TestCase, TestBedInitializer):
    
    def setUp(self):
        self.init_testbed_for_datastore_tests()
    
    def test_is_old(self):  
        person = Person(name='JJ', age=22)
        self.assertFalse(person.is_old())
        
    def test_is_empty(self):
        self.assertEqual(Person.all().count(), 0)

        person = Person(name='JJ', age=22)
        person.put()

        self.assertEqual(Person.all().count(), 1)

    def test_assert_empty_again(self):
        self.assertEqual(Person.all().count(), 0)
    
        person = Person(name='JJ', age=22)
        person.put()
    
        self.assertEqual(Person.all().count(), 1)
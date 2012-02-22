import unittest
from google.appengine.ext import db

"""
    This test must be executed in first place in order to avoid settings problems
"""
class ATestCase(unittest.TestCase):

    def setUp(self):
        db.Model()
     
    def test_calling_an_existing_method(self):
        self.assertFalse(False)
           

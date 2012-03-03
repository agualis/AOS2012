import unittest
from aos.lib.common_utils.test_utils import TestBedInitializer

from aos.lib.timetable.hour_row import HourRow
from aos.models.talk_model import Talk

class HourTestCase(unittest.TestCase, TestBedInitializer):

    def setUp(self):
        self.init_testbed_for_datastore_tests()
        self.init_django_settings()
        
    def test_row_without_talks(self):
        self.assertEquals([], HourRow(16).talks_by_room())
        
    def test_add_talks(self):
        talk = Talk(title='Charla1')
        talk2 = Talk(title='Charla2')
        row = HourRow(16)
        row.add_talk(talk)
        row.add_talk(talk2)
        self.assertEqual([talk, talk2], row.talks_by_room())
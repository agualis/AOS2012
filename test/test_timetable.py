import unittest
from aos.lib.common_utils.test_utils import TestBedInitializer
from aos.models.talk_model import Room, Talk
from datetime import time
from aos.lib.timetable.timetable import Timetable
import logging

class TimetableTestCase(unittest.TestCase, TestBedInitializer):

    def setUp(self):
        self.init_testbed_for_datastore_tests()
        self.init_django_settings()
        self.room1 = Room(key_name = 'sala1', name = "sala1")
        self.room2 = Room(key_name = 'sala2', name = "sala2")
        self.room1.put()
        self.room2.put()
        self.talk = Talk(title = 'Titulo1', room = self.room1, session=1)
    
    def test_empty_schedule_grid(self):
        grid = Timetable().get_grid()
        for session in Talk.get_talk_sessions():
            for room in Room.get_rooms():
                self.assertFalse(grid[session][room.name])
                
    def test_schedule_grid_with_one_talk(self):
        self.talk.put()
        grid = Timetable().get_grid()
        self.assertEquals('Titulo1', grid[1]['sala1'].title)

    def test_add_talk_to_schedule_grid(self):
        timetable = Timetable()
        timetable.add_talk(self.talk)
        self.assertEquals('Titulo1', timetable.get_grid()[1]['sala1'].title)
        
    def test_get_rows_for_template(self):
        self.talk.room = self.room2
        timetable = Timetable()
        timetable.add_talk(self.talk)
        number_of_sessions = len(Talk.get_talk_sessions())
        self.assertEquals(number_of_sessions, len(timetable.get_rows_for_template()))
        for row in timetable.get_rows_for_template():
            self.assertEquals(2, len(row.talks_by_room()))
            if row.session == 1:
                self.assertEquals(row.talks_by_room()[0], None)
                self.assertEquals(row.talks_by_room()[1], self.talk)                        
                
    def test_timetable_json(self):
        timetable = Timetable()
        timetable.add_talk(self.talk)
        self.talk.put()
        talk2 = Talk(title = 'Titulo2', room = self.room2).put()

        
        talks = timetable.get_talks()
        
        talks_json = timetable.get_talks_json()
        logging.error("AG:  %s " %  talks_json)
        
        

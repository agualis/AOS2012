from aos.models.talk_model import Talk
from aos.models.room_model import Room
from aos.lib.timetable.hour_row import HourRow

class Timetable():
    grid = {}

    def __init__(self):
        for hour in Talk.get_talk_hours():
            room_dict = {}
            for room in Room.get_rooms():
                room_dict[room.name] = None
            self.grid[hour]= dict(room_dict)
                
        for talk in Talk.all().fetch(1000):
            if talk.hour:
                self.add_talk(talk)
                
    def get_grid(self):
        return self.grid
                
    def add_talk(self, talk):
        self.grid[talk.hour][talk.room.name] = talk
        
    def get_rows_for_template(self):
        hour_rows = []
        for hour in Talk.get_talk_hours():
            row = HourRow(hour)
            for room in Room.get_rooms():
                row.add_talk(self.grid[hour][room.name])
            hour_rows.append(row)
        return hour_rows
    
    def get_talks(self):
        return Talk.all().fetch(1000)

    
    def get_talks_json(self):
        result  = {}
        for talk in self.get_talks():
            result[talk.title] = talk.to_json()
        return result
    
    

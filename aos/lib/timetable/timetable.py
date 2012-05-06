from aos.models.talk_model import Talk
from aos.models.room_model import Room
from aos.lib.timetable.session_row import SessionRow

class Timetable():
    grid = {}

    def __init__(self):
        for session in Talk.get_talk_sessions():
            room_dict = {}
            for room in Room.get_rooms():
                room_dict[room.name] = None
            self.grid[session]= dict(room_dict)
                
        for talk in Talk.all().fetch(1000):
            if talk.session:
                self.add_talk(talk)
                
    def get_grid(self):
        return self.grid
                
    def add_talk(self, talk):
        self.grid[talk.session][talk.room.name] = talk
        
    def get_rows_for_template(self):
        session_rows = []
        for session in Talk.get_talk_sessions():
            row = SessionRow(session)
            for room in Room.get_rooms():
                row.add_talk(self.grid[session][room.name])
            session_rows.append(row)
        return session_rows
    
    def get_talks(self):
        return Talk.all().fetch(1000)

    
    def get_talks_json(self):
        result  = {}
        for talk in self.get_talks():
            result[talk.key().id()] = talk.to_json()
        return result
    
    

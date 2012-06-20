SESSION_HOURS = ['','9:30','10:30','12:00','13:00','16:00','17:00']    
class SessionRow():
    def __init__(self, session):
        self.session = session
        self.hour = SESSION_HOURS[session]
        self.talks = []
    
    def talks_by_room(self):
        return self.talks
    
    def add_talk(self, talk):
        self.talks.append(talk)
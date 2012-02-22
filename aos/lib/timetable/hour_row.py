class HourRow():
    def __init__(self, hour):
        self.hour = hour
        self.talks = []
    
    def talks_by_room(self):
        return self.talks
    
    def add_talk(self, talk):
        self.talks.append(talk)
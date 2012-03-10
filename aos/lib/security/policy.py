class PolicyError(Exception):
    pass
       
class AdminPolicy():
    def permits(self, user, request, pos_key_name=None, **kwargs):
        if user.is_admin():
            return True
        else:
            return False

class SpeakerPolicy():
    def permits(self, user, request, pos_key_name=None, **kwargs):
        if user.is_speaker() or user.is_admin():
            return True
        else:
            return False

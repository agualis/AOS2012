from datetime import time
from django.http import HttpResponse
from aos.models.user_model import User
from aos.models.room_model import Room
from aos.models.attendant_model import Attendant
from aos.models.talk_model import Talk
from aos.lib.common_utils.decorators import catch_exceptions
from aos.lib.security.authentication import authorize_web_access
from aos.lib.security.policy import AdminPolicy
import logging

@catch_exceptions
#@authorize_web_access(AdminPolicy())
def init_app(request):
    if request.method == 'GET':
        User.create_admin('admin', 'aos').put()
        Room.init_rooms()
        if not Talk.all().count(1) > 0:
            talk = Talk(title = 'Android')
            talk.set_room(Room.get_rooms()[0])
            talk.set_time(time(11))
            talk.put()
            talk = Talk(title = 'Kanban')
            talk.set_room(Room.get_rooms()[1])
            talk.set_time(time(9))
            talk.put()
        if not Attendant.all().count(1) > 0:
            bill = Attendant.create('Bill', 'Gates', 'bill@microsoft.com', 'Zaragoza', False)
            bill.twitter_id = 'fbgblog'
            bill.set_as_speaker()
            bill.put()
            richard = Attendant.create('Richard', 'Stallman', 'richard@gnu.org', 'Pamplona', True)
            richard.twitter_id = 'GNUplusLINUX'
            richard.set_as_speaker()
            richard.put()
        return HttpResponse("App ready to rumble...", mimetype="text/plain")
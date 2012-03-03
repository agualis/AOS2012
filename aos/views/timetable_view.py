import logging
from django.shortcuts import render_to_response
from aos.lib.timetable.timetable import Timetable
from aos.models.room_model import Room
from aos.models.talk_model import Talk
from common_utils import TextPlainResponse
from google.appengine.api import urlfetch
from django.http import HttpResponse
from aos.models.attendant_model import Attendant

def show_timetable(request):
        
#        img_response = HttpResponse(mimetype="image/jpeg")
#        img_response.content = attendant.twitter_avatar
#        return img_response
    timetable = Timetable()
    rooms = Room.get_rooms()
    hours = Talk.get_talk_hours()
    return render_to_response('timetable.html', {'rooms': rooms, 'hours': hours, 'rows': timetable.get_rows_for_template()})
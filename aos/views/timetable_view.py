from django.shortcuts import render_to_response
from aos.lib.timetable.timetable import Timetable
from aos.models.room_model import Room
from aos.models.talk_model import Talk
from aos.lib.security.authentication import authorize_web_access
from aos.lib.security.policy import AdminPolicy

def show_timetable(request):
    user = request.session.get('user')
    timetable = Timetable()
    rooms = Room.get_rooms()
    sessions = Talk.get_talk_sessions()
    return render_to_response('timetable_app.html', {'user': user, 'rooms': rooms, 'sessions': sessions, 'rows': timetable.get_rows_for_template()})

def show_timetable_user(request):
    user = request.session.get('user')
    timetable = Timetable()
    rooms = Room.get_rooms()
    sessions = Talk.get_talk_sessions()
    return render_to_response('timetable_user.html', {'user': user, 'rooms': rooms, 'sessions': sessions, 'rows': timetable.get_rows_for_template()})

def show_admin_timetable(request):
    user = request.session.get('user')
    timetable = Timetable()
    rooms = Room.get_rooms()
    sessions = Talk.get_talk_sessions()
    return render_to_response('timetable.html', {'user': user, 'rooms': rooms, 'sessions': sessions, 'rows': timetable.get_rows_for_template()})
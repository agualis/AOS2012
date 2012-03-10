from django.shortcuts import render_to_response
from aos.models.talk_model import Talk
from google.appengine.ext.db import djangoforms
from django.http import HttpResponseRedirect
from aos.models.room_model import Room
from aos.models.attendant_model import Attendant

"""
If we want to use a pure django form 
http://jamesgae.appspot.com/blog/2010/01/08/using-django-forms-on-app-engine
"""
class TalkForm(djangoforms.ModelForm):
    class Meta:
        model = Talk
        exclude = ['date', 'time']
        
    def __init__(self, *args, **kwargs):
        super(TalkForm, self).__init__(*args, **kwargs)
        self.fields['speaker'].query = Attendant.all().filter('speaker', True).fetch(100)
    
def create_talk(request, hour, room_id):
    room = Room.get_by_id(int(room_id))
    talk = Talk(title = 'New Talk', room = room, hour = int(hour))
    if request.method == "GET":
        return show_talk_form_to_edit(request, TalkForm(instance=talk))
    else:
        return save_talk_form(request, talk)

def show_talk_form_to_edit(request, form):
    return render_to_response('talk.html',{'form': form, 'action': request.path})

def save_talk_form(request, talk=None):
    form = TalkForm(request.POST, instance=talk) 
    if not form.is_valid():
        return show_talk_form_to_edit(request, form)
    talk = form.save(commit=False) 
    talk.put()
    return HttpResponseRedirect('/timetable')

def edit_talk(request, talk_id=None):
    talk = Talk.get_by_id(int(talk_id))
    if request.method == "GET":
        return show_talk_form_to_edit(request, TalkForm(instance=talk))
    else:
        return save_talk_form(request, talk)
        

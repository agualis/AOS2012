from django.shortcuts import render_to_response
from aos.models.talk_model import Talk
from google.appengine.ext.db import djangoforms
from django.http import HttpResponse, HttpResponseRedirect
import logging
from django import forms
from aos.models.room_model import Room
from django.core.urlresolvers import reverse

"""
If we want to use a pure django form 
http://jamesgae.appspot.com/blog/2010/01/08/using-django-forms-on-app-engine
"""
class TalkForm(djangoforms.ModelForm):
    class Meta:
        model = Talk
        exclude = ['time']
        
    """
    def save(self, talk=None, commit=True):
        data = self.cleaned_data
        if talk:
            return super(TalkForm, self).save()
    """
    
def create_talk(request, hour, room_id):
    room = Room.get_by_id(int(room_id))
    talk = Talk(title = 'New Talk', room = room, hour = int(hour))
    if request.method == "GET":
        return show_talk_form_to_edit(request, TalkForm(instance=talk))
    else:
        return save_talk_form(request, talk)
    #url = reverse('/talk', kwargs ={'room': talk.room, 'hour': talk.hour})
    #return HttpResponseRedirect(url)


def show_talk_form_to_edit(request, form):
    #form = TalkForm(instance=talk)
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
        

from django.http import HttpResponse, HttpResponseRedirect
from aos.models.attendant_model import Attendant
from django.shortcuts import render_to_response
from google.appengine.ext.db import djangoforms
from django.core.exceptions import ValidationError
import logging
from django import forms

class AttendantForm(djangoforms.ModelForm):
    class Meta:
        model = Attendant
        exclude = ['twitter_avatar', 'user']
        
    def save(self, commit=True):
        data = self.cleaned_data
        if data.get('email'):
            self.cleaned_data['key_name'] = data.get('email')
            return super(AttendantForm, self).save()
    
    def clean(self):
        if not Attendant.is_valid_email(self.data['email']):
            raise ValidationError("Invalid email!")
        return super(AttendantForm, self).clean()

def create_attendant(request):
    if request.method == "GET":
        return show_attendant_form_to_edit(request, AttendantForm())
    else:
        return save_attendant_form(request, None)

def show_attendant_form_to_edit(request, form):
    return render_to_response('attendant.html',{'form': form, 'action': request.path})

def save_attendant_form(request, attendant=None):
    form = AttendantForm(request.POST, instance=attendant) 
    if not form.is_valid():
        return show_attendant_form_to_edit(request, form)
    attendant = form.save(commit=False)
    request.session['user'] = attendant.create_user() 
    if attendant.speaker:
        attendant.set_as_speaker()
    attendant.put()
    return HttpResponseRedirect("/timetable")

def get_avatar(request):
    if request.method == 'GET':
        email = request.GET.get('email', '')
        if Attendant.is_valid_email(email):
            attendant = Attendant.get_by_key_name(email)
            if attendant.twitter_id:
                if not attendant.twitter_avatar:
                    attendant.fetch_twitter_avatar()
                img_response = HttpResponse(mimetype="image/jpeg")
                img_response.content = attendant.twitter_avatar 
                return img_response
            else:
                return HttpResponse('No twitter account')
        else:
            return HttpResponse('Invalid email')
    
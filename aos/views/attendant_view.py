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
        exclude = ['twitter_avatar', 'user', 'speaker']
        
    def save(self, commit=True):
        data = self.cleaned_data
        if data.get('email'):
            self.cleaned_data['key_name'] = data.get('email')
            if data.get('twitter_id'):
                self.cleaned_data['twitter_id'] = data.get('twitter_id')[1:]
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
    
def edit_attendant(request):
    email = request.GET.get('email', '')
    attendant = Attendant.get_by_key_name(email)
    if request.method == "GET":
        return show_attendant_form_to_edit(request, AttendantForm(instance=attendant))
    else:
        return save_attendant_form(request, attendant)

def show_attendant_form_to_edit(request, form):
    user = request.session.get('user')
    return render_to_response('attendant.html',{'user': user, 'form': form, 'action': request.path})

def save_attendant_form(request, attendant=None):
    user = request.session.get('user')
    form = AttendantForm(request.POST, instance=attendant) 
    if not form.is_valid():
        return show_attendant_form_to_edit(request, form)
    attendant = form.save(commit=False)
    attendant.put()
    return render_to_response('attendant_created.html',{'user': user, 'attendant': attendant})

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
    

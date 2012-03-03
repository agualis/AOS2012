from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from aos.models.attendant_model import Attendant
import settings
from django.shortcuts import render_to_response
from google.appengine.ext.db import djangoforms

from aos.models.shout_model import Shout
from django.core.validators import email_re

class AttendantForm(djangoforms.ModelForm):
    class Meta:
        model = Attendant
        exclude = ['twitter_avatar']
        
    def save(self, commit=True):
        logging.error("AG:  %s " %  self.cleaned_data)
        data = self.cleaned_data
        if data.get('email'):
            self.cleaned_data['key_name'] = data.get('email')
            return super(AttendantForm, self).save()

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
    attendant.put()
    return HttpResponse('Registro completado')


def is_valid_email(email):
    return True if email_re.match(email) else False

def create_attendant_response(request):	
    first_name = request.POST['first_name'][:20]
    last_name = request.POST['last_name'][:20]
    email = request.POST['email'][:20]
    city = request.POST['city'][:20]
    catering = request.POST.has_key('catering')

    emailValido='puede'
    if is_valid_email(email):
        emailValido='si'
    else:
        emailValido='no'




    try:
        attendant = Attendant.create(first_name, last_name, email, city, catering)
        ok = attendant.put()

        return HttpResponse('Creado Attendant ' + first_name + ' ok' + emailValido)
    except Exception, e:
        return HttpResponse('Creado Attendant ' + first_name + ' err')

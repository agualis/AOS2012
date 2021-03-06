from aos.models.attendant_model import Attendant
from django.shortcuts import render_to_response
import logging
import simplejson as json
from django.http import HttpResponseRedirect
from aos.lib.common_utils.decorators import catch_exceptions
from aos.lib.security.policy import AdminPolicy
from aos.lib.security.authentication import authorize_web_access

@catch_exceptions
@authorize_web_access(AdminPolicy())
def get_speakers_list(request):
    if request.method == 'GET':
        speakers = Attendant.get_speakers()
        return render_to_response('speakers_list.html', 
                                  {'attendants': json.dumps(Attendant.get_selection_array()), 
                                   'speakers': speakers, 'user': request.session.get('user')})
    else:
        speakers = Attendant.get(request.POST.getlist('speakers'))
        
        return HttpResponseRedirect('admin/speakers')
   
@catch_exceptions 
def set_speaker(request):
    attendant = get_attendant(request)
    attendant.set_as_speaker()
    attendant.put()
    return get_speakers_div()

@catch_exceptions 
def remove_speaker(request):
    attendant = get_attendant(request)
    attendant.remove_as_speaker()
    attendant.put()
    return get_speakers_div()
    
def get_attendant(request):
    if request.is_ajax():
        if request.method == 'POST':
            email = request.POST.get('email', '')
            if Attendant.is_valid_email(email):
                return Attendant.get_by_key_name(email)

def get_speakers_div():
        speakers = Attendant.get_speakers()
        return render_to_response('speakers.html', {'speakers': speakers})


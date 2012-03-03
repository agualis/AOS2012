from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from aos.models.attendant_model import Attendant
import settings
from django.shortcuts import render_to_response

from aos.models.shout_model import Shout
from django.core.validators import email_re
import logging

def create_attendant(request):
    return render_to_response('attendant.html', {})

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

def get_avatar(request):
    if request.method == 'GET':
        email = request.GET.get('email', '')
        if is_valid_email(email):
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
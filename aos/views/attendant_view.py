from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from aos.models.attendant_model import Attendant
import settings
from django.shortcuts import render_to_response

from aos.models.shout_model import Shout

def create_attendant(request):
    return render_to_response('attendant.html', {})


def create_attendant_response(request):	
    first_name = request.POST['first_name'][:20]
    last_name = request.POST['last_name'][:20]
    email = request.POST['email'][:20]
    city = request.POST['city'][:20]
    catering = request.POST.has_key('catering')






    try:
        attendant = Attendant.create(first_name, last_name, email, city, catering)
        ok = attendant.put()

        return HttpResponse('Creado Attendant ' + first_name + ' ok')
    except Exception, e:
        return HttpResponse('Creado Attendant ' + first_name + ' err')

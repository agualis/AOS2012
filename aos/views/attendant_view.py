from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
import settings
from django.shortcuts import render_to_response

from aos.models.shout_model import Shout

def create_attendant(request):
	if request.method == 'GET':
		return render_to_response('attendant.html',{})
	else:
		first_name = request.POST['first_name'][:20] 
		return HttpResponse('Creado Attendant ' + first_name)
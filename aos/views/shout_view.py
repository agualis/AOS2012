from aos.users.authentication import authorize_web_access
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
import settings
from django.shortcuts import render_to_response
from google.appengine.ext.db import djangoforms
from aos.models.shout_model import Shout

class ShoutForm(djangoforms.ModelForm):
    class Meta:
        model = Shout
        exclude = ['mtime', 'user']

@authorize_web_access()
def shout(request):
    query = Shout.gql("ORDER BY mtime DESC")
    user = request.session.get('user')
    return render_to_response('shout_example.html',
                              {'user': user, 'shouts': query.run(), 'form': ShoutForm()})
@authorize_web_access()
def post(request):
    user = request.session.get('user')
    form = ShoutForm(request.POST) 
    if not form.is_valid():
        return render_to_response('shout_example.html',
                                       {'user': user, 'form': form})
    shout = form.save(commit=False) 
    shout.user = request.session.get('user').user_id
    shout.put()
    return HttpResponseRedirect('/shout')
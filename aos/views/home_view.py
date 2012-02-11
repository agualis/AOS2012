from aos.users.authentication import authorize_web_access
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
import settings

@authorize_web_access()
def get_homepage(request):
    user = request.session.get('user')
    if not user:
        return HttpResponseRedirect("%s%s" % (settings.LOGIN_URL, request.path))
    else:
        return direct_to_template(request, 'home.html', {'user': user})   
        

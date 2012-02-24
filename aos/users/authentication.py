# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponseForbidden
from django.views.generic.simple import direct_to_template
from django.utils.hashcompat import sha_constructor as sha
 
from aos.users.user_model import User
from aos.web_admin.role import Role
from common_utils import tokens

import logging, settings
from aos.utils.json_utils import JsonResponse

class PolicyError(Exception):
    pass

class AuthorizationPolicy(object):
    def __init__(self, **kwds):
        self._kwds = kwds
    
    def get(self, key):
        return self._kwds.get(key, None) if self._kwds else None
    
    def pop(self, key):
        return self._kwds.pop(key, None) if self._kwds else None

    def permits(self, user, request):
        """Return True if the request can be served for the given user. 
        
        Subclasses are encouraged to save any objects retrieved from the 
        database in the request.
        """
        return False

    
class UserTest(AuthorizationPolicy):
    def permits(self, user, request):
        method = self.pop('method')
        return method and method(user, **self._kwds)

def UserIs(role):
    return UserTest(method=User.has_role, role=role)
                        
def UserIsUser():
    return UserTest(User.is_user)
        
def authorize_web_access(policy=None, login_allowed=True, ajax_call= False):
    '''
        Checks if there is a valid session and the current user has privileges to open a view
            policy: roles needed to open a view
            login_allowed: True if user can visit web
            ajax_call: True if the request was sent via Ajax
            
        If the session has expired, it returns a 302 response so the browser automatically redirects to the login page 
        (In case of ajax_call, it returns a 403 so the Ajax controls can perform the redirection).
    '''
    def decorator(view):
        def gen_view(request, *args, **kwargs):
            user = request.session.get('user')
            if not user:
                return redirect_to_login_if_allowed(request, login_allowed, ajax_call)
            try:
                if policy and not policy.permits(user, request, *args, **kwargs):
                    return HttpResponseForbidden('Unauthorized resource.')
            except PolicyError, e:
                logging.exception(e)
                return HttpResponseForbidden()                
            request.user = user
            response = view(request, *args, **kwargs)
            return response
        return gen_view
    return decorator

def redirect_to_login_if_allowed(request, login_allowed, ajax_call):
    if not login_allowed:
        return HttpResponseForbidden()
    else:
        logging.info("From %s to %s%s" % (request.path, settings.LOGIN_URL, request.path))
        if ajax_call:
            return HttpResponseForbidden()
        else:
            return HttpResponseRedirect("%s%s" % (settings.LOGIN_URL, request.path))

def login(request, return_url='/'):
    '''
        When it's first called (using GET) it creates a new FormToken in cache and redirects to login page
        Once it's called again  (using POST with an AJAX request) it validates the token, user and pass of the request. 
    '''
    if request.method == 'GET':
        request.session.pop('user', None)
        return direct_to_template(request, 'login.html', {'token': tokens.get_form_token(request)})
    elif request.method == 'POST':
        try:
            if not request.is_ajax():
                request.session.delete()
                return HttpResponseForbidden()
            token = request.POST.get('token')
            tokens.validate(request, token)
            user_id = request.POST.get('user_id')[:20]
            user = User.by_user_id(user_id) if user_id else None
            if user:
                passhash = request.POST.get('passhash')
                if passhash and (sha(token + user.passhash).hexdigest() == passhash):
                    request.session['user'] = user
                    if user.has_role(Role.ADMIN) and (not return_url or return_url=='/'):
                        return_url = '/admin'
                    else :
                        return_url = return_url or '/'
                    return JsonResponse({'return_url': return_url})
                else:

                    return JsonResponse({'error': ('passphrase', 'Clave incorrecta'),
                                                    'token': tokens.get_form_token(request),
                                        })
            else:
                message = 'Usuario o password incorrectos. Por favor inténtelo de nuevo.'
                return JsonResponse({'error': ('uid', message.decode('utf-8')),
                                                'token': tokens.get_form_token(request),
                                    })
        except tokens.InvalidToken, t:
            logging.warning(t)
            return JsonResponse({'return_url': '/login%s' % return_url or ''})
        except Exception, e:
            logging.exception(e)
            return HttpResponseServerError()
        
def logout(request):
    request.session.delete()
    return direct_to_template(request, 'home.html', {})   

from django.http import HttpResponse, HttpResponseServerError
import logging
from aos.users.user_model import User
from aos.web_admin.role import Role
from aos.users.authentication import authorize_web_access, UserIs
from common_utils import TextPlainResponse

def create_admin_user(request):
    if request.method == 'GET':
        try:
            User.create_admin('admin', 'admin')
            return HttpResponse("User created correctly", mimetype="text/plain")
        except Exception, e:
            logging.warning(e)
            return HttpResponseServerError(e)

@authorize_web_access(UserIs(Role.ADMIN))
def init_all(request):
    init_all_roles()
    return TextPlainResponse('Ok, system in place! We are ready to rumble ;)')

def create_admin_role():
    role = Role(key_name = Role.ADMIN, name = Role.ADMIN)
    role.put()
    
def init_all_roles():
    for role_name in Role.ROLES:
        init_role(role_name)
        
def init_role(role_name):
    role = Role(key_name = role_name, name = role_name)
    role.put()
    init_permissions_for(role)
    
def init_permissions_for(role):
    if role.name == Role.ADMIN:
        tags = ['all_tags']
        menus = ['all_menus']
        buttons = ['all_buttons']
        role.add_permissions(tags + menus + buttons)

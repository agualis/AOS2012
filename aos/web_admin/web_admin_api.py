from datetime import time
from django.http import HttpResponse
from aos.users.user_model import User
from aos.web_admin.role import Role
from aos.users.authentication import authorize_web_access, UserIs
from common_utils import TextPlainResponse
from aos.models.room_model import Room
from aos.models.attendant_model import Attendant
from aos.models.talk_model import Talk
from aos.utils.decorators import catch_exceptions
from google.appengine.api.datastore import Key

@catch_exceptions
def init_app(request):
    if request.method == 'GET':
        User.create_admin('admin', 'admin')
        Room.init_rooms()
        if not Talk.all().count(1) > 0:
            talk = Talk(title = 'Android')
            talk.set_room(Key.from_path('Room', 1))
            talk.set_time(time(11))
            talk.put()
            talk = Talk(title = 'Kanban')
            talk.set_room(Key.from_path('Room', 2))
            talk.set_time(time(9))
            talk.put()
        if not Attendant.all().count(1) > 0:
            Attendant.create('Bill', 'Gates', 'bill@microsoft.com', 'Zaragoza', False).put()
            Attendant.create('Steve', 'Jobs', 'steve@apple.com', 'Pamplona', True).put()

        return HttpResponse("App ready to rumble...", mimetype="text/plain")

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
        
def create_example_talks(request):
    room1 = Room(key_name = 'sala1', name = "sala1")
    room2 = Room(key_name = 'sala2', name = "sala2")
    room_key1 = room1.put()
    room_key2 = room2.put()
    attendant_key = Attendant(key_name = 'at1@gmail.com' , first_name='Ponente1', email= 'at1@gmail.com').put()
    Talk(title = 'Titulo1',  schedule = '18:30', speaker = attendant_key, room = room_key1).put()
    Talk(title = 'Titulo2',  schedule = '19:30', speaker = attendant_key, room = room_key2).put()
    Talk(title = 'Titulo3',  schedule = '19:30', speaker = attendant_key, room = room_key1).put()
    talk_key_4 = Talk(title = 'Titulo4',  schedule = '19:30', speaker = attendant_key).put()
    return HttpResponse('ok')
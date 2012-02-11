from google.appengine.ext import db
import logging
from google.appengine.ext.db import Key
from aos.web_admin.role import Role
from hashlib import sha1 as sha
import itertools
from aos.web_admin.permission import Permission
from common_utils import is_in_list
   
class Error(Exception):
    pass
class PassphraseError(Error):
    pass

class User(db.Expando):
    server_changed = db.DateTimeProperty(auto_now=True)
    name = db.StringProperty(required=True)
    passhash = db.StringProperty()
    user_id = db.StringProperty()
    roles = db.StringListProperty(default=[], indexed=False)
    language = db.StringProperty() #preferred language of this user/operator
    creation_date = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_user_id(cls, user_id):
        return cls.all().filter('user_id', user_id).get()
    
    @classmethod
    def by_phone_number_and_pos(cls, phone_number, pos):
        return  db.Query(User).filter('pos', pos).filter('phone_number', phone_number).get()
    
    @classmethod
    def by_key(cls, key):
        return db.get(Key.from_path('User', key))

    @classmethod
    def create_admin(cls, user, password):
        return User.create_web_user(user, password, [Role.ADMIN])
    
    @classmethod
    def create_web_user(cls, name, password, roles=None):
        user = User(user_id=name, key_name=name, name=name, 
                passhash= User.__create_password_hash(password), roles=roles)
        user.put()
        return user

    @classmethod
    def __create_password_hash(cls, password):
        return sha(password).hexdigest()
    
    def update_password(self, password):
        self.passhash = password
        self.put()

    def check_password(self, password):
        logging.error("PASS NEW %s"%password)
        logging.error("PASS OLD %s"%self.passhash)
        if self.passhash == password:
            return True
        else:
            return False

    def permissions(self):
        return UserPermissions(self._flatten_permission_list())
    
    def _flatten_permission_list(self):
        return list(itertools.chain(*self._all_permissions()))
        
    def _all_permissions(self):
        return map(self._all_permissions_from, self.roles)
        
    def _all_permissions_from(self, role):
        return Role().by_name(role).permissions
    
    def update_phone_with_intl_code(self):
        self.phone_number = self._internationalize(self.phone_number) 
        self.put()
        
    def __str__(self):
        return "user %s" % self.key().name() if self.key() else super(User, self).__str__()
    
    def __repr__(self):
        return "<%s>" % self
    
    def has_role(self, role):
        return role in self.roles
    
    def is_user(self):
        return self.has_role(Role.USER)
    
    def is_admin(self): 
        return self.has_role(Role.ADMIN)
    
    def is_owner(self): 
        return self.has_role(Role.OWNER)
    
    def is_carvajal(self): 
        return self.has_role(Role.CARVAJAL)
    
    def has_permission_to_country(self, country_code):
        if self.is_admin():
            return True
        else:
            return getattr(self.permissions(), country_code)
    
class UserPermissions:
    
    def __init__(self, permissions):
        self.permissions = permissions
        
    def __getattr__(self, permission):
        permission = Permission.by_name(permission)
        if permission and self.permissions:
            return is_in_list(permission.key(), self.permissions)
        return False        
    def all(self):
        return self.permissions
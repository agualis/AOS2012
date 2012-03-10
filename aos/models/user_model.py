from google.appengine.ext import db
from google.appengine.ext.db import Key
from hashlib import sha1 as sha
from aos.lib.common_utils.list_utils import is_in_list
   
class Error(Exception):
    pass
class PassphraseError(Error):
    pass

class Role():
    ADMIN = 'admin'
    SPEAKER = 'speaker'

class User(db.Model):
    server_changed = db.DateTimeProperty(auto_now=True)
    creation_date = db.DateTimeProperty(auto_now_add=True)
    user_id = db.StringProperty()
    passhash = db.StringProperty()
    roles = db.StringListProperty(default=[], indexed=False)
    
    @classmethod
    def by_user_id(cls, user_id):
        return cls.all().filter('user_id', user_id).get()
    
    @classmethod
    def by_key(cls, key):
        return db.get(Key.from_path('User', key))

    @classmethod
    def create_admin(cls, user, password):
        return User.create_web_user(user, password, [Role.ADMIN])
    
    @classmethod
    def create_web_user(cls, name, password, roles=[]):
        user = User(user_id=name, key_name=name, name=name, 
                passhash= User.__create_password_hash(password), roles=roles)
        return user

    @classmethod
    def __create_password_hash(cls, password):
        return sha(password).hexdigest()
    
    def update_password(self, password):
        self.passhash = password
        self.put()

    def check_password(self, password):
        if self.passhash == password:
            return True
        else:
            return False
        
    def __str__(self):
        return "user %s" % self.key().name() if self.key() else super(User, self).__str__()
    
    def __repr__(self):
        return "<%s>" % self
    
    def has_role(self, role):
        return role in self.roles
    
    def set_as_speaker(self):
        self.add_role(Role.SPEAKER)
    
    def add_role(self, role):
        if not is_in_list(role, self.roles):
            self.roles.append(role)
    
    def is_user(self):
        return self.has_role(Role.USER)
    
    def is_admin(self): 
        return self.has_role(Role.ADMIN)
    
    def is_speaker(self): 
        return self.has_role(Role.SPEAKER)
    
    def can_edit(self):
        return self.is_speaker() or self.is_admin()
from google.appengine.ext import db
from aos.web_admin.permission import Permission
from common_utils import is_in_list
    
class Role(db.Model):
    USER = 'user'
    ADMIN = 'admin'
    
    ROLES = [USER, ADMIN]
        
    name = db.StringProperty()
    permissions = db.ListProperty(db.Key)

    @classmethod
    def build_role(cls, name, permissions=None):
        role = Role(name = name)
        if permissions: role.permissions.append(permissions)
        role.put()
        return role

    def __getattr__(self, name):
        if self.__is_permission(name): return self
        return self.has_permission(name)
    
    def __is_permission(self, name):
        return name == 'permission'
        
    def by_name(self, name):
        return db.Query(Role).filter('name', name).get()
    
    def add_permissions(self, permission_names):
        for i in range(len(permission_names)):
            self.permissions.append(Permission.build_permission(permission_names[i]).key())
        self.put()
    
    def has_permission(self, permission):
        return is_in_list(Permission.by_name(permission).key(), self.permissions)
'''
Created on 05/10/2011

@author: agualis
'''
from google.appengine.ext import db

class Permission(db.Model):    
    name = db.StringProperty()
    
    @classmethod
    def build_permission(cls, name):
        permission = Permission(key_name = name, name = name)
        permission.put()
        return permission
    
    def __getattr__(self, name):
        return self.__load_permission__(name)
    
    def __load_permission__(self, name):
        return Permission.by_name(name) is not None
    
    @classmethod
    def by_name(cls, name):
        return db.Query(Permission).filter('name', name).get()
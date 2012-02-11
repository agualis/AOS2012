'''Sessions for GAE in stored in memcache (only)

Created on Nov 24, 2009

@author: robert
'''
from google.appengine.api import memcache 
from django.contrib.sessions.backends import base as session_base

class SessionStore(session_base.SessionBase):
        
    def exists(self, session_key):
        """
        Returns True if the given session_key already exists.
        """
        return not memcache.get("ses_%s" % session_key) == None

    def create(self):
        """
        Creates a new session instance. Guaranteed to create a new object with
        a unique key and will have saved the result once (with empty data)
        before the method returns.
        """
        for i in xrange(10):
            self._session_key = self._get_new_session_key()
            try:
                self.save(must_create=True)
            except session_base.CreateError:
                continue
            self.modified = True
            return
        raise RuntimeError("Unable to create a new session key.")

    def save(self, must_create=False):
        """
        Saves the session data. If 'must_create' is True, a new session object
        is created (otherwise a CreateError exception is raised). Otherwise,
        save() can update an existing object with the same key.
        """
        if must_create:
            func = memcache.add
        else:
            func = memcache.set
        result = func("ses_%s" % self.session_key, self._get_session(no_load=must_create),
                self.get_expiry_age())
        if must_create and not result:
            raise session_base.CreateError

    def delete(self, session_key=None):
        """
        Deletes the session data under this key. If the key is None, the
        current session key value is used.
        """
        if session_key is None:
            if self._session_key is None:
                return
            session_key = self._session_key
        memcache.delete("ses_%s" % session_key)

    def load(self):
        """
        Loads the session data and returns a dictionary.
        """
        session_data = memcache.get("ses_%s" % self.session_key)
        if session_data is not None:
            return session_data
        self.create()
        return {}
    

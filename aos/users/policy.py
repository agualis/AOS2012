from aos.users.authentication import AuthorizationPolicy
from aos.web_admin.role import Role

class OwnerOrUserPolicy(AuthorizationPolicy):
    def permits(self, user, request, pos_key_name=None, **kwargs):
        if user.is_user():
            return True
        if user.has_role(Role.ADMIN):
            return True

class AdminPolicy(OwnerOrUserPolicy):
    def permits(self, user, request, pos_key_name=None, **kwargs):
        if user.has_role(Role.ADMIN):
            return True
        else:
            return False
        

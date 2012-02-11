import unittest
from aos.web_admin.role import Role
from aos.web_admin.role import Permission
import logging

class RoleTestCase(unittest.TestCase):
        
    def setUp(self):
        self.permission = Permission.build_permission("admin_menu")
        self.role = Role.build_role(Role.ADMIN, self.permission.key())
        
    def test_admin_role(self):
        self.assertEquals(Role.ADMIN, self.role.by_name(Role.ADMIN).name)
    
    def test_has_admin_menu_permission(self):
        self.assertTrue(self.role.has_permission(self.permission.name))
        
    def test_contains_two_permissions(self):
        self.role.permissions.append(Permission.build_permission('other').key())
        self.assertTrue(len(self.role.permissions) == 2)
    
    def test_has_two_permissions(self):
        self.role.permissions.append(Permission.build_permission('other').key())
        for permission in self.role.permissions:
            self.assertTrue(self.role.has_permission(Permission.get(permission).name))
    
    def test_roles_have_different_permissions(self):
        self.admin_role = Role.build_role(Role.ADMIN)
        self.assertFalse(self.admin_role.has_permission(self.permission.name))
        
    def test_permission(self):
        self.assertTrue(self.role.permission.admin_menu)

    def test_add_permissions(self):
        permission_names = ['perm1, perm2, perm3']
        self.role.add_permissions(permission_names)
        for i in range(len(permission_names)):
            self.assertTrue(getattr(self.role.permission, permission_names[i]))
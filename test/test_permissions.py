import unittest
from aos.web_admin.permission import Permission

class PermissionTestCase(unittest.TestCase):

    def setUp(self):
        self.permission = Permission(name = "menu_general")
        self.permission.put()
     
    def test_calling_an_existing_method(self):
        self.assertFalse(self.permission.hello)
           
    def test_when_permission_is_defined(self):
        self.assertTrue(self.permission.menu_general)
        
    def test_get_permission_by_name(self):
        self.assertEquals(self.permission.name, Permission.by_name('menu_general').name)

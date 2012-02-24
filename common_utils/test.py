from google.appengine.ext import testbed
class TestBedInitializer():
    def init_testbed_for_datastore_tests(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        
    def init_django_settings(self):
        import settings
        import os
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import os
import traceback
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#This 2 lines must appear before other GAE imports in order to avoid Django version conflicts
from google.appengine.dist import use_library
use_library('django', '1.2')

import logging
import django.core.handlers.wsgi
from google.appengine.ext.webapp import util

def real_main():
    # Create a Django application for WSGI.
    application = django.core.handlers.wsgi.WSGIHandler()
    # Run the WSGI CGI handler with that application.
    util.run_wsgi_app(application)
    
def profile_main():
    # This is the main function for profiling
    # We've renamed our original main() above to real_main()
    import cProfile, pstats, StringIO
    prof = cProfile.Profile()
    prof = prof.runctx("real_main()", globals(), locals())
    stream = StringIO.StringIO()
    stats = pstats.Stats(prof, stream=stream)
    stats.sort_stats("time")  # Or cumulative
    stats.print_stats(80)  # 80 = how many to print
    # The rest is optional.
    # stats.print_callees()
    # stats.print_callers()
    logging.info("Profile data:\n%s", stream.getvalue())

if __name__ == '__main__':
    real_main()
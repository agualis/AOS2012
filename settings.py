import os
import logging
DEBUG = True
# Force debug to off on the real Google App Engine

if os.environ.get('SERVER_SOFTWARE','').startswith('Goog'):
    DEBUG = False
    logging.disable(logging.INFO)
        
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alberto Gualis', 'alberto@frogtek.org'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = '!7&72la6nrui)%h@l8_z@x!%14ix!a=kg=_zjfri#6gqq9*gq='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'google.appengine.ext.appstats.recording.AppstatsDjangoMiddleware',
)
SESSION_COOKIE_AGE = 1800 #half hour in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_ENGINE = 'aos.lib.common_utils.sessions'

LOGIN_URL = '/login'
ROOT_URLCONF = 'urls'

ROOT_PATH = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH, 'templates')
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.i18n",
)

INSTALLED_APPS = (
    # 'django.contrib.contenttypes',
    'aos'
)

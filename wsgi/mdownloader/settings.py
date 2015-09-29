# Django settings for a generic project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587

EMAIL_HOST_USER = 'TuFanatico5@gmail.com'
DEFAULT_FROM_EMAIL = 'TuFanatico5@gmail.com'
SERVER_EMAIL = 'TuFanatico5@gmail.com'
EMAIL_HOST_PASSWORD='bmfkhmpzitaslgnp'

ADMINS = (
    ('', ''),
)

MANAGERS = ADMINS

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "lansnake.db",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
        }
    }


TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = ''

MEDIA_URL = ''

STATIC_ROOT = os.path.abspath(os.path.dirname(__file__))+'/static'

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

#STATIC_ROOT = os.path.abspath(os.getcwd())+'/static'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT,'static/img'),
)

SECRET_KEY = '0tc6gk^8x=lfzyh0&amp;%1u^7tu0wb(aho7o6+6!*yr!=#c#b4c$@'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

BUFER=0


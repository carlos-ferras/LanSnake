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

EMAIL_HOST_PASSWORD='~LanSnake~'


ADMINS = (
    ('Carlos Ferras', 'c4rlos.ferra5@gmail.com'),
)

MANAGERS = ADMINS

if 'VCAP_SERVICES' in os.environ:
    import json
    vcap_services = json.loads(os.environ['VCAP_SERVICES'])
    mysql_srv = vcap_services['mysql-5.1'][0]
    cred = mysql_srv['credentials']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': cred['name'],
            'USER': cred['user'],
            'PASSWORD': cred['password'],
            'HOST': cred['hostname'],
            'PORT': cred['port'],
            }
        }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "dev.db",
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

STATIC_ROOT = ''

STATIC_URL = '/static/'

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
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

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
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


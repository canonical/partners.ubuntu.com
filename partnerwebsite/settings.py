"""
Django settings for partnerwebsite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-q7g=b=d0($mr8vxb!_*-1aly29)v3@$ku(n5))z=orggymy9)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
    '.ubuntu.qa'
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'cms',
    'south',
    'django_openid_auth',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'partnerwebsite.urls'

WSGI_APPLICATION = 'partnerwebsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'partners',
        'USER': 'postgres',
        'PASSWORD': 'dev',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Update database settings from DATABASE_URL environment variable
import dj_database_url
DATABASES['default'].update(dj_database_url.config())

if 'test' in sys.argv:
  DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-uk'

TIME_ZONE = 'Europe/London'

USE_I18N = False

USE_L10N = False

USE_TZ = True

TEMPLATE_DIRS = (BASE_DIR + "/templates")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = (BASE_DIR + "/static")

# Django openID auth
# ===

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

AUTHENTICATION_BACKENDS = (
    'django_openid_auth.auth.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = '/openid/login/'
LOGIN_REDIRECT_URL = '/'

OPENID_CREATE_USERS = True
OPENID_SSO_SERVER_URL = 'https://login.launchpad.net/'
OPENID_LAUNCHPAD_TEAMS_REQUIRED = ['partners.u.c-authors']
OPENID_USE_AS_ADMIN_LOGIN = True
OPENID_LAUNCHPAD_TEAMS_MAPPING_AUTO = True

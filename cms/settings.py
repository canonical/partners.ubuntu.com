# Standard library
import os
import sys

# Packages
import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = os.environ.get("DJANGO_DEBUG", "false").lower() == "true"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.auth",
    "django_openid_auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cms",
    "markdown_deux",
]

MIDDLEWARE = (
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "cms.urls"

WSGI_APPLICATION = "cms.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Set up DB
db_config = dj_database_url.config()

if not db_config:
    print("Error: DATABASE_URL environment variable is required")
    sys.exit(4)

DATABASES = {"default": db_config}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = "en-uk"

TIME_ZONE = "Europe/London"

USE_I18N = False

USE_L10N = False

USE_TZ = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": {
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            }
        },
    }
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR + "/static"
STATICFILES_FINDERS = [
    "django_static_root_finder.finders.StaticRootFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django openID auth
# ===

SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"

AUTHENTICATION_BACKENDS = (
    "django_openid_auth.auth.OpenIDBackend",
    "django.contrib.auth.backends.ModelBackend",
)

LOGIN_URL = "/openid/login/"
LOGIN_REDIRECT_URL = "/"

OPENID_CREATE_USERS = True
OPENID_SSO_SERVER_URL = "https://login.launchpad.net/"
OPENID_LAUNCHPAD_TEAMS_REQUIRED = ["partners.u.c-authors"]
OPENID_USE_AS_ADMIN_LOGIN = True
OPENID_LAUNCHPAD_TEAMS_MAPPING_AUTO = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "error_file": {
            "level": "WARNING",
            "filename": os.path.join(BASE_DIR, "django-error.log"),
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1 * 1024 * 1024,
            "backupCount": 2,
        }
    },
    "loggers": {
        "django": {
            "handlers": ["error_file"],
            "level": "WARNING",
            "propagate": True,
        }
    },
}

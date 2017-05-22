"""
WSGI config for the partners.ubuntu.com project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

# Core
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.settings")

# Modules
from django.core.wsgi import get_wsgi_application  # noqa
from whitenoise.django import DjangoWhiteNoise  # noqa

application = DjangoWhiteNoise(get_wsgi_application())


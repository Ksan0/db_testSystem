"""
WSGI config for db_testSystem project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""


import sys, os

# sys.path.append('/var/www/ksan/data/www/db_testSystem')
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db_testSystem.settings")

BASE_DIR = os.path.dirname(__file__) + '/..'
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db_testSystem.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
"""
WSGI config for db_testSystem project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""


import sys, os
sys.path.append('/var/www/ksan/data/www/db_testSystem')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db_testSystem.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

"""

import os, sys

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

sys.path.append('/var/www/ksan/data/www/cimg.ru')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
"""
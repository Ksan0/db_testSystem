from datetime import timedelta

from django.utils import timezone
from db_testSystem.models import *
from db_testSystem.settings_system import *


def user_time_update(user):
    if True:
    #try:
        session = UserSession.objects.get(user=user, running=True)
    #except:
    #    return -1
    have_time = session.registered_at + timedelta(minutes=TIME_FOR_ATTEMPT) - timezone.now()
    have_minutes = have_time.total_seconds() / 60
    if have_minutes <= 0:
        session.running = False
        session.save()
    return int(have_minutes)


def toHex(x):
    return "".join([hex(ord(c))[2:].zfill(2) for c in x])


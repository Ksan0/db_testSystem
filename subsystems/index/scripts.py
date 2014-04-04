from datetime import timedelta

from django.utils import timezone

from subsystems.db_raw_sql_works.DB import Review
from db_testSystem.models import *
from db_testSystem.settings_system import *
import json
import datetime


def user_time_update(user):
    try:
        session = UserSession.objects.get(user=user, running=True)
    except:
        return -1
    have_time = session.registered_at + timedelta(minutes=TIME_FOR_ATTEMPT) - timezone.now()
    have_minutes = have_time.total_seconds() / 60
    if have_minutes <= 0:
        session.running = False
        session.save()
    return int(have_minutes)


def toHex(x):
    return "".join([hex(ord(c))[2:].zfill(2) for c in x])


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            encoded_object = str(obj)
        else:
            encoded_object =json.JSONEncoder.default(self, obj)
        return encoded_object



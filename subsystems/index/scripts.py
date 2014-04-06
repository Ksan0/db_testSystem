from datetime import timedelta

from django.utils import timezone
from db_testSystem.models import *
from db_testSystem.settings_system import *
from user_messages import UserMessage


def get_user_message(request):
    try:
        return UserMessage(request.GET['user_msg'])
    except:
        return None


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


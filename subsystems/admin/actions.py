# encoding: utf-8
from db_testSystem.models import *
from forms import *
from scripts import *


def action(request):
    try:
        action = request.GET['action']
    except:
        return {'error': 'no action'}

    if action == 'create_user':
        form = UserForm(request.POST)
        password = random_str(size=8)

        try:
            User.objects.get(username=form.data['login'])
            return {'error': 'user exists'}
        except:
            pass  # юзер не существует

        try:
            User.objects.create_user(username=form.data['login'], password=password)
        except:
            return {'error': 'can\'t create user'}

        return {'error': ''}
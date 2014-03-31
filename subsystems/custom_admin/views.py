# coding: utf-8

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from db_testSystem.models import *
from django.contrib.auth.decorators import login_required
from output_models import *


@login_required(redirect_field_name='')
def user_stats(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')

    user = User.objects.get(username=request.GET['login'])
    user_sessions = UserSession.objects.filter(user=user).order_by('-rk', '-attempt')
    user_sessions_output = []
    for usr_sess in user_sessions:
        user_sessions_output.append(UserSessionOutputModel(usr_sess))

    return render(request, 'custom_admin_userinfo.html', {
        'user_sessions': user_sessions_output
    })


@login_required(redirect_field_name='')
def test_stats(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')

    return render(request, 't2.html', {'msg': 'ok'})


@login_required(redirect_field_name='')
def index(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')

    users = User.objects.filter(is_superuser=False)
    rks = RK.objects.all()
    return render(request, 'custom_admin_index.html', {
        'users': users,
        'tests': rks
    })
# coding: utf-8

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from db_testSystem.models import *
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name='')
def statistic(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')

    return render(request, 't2.html', {'msg': 'ok'})


@login_required(redirect_field_name='')
def index(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')

    return render(request, 't2.html', {'msg': 'ok'})
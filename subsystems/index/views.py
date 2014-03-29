from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from forms import *
from db_testSystem.models import *


def login_view(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            return HttpResponseRedirect('admin/')
        return HttpResponseRedirect('/')

    if request.method == 'GET':
        return render(request, 'login.html', {'login_form': LoginForm()})

    form = LoginForm(request.POST)
    user = authenticate(username=form.data["login"], password=form.data["password"])
    if user is None:
        return render(request, 'login.html', {
            'login_form': form,
            'error_msg': 'bad login or password'
        })

    if not user.is_active:
        return render(request, 'login.html', {
            'login_form': form,
            'error_msg': 'user is disabled'
        })

    login(request, user)
    if user.is_superuser:
        if 'next' in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        return HttpResponseRedirect('admin/')

    if 'next' in request.GET:
        return HttpResponseRedirect(request.GET['next'])
    return HttpResponseRedirect('/')
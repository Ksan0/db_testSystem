from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from forms import *
from db_testSystem.models import *
from django.contrib.auth.decorators import login_required


static_context = {
    'tests_url': 'tests/',
    'login_url': 'login/',
    'logout_url': 'logout/'
}


class OutputRKModel(RK):
    def __init__(self, sup, user):
        self.id = sup.id
        self.title = sup.title
        self.description = sup.description

        try:
            self.attemptes_amount = 3 - Attempt.objects.get(user=user, rk=sup)
        except:
            self.attemptes_amount = 3
            Attempt.objects.create(user=user, rk=sup, used=1)


@login_required(redirect_field_name='')
def index(request):
    template_name = 'test_list.html'

    tests = []
    for obj in RK.objects.filter(is_active=True):
        tests.append(OutputRKModel(obj, request.user))

    context = {
        'user': request.user,
        'tests': tests
    }
    context.update(static_context)
    return render(request, template_name, context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    template_name = 'auth.html'

    if request.user.is_authenticated():
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        return HttpResponseRedirect('/')

    if request.method == 'GET':
        context = {'form': LoginForm()}
        context.update(static_context)
        return render(request, template_name, context)

    form = LoginForm(request.POST)
    user = authenticate(username=form.data["login"], password=form.data["password"])
    if user is None:
        return render(request, template_name, {
            'form': form,
            'error_msg': 'bad login or password'
        })

    if not user.is_active:
        return render(request, template_name, {
            'form': form,
            'error_msg': 'user is disabled'
        })

    login(request, user)
    if user.is_superuser:
        if 'next' in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        return HttpResponseRedirect('/admin/')

    if 'next' in request.GET:
        return HttpResponseRedirect(request.GET['next'])
    return HttpResponseRedirect('/')
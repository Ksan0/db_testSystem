from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from actions import action
from forms import *


#@login_required
def index(request):
    #if not request.user.is_superuser:
    #    return HttpResponseRedirect('/')
    return render(request, 'reg.html', {'form': UserForm()})


#@login_required
def make(request):
    #if not request.user.is_superuser:
    #    return HttpResponseRedirect('/')

    ret = action(request)

    return render(request, 'ok.html', {
        'msgs': (ret,),
    })
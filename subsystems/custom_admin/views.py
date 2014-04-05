# coding: utf-8

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from db_testSystem.models import *
from django.contrib.auth.decorators import login_required
from output_models import *
from subsystems.index.scripts import user_time_update


@login_required(redirect_field_name='')
def user_stats(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/custim-admin/')

    try:
        user = User.objects.get(username=request.GET['login'])
    except:
        return HttpResponseRedirect('/custom-admin/')

    user_time_update(user)
    user_sessions = UserSession.objects.filter(user=user).order_by('-rk', '-attempt')
    user_sessions_output = []
    for usr_sess in user_sessions:
        user_sessions_output.append(UserSessionOutputModel(usr_sess))

    return render(request, 'custom_admin/userinfo.html', {
        'user_sessions': user_sessions_output,
        'student': user,
        'is_admin': True,
        'hide_tests_url': True
    })



def statistic_user(request, id):
    try:
        user = User.objects.get(id=id)
    except:
        return HttpResponseRedirect('/admin/')

    user_time_update(user)
    user_sessions = UserSession.objects.filter(user=user).order_by('-rk', '-attempt')
    user_sessions_output = []
    for usr_sess in user_sessions:
        user_sessions_output.append(UserSessionOutputModel(usr_sess))

    return render(request, 'custom_admin/userinfo.html', {
        'user_sessions': user_sessions_output,
        'student': user,
        'is_admin': True,
        'hide_tests_url': True
    })


def statistic_question(request, id):
    try:
        question = Question.objects.get(id=id)
    except:
        return HttpResponseRedirect('/admin/')

    answers = SessionQuestions.objects.filter(question=question)
    return render(request, 'custom_admin/statistic_question.html', {
        'question': question,
        'answers': answers
    })


@login_required(redirect_field_name='')
def statistic(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')

    try:
        type = request.GET['type']
        id = request.GET['id']
    except:
        return HttpResponseRedirect('/admin/')

    if type == 'user':
        return statistic_user(request, id)
    if type == 'question':
        return statistic_question(request, id)

    return HttpResponseRedirect('/admin/')


@login_required(redirect_field_name='')
def index(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')

    users = User.objects.filter(is_superuser=False)
    # rks = RK.objects.all()
    return render(request, 'custom_admin/index.html', {
        'users': users,
        'is_admin': True,
        'hide_tests_url': True,
        'is_custom_admin_index': True
        #'tests': rks
    })
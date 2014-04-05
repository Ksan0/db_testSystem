# coding: utf-8

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from db_testSystem.models import *
from django.contrib.auth.decorators import login_required
from output_models import *
from subsystems.index.scripts import user_time_update
import re


@login_required(redirect_field_name='')
def test_question(request):
    if not request.user.is_superuser:
        return render(request, 't.html', {
            'msg': json.dumps({'error': 'Access denied'}, cls=CustomJSONEncoder)
        })

    try:
        query = request.POST['message']
    except:
        return render(request, 't.html', {
            'msg': json.dumps({'error': 'POST error'}, cls=CustomJSONEncoder)
        })

    reviewer = Review()
    back = reviewer.select(query)
    if back['error']:
        msg = {'sql_query_error': back['error']}
    else:
        msg = back['records']

    msg = json.dumps(msg, cls=CustomJSONEncoder)

    return render(request, 't.html', {
        'msg': msg
    })


def user_add_attempt(request):
    try:
        user = User.objects.get(id=request.GET['uid'])
        rk = RK.objects.get(id=request.GET['rkid'])
    except:
        return render(request, 't.html', {
            'msg': json.dumps({'error': 'Args error'}, cls=CustomJSONEncoder)
        })

    try:
        attempt = Attempt.objects.get(user=user, rk=rk)
        attempt.have += 1
        attempt.save()
    except:
        attempt = Attempt.objects.create(user=user, rk=rk, have=ATTEMPTES_MAX + 1)

    return render(request, 't.html', {
        'msg': 'OK'
    })


def make_user_answer_right(request):
    try:
        user = User.objects.get(id=request.GET['uid'])
        rk = RK.objects.get(id=request.GET['rkid'])
        attempt = request.GET['attid']
        question = Question.objects.get(id=request.GET['queid'])
    except:
        return render(request, 't.html', {
            'msg': json.dumps({'error': 'Args error'}, cls=CustomJSONEncoder)
        })

    try:
        session = UserSession.objects.get(user=user, rk=rk, attempt=attempt)
        session_question = SessionQuestions.objects.get(session=session, question=question)
        session_question.is_right = True
        session_question.save()
    except:
        return render(request, 't.html', {
            'msg': json.dumps({'error': 'Internal server error'}, cls=CustomJSONEncoder)
        })

    return render(request, 't.html', {
        'msg': 'OK'
    })


@login_required(redirect_field_name='')
def user_action(request):
    if not request.user.is_superuser:
        return render(request, 't.html', {
            'msg': json.dumps({'error': 'Access denied'}, cls=CustomJSONEncoder)
        })

    try:
        type = request.GET['type']
    except:
        return render(request, 't.html', {
            'msg': json.dumps({'error': 'Wrong action type'}, cls=CustomJSONEncoder)
        })

    if type == 'add_attempt':
        return user_add_attempt(request)

    if type == 'answer_is_right':
        return make_user_answer_right(request)

    return render(request, 't.html', {
        'msg': json.dumps({'error': 'Wrong action type'}, cls=CustomJSONEncoder)
    })


def statistic_user(request, id):
    try:
        user = User.objects.get(id=id)
    except:
        return HttpResponseRedirect('/admin/')

    user_time_update(user)
    user_sessions = UserSession.objects.filter(user=user)  # .order_by('-rk', '-attempt')
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

    answers = SessionQuestions.objects.filter(question=question).order_by('is_right')
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
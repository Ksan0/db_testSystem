# coding: utf-8

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
# from django.views.decorators.csrf import csrf_exempt
from db_testSystem.models import *
from django.contrib.auth.decorators import login_required
from output_models import *
from subsystems.index.scripts import user_time_update
from scripts import *
from subsystems.db_raw_sql_works.DB import MySQLReviewer, NoSQLReviewer


@login_required(redirect_field_name='')
def test_question(request):
    if not request.user.is_superuser:
        return render(request, 't.html', {
            'msg': json.dumps({'error': 'Access denied'}, cls=CustomJSONEncoder)
        })

    try:
        query = request.POST['message']
        type_txt = request.POST['type_txt']
        type = QuestionType.objects.get(title=type_txt)
    except:
        return render(request, 't.html', {
            'msg': json.dumps({'error': 'POST error'}, cls=CustomJSONEncoder)
        })

    if type.isSQLQuery():
        model = MySQLReviewer
    elif type.isNoSQLQuery():
        model = NoSQLReviewer
    else:
        return render(request, 't.html', {
            'msg': json.dumps({'error': 'wrong type'}, cls=CustomJSONEncoder)
        })

    with model() as reviewer:
        back = reviewer.execute(query)

    if back['error']:
        msg = {'query_error': back['error']}
    else:
        msg = back['records']

    msg = json.dumps(msg, cls=CustomJSONEncoder)

    return render(request, 't.html', {
        'msg': msg
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


@login_required(redirect_field_name='')
def question_action(request):
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

    if type == 'recalc':
        return recalc_question(request)

    return render(request, 't.html', {
            'msg': json.dumps({'error': 'Wrong action type'}, cls=CustomJSONEncoder)
        })


@login_required(redirect_field_name='')
def statistic(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')

    try:
        type = request.GET['type']
    except:
        return HttpResponseRedirect('/admin/')

    if type == 'user':
        return statistic_user(request)
    if type == 'question':
        return statistic_question(request)
    if type == 'rk':
        return statistic_tech(request)

    return HttpResponseRedirect('/admin/')


@login_required(redirect_field_name='')
def index(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')

    users = []
    for user in User.objects.filter(is_staff=False, is_superuser=False):
        users.append(UserOutputModel(user))

    return render(request, 'custom_admin/index.html', {
        'users': users,
        'is_admin': True,
        'hide_tests_url': True,
        'is_custom_admin_index': True
        #'tests': rks
    })
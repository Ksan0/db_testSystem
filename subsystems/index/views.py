# coding: utf-8

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from forms import *
from db_testSystem.models import *
from django.contrib.auth.decorators import login_required
from scripts import *
from output_models import *
from random import choice
import string
from datetime import timedelta
from user_messages import *


static_context = {
    'tests_url': '/tests/',
    'login_url': '/login/',
    'logout_url': '/logout/',
    'pass_restore_url': '/password_restore/',
}


@login_required(redirect_field_name='')
def index(request, other_context=None):  # list of RK
    is_admin = request.user.is_superuser

    template_name = 'test_list.html'

    tests = []
    for obj in RK.objects.filter(is_active=True):
        tests.append(OutputRKModel(obj, request.user))

    context = {
        'user': request.user,
        'is_admin': is_admin,
        'is_user_index': True,
        'tests': tests,
        'have_time': user_time_update(request.user)
    }
    context.update(static_context)
    if other_context is not None:
        context.update(other_context)
    return render(request, template_name, context)


def password_restore_confirm(request):
    try:
        username = request.GET['login']
        confirm = request.GET['confirm']

        user = User.objects.get(username=username)
        passw_hex = toHex(user.password)
        if confirm != passw_hex:
            return login_view(request, {
                'error_msg': CONFIRM_FAILED
            })

        new_pass = ''.join([choice(string.ascii_uppercase) for _ in xrange(12)])
        user.set_password(new_pass)
        user.save()

        send_mail('Restore successful', 'Ваш новый пароль: {0}'.format(new_pass), 'db.testSystem@gmail.com', [user.email])
        return login_view(request, {
            'success_msg': CONFIRM_SUCCESS
        })
    except:
        return login_view(request, {
            'error_msg': CONFIRM_FAILED
        })


def password_restore(request):
    try:
        restore_form = PassRestoreForm(request.POST)
        username = restore_form.data['login']
        user = User.objects.get(username=username)
        password = toHex(user.password)
        msg =   ('Что бы восстановить пароль, перейдите по ссылке\n'
                'http://localhost:8000/password_restore_confirm?'
                'login={0}&confirm={1}').format(username, password)

        send_mail('Password restore', msg, 'db.testSystem@gmail.com', [user.email])

        request.method = 'GET'

        return login_view(request, {
            'success_msg': LOOK_AT_MAIL
        })
    except:
        request.method = 'GET'

        return login_view(request, {
            'error_msg': NO_USER
        })


@login_required(redirect_field_name='')
def close_session(request):
    user_session = UserSession.objects.get(user=request.user, running=True)
    user_session.running = False
    user_session.save()
    return HttpResponseRedirect('/')


def test_answer(request):
    try:
        testid = request.GET['testid']
    except:
        HttpResponseRedirect('/')
    try:
        queid = request.GET['queid']
    except:
        HttpResponseRedirect('/tests/?testid={0}'.format(testid))

    good_ids = False
    try:
        question = Question.objects.get(id=queid)
        rk = RK.objects.get(id=testid)
        attempt = Attempt.objects.get(user=request.user, rk=rk)
        user_session = UserSession.objects.get(user=request.user, rk=rk, attempt=attempt.used)
        session_question = SessionQuestions.objects.get(session=user_session, question=question)
        good_ids = True
        # если это все отработало, значит такая сессия действительно существует
    except:
        pass

    if not good_ids:
        HttpResponseRedirect('/')

    if user_time_update(request.user) <= 0:
        return render(request, 't.html', {
            'msg': NO_TIME
        })
    if not user_session.running:
        return render(request, 't.html', {
            'msg': SESSION_CLOSED
        })

    if request.method != 'POST':
        HttpResponseRedirect('/question/?testid={0}&queid={1}')

    form = AnswerForm(request.POST)

    reviewer = Review(sql_query=form.data['answer'])

    #session_question.last_answer = form.data['answer']
    #session_question.is_right = reviewer.is_user_right
    back = reviewer.user_records
    error = reviewer.error
    #session_question.save()

    return render(request, 't.html', {
        'msg': error and 'Syntax error' or back
    })


@login_required(redirect_field_name='')
def question(request):
    template_name = 'answer_form.html'

    have_time = user_time_update(request.user)
    if have_time <= 0:
        return index(request, {
            'warn_msg': NO_TIME
        })

    try:
        rk_id = request.GET['testid']
    except:
        return HttpResponseRedirect('/')

    try:
        que_id = request.GET['queid']
    except:
        return HttpResponseRedirect('/tests/?testid={0}'.format(rk_id))

    context = {
    }
    context.update(static_context)

    good_ids = False
    try:
        question = Question.objects.get(id=que_id)
        rk = RK.objects.get(id=rk_id)
        attempt = Attempt.objects.get(user=request.user, rk=rk)
        user_session = UserSession.objects.get(user=request.user, rk=rk, attempt=attempt.used)
        session_question = SessionQuestions.objects.get(session=user_session, question=question)
        good_ids = True
        # если это все отработало, значит такая сессия действительно существует
    except:
        pass

    if not user_session.running:
        return index(request, {
            'warn_msg': SESSION_CLOSED
        })

    if not good_ids:
        return HttpResponseRedirect('/tests/')

    if request.method == 'GET':
        form = AnswerForm({'answer': session_question.last_answer})
        context.update({
            'form': form,
            'testid': rk_id,
            'question': question,
            'have_time': have_time
        })
        return render(request, template_name, context)

    form = AnswerForm(request.POST)
    context.update({'form': form})

    reviewer = Review(sql_query=form.data['answer'], right_sql_query=question.answer)

    session_question.last_answer = form.data['answer']
    session_question.is_right = reviewer.is_user_right
    back = reviewer.user_records
    error = reviewer.error
    session_question.save()

    return HttpResponseRedirect('/tests/?testid={0}'.format(rk_id))


def start_new_session(request, user, rk, attempt):
    try:
        confirm = request.GET['confirm_start']
    except:
        confirm = ''

    if confirm != 'yes':
        return HttpResponseRedirect('/')

    if attempt.have <= 0:
        return index(request, {
            'error_msg': NO_ATTEMPTES
        })

    indexes = []
    for obj in Question.objects.filter(rk=rk, is_active=True):
        indexes.append(obj.id)

    good_indexes = []
    for i in range(min(QUESTIONS_COUNT, len(indexes))):
        ch = choice(indexes)
        good_indexes.append(ch)
        indexes.remove(ch)

    attempt.used += 1
    attempt.have -= 1
    attempt.save()
    user_session = UserSession.objects.create(user=user, rk=rk, attempt=attempt.used)

    questions = []
    for id in good_indexes:
        question = Question.objects.get(id=id)
        questions.append(question)
        SessionQuestions.objects.create(session=user_session, question=question)

    context = {
        'question_list': questions,
        'testid': rk.id,
        'have_time': user_time_update(user)
    }
    context.update(static_context)
    return render(request, 'question_list.html', context)


@login_required(redirect_field_name='')
def test(request):
    have_time = user_time_update(request.user)

    try:
        rk_id = request.GET['testid']
        rk = RK.objects.get(id=rk_id)
    except:
        return HttpResponseRedirect('/')

    try:
        attempt = Attempt.objects.get(user=request.user, rk=rk)
    except:
        attempt = Attempt.objects.create(user=request.user, rk=rk, used=0)
        return start_new_session(request, request.user, rk, attempt)

    try:
        user_session = UserSession.objects.get(user=request.user, rk=rk, attempt=attempt.used)
    except:
        if have_time > 0:
            return index(request, {
                'error_msg': ANOTHER_TEST_RUNNING
            })
        return start_new_session(request, request.user, rk, attempt)

    if not user_session.running:
        return start_new_session(request, request.user, rk, attempt)

    questions_s = SessionQuestions.objects.filter(session=user_session)
    questions = []
    for que_s in questions_s:
        status = ''
        if que_s.last_answer != '':
            status = 'sended'
        questions.append(OutputQuestionModel(que_s.question, status))

    context = {
        'question_list': questions,
        'testid': rk_id,
        'have_time': have_time
    }
    context.update(static_context)
    return render(request, 'question_list.html', context)


def login_view(request, extra_context=None):
    template_name = 'auth.html'

    context = {
        'form_auth': LoginForm(),
        'form_pass_restore': PassRestoreForm(),
        'is_login_page': 'True'
    }
    if extra_context is not None:
        context.update(extra_context)
    context.update(static_context)

    if request.method == 'GET':
        if request.user.is_authenticated():
            if request.user.is_superuser:
                return HttpResponseRedirect('/admin/')
            return HttpResponseRedirect('/')
        return render(request, template_name, context)

    form_auth = LoginForm(request.POST)
    context.update({'form_auth': form_auth})
    user = authenticate(username=form_auth.data["login"], password=form_auth.data["password"])

    if user is None:
        context.update({'error_msg': LOGIN_FAILED})
        return render(request, template_name, context)

    if not user.is_active:
        context.update({'error_msg': DISABLED_USER})
        return render(request, template_name, context)

    login(request, user)
    if user.is_superuser:
        if 'next' in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        return HttpResponseRedirect('/admin/')

    if 'next' in request.GET:
        return HttpResponseRedirect(request.GET['next'])
    return HttpResponseRedirect('/')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
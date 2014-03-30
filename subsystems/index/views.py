# coding: utf-8

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from forms import *
from db_testSystem.models import *
from django.contrib.auth.decorators import login_required
from random import choice
import string
from DB import *


static_context = {
    'tests_url': '/tests/',
    'login_url': '/login/',
    'logout_url': '/logout/',
    'pass_restore_url': '/password_restore/'
}
ATTEMPTES_MAX = 3
QUESTIONS_COUNT = 10


class OutputRKModel(RK):
    def __init__(self, sup, user):
        self.id = sup.id
        self.title = sup.title
        self.description = sup.description

        try:
            self.attemptes_amount = ATTEMPTES_MAX - Attempt.objects.get(user=user, rk=sup).used
        except:
            self.attemptes_amount = ATTEMPTES_MAX


class OutputQuestionModel(Question):
    def __init__(self, sup, status):
        self.id = sup.id
        self.description = sup.description
        self.status = status


@login_required(redirect_field_name='')
def index(request, other_context=None):  # list of RK
    template_name = 'test_list.html'

    tests = []
    for obj in RK.objects.filter(is_active=True):
        tests.append(OutputRKModel(obj, request.user))

    context = {
        'user': request.user,
        'tests': tests
    }
    context.update(static_context)
    if other_context is not None:
        context.update(other_context)
    return render(request, template_name, context)


def test_answer(sql_query, right_sql_query):
    return Review.check_answer(sql_query=sql_query, right_sql_query=right_sql_query)


def toHex(x):
    return "".join([hex(ord(c))[2:].zfill(2) for c in x])

def password_restore_confirm(request):
    try:
        username = request.GET['login']
        confirm = request.GET['confirm']

        user = User.objects.get(username=username)
        passw_hex = toHex(user.password)
        if confirm != passw_hex:
            return login_view(request, {
                'error_msg': 'confirm failed'
            })

        new_pass = ''.join([choice(string.ascii_uppercase) for _ in xrange(12)])
        user.set_password(new_pass)
        user.save()

        send_mail('Password restore', 'Ваш новый пароль: {0}'.format(new_pass), 'db.testSystem@gmail.com', ['kgfq@mail.ru'])
        return login_view(request, {
            'success_msg': 'confirm success'
        })
    except:
        return login_view(request, {
            'error_msg': 'confirm failed'
        })


def password_restore(request):
    try:
        restore_form = PassRestoreForm(request.POST)
        username = restore_form.data['login']
        password = toHex(User.objects.get(username=username).password)
        msg =   ('Что бы восстановить пароль, перейдите по ссылке\n'
                'http://localhost:8000/password_restore_confirm?'
                'login={0}&confirm={1}').format(username, password)

        send_mail('Password restore', msg, 'db.testSystem@gmail.com', ['kgfq@mail.ru'])

        request.method = 'GET'

        return login_view(request, {
            'success_msg': 'look at mail'
        })
    except:
        request.method = 'GET'

        return login_view(request, {
            'error_msg': 'no user'
        })


def answer(request):
    try:
        testid = request.GET['testid']
    except:
        HttpResponseRedirect('/')
    try:
        queid = request.GET['queid']
    except:
        HttpResponseRedirect('/tests/?testid={0}'.format(testid))
    try:
        type = request.GET['type']
    except:
        HttpResponseRedirect('/question/?testid={0}&queid={1}'.format(testid, queid))

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

    if request.method != 'POST':
        HttpResponseRedirect('/question/?testid={0}&queid={1}')

    if not good_ids:
        HttpResponseRedirect('/')

    form = AnswerForm(request.POST)
    if type == 'answer':
        session_question.last_answer = form.data['answer']
        session_question.is_right, back = test_answer(form.data['answer'], question.answer)
        session_question.save()
        return render(request, 't.html', {
            'msg': 'fgkdfjg'
        })

    return render(request, 't.html', {
        'msg': 'her obanoo'
    })

@login_required(redirect_field_name='')
def question(request):
    template_name = 'answer_form.html'

    try:
        rk_id = request.GET['testid']
    except:
        return HttpResponseRedirect('/')

    try:
        que_id = request.GET['queid']
    except:
        return HttpResponseRedirect('/test/')

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

    if not good_ids:
        return HttpResponseRedirect('/test/')

    if request.method == 'GET':
        form = AnswerForm()
        form.set_value(session_question.last_answer)
        context.update({
            'form': form,
            'testid': rk_id,
            'question': question
        })
        return render(request, template_name, context)

    form = AnswerForm(request.POST)
    context.update({'form': form})
    session_question.last_answer = form.data['answer']
    session_question.is_right, back = test_answer(form.data['answer'], question.answer)
    session_question.save()

    return HttpResponseRedirect('/tests/?testid={0}'.format(rk_id))


def start_new_session(request, user, rk, attempt):
    if attempt.used >= ATTEMPTES_MAX:
        return index(request, {'error_msg': 'no attemptes'})

    indexes = []
    for obj in Question.objects.filter(rk=rk, is_active=True):
        indexes.append(obj.id)

    good_indexes = []
    for i in range(min(QUESTIONS_COUNT, len(indexes))):
        ch = choice(indexes)
        good_indexes.append(ch)
        indexes.remove(ch)

    attempt.used += 1
    attempt.save()
    user_session = UserSession.objects.create(user=user, rk=rk, attempt=attempt.used)

    questions = []
    for id in good_indexes:
        question = Question.objects.get(id=id)
        questions.append(question)
        SessionQuestions.objects.create(session=user_session, question=question)

    context = {
        'question_list': questions,
        'testid': rk.id
    }
    context.update(static_context)
    return render(request, 'question_list.html', context)



@login_required(redirect_field_name='')
def test(request):
    try:
        rk_id = request.GET['testid']
        rk = RK.objects.get(id=rk_id)
    except:
        return index(request)

    try:
        attempt = Attempt.objects.get(user=request.user, rk=rk)
    except:
        attempt = Attempt.objects.create(user=request.user, rk=rk, used=0)
        return start_new_session(request, request.user, rk, attempt)

    try:
        user_session = UserSession.objects.get(user=request.user, rk=rk, attempt=attempt.used)
    except:
        return start_new_session(request, request.user, rk, attempt)

    if not user_session.running:
        return start_new_session(request, request.user, rk, attempt)

    questions_s = SessionQuestions.objects.filter(session=user_session)
    questions = []
    for que_s in questions_s:
        questions.append(OutputQuestionModel(que_s.question, que_s.last_answer == '' and '' or 'sended'))

    context = {
        'question_list': questions,
        'testid': rk_id
    }
    context.update(static_context)
    return render(request, 'question_list.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


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
        context.update({'error_msg': 'bad login or password'})
        return render(request, template_name, context)

    if not user.is_active:
        context.update({'error_msg': 'user is disabled'})
        return render(request, template_name, context)

    login(request, user)
    if user.is_superuser:
        if 'next' in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        return HttpResponseRedirect('/admin/')

    if 'next' in request.GET:
        return HttpResponseRedirect(request.GET['next'])
    return HttpResponseRedirect('/')

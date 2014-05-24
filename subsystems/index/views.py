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
from classes import CustomJSONEncoder


static_context = {
    'tests_url': '/tests/',
    'login_url': '/login/',
    'logout_url': '/logout/',
    'pass_restore_url': '/password_restore/',
}


# user_time_update called
@login_required(redirect_field_name='')
def index(request, other_context=None):  # list of RK
    running_added = False
    tests = []
    for obj in RK.objects.order_by('-is_active'):
        tests.append(OutputRKModel(obj, request.user))
        try:
            session = UserSession.objects.get(user=request.user, rk=obj, running=True)
            running_added = True
        except:
            pass

    try:
        session = UserSession.objects.get(user=request.user, running=True)
        if not running_added:
            tests.append(OutputRKModel(session.rk, request.user))
    except:
        pass

    context = {
        'user': request.user,
        'is_admin': request.user.is_superuser,
        'is_user_index': True,
        'tests': tests,
        'have_time': user_time_update(request.user),
        'user_msg': get_user_message(request),
    }
    context.update(static_context)
    if other_context is not None:
        context.update(other_context)
    return render(request, 'test_list.html', context)


def password_restore_confirm(request):
    try:
        username = request.GET['login']
        confirm = request.GET['confirm']

        user = User.objects.get(username=username)
        passw_hex = toHex(user.password)
        if confirm != passw_hex:
            return HttpResponseRedirect('/login/?{0}'.format('user_msg=confirm_failed'))

        new_pass = ''.join([choice(string.ascii_uppercase) for _ in xrange(12)])
        user.set_password(new_pass)
        user.save()

        msg = 'Ваш логин: {0}\nВаш новый пароль: {1}'.format(username, new_pass)
        send_mail('Password restore successful', msg, 'db.testSystem@gmail.com', [user.email])
        return HttpResponseRedirect('/login/?{0}'.format('user_msg=confirm_success'))
    except:
        return HttpResponseRedirect('/login/?{0}'.format('user_msg=confirm_failed'))


def password_restore(request):
    try:
        restore_form = PassRestoreForm(request.POST)
        username = restore_form.data['login']
        user = User.objects.get(username=username)
        password = toHex(user.password)
        msg = (
                'Что бы восстановить пароль, перейдите по ссылке\n'\
                'http://{0}/password_restore_confirm?login={1}&confirm={2}'
        ).format(INET_ADDRESS, username, password)

        send_mail('Password restore', msg, 'db.testSystem@gmail.com', [user.email])

        return HttpResponseRedirect('/login/?{0}'.format('user_msg=look_at_mail'))
    except:
        return HttpResponseRedirect('/login/?{0}'.format('user_msg=no_user'))


@login_required(redirect_field_name='')
def close_session(request):
    try:
        for user_session in UserSession.objects.filter(user=request.user, running=True):
            user_session.running = False
            user_session.save()
    except:
        pass
    return HttpResponseRedirect('/')


@login_required
def test_answer(request):
    try:
        testid = request.GET['testid']
    except:
        return render(request, 't.html', {
            'msg': 'Внутренняя ошибка'
        })

    try:
        queid = request.GET['queid']
    except:
        return render(request, 't.html', {
            'msg': 'Внутренняя ошибка'
        })

    if user_time_update(request.user) <= 0:
        return render(request, 't.html', {
            'msg': 'Время вышло'
        })

    try:
        question = Question.objects.get(id=queid)
        rk = RK.objects.get(id=testid)
        attempt = Attempt.objects.get(user=request.user, rk=rk)
        user_session = UserSession.objects.get(user=request.user, rk=rk, attempt=attempt.used)
        session_question = SessionQuestions.objects.get(session=user_session, question=question)
        # если это все отработало, значит такая сессия действительно существует
    except:
        HttpResponseRedirect('/')

    if not user_session.running:
        return render(request, 't.html', {
            'msg': 'Сессия закрыта'
        })

    try:
        form = AnswerForm(request.POST)

        if question.type.isSQLQuery():
            model = MySQLReviewer
        elif question.type.isNoSQLQuery():
            model = NoSQLReviewer

        with model() as reviewer:
            back = reviewer.execute(form.data['answer'])

        if back['error']:
            msg = {'query_error': back['error']}
        else:
            msg = back['records']

        msg = json.dumps(msg, cls=CustomJSONEncoder)
    except:
        return render(request, 't.html', {
            'msg': 'Внутренняя ошибка'
        })

    return render(request, 't.html', {
        'msg': msg
    })


@login_required(redirect_field_name='')
def question(request):
    have_time = user_time_update(request.user)
    if have_time <= 0:
        return HttpResponseRedirect('/?{0}'.format('user_msg=no_time'))

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
        return HttpResponseRedirect('/tests/')

    if not user_session.running:
        return HttpResponseRedirect('/?{0}'.format('user_msg=session_closed'))

    if request.method == 'GET':
        if question.type.isSQLQuery() or question.type.isNoSQLQuery():
            tmpl = 'sql_query_answer_form.html'
            form = AnswerForm({'answer': session_question.last_answer})
        elif question.type.isTestMultianswer():
            tmpl = 'test_multianswer_form.html'
            answers_html = ''
            count = 0
            for ans in question.get_multianswer_strings():
                checked = ''
                try:
                    if session_question.last_answer[count] == '1':
                        checked = 'checked'
                except:
                    pass
                answers_html += '<input type="checkbox" id="id_answer_{0}" name="answer_{0}" {1}> '.format(count, checked)
                answers_html += ans
                answers_html += '<br/>'
                count += 1
            form = answers_html

        context.update({
            'form': form,
            'testid': rk_id,
            'question': question,
            'have_time': have_time,
            'user_msg': get_user_message(request)
        })
        return render(request, tmpl, context)

    try:
        if question.type.isSQLQuery() or question.type.isNoSQLQuery():
            form = AnswerForm(request.POST)
            user_query = form.data['answer'].strip()
            context.update({'form': form})

            if question.type.isSQLQuery():
                model = MySQLReviewer
            elif question.type.isNoSQLQuery():
                model = NoSQLReviewer
            with model() as reviewer:
                back = reviewer.execute_double(right_query=question.answer, user_query=user_query)

            session_question.last_answer = user_query
            session_question.check()
            session_question.save()
        elif question.type.isTestMultianswer():
            right_answers = question.get_multianswer_bools()
            answers = ''
            count = 0
            for ans in question.get_multianswer_strings():
                ans_key = 'answer_{0}'.format(count)
                if ans_key in request.POST and request.POST[ans_key] == 'on':
                    answers += '1'
                else:
                    answers += '0'
                count += 1
            session_question.last_answer = answers
            session_question.check()
            session_question.save()

        return HttpResponseRedirect('/tests/?testid={0}'.format(rk_id))
    except:
        return HttpResponseRedirect('/')


def start_new_session(request, user, rk, attempt):
    try:
        confirm = request.GET['confirm_start']
    except:
        confirm = ''

    if confirm != 'yes':
        return HttpResponseRedirect('/?{0}'.format('user_msg=start_session_failed'))

    if not rk.is_active:
        return HttpResponseRedirect('/')

    try:
        rk = UserSession.objects.get(user=user, running=True)
        # Если такую нашли, новую начать невозможно
        return HttpResponseRedirect('/?{0}'.format('user_msg=another_test_running'))
    except:
        pass

    if attempt.have <= 0:
        return HttpResponseRedirect('/?{0}'.format('user_msg=no_attemptes'))

    indexes = []
    for obj in Question.objects.filter(rk=rk, is_active=True):
        indexes.append(obj.id)

    good_indexes = []
    for i in range(min(QUESTIONS_COUNT, len(indexes))):
        ch = choice(indexes)
        good_indexes.append(ch)
        indexes.remove(ch)

    try:
        attempt.used += 1
        attempt.have -= 1
        attempt.save()
        user_session = UserSession.objects.create(user=user, rk=rk, attempt=attempt.used)

        questions = []
        for id in good_indexes:
            question = Question.objects.get(id=id)
            questions.append(question)
            SessionQuestions.objects.create(session=user_session, question=question)
    except:
        return HttpResponseRedirect('/')

    return HttpResponseRedirect('/tests/?testid={0}'.format(rk.id))


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
        attempt = Attempt.objects.create(user=request.user, rk=rk)
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
        status = ''
        if que_s.last_answer != '':
            status = 'sended'
        questions.append(OutputQuestionModel(que_s.question, status))

    context = {
        'question_list': questions,
        'testid': rk_id,
        'have_time': have_time,
        'user_msg': get_user_message(request),
    }
    context.update(static_context)
    return render(request, 'question_list.html', context)


def login_view(request):
    context = {
        'form_auth': LoginForm(),
        'form_pass_restore': PassRestoreForm(),
        'is_login_page': 'True',
        'user_msg': get_user_message(request),
    }
    context.update(static_context)

    if request.method == 'GET':
        if request.user.is_authenticated():
            if request.user.is_superuser:
                return HttpResponseRedirect('/admin/')
            return HttpResponseRedirect('/')
        return render(request, 'auth.html', context)

    form_auth = LoginForm(request.POST)
    context.update({'form_auth': form_auth})
    user = authenticate(username=form_auth.data["login"], password=form_auth.data["password"])

    if user is None:
        context.update({'user_msg': UserMessage('login_failed')})
        return render(request, 'auth.html', context)

    if not user.is_active:
        context.update({'user_msg': UserMessage('disabled_user')})
        return render(request, 'auth.html', context)

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
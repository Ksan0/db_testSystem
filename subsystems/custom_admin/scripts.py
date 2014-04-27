from django.http import HttpResponseRedirect
from django.shortcuts import render
from output_models import *
from subsystems.index.scripts import user_time_update
import re

def user_add_attempt(request):
    try:
        user = User.objects.get(id=request.GET['uid'])
        rk = RK.objects.get(id=request.GET['rkid'])
    except:
        return render(request, 't.html', {
            'msg': 'Args error'
        })

    try:
        attempt = Attempt.objects.get(user=user, rk=rk)
        attempt.have += 1
        attempt.save()
    except:
        Attempt.objects.create(user=user, rk=rk, have=ATTEMPTES_MAX + 1)

    return render(request, 't.html', {
        'msg': ''
    })


def make_user_answer_right(request):
    try:
        user = User.objects.get(id=request.GET['uid'])
        rk = RK.objects.get(id=request.GET['rkid'])
        attempt = request.GET['att']
        question = Question.objects.get(id=request.GET['queid'])
    except:
        return render(request, 't.html', {
            'msg': 'Args error'
        })

    try:
        session = UserSession.objects.get(user=user, rk=rk, attempt=attempt)
        session_question = SessionQuestions.objects.get(session=session, question=question)
        session_question.is_right = True
        session_question.save()
    except:
        return render(request, 't.html', {
            'msg': 'Args error'
        })

    return render(request, 't.html', {
        'msg': ''
    })


def recalc_question(request):
    try:
        splitter = re.compile(r'/')
        split_url = splitter.split(request.META['HTTP_REFERER'])
        question = Question.objects.get(id=int(split_url[-2]))
    except:
        return render(request, 't.html', {
            'msg': 'Args error '
        })

    try:
        for obj in SessionQuestions.objects.filter(question=question, is_right=False):
            obj.check()
    except:
        pass

    return render(request, 't.html', {
        'msg': ''
    })


def statistic_tech(request):
    try:
        id = request.GET['id']
        rk = RK.objects.get(id=id)
    except:
        return HttpResponseRedirect('/admin/')

    users = []
    for user in User.objects.filter(is_staff=False, is_superuser=False):
        users.append(UserOutputModel(user))

    result_data = []
    for user in users:
        try:
            tech_id = UserExtraInfo.objects.get(user=user).tech_id
        except:
            tech_id = None

        result = 0
        for row in user.rk:
            if row[0].id == rk.id:
                result = row[-1]
                break
        result *= QUESTION_WEIGHT

        result_data.append((tech_id, result))

    return render(request, 'custom_admin/statistic_tech.html', {
        'results': result_data
    })


def statistic_user(request):
    try:
        id = request.GET['id']
        user = User.objects.get(id=id)
    except:
        return HttpResponseRedirect('/admin/')

    user_time_update(user)
    user_sessions = UserSession.objects.filter(user=user).order_by('rk', 'attempt')
    user_sessions_output = []
    for usr_sess in user_sessions:
        user_sessions_output.append(UserSessionOutputModel(usr_sess))

    return render(request, 'custom_admin/userinfo.html', {
        'user_sessions': user_sessions_output,
        'student': user,
        'is_admin': True,
        'hide_tests_url': True
    })


def statistic_question(request):
    try:
        id = request.GET['id']
        question = Question.objects.get(id=id)
    except:
        return HttpResponseRedirect('/admin/')

    answers = SessionQuestions.objects.filter(question=question).order_by('is_right')
    return render(request, 'custom_admin/statistic_question.html', {
        'question': question,
        'answers': answers,
        'is_admin': True,
        'hide_tests_url': True
    })
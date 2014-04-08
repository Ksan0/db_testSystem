from django.http import HttpResponseRedirect
from django.shortcuts import render
from output_models import *
from subsystems.index.scripts import user_time_update


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
        split_url = request.POST['url']
        question = Question.objects.get(id=int(split_url[-2]))
    except:
        return render(request, 't.html', {
            'msg': 'Args error'
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

    mysmalldb = {
        'oleg_b_94@mail.ru': '866',
        'igor.gigi13@gmail.com': '888',
        'abbadoh@mail.ru': '926',
        'f1nal@cgaming.org': '963',
        'kirsanov.do@yandex.ru': '968',
        'p02p@yandex.ru': '976',
        'krygin.ia@gmail.com': '961',
        'lifar_tut_net@mail.ru': '796',
        'fleur-du-jour@rambler.ru': '1009',
        'minaev.mike@gmail.com': '817',
        'rumotame@gmail.com': '944',
        'gifla@ya.ru': '1002',
        'Tanyadmp@mail.ru': '978',
        'rudiny@rambler.ru': '940',
        'Rakhubov@yandex.ru': '852',
        'rubtsov.dmv@gmail.com': '808',
        'esusekov@gmail.com': '895',
        'e.sycheva_nn@mail.ru': '979',
        'ff.warprobot@gmail.com': '348',
        'seregachern@mail.ru': '962',
        'svr93@i.ua': '905',
        'queenliestme@mail.ru': '907',
        'abashinos@gmail.com': '490',
        'Artur_pskov@mail.ru': '772',
        'alexvasiliev92@gmail.com': '984',
        'kgfq@mail.ru': '494',
        'delfin1995@yandex.ru': '781',
        'govorovskij@gmail.com': '524',
        'kolesofortuni@mail.ru': '308',
        'salting@bk.ru': '597',
        'ria6@yandex.ru': '346',
        'kolesnikovakatya91@gmail.com': '174',
        'ko_viktoria@inbox.ru': '782',
        'igor.latkin@outlook.com': '323',
        'alekseyl@list.ru': '686',
        'LinDeni@mail.ru': '574',
        'napster8192@hotmail.com': '290',
        'h12vbn6@gmail.com': '391',
        'maxmyalkin@gmail.com': '531',
        'Alexopryshko@yandex.ru': '321',
        'radochin_ilya@list.ru': '271',
        'timonin.maksim@mail.ru': '514',
        'Anis-007@yandex.ru': '307',
        'wequbelity@gmail.com': '272'
    }

    users = []
    for user in User.objects.filter(is_staff=False, is_superuser=False):
        users.append(UserOutputModel(user))

    result_data = []
    for user in users:
        email = user.user.email
        if email not in mysmalldb.keys():
            continue
        tech_id = mysmalldb[email]
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
        'answers': answers
    })
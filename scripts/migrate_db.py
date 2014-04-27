import os, sys
import random
import string


def migrate_db():
    from db_testSystem.models import Question, RK, Attempt, UserSession, SessionQuestions, UserExtraInfo
    from django.contrib.auth.models import User
    from subsystems.db_raw_sql_works.DB import Review

    db_settings = {
        'HOST_NAME': '',
        'DB_NAME': 'mailtp',
        'USER_NAME': 'root',
        'USER_PASSWORD': 'eCR7qeJS',
        'DB_CHARSET': 'utf8'
    }

    reviewer = Review(db_settings)
    
    # questions migrate
    """
    count = int( reviewer.select('SELECT COUNT(*) FROM knowledge_test_question')['records'][0]['COUNT(*)'] )
    for i in range(count):
        query = ('SELECT * FROM knowledge_test_question LIMIT {0},1').format(i)
        que = reviewer.select(query)['records'][0]
        Question.objects.create(title=que['title'], description=que['description'], answer=que['answer'], is_active=False)
    """

    # users migrate
    """
    with open('out_users_db', 'w') as outfile:
        count = int( reviewer.select('SELECT COUNT(*) FROM auth_user')['records'][0]['COUNT(*)'] )
        for i in range(count):
            query = ('SELECT * FROM auth_user LIMIT {0},1').format(i)
            que = reviewer.select(query)['records'][0]
            newpass = ''.join([random.choice(string.ascii_uppercase) for _ in xrange(12)])

            User.objects.create_user(username=que['username'], email=que['email'], password=newpass)
            outfile.write('{0} {1}\n'.format(que['username'], newpass))
    """

    # attempt sub
    """
    usernames = []
    count = int( reviewer.select('SELECT COUNT(*) FROM knowledge_test_gameranswer')['records'][0]['COUNT(*)'] )
    for i in range(count):
        query = ('SELECT * FROM knowledge_test_gameranswer LIMIT {0},1').format(i)
        que = reviewer.select(query)['records'][0]
        user_id = que['gamer_id']
        query = ('SELECT * FROM auth_user WHERE id={0}').format(user_id)
        que = reviewer.select(query)['records'][0]
        username = que['username']
        if username not in usernames:
            usernames.append(username)

    with open('out_att_sub', 'w') as outfile:
        for username in usernames:
            outfile.write('{0}\n'.format(username))
    """

    # sub attemptes
    """
    with open('att_sub', 'r') as infile:
        for line in infile:
            user_list = [word for word in line.split()]
            user = User.objects.get(username=user_list[0])
    """

    # add score
    """
    with open('sc_add', 'r') as infile:
        for line in infile:
            user_list = [word for word in line.split()]
            user = User.objects.get(username=user_list[0])
            count = int(user_list[1])
            if count > 0:
                rk = RK.objects.get(id=1)
                Attempt.objects.create(user=user, rk=rk, used=1, have=2)
                session = UserSession.objects.create(user=user, rk=rk, attempt=1, running=False)
                question = Question.objects.get(id=19)
                for i in range(count):
                    SessionQuestions.objects.create(session=session, question=question, is_right=True)
    """

    # add extra info (tech-id)
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
    for user in User.objects.all():
        try:
            tech_id = mysmalldb[user.email]
            UserExtraInfo.objects.create(user=user, tech_id=tech_id)
        except:
            pass

    return 0


if __name__ == '__main__':
    BASE_DIR = os.getcwd() + '/' + os.path.dirname(__file__) + '/..'
    sys.path.append(BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db_testSystem.settings")
    migrate_db()

import os, sys
import random
import string


def migrate_db():
    from db_testSystem.models import Question, RK
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

    return 0


if __name__ == '__main__':
    BASE_DIR = os.getcwd() + '/' + os.path.dirname(__file__) + '/..'
    sys.path.append(BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db_testSystem.settings")
    migrate_db()

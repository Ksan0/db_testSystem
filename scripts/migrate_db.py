import os, sys
import random
import string


def migrate_db():
    from db_testSystem.models import Question
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
    with open(new_file, 'w') as outfile:
    count = int( reviewer.select('SELECT COUNT(*) FROM auth_user')['records'][0]['COUNT(*)'] )
    for i in range(count):
        query = ('SELECT * FROM knowledge_test_question LIMIT {0},1').format(i)
        que = reviewer.select(query)['records'][0]
        newpass = ''.join([random.choice(string.ascii_uppercase) for _ in xrange(12)])
                
    return 0


if __name__ == '__main__':
    BASE_DIR = os.getcwd() + '/' + os.path.dirname(__file__) + '/..'
    sys.path.append(BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db_testSystem.settings")
    migrate_db()

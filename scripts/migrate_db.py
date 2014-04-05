import os, sys
import random
import string


def migrate_db():
    from django.contrib.auth.models import User
    from subsystems.db_raw_sql_works.DB import Review

    db_settings = {
        'HOST_NAME': '',
        'DB_NAME': 'db_testSystem',
        'USER_NAME': 'testUser',
        'USER_PASSWORD': 'qwe',
        'DB_CHARSET': 'utf8'
    }

    reviewer = Review(db_settings)
    count = int( reviewer.select('SELECT COUNT(*) FROM knowledge_test_question')['records'] )
    for i in range(count):
        query = ('SELECT * FROM knowledge_test_question LIMIT {0},1').format(i)
        que = reviewer.select(query)['records']
        print que

    return 0


if __name__ == '__main__':
    BASE_DIR = os.getcwd() + '/' + os.path.dirname(__file__) + '/..'
    sys.path.append(BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db_testSystem.settings")
    migrate_db()
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db_testSystem.settings")
import random
import string
from django.contrib.auth.models import User


def filling_users(users_file, new_file):
    with open(new_file, 'w') as outfile, open(users_file, 'r') as infile:
        for line in infile:
            user_list = [word for word in line.split()]
            user_list.append(''.join([random.choice(string.ascii_uppercase) for _ in xrange(12)]))
            User.objects.create_user(user_list[-2], user_list[-2], user_list[-1])
            outfile.write('{} {} {} {}\n'.format(*user_list))
    return 0


if __name__ == '__main__':
    filling_users('in_users_db', 'out_users_db')
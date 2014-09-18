import os, sys
import random
import string

# run from "scripts" folder

# last_name  first_name  mail(=login)  pass

def filling_users(users_file, new_file):
    from django.contrib.auth.models import User
    with open(new_file, 'w') as outfile, open(users_file, 'r') as infile:
        for line in infile:
            user_list = [word for word in line.split()]
            if user_list[0] == '#':
                continue
            # user_list.append(''.join([random.choice(string.ascii_uppercase) for _ in xrange(12)]))
            User.objects.create_user(username=user_list[2], email=user_list[2], password=user_list[3], first_name=user_list[1], last_name=user_list[0])
            outfile.write('{} {} {} {}\n'.format(*user_list))
    return 0


if __name__ == '__main__':
    BASE_DIR = os.getcwd() + '/' + os.path.dirname(__file__) + '/..'
    sys.path.append(BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db_testSystem.settings")
    filling_users('in_users_db', 'out_users_db')
# db with users, tests, statistic etc
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': 'db_testSystem',

		'USER': 'root',
		'PASSWORD': '1',
		'HOST': '', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
		'PORT': '', # Set to empty string for default.
   }
}


# db for user's tests. It contains tables as Movie, Reviewer etc
MYSQL_TEST_DB = {
    'HOST_NAME': '',
    'DB_NAME': 'db_test',
    'USER_NAME': 'testUser',
    'USER_PASSWORD': 'qwe',
    'DB_CHARSET': 'utf8'
}


NOSQL_TEST_DB = {
    'HOST_NAME': 'localhost',
    'HOST_PORT': 27017,
    'DB_NAME': 'wow',
    'USER_NAME': 'readonly',
    'USER_PASSWORD': 'readMeAll!'
}

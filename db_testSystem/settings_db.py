# db with users, tests, statistic etc
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': 'db_testSystem',

		'USER': 'root',
		'PASSWORD': '',
		'HOST': '', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
		'PORT': '', # Set to empty string for default.
   }
}

# db for user's tests. It contains tables as Movie, Reviewer etc
TEST_DB = {
    'HOST_NAME': '',
    'DB_NAME': 'db_test',
    'USER_NAME': 'root',
    'USER_PASSWORD': 'qwe',
    'DB_CHARSET': 'utf8'
}

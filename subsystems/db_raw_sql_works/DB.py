#coding: utf-8
import MySQLdb
from _mysql_exceptions import DataError, DatabaseError, InternalError, IntegrityError, InterfaceError, MySQLError, OperationalError, ProgrammingError
from db_testSystem.models import *


HOST_NAME = ''
DB_NAME = 'db_test'
USER_NAME = 'root'
USER_PASSWORD = ''
DB_CHARSET = 'utf8'


class MySqlDB(object):
    def __init__(self, host_name, username, passwd, db_name, charset):
        db = MySQLdb.connect(host=host_name, user=username, passwd=passwd, db=db_name, charset=charset)
        self.cursor = db.cursor()

    @staticmethod
    def dictfetchall(cursor):
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

    def select(self, sql_query):
        try:
            self.cursor.execute(sql_query)
            sql_records = MySqlDB.dictfetchall(self.cursor)
            return sql_records, False
        except (DataError, DatabaseError, InternalError, IntegrityError,
                InterfaceError, MySQLError, OperationalError, ProgrammingError) as e:
            return dict(), e.args[1]


class Review(object):
    @staticmethod
    def check_answer(sql_query, right_sql_query):
        orm = MySqlDB(HOST_NAME, USER_NAME, USER_PASSWORD, DB_NAME, DB_CHARSET)
        answer_records, error = orm.select(right_sql_query)
        user_records, error = orm.select(sql_query)
        return [a.values() for a in user_records] == [a.values() for a in answer_records], user_records, error
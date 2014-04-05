#coding: utf-8
import MySQLdb
from _mysql_exceptions import DataError, DatabaseError, InternalError, IntegrityError, InterfaceError, MySQLError, OperationalError, ProgrammingError
#from db_testSystem.models import *


from db_testSystem.settings_db import TEST_DB



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
    def __init__(self, db_settings=None):
        if db_settings is None:
            db_settings = TEST_DB
        self.orm = MySqlDB(db_settings['HOST_NAME'],
                           db_settings['USER_NAME'],
                           db_settings['USER_PASSWORD'],
                           db_settings['DB_NAME'],
                           db_settings['DB_CHARSET'])


    def select(self, sql_query):
        records, error = self.orm.select(sql_query)
        return {
            'records': records,
            'error': error
        }

    def check_results(self, sql_query_right, sql_query_user):
        r_records, r_error = self.orm.select(sql_query_right)
        u_records, u_error = self.orm.select(sql_query_user)
        is_equal = [a.values() for a in r_records] == [a.values() for a in u_records]
        return {
            'r_records': r_records,
            'r_error': r_error,
            'u_records': u_records,
            'u_error': u_error,
            'is_equal': is_equal
        }
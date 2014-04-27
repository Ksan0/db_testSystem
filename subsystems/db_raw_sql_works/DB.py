#coding: utf-8
import MySQLdb
from _mysql_exceptions import DataError, DatabaseError, InternalError, IntegrityError, InterfaceError, MySQLError, OperationalError, ProgrammingError
import re
#from db_testSystem.models import *


from db_testSystem.settings_db import TEST_DB



class MySqlDB(object):
    def __init__(self, host_name, username, passwd, db_name, charset):
        db = MySQLdb.connect(host=host_name, user=username, passwd=passwd, db=db_name, charset=charset)
        self.cursor = db.cursor()

    def dictfetchall(self):
        title_set = []
        for set in self.cursor.description:
            title_set.append(set[0])

        result_set = []
        for row in self.cursor.fetchall():
            pre_result = []
            for data in row:
                pre_result.append(data)
            result_set.append(pre_result)
        return title_set, result_set


    def select(self, sql_query):
        try:
            self.cursor.execute(sql_query)
            titles, sql_records = self.dictfetchall()
            return titles, sql_records, False
        except (DataError, DatabaseError, InternalError, IntegrityError,
                InterfaceError, MySQLError, OperationalError, ProgrammingError) as e:
            return [], [], e.args[1]


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
        titles, records, error = self.orm.select(sql_query)
        return {
            'records': records,
            'titles': titles,
            'error': error
        }

    def check_results(self, sql_query_right, sql_query_user):
        r_titles, r_records, r_error = self.orm.select(sql_query_right)
        u_titles, u_records, u_error = self.orm.select(sql_query_user)
        is_equal = [a.values() for a in r_records] == [a.values() for a in u_records]
        return {
            'r_titles': r_titles,
            'r_records': r_records,
            'r_error': r_error,
            'u_titles': u_titles,
            'u_records': u_records,
            'u_error': u_error,
            'is_equal': is_equal
        }
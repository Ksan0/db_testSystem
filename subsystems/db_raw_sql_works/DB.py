#coding: utf-8
import MySQLdb
from _mysql_exceptions import DataError, DatabaseError, InternalError, IntegrityError, InterfaceError, \
                              MySQLError, OperationalError, ProgrammingError
from db_testSystem.settings_db import MYSQL_TEST_DB, NOSQL_TEST_DB
import pymongo


class MySqlDB(object):
    def __init__(self, host_name, username, passwd, db_name, charset):
        self.db = MySQLdb.connect(host=host_name, user=username, passwd=passwd, db=db_name, charset=charset)
        self.cursor = self.db.cursor()

    def close(self):
        self.cursor.close()
        self.db.close()

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


    def select(self, query):
        try:
            self.cursor.execute(query)
            titles, sql_records = self.dictfetchall()
            return titles, sql_records, False
        except (DataError, DatabaseError, InternalError, IntegrityError,
                InterfaceError, MySQLError, OperationalError, ProgrammingError) as e:
            return [], [], e.args[1]


class NoSqlDB(object):  # with pymongo
    def __init__(self, host_name, username, passwd, db_name, charset):
        self.client = pymongo.MongoClient(NOSQL_TEST_DB['HOST_NAME'], NOSQL_TEST_DB['HOST_PORT'])
        self.db = self.client[NOSQL_TEST_DB['DB_NAME']]
        self.db.authenticate(NOSQL_TEST_DB['USER_NAME'], NOSQL_TEST_DB['USER_PASSWORD'])

    def close(self):
        self.db.logout()
        self.client.close()

    def execute(self, query):
        jscode = """
            var getType = function (obj) {
                var _getClassType = function (obj) {
                    // if (obj instanceof DBQuery)
                    //     return "dbquery";   // find
                    // if (obj instanceof DBCommandCursor)
                    //     return "dbcommandcursor";   // aggregate
                    return "Uclass";
                };
                var _getInlineType = function (obj) {
                    switch(typeof(obj)) {
                        case "undefined":
                        case "number":
                        case "string":
                        case "boolean":
                        case "function":
                            return typeof(obj);
                        default:
                            return "Uinline";
                    }
                };

                if (obj == null)
                    return "null";
                if (typeof(obj) == "object")
                    return _getClassType(obj);
                return _getInlineType(obj);
            };

            var cursor = eval(\"""" + query + """\");
            var type = getType(cursor);

            switch(type) {
                case "number":
                case "string":
                case "boolean":
                    return cursor;
                case "Uclass":
                    return cursor.toArray();
            }

            throw "mongo-eval-JS error";
        """

        try:
            res = self.db.eval(jscode)
        except Exception, errmsg:
            err = str(errmsg).split('exception: ')[1]
            return [], err

        if type(res) is not list:
            res = [res]
        return res, None


class Review(object):
    def __init__(self, db_settings=None):
        if db_settings is None:
            db_settings = MYSQL_TEST_DB
        self.orm = MySqlDB(db_settings['HOST_NAME'],
                           db_settings['USER_NAME'],
                           db_settings['USER_PASSWORD'],
                           db_settings['DB_NAME'],
                           db_settings['DB_CHARSET'])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.orm.close()

    def select(self, query):
        titles, records, error = self.orm.select(query)
        return {
            'records': records,
            'titles': titles,
            'error': error
        }

    def check_results(self, right_query, user_query):
        r_titles, r_records, r_error = self.orm.select(right_query)
        u_titles, u_records, u_error = self.orm.select(user_query)
        is_equal = [a for a in r_records] == [a for a in u_records]
        return {
            'r_titles': r_titles,
            'r_records': r_records,
            'r_error': r_error,
            'u_titles': u_titles,
            'u_records': u_records,
            'u_error': u_error,
            'is_equal': is_equal
        }
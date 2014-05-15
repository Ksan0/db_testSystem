#coding: utf-8
import MySQLdb
from _mysql_exceptions import DataError, DatabaseError, InternalError, IntegrityError, InterfaceError, \
                              MySQLError, OperationalError, ProgrammingError
from db_testSystem.settings_db import MYSQL_TEST_DB, NOSQL_TEST_DB
import pymongo


class MySqlDB:
    def __init__(self, host_name, username, password, db_name, charset):
        self.db = MySQLdb.connect(host=host_name, user=username, passwd=password, db=db_name, charset=charset)
        self.cursor = self.db.cursor()

    def close(self):
        self.cursor.close()
        self.db.close()

    def __dictfetchall(self):
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


    def execute(self, query):
        try:
            self.cursor.execute(query)
            titles, sql_records = self.__dictfetchall()
            return titles, sql_records, False
        except (DataError, DatabaseError, InternalError, IntegrityError,
                InterfaceError, MySQLError, OperationalError, ProgrammingError) as e:
            return [], [], e.args[1]


class NoSqlDB:  # with pymongo
    def __init__(self, host_name, host_port, username, password, db_name):
        self.client = pymongo.MongoClient(host_name, host_port)
        self.db = self.client[db_name]
        self.db.authenticate(username, password)

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
                case "null":
                    return "Empty set";
                case "Uclass":
                    return cursor.toArray();
            }

            throw "mongo-eval-JS cursor-type error: " + type.toString();
        """

        try:
            res = self.db.eval(jscode)
        except Exception, errmsg:
            err = str(errmsg).split('exception: ')[1]
            return [], err

        if type(res) is not list:
            res = [res]
        return res, False


class MySQLReviewer:
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

    def execute(self, query):
        titles, records, error = self.orm.execute(query)
        return {
            'records': records,
            'titles': titles,
            'error': error
        }

    def execute_double(self, right_query, user_query):
        r_titles, r_records, r_error = self.orm.execute(right_query)
        u_titles, u_records, u_error = self.orm.execute(user_query)
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


class NoSQLReviewer:
    def __init__(self, db_settings=None):
        if db_settings is None:
            db_settings = NOSQL_TEST_DB
        self.orm = NoSqlDB(db_settings['HOST_NAME'],
                           db_settings['HOST_PORT'],
                           db_settings['USER_NAME'],
                           db_settings['USER_PASSWORD'],
                           db_settings['DB_NAME'])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.orm.close()

    def execute(self, query):
        records, error = self.orm.execute(query)
        return {
            'records': records,
            'error': error
        }

    def execute_double(self, right_query, user_query):
        r_records, r_error = self.orm.execute(right_query)
        u_records, u_error = self.orm.execute(user_query)

        is_equal = [a for a in r_records] == [a for a in u_records]

        return {
            'r_records': r_records,
            'r_error': r_error,
            'u_records': u_records,
            'u_error': u_error,
            'is_equal': is_equal
        }
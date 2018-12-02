# -*- coding: UTF-8 -*-

from __init__ import *

mserver = ""
muser = ""
mpassword = ""
mdatabase = ""


class db_manage:
    def __init__(self, server=mserver, user=muser, password=mpassword, database=mdatabase):
        self.db = MySQLdb.connect(server, user, password, database, charset='utf8')
        self.cursor = self.db.cursor()

    def updae(self, sql):
        self.cursor.execute(sql)
        # 提交到数据库执行
        self.db.commit()
        return "ok"

    def query(self, query_sql):
        result = self.fetchall(query_sql)
        return result

    def fetchall(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def queryall(self, db):
        query_sql = "SELECT * FROM `%s` WHERE 1" % db
        result = self.fetchall(query_sql)
        return result

    def close(self):
        self.db.close()


def datetime_now():
    return datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

# coding=utf-8
from __future__ import print_function
from datetime import date
import datetime
from dbconnect.dbmanage import db_manage
import json


def db2json(dbname):
    # db应为字符串类型
    db = db_manage()
    result = db.queryall(dbname)
    db.close()
    return json.dumps(result, cls=ComplexEncoder)


def query2json(sql):
    # sql 应为字符串类型的sql语句
    db = db_manage()
    result = db.query(sql)
    db.close()
    return json.dumps(result, cls=ComplexEncoder)


def update2json(sql):
    db = db_manage()
    result = db.updae(sql)
    db.close()
    return result


def user_confirm_query(uid, password):
    sql = "SELECT * FROM `user` WHERE passwd= '%s' AND uid = '%s'" % (password, uid)
    return sql


def datetime_now():
    # 返回明天对应的现在时刻
    return (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%I:%S')


def datetime_after(n):
    return (datetime.datetime.now() + datetime.timedelta(days=n)).strftime('%Y-%m-%d')


def delete_by_id_sql(uid):
    sql = "DELETE FROM `user` WHERE uid = '%s'" % uid
    return sql


def delete_record_by_id_sql(uid, bid):
    sql = "DELETE FROM `records` WHERE uid = '%s' AND bid = '%s'" % (uid, bid)
    print(sql)
    return sql


def result2json(result):
    return json.loads(result)


def query_record_by_id_sql(uid):
    sql = "SELECT * FROM `records` WHERE uid = %s" % uid
    return sql


def query_book_name_by_id_sql(bid):
    sql = "SELECT name FROM `books` WHERE bid = %s" % bid
    print(sql)
    return sql


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def query_book_by_name_sql(name):
    sql = "SELECT * FROM `books` WHERE name = '《%s》'" % name
    return sql


def add_record_sql(bid, uid):
    sql = "INSERT INTO `records` (`id`, `uid`, `bid`, `Rdate`) VALUES (NULL, '%s', '%s', '%s');" % (
        uid, bid, datetime_after(31))
    return sql


def set_book_status_sql(bid, status):
    sql = "UPDATE `books` SET `status` = '%s' WHERE `bid` = %s;" % (status, bid)
    return sql


def add_book_sql(Bookname, Booktype, Bookpress):
    sql = "INSERT INTO `iot2017`.`books` (`bid`, `type`, `status`, `name`, `press`, `remarks`) VALUES (NULL, '%s', '1', '《%s》', '%s', '');" % (
        Booktype, Bookname, Bookpress)
    return sql


def add_user_sql(password, name, type, email, availability, remarks):
    sql = "INSERT INTO `user`(`passwd`, `name`, `type`, `email`,`availability`,`remarks`) VALUES ('%d','%s','%d','%s','%d', '%s')" % (
        password, name, type, email, availability, remarks)
    return sql


def disable_User_sql(uid):
    sql = "UPDATE `iot2017`.`user` SET `availability` = '0' WHERE `user`.`uid` = %s;" % uid
    return sql


def enable_User_sql(uid):
    sql = "UPDATE `iot2017`.`user` SET `availability` = '1' WHERE `user`.`uid` = %s;" % uid
    return sql


def del_book_sql(bid):
    sql = "DELETE FROM `iot2017`.`books` WHERE `books`.`bid` = %s" % bid
    return sql


def reset_password_sql(email):
    sql = "UPDATE `iot2017`.`user` SET `passwd` = '10086' WHERE `user`.`email` = '%s';" % email
    return sql


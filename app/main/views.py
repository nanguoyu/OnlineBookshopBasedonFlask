# coding=utf-8
from datetime import datetime
from flask import url_for, redirect, session, render_template, request
from flask_wtf import Form
import logging
import time
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, PasswordField
from app.main.mdb import user_confirm_query, query2json, result2json, query_record_by_id_sql, query_book_name_by_id_sql, \
    delete_record_by_id_sql, update2json, query_book_by_name_sql, add_record_sql, set_book_status_sql, add_book_sql, \
    db2json, add_user_sql, enable_User_sql, disable_User_sql, del_book_sql, reset_password_sql
from . import main

logging.basicConfig(filename=time.strftime("%Y-%m-%d", time.localtime()) + 'mention_database.log', level=logging.DEBUG)
logging.info(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) + 'mention_database start')


@main.route('/', methods=['GET', 'POST'])
def index():
    form = log_on_form()
    if form.validate_on_submit():
        uid = form.uid.data
        password = form.password.data
        resultJson = result2json(query2json(user_confirm_query(uid=uid, password=password)))
        if len(resultJson) == 1:
            session['uid'] = uid
            session['name'] = resultJson[0][2]
            # 这里验证用户账户
            return redirect(url_for('main.dashboard'))
        elif len(resultJson) == 0:
            return render_template('/index.html', form=form)

    return render_template('/index.html', form=form)


@main.route('/reset', methods=['GET', 'POST'])
def reset():
    info = "please intput your email"
    return render_template('/reset.html', info=info)


@main.route('/resetPassword', methods=['GET', 'POST'])
def resetPassword():
    email = request.args.get('email')
    if update2json(reset_password_sql(email)) == 'ok':
        info = "reset " + str(email) + " account password 10086"
        return render_template('/reset.html', info=info)
    else:
        info = "重置失败"
        return render_template('/reset.html', info=info)


@main.route('/deleteRecord', methods=['GET', 'POST'])
def deleteRecord():
    bid = request.form.get('bid')
    update2json(set_book_status_sql(bid, 1))
    update2json(delete_record_by_id_sql(session['uid'], bid))
    return redirect(url_for('main.dashboard'))


# lossBook

@main.route('/lossBook', methods=['GET', 'POST'])
def lossBook():
    bid = request.form.get('fbid')
    update2json(set_book_status_sql(bid, str(2)))
    # update2json(delete_record_by_id_sql(session['uid'], bid))
    return redirect(url_for('main.dashboard'))


@main.route('/getBook', methods=['GET', 'POST'])
def getBook():
    bid = request.form.get('gbid')
    # update2json(delete_record_by_id_sql(session['uid'], bid))
    # 增加图书借阅记录
    # 修改图书状态
    update2json(add_record_sql(bid, session['uid']))
    update2json(set_book_status_sql(bid, 0))
    # update2json()
    return redirect(url_for('main.dashboard'))


@main.route('/SearchBook', methods=['GET', 'POST'])
def SearchBook():
    BookName = request.form.get('BookName')
    # SearchBookResult = query2json(query_book_by_name_sql(BookName))
    return result2json(query2json(query_book_by_name_sql(BookName)))


@main.route('/addBook', methods=['GET', 'POST'])
def addBook():
    BookName = request.form.get('newbname')
    BookPress = request.form.get('newbpress')
    BookType = request.form.get('newbtype')
    update2json(add_book_sql(BookName.encode('utf8'), BookType.encode('utf8'), BookPress.encode('utf8')))
    return redirect(url_for('main.dashboard'))


@main.route('/disableUser', methods=['GET', 'POST'])
def disableUser():
    duid = request.form.get('duid')
    update2json(disable_User_sql(duid.encode('utf8')))
    return redirect(url_for('main.dashboard'))


@main.route('/enableUser', methods=['GET', 'POST'])
def enableUser():
    duid = request.form.get('duid')
    update2json(enable_User_sql(duid.encode('utf8')))
    return redirect(url_for('main.dashboard'))


@main.route('/delBook', methods=['GET', 'POST'])
def delBook():
    delbid = request.form.get('delbid')
    update2json(del_book_sql(delbid.encode('utf8')))
    return redirect(url_for('main.dashboard'))


@main.route('/addUser', methods=['GET', 'POST'])
def addUser():
    UserName = request.form.get('newuname')
    UserType = request.form.get('newutype')
    UserEmail = request.form.get('newuemail')
    update2json(add_user_sql(10086, UserName.encode('utf8'), int(UserType), UserEmail.encode('utf8'), 1, '备注'))
    return redirect(url_for('main.dashboard'))


@main.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    user_records = result2json(query2json(query_record_by_id_sql(uid=session['uid'])))
    BookName = request.form.get('BookName')
    AllBook = result2json(db2json('books'))
    AllStudent = result2json(db2json('user'))
    if BookName is not None:
        SearchBookResult = result2json(query2json(query_book_by_name_sql(BookName.encode('utf8'))))
        for record in user_records:
            rdate = record[3]
            today = datetime.today().strftime('%Y-%m-%d')
            day = (int(today[5:7]) - int(rdate[5:7])) * 30 + (int(today[8:10]) - int(rdate[8:10]))
            bookname = result2json(query2json(query_book_name_by_id_sql(record[2])))[0][0]
            if day < 0:
                record.append(bookname)
                record.append(0)
            else:
                record.append(bookname)
                record.append(day * 0.5)
        return render_template('/dashboard.html', name=session['name'], uid=session['uid'], records=user_records,
                               SearchBookResult=SearchBookResult, AllBook=AllBook, AllStudent=AllStudent)
    else:
        for record in user_records:
            rdate = record[3]
            today = datetime.today().strftime('%Y-%m-%d')
            day = (int(today[5:7]) - int(rdate[5:7])) * 30 + (int(today[8:10]) - int(rdate[8:10]))
            bookname = result2json(query2json(query_book_name_by_id_sql(record[2])))[0][0]
            if day < 0:
                record.append(bookname)
                record.append(0)
            else:
                record.append(bookname)
                record.append(day * 0.5)
        return render_template('/dashboard.html', name=session['name'], uid=session['uid'], records=user_records,
                               AllBook=AllBook, AllStudent=AllStudent)


class log_on_form(Form):
    uid = StringField(U'借阅号', validators=[DataRequired()])
    password = PasswordField(U'密码', validators=[DataRequired()])
    submit = SubmitField(U'登录')

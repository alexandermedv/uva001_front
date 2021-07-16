from flask_login import current_user, login_required, login_user, logout_user
from flask import url_for, redirect, render_template, flash, request, jsonify
import pandas as pd

from . import app, db, login
from .forms import LoginForm, CreateUserForm, ProfileForm, EditUserForm, PasswordUserForm
from .models import User, requires_roles, Report
from sqlalchemy import create_engine
import os
import front_ex.config as config
from .report1 import utils as report1
from .report_equipment import utils as report_equipment
import json
import datetime
import requests
from pprint import pprint
import flask
import psycopg2


# Доступы по текущей сессии
@login.user_loader
def load_user(id):
    """Инициализация пользователя"""
    user = User.query.filter_by(id=id).first()
    return user


# Руты к дэшбордам
@app.route('/limit_oper/')
@login_required
def render_limit_oper():
    """Дашборд по дебиторской задолженности и превышению лимита"""
    return render_template('/limit_oper/overview.html')

@app.route('/dashapp1/')
@login_required
def render_dashapp1():
    """Дашборд по размеру и динамике недостачи"""
    return render_template('/dashapp1/overview.html')    

@app.route('/dashboard3/')
@login_required
def render_dashapp3():
    """Дашборд по полномочиям в SAP"""
    return render_template('/dashapp3/overview.html')   

@app.route('/report1/')
@login_required
def render_report1():
    # con = create_engine(config.POSTGRE_DB, max_identifier_length=128, encoding='utf-8')
    # sql = '''SELECT *
    # FROM dashboard.equipment
    # LIMIT 100
    # '''
    df1 = report1.get_details_dost()
    print(df1)
    return render_template('/report1/report1.html', title='report1', items=df1[[
        'equnr', 'eartx', 'status', 'erdat', 'hequi', 'typtx', 
        'last_oper_date']].to_dict(orient='records'))


@app.route('/report_equipment/')
@login_required
def render_report_equipment():
    # start = datetime.datetime.now()
    # df1 = report_equipment.get_equipment()
    # print(df1[['equnr', 'eqktx', 'erdat', 'ernam', 'typtx', 'eartx', 'maktx', 'mtbez', 'wgbez', 'status', 'hequi', 'last_oper_date']])
    # end = datetime.datetime.now()
    # print('df loading took: ', end-start)
    # # data = requests.get('/_get_table')
    # # print(data.json())
    # return render_template('/report_equipment/report_equipment.html', title='report_equipment')
    return render_template("/report_equipment/report_equipment.html")


# @app.route('/_get_table_clientside')
# def _get_table_clientside():

#     df1 = report_equipment.get_equipment()
#     print('Формирование таблицы _get_table')
#     # print('_get_table:', df1)
#     pprint(df1.to_dict('records'))
#     print(jsonify(
#                    my_table=json.loads(df1[['equnr', 'eqktx', 'erdat',
#                     'ernam', 'typtx', 'eartx', 'maktx', 'mtbez', 'wgbez', 'status', 'hequi',
#                      'last_oper_date']].to_json(orient="split"))["data"],
#                    columns=[{"title": str(col)} for col in json.loads(df1[['equnr', 'eqktx', 'erdat',
#                     'ernam', 'typtx', 'eartx', 'maktx', 'mtbez', 'wgbez', 'status', 'hequi',
#                      'last_oper_date']].to_json(orient="split"))["columns"]]))
#     # return jsonify(
#     #                my_table=json.loads(df1.to_json(orient="split"))["data"],
#     #                columns=[{"title": str(col)} for col in json.loads(df1.to_json(orient="split"))["columns"]])
#     return jsonify(my_table=df1[['equnr', 'eqktx', 'erdat',
#                     'ernam', 'typtx', 'eartx', 'maktx', 'mtbez', 'wgbez', 'status', 'hequi',
#                      'last_oper_date']].to_html(classes='table table-striped" id = "a_nice_table',index=False, border=0))


@app.route("/_get_table_serverside", methods=["POST", "GET"])
def serverside_table():
    req = flask.request.form
    print("Request data", flask.request.data)
    print("Request form", flask.request.form)
    table_name = str(req['table_name'])
    schema_name = str(req['schema_name'])
    print("table_name", table_name)
    print("schema_name", schema_name)

    column_names = []
    for item in req:
        if 'columns[' in item and '][data]' in item:
            column_names.append(req[item])
    print("column_names", column_names)

    try:
        with psycopg2.connect(user="locadm",
                                password="Temp001",
                                host="msc199-sdb04.domain.local",
                                port="8031",
                                database="uva_cons") as pg_con:
            cursor = pg_con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            print('Соединение с базой данных установлено')

            if request.method == 'POST':
                draw = request.form['draw']
                row = int(request.form['start'])
                rowperpage = int(request.form['length'])
                searchValue = request.form["search[value]"]
                print('draw =', draw)
                print('row =', row)
                print('rowperpage =', rowperpage)
                print('searchValue =', searchValue)

                # Total number of records without filtering
                sql = "SELECT count(*) from " + schema_name + '.' + table_name
                cursor.execute(sql)
                totalRecords = int(cursor.fetchone()[0])
                print('totalRecords =', totalRecords)

                # Total number of records with filtering
                if len(searchValue) < 3:
                    totalRecordwithFilter = totalRecords
                    print('totalRecordwithFilter =', totalRecordwithFilter)
                else:
                    likestrings = searchValue.split(' ')
                    likestrings = ['%' + i + '%' for i in likestrings]
                    print('likestrings', likestrings)
                    s = ''
                    for column in column_names:
                        s += str(column) + ', '
                    s = s[:-2].replace("['index'], ", "")
                    print('s =', s)
                    cols = s.replace("['", "")
                    cols = cols.replace("']", "")
                    print('cols =', cols)

                    sql = """SELECT count(*) from """ + schema_name + '.' + table_name + """ WHERE
                     concat(""" + cols + """) LIKE %s"""
                    for i in range(len(likestrings) - 1):
                        sql += """ AND concat(""" + cols + """) LIKE %s"""
                    print('sql =', sql)
                    print('likeString =', tuple(likestrings))
                    cursor.execute(sql, (tuple(likestrings)))
                    totalRecordwithFilter = int(cursor.fetchone()[0])
                    print('totalRecordwithFilter =', totalRecordwithFilter)

                # Fetch records
                if len(searchValue) < 3:
                    sql = "SELECT * FROM " + schema_name + '.' + table_name + " ORDER BY equnr asc limit %s offset %s;"
                    cursor.execute(sql, (rowperpage, row))
                    resultlist = cursor.fetchall()
                    print('resultlist получен (пустой поиск)')
                else:
                    print('rowperpage =', rowperpage)
                    sql = """SELECT * from """ + schema_name + '.' + table_name + """ WHERE
                            concat(""" + cols + """) LIKE %s"""
                    for i in range(len(likestrings) - 1):
                        sql += """ AND concat(""" + cols + """) LIKE %s"""
                    if rowperpage > 0:
                        sql += """limit %s offset %s"""
                        # sql = "SELECT * FROM " + schema_name + '.' + table_name + " WHERE eqktx LIKE %s OR maktx LIKE %s OR wgbez LIKE %s OR status LIKE %s limit %s offset %s;"
                        likestrings += (rowperpage,) + (row,)
                        cursor.execute(sql, (likestrings))
                    else:
                        # sql = "SELECT * FROM " + schema_name + '.' + table_name + " WHERE eqktx LIKE %s OR maktx LIKE %s OR wgbez LIKE %s OR status LIKE %s;"
                        cursor.execute(sql, (likestrings))
                    resultlist = cursor.fetchall()
                    print('resultlist получен (не пустой поиск)')

                data = []
                for row in resultlist:
                    data.append({
                        'equnr': row['equnr'],
                        'eqktx': row['eqktx'],
                        'erdat': row['erdat'],
                        'ernam': row['ernam'],
                        'typtx': row['typtx'],
                        'eartx': row['eartx'],
                        'maktx': row['maktx'],
                        'mtbez': row['mtbez'],
                        'wgbez': row['wgbez'],
                        'status': row['status'],
                        'hequi': row['hequi'],
                        'last_oper_date': row['last_oper_date'],
                    })

                response = {
                    'draw': draw,
                    'iTotalRecords': totalRecords,
                    'iTotalDisplayRecords': totalRecordwithFilter,
                    'column_names': column_names,
                    'aaData': data,
                }
                # print('response =', response)
                return jsonify(response)
    except Exception as e:
        print('Не удалось получить ajax ответ. Ошибка:', e)
    finally:
        cursor.close()


# Общий роутинг
@app.route('/', methods=['GET', 'POST'])
def signin():
    """Вход в систему"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        # print('email', form.email.data, 'password', form.password.data, 'remeber',form.remember.data)
        user = User.query.filter_by(email=form.email.data).first()
        if user: # and user.check_password(password):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Invalid username')
            return redirect(url_for('signin'))
    else: print('errors', form.errors)
    return render_template('/user/signin.html', title='Sign In', form=form)


# Общие вводные
@app.route('/index')
@login_required
def index():
    """Первичная страница"""
    return render_template('index.html')

#### Действия пользователя
@app.route('/user/create_user', methods=['get', 'post'])
@login_required
@requires_roles('Администратор')
def create_user():
    """Создание пользователя"""
    form = CreateUserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            usr = User(personnel_number=form.personnel_number.data,
                            email= form.email.data,
                            full_name=form.family_name.data + " " + form.first_name.data + " " + form.second_name.data,
                            family_name=form.family_name.data,
                            first_name=form.first_name.data,
                            second_name=form.second_name.data,
                            dept_id=form.dept_id.data,
                            position=form.position.data,
                            role=form.role.data,
                            status=form.status.data
                            )
            usr.set_password(form.password.data)
            db.session.add(usr)
            db.session.commit()

            # return 'Данные сохранены'
            users = User.query.all()
            return render_template('/user/users.html', users = users, user=usr)
        else:
            message = 'Поля заполнены некорректно. Пожалуйста, проверьте введенные данные.'
            flash(message)

            return render_template('/user/create_user.html', form=form)

    return render_template('/user/create_user.html', title='create user', form=form)

@app.route('/user/edit_user/<user>', methods=['get', 'post'])
@login_required
@requires_roles('Администратор')
def edit_user(user):
    """Редактирование пользователя"""
    if current_user.is_authenticated:

        user = User.query.filter_by(id=user).first()
        form = EditUserForm()

        if request.method == 'GET':
            form.personnel_number.data = user.personnel_number
            form.email.data = user.email
            form.family_name.data = user.family_name 
            form.first_name.data = user.first_name
            form.second_name.data = user.second_name
            form.dept_id.data = user.dept_id
            form.position.data = user.position
            form.role.data = user.role
            form.status.data = user.status

        if request.method == 'POST':
            if form.validate_on_submit():
                user.personnel_number = form.personnel_number.data 
                user.email = form.email.data
                user.family_name = form.family_name.data 
                user.first_name = form.first_name.data
                user.second_name = form.second_name.data
                user.dept_id = form.dept_id.data
                user.position = form.position.data
                user.role = form.role.data
                user.status = form.status.data
                db.session.commit()

            # return 'Данные сохранены'
            users = User.query.all()
            return redirect(url_for('users', user=user.id))

    return render_template('/user/edit_user.html', title='edit user', form = form, user = user.id)

@app.route('/user/edit_password_user/<user>', methods=['GET', 'POST'])
@login_required
@requires_roles('Администратор')
def edit_password_user(user):
    """Изменение пароля пользователя"""
    if current_user.is_authenticated:

        user = User.query.filter_by(id=user).first()
        form = PasswordUserForm()

        if request.method == 'POST':    
            if form.cancel.data:  # if cancel button is clicked, the form.cancel.data will be True
                return redirect(url_for('users', user=user.id)) 
                # redirect(url_for('previous_page_view_name'))
            if form.validate_on_submit():
                if user:
                    user.set_password(form.password.data)
                    db.session.commit()
            return redirect(url_for('users', user=user.id))

    return render_template('/user/edit_password_user.html', title='edit password user', form=form, user=user.id)

@app.route('/user/delete_user/<user>', methods=['GET', 'POST'])
@login_required
@requires_roles('Администратор')
def delete_user(user):
    """Удаление пользователя"""
    if current_user.is_authenticated:

        user = User.query.filter_by(id=user).delete()
        db.session.commit()
        return redirect(url_for('users', user=current_user.id))

    return redirect(url_for('users', user=current_user.id))

@app.route('/user/users/<user>', methods=['GET', 'POST'])
@login_required
@requires_roles('Admin')
def users(user=current_user):
    """Управление пользователями"""
    # if current_user.is_authenticated:
    users = User.query.order_by(User.id.asc()).all()
    cur_user = User.query.filter_by(id=user).first()
    return render_template('/user/users.html', users=users, user=cur_user)
    
@app.route('/user/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Профиль пользователя"""
    if current_user.is_authenticated:
        form = ProfileForm()
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        if request.method == 'POST':
            if form.validate_on_submit():
                user = User.query.filter_by(email=current_user.email).first()
                if user:
                    user.set_password(form.password.data)
                    db.session.commit()
                    flash('Пароль изменен')
    return render_template('/user/profile.html', title='profile', form=form)

@app.route('/logout')
def logout():
    """Выход из системы"""
    logout_user()
    return redirect(url_for('signin'))


# Отчетность
@app.route('/reports/')
@app.route('/reports/<id>', methods=['GET'])
def reports(id=None):
    if id:
        report = Report.query.filter_by(active=True, id=id ).order_by(Report.id.asc()).first()
        return redirect('/reports/filter/{instance}'.format(instance=report.instance))

    else:
        reports = Report.query.filter_by(active=True).order_by(Report.id.asc()).all()
        # cur_report = User.query.filter_by(id=id).first()
        return render_template('/reports/reports.html', reports=reports)

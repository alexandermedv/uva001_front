import json
from pprint import pprint
import flask
import psycopg2
from flask import url_for, redirect, render_template, flash, request, jsonify
from flask_security import login_required, current_user, login_user, logout_user
import pandas as pd

from . import app, db
from .forms import LoginForm, ProfileForm
from .models import User, requires_roles, Report
from sqlalchemy import create_engine
from .report1 import utils as report1
from .glossary import utils as glossary
from .ldap import ldap_authentication

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

@app.route('/glossary/')
@login_required
def render_glossary():

    glos = pd.DataFrame.from_dict(glossary.get_glossary())

    return render_template('/glossary/glossary.html', title='glossary', items=glos[[
        'Название', 'Определение']].to_dict(orient='records'))

    return jsonify(
                   my_table=json.loads(df1.to_json(orient="split"))["data"],
                   columns=[{"title": str(col)} for col in json.loads(df1.to_json(orient="split"))["columns"]])

@app.route('/report1/')
@login_required
def render_report1():
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

@app.route("/_get_table_serverside", methods=["POST", "GET"])
def serverside_table():
    req = flask.request.form
    # print("Request data", flask.request.data)
    # print("Request form", flask.request.form)
    table_name = str(req['table_name'])
    key = str(req['key'])
    schema_name = str(req['schema_name'])
    # print("table_name", table_name)
    # print("key", key)
    # print("schema_name", schema_name)

    column_names = []
    for item in req:
        if 'columns[' in item and '][data]' in item:
            column_names.append(req[item])
    # print("column_names", column_names)

    try:
        with psycopg2.connect(user="locadm",
                                password="Temp001",
                                host="msc199-sdb04.domain.local",
                                port="8031",
                                database="uva_cons") as pg_con:
            cursor = pg_con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            # print('Соединение с базой данных установлено')

            if request.method == 'POST':
                draw = request.form['draw']
                row = int(request.form['start'])
                rowperpage = int(request.form['length'])
                searchValue = request.form["search[value]"]
                # print('draw =', draw)
                # print('row =', row)
                # print('rowperpage =', rowperpage)
                # print('searchValue =', searchValue)

                # Total number of records without filtering
                sql = "SELECT count(*) from " + schema_name + '.' + table_name
                cursor.execute(sql)
                totalRecords = int(cursor.fetchone()[0])
                # print('totalRecords =', totalRecords)

                # Total number of records with filtering
                if len(searchValue) < 3:
                    totalRecordwithFilter = totalRecords
                    # print('totalRecordwithFilter =', totalRecordwithFilter)
                else:
                    likestrings = searchValue.split(' ')
                    likestrings = ['%' + i + '%' for i in likestrings]
                    # print('likestrings', likestrings)
                    s = ''
                    for column in column_names:
                        s += '"' + str(column) + '", '
                    s = s[:-2].replace("['index'], ", "")
                    # print('s =', s)
                    cols = s.replace("['", "")
                    cols = cols.replace("']", "")
                    
                    # print('cols =', cols)

                    sql = """SELECT count(*) from """ + schema_name + '.' + table_name + """ WHERE
                     concat(""" + cols + """) LIKE %s"""
                    for i in range(len(likestrings) - 1):
                        sql += """ AND concat(""" + cols + """) LIKE %s"""
                    # print('sql =', sql)
                    # print('likeString =', tuple(likestrings))
                    cursor.execute(sql, (tuple(likestrings)))
                    totalRecordwithFilter = int(cursor.fetchone()[0])
                    # print('totalRecordwithFilter =', totalRecordwithFilter)

                # Fetch records
                if len(searchValue) < 3:
                    sql = 'SELECT * FROM ' + schema_name + '.' + table_name + ' ORDER BY "' + key + '" asc limit %s offset %s;'
                    cursor.execute(sql, (rowperpage, row))
                    resultlist = cursor.fetchall()
                    # print('resultlist получен (пустой поиск)')
                else:
                    # print('rowperpage =', rowperpage)
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
                    # print('resultlist получен (не пустой поиск)')

                sql = """
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_schema = %s
                    AND table_name   = %s"""
                cursor.execute(sql, (schema_name, table_name))
                columns = cursor.fetchall()
                # print('columns =', columns)

                data = []

                for row in resultlist:
                    d = {}
                    for col in column_names:
                        d[col] = row[col]
                    # print('d =', d)
                    data.append(d)

                # print('data =', data[:5])

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

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """Вход в систему"""
    print(request.args['next'])
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        login = form.ldap_account.data.lower()  
        password = form.password.data
        user = User.query.filter_by(ldap_account=login).first()
        if user and ldap_authentication(login, password): 
            login_user(user)
            return redirect(request.args['next'] or url_for('index'))
        # Переписать
        else:
            flash('Аккаунт Windows, либо пароль указаны некорректно.')
            return redirect(url_for('signin'))
    return render_template('/user/signin.html', title='Sign In', form=form)

# Общие вводные
@app.route('/')
def redirect_login():
    return redirect(url_for('signin'))

@app.route('/login', methods=['GET', 'POST'])
def get_login():
    print('get_login')
    return {}

@app.route('/index')
@login_required
def index():
    """Первичная страница"""
    return render_template('index.html')
    
@app.route('/user/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Профиль пользователя"""
    if current_user.is_authenticated:
        form = ProfileForm()
        form.full_name.data = current_user.last_name
        form.login.data = current_user.ldap_account
        form.email.data = current_user.email
        return render_template('/user/profile.html', title='profile', form=form)

@app.route('/logout')
@login_required
def logout():
    """Выход из системы"""
    logout_user()
    return redirect(url_for('signin'))


# Отчетность
@app.route('/reports/')
@app.route('/reports/<id>', methods=['GET'])
@login_required
def reports(id=None):
    if id:
        report = Report.query.filter_by(active=True, id=id ).order_by(Report.id.asc()).first()
        return redirect('/reports/filter/{instance}'.format(instance=report.instance))

    else:
        reports = Report.query.filter_by(active=True).order_by(Report.id.asc()).all()
        # cur_report = User.query.filter_by(id=id).first()
        return render_template('/reports/reports.html', reports=reports)


@app.route('/repairs/repair0/')
@login_required
def render_repair0():
    return render_template("/repairs/repair0.html")

@app.route('/repairs/repair1/')
@login_required
def render_repair1():
    return render_template("/repairs/repair1.html")

@app.route('/repairs/repair2/')
@login_required
def render_repair2():
    return render_template("/repairs/repair2.html")

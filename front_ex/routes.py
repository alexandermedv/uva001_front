import json
import flask
import psycopg2
from flask import url_for, redirect, render_template, flash, request, jsonify, send_from_directory
from flask_security import login_required, current_user, login_user, logout_user, auth_required, roles_required
import pandas as pd
from sqlalchemy import func
import os

from . import app, db, security, login
from .forms import LoginForm, ProfileForm
from .models import User, requires_roles, Report
from sqlalchemy import create_engine
from .report1 import utils as report1
from .glossary import utils as glossary
from .ldap import ldap_authentication
from .utils import logger

# Руты к дэшбордам
@app.route('/airflow_dash/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_dashapp15():
    """Дашборд по статистике airflow"""
    return render_template('/dashapp15_airflow/overview.html')

# Руты к дэшбордам
@app.route('/risks_dash/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_dashapp11():
    """Дашборд по размеру и динамике недостачи"""
    return render_template('/dashapp11_risks/overview.html')

@app.route('/spark_api_count_request_dash/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_dashapp14():
    """Кол-во запросов СПАРК"""
    return render_template('/dashapp14_spark_api_count_request/overview.html')

@app.route('/credibility_rating_dash/')
#@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_dashapp_credibility_rating():
    """Рейтинг добросовестности клиентов"""
    return render_template('/dashapp_credibility_rating/overview.html')

@app.route('/resellers_uru_dash/')
#@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_dashapp_resellers_uru():
    """Автоматизированный мониторинг: выявление потенциальных посредников"""
    return render_template('/dashapp_resellers_uru/overview.html')

@app.route('/credit_risks_dash/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_dashapp13():
    """Кредитные риски"""
    return render_template('/dashapp13_credit_risks/overview.html')

@app.route('/limit_oper/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_limit_oper():
    """Дашборд по дебиторской задолженности и превышению лимита"""
    return render_template('/limit_oper/overview.html')


@app.route('/dashapp1/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_dashapp1():
    """Дашборд по размеру и динамике недостачи"""
    return render_template('/dashapp1/overview.html')


@app.route('/dashboard3/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_dashapp3():
    """Дашборд по полномочиям в SAP"""
    return render_template('/dashapp3/overview.html')


@app.route('/resellers_dash/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_dashapp5():
    """Дашборд по посредникам"""
    return render_template('/dashapp5/overview.html')


@app.route('/resellers_dash_commerce/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_dashapp9():
    """Дашборд по посредникам (вариант2 - вместо проверки холдингов и операторов проверяется список легитимных контрагентов)"""
    return render_template('/dashapp9_resellers_commerce/overview.html')


@app.route('/monitoring_dash/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_dashapp6_monitoring():
    """Дашборд по мониторингу"""
    return render_template('/dashapp6_monitoring/overview.html')


@app.route('/repairs_dash/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_dashapp7_repairs():
    """Дашборд по ремонтам"""
    return render_template('/dashapp7_repairs/overview.html')

@app.route('/tor_ik_dash/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_dashapp12_tor_neis():
    """Дашборд по ремонтам"""
    return render_template('/dashapp12_tor_neis/overview.html')

@app.route('/empty_transportations_dash/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_dashapp8_empty_transportations():
    """Дашборд по порожним рейсам"""
    return render_template('/dashapp8_empty_transportations/overview.html')


@app.route('/glossary/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_glossary():

    glos = pd.DataFrame.from_dict(glossary.get_glossary())

    return render_template('/glossary/glossary.html', title='glossary', items=glos[[
        'Название', 'Определение']].to_dict(orient='records'))

    return jsonify(
                   my_table=json.loads(df1.to_json(orient="split"))["data"],
                   columns=[{"title": str(col)} for col in json.loads(df1.to_json(orient="split"))["columns"]])


@app.route('/IssueTrack_instruction/')
@logger(os.environ['USER_ACTIONS_FILE'])
def render_IssueTrack_instruction():

    # wtforms.fieldsos.getcwd())

    return send_from_directory(os.getcwd() + '/front_ex/files/' ,'Инструкция по работе с мероприятиями.docx', as_attachment=True)


@app.route('/report1/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_report1():
    df1 = report1.get_details_dost()
    # wtforms.fieldsdf1)
    return render_template('/report1/report1.html', title='report1', items=df1[[
        'equnr', 'eartx', 'status', 'erdat', 'hequi', 'typtx', 
        'last_oper_date']].to_dict(orient='records'))


@app.route('/report_equipment/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_report_equipment():

    return render_template("/report_equipment/report_equipment.html")


@app.route("/_get_table_serverside", methods=["POST", "GET"])
@logger(os.environ['USER_ACTIONS_FILE'])
def serverside_table():
    req = flask.request.form
    # wtforms.fields"Request data", flask.request.data)
    # wtforms.fields"Request form", flask.request.form)
    table_name = str(req['table_name'])
    key = str(req['key'])
    schema_name = str(req['schema_name'])
    # wtforms.fields"table_name", table_name)
    # wtforms.fields"key", key)
    # wtforms.fields"schema_name", schema_name)

    column_names = []
    for item in req:
        if 'columns[' in item and '][data]' in item:
            column_names.append(req[item])
    # wtforms.fields"column_names", column_names)

    try:
        # Убрать хардкод!
        with psycopg2.connect(user="locadm",
                                password="Temp001",
                                host="msc199-sdb04.domain.local",
                                port="8031",
                                database="uva_cons") as pg_con:
            cursor = pg_con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            # wtforms.fields'Соединение с базой данных установлено')

            if request.method == 'POST':
                draw = request.form['draw']
                row = int(request.form['start'])
                rowperpage = int(request.form['length'])
                searchValue = request.form["search[value]"]
                # wtforms.fields'draw =', draw)
                # wtforms.fields'row =', row)
                # wtforms.fields'rowperpage =', rowperpage)
                # wtforms.fields'searchValue =', searchValue)

                # Total number of records without filtering
                sql = "SELECT count(*) from " + schema_name + '.' + table_name
                cursor.execute(sql)
                totalRecords = int(cursor.fetchone()[0])
                # wtforms.fields'totalRecords =', totalRecords)

                # Total number of records with filtering
                if len(searchValue) < 3:
                    totalRecordwithFilter = totalRecords
                    # wtforms.fields'totalRecordwithFilter =', totalRecordwithFilter)
                else:
                    likestrings = searchValue.split(' ')
                    likestrings = ['%' + i + '%' for i in likestrings]
                    # wtforms.fields'likestrings', likestrings)
                    s = ''
                    for column in column_names:
                        s += '"' + str(column) + '", '
                    s = s[:-2].replace("['index'], ", "")
                    # wtforms.fields's =', s)
                    cols = s.replace("['", "")
                    cols = cols.replace("']", "")

                    # wtforms.fields'cols =', cols)

                    sql = """SELECT count(*) from """ + schema_name + '.' + table_name + """ WHERE
                     concat(""" + cols + """) LIKE %s"""
                    for i in range(len(likestrings) - 1):
                        sql += """ AND concat(""" + cols + """) LIKE %s"""
                    # wtforms.fields'sql =', sql)
                    # wtforms.fields'likeString =', tuple(likestrings))
                    cursor.execute(sql, (tuple(likestrings)))
                    totalRecordwithFilter = int(cursor.fetchone()[0])
                    # wtforms.fields'totalRecordwithFilter =', totalRecordwithFilter)

                # Fetch records
                if len(searchValue) < 3:
                    sql = 'SELECT * FROM ' + schema_name + '.' + table_name + ' ORDER BY "' + key + '" asc limit %s offset %s;'
                    cursor.execute(sql, (rowperpage, row))
                    resultlist = cursor.fetchall()
                    # wtforms.fields'resultlist получен (пустой поиск)')
                else:
                    # wtforms.fields'rowperpage =', rowperpage)
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
                    # wtforms.fields'resultlist получен (не пустой поиск)')

                sql = """
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_schema = %s
                    AND table_name   = %s"""
                cursor.execute(sql, (schema_name, table_name))
                columns = cursor.fetchall()
                # wtforms.fields'columns =', columns)

                data = []

                for row in resultlist:
                    d = {}
                    for col in column_names:
                        d[col] = row[col]
                    # wtforms.fields'd =', d)
                    data.append(d)

                # wtforms.fields'data =', data[:5])

                response = {
                    'draw': draw,
                    'iTotalRecords': totalRecords,
                    'iTotalDisplayRecords': totalRecordwithFilter,
                    'column_names': column_names,
                    'aaData': data,
                }

                # wtforms.fields'response =', response)

                return jsonify(response)
    except Exception as e:
        print('Не удалось получить ajax ответ. Ошибка:', e)
    finally:
        cursor.close()


@app.route('/signin', methods=['GET', 'POST'])
@logger(os.environ['USER_ACTIONS_FILE'])
def signin():
    """Вход в систему"""
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # print('user = ', User.ldap_account)
    # print('user = ', form.ldap_account.data)
    if form.validate_on_submit():
        login = form.ldap_account.data.lower()  
        print('login =', login)
        password = form.password.data
        print('password =', password)
        print('ldap_authentication(login, password) = ', ldap_authentication(login, password))
        print(User.query.first().id)
        user = User.query.filter(func.lower(User.ldap_account)==login).first()
        print('user =', user.ldap_account)
        print('user =', security.datastore.find_user(email="svc_fs_uva@pgkweb.ru"))
        if user and ldap_authentication(login, password):
            print('Логиним юзера')
            login_user(user)
            # security.datastore.commit()
            print('Получилось залогиниться?', current_user.is_authenticated())
            print('current_user =', current_user)
            print('current_user.email =', current_user.email)
            print('current_user.check_report_roles(glossary) =', current_user.check_report_roles('glossary'))
            if 'next' in request.args:
                return redirect(request.args['next'])
            print('редиректим на индекс')
            return redirect(url_for('index'))
        # Переписать
        else:
            flash('Аккаунт Windows, либо пароль указаны некорректно.')
            return redirect(url_for('signin'))
    return render_template('/user/signin.html', title='Sign In', form=form)


# Общие вводные
@app.route('/')
@logger(os.environ['USER_ACTIONS_FILE'])
def redirect_login():
    return redirect(url_for('signin'))


@app.route('/index')
# @login_required
# @auth_required('session')
# @roles_required('admin')
@logger(os.environ['USER_ACTIONS_FILE'])
def index():
    """Первичная страница"""
    # print('login.current_user.is_authenticated() =', login.current_user.is_authenticated())
    # print('authenticated?', current_user.is_authenticated())
    return render_template('index.html')
    

@app.route('/user/profile', methods=['GET', 'POST'])
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
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
@logger(os.environ['USER_ACTIONS_FILE'])
def logout():
    """Выход из системы"""
    logout_user()
    return redirect(url_for('signin'))


# Отчетность
@app.route('/reports/')
@app.route('/reports/<id>', methods=['GET'])
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
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
@logger(os.environ['USER_ACTIONS_FILE'])
def render_repair0():
    return render_template("/repairs/repair0.html")


@app.route('/repairs/repair1/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_repair1():
    return render_template("/repairs/repair1.html")


@app.route('/repairs/repair2/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_repair2():
    return render_template("/repairs/repair2.html")


@app.route('/resellers/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_resellers():
    return render_template("/resellers/resellers.html")


@app.route('/resellers_table/')
@login_required
@logger(os.environ['USER_ACTIONS_FILE'])
def render_resellers_table():
    return render_template("/resellers/resellers_table.html")

@app.route('/reports/download_test')
@login_required
def report_download_test():
    return render_template('/dashapp8_empty_transportations/download_test.html')

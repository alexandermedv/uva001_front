'''Утилиты загрузки данных'''
import time, os
from io import StringIO
import csv
from datetime import datetime
from sqlalchemy import create_engine
from flask_security import login_required, current_user, login_user, logout_user
from .models import Log

from . import app, db


def get_postgre_con_str():
    """Строка подключения к postgre прод"""
    return os.environ['POSTGRE_URL_DASH']

def get_log_con_str():
    """Строка подключения к log прод"""
    return os.environ['SQLALCHEMY_DATABASE_LOG']

def get_sap_s4_con_str():
    """Строка подключения к S4 прод"""
    return os.environ['SAP_HOST_S4']

def get_udv_con_str():
    """Строка подключения к УДВ прод"""
    return os.environ['UDV']
    # return "DRIVER={ODBC Driver 17 for SQL Server};SERVER=172.16.2.186,1433;DATABASE=ERVP;uid=db_uva;pwd=uva123"

def get_mandant():
    """Мандант"""
    return app.config['MANDANT']

# -- Подключение
def psql_insert_copy(table, conn, keys, data_iter):
    """Метод для загрузки датафрейма в postgre"""
    # gets a DBAPI connection that can provide a cursor
    dbapi_conn = conn.connection

    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name

        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
            table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)

def debug_info(df1, offset, start_time = time.time()):
    """Вывод лога выполнения"""
    print("--- %s seconds ---" % (int(time.time() - start_time)))
    print('Загружено записей: {}'.format(len(df1.index) + offset))
    ## print(df.head(1))

def completeness_check(tables, engine_sap_s4, engine_postgre, schema):
    """Проверка полноты загруженных данных"""
    check = True
    for table in tables:
        count1 = engine_sap_s4.execute("SELECT COUNT (*) FROM %s.%s" %(schema, table)).fetchone()
        count2 = engine_postgre.execute("SELECT COUNT (*) FROM sap_s4.%s" %(table)).fetchone()
        if count1 != count2:
            check = False
            break
    if check:
        return print('Проверка полноты данных успешно выполнена')
    else:
        return print('Проверка полноты не выполнена, данные искажены, утеряны или задублированы')

def logger(path):

    def _logger(old_function):

        def new_function(*args, **kwargs):
            if current_user.is_authenticated:
                log_item = Log(login=current_user.ldap_account, timestamp=str(datetime.now()), message=old_function.__name__)
                db.session.add(log_item)
                db.session.commit()
            # with open(path, 'a') as file:
                # if current_user.is_authenticated:
                #     file.write(f'Логин: {current_user.ldap_account}\n')
                # else:
                #     file.write(f'Логин: неавторизованный пользователь\n')
                # file.write(f'Дата и время: {str(datetime.now())}\n')
                # file.write(f'Вызвана функция: {old_function.__name__}\n')
                # file.write('-------------------------------------------' + '\n')
                
            result = old_function(*args, **kwargs)

            return result

        new_function.__name__ = old_function.__name__
        return new_function

    return _logger
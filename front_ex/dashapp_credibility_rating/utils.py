"""Выгрузка данных и вспомогательные функции"""
import os
from contextlib import contextmanager
from typing import Optional
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import json
from datetime import datetime
import xmlschema  # type: ignore
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from datetime import date

# Переменные
min_date = date(2020,1,1)
max_date = date.today()

# Таблица по клиентам
def get_clients_df(client=None):
    """Таблица по клиентам"""
    if client is None:
        sql = '''
            SELECT "Клиент",
                    "Наименование клиента",
                    "Холдинг клиента",
                    "ИНН клиента",
                    "ОГРН клиента",
                    "Дата регистрации клиента",
                    "ОКВЭД",
                    "Кол-во рейсов ТМ",
                    "Доля посредничества",
                    "Изменение доли основного груза",
                    "Разных грузов у клиента",
                    "Последний фин период", 
			        "Выручка посл фин период",
                    "ДО: Доходность",
                    "СХ: Доходность",
                    "Кол-во рейсов" AS "ДО: Кол-во рейсов",
                    "Кол-во груженых рейсов" AS "ДО: Кол-во груженых рейсов",
                    "ДО миним",
                    "ДО критичн",
                    "ДО норматив",
                    "ДО целев",
                    "Доля низкодоходности",
                    "Доля критичнодоходности"
            FROM dashboard.credibility_uru
        '''
        df_clients = pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))
        df_clients = df_clients.sort_values(by=['Доля посредничества', 'Холдинг клиента'], ascending=False).reset_index(drop=True)
        return df_clients
    else:
        sql = '''
            SELECT "Клиент",
                    "Наименование клиента",
                    "Холдинг клиента",
                    "ИНН клиента",
                    "ОГРН клиента",
                    "Дата регистрации клиента",
                    "ОКВЭД",
                    "Кол-во рейсов ТМ",
                    "Доля посредничества",
                    "Изменение доли основного груза",
                    "Разных грузов у клиента",
                    "Последний фин период", 
			        "Выручка посл фин период",
                    "ДО: Доходность",
                    "СХ: Доходность",
                    "Кол-во рейсов" AS "ДО: Кол-во рейсов",
                    "Кол-во груженых рейсов" AS "ДО: Кол-во груженых рейсов",
                    "ДО миним",
                    "ДО критичн",
                    "ДО норматив",
                    "ДО целев",
                    "Доля низкодоходности",
                    "Доля критичнодоходности"
            FROM dashboard.credibility_uru
            WHERE "Клиент" = '%s'
        ''' % (client)
        df_client = pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))
        return df_client

# Таблица по грузам
def get_gruzes_df(client=None):
    if client is None:
        sql = '''
            SELECT "Клиент",
                    "Наименование клиента",
                    "Код груза",
                    "Наименование груза",
                    "Рейсов 2020",
                    "Рейсов 2021",
                    "Рейсов 2022",
                    "Рейсов 2023"
            FROM dashboard.credibility_gruz_changes_uru
        '''
        return "Выберите клиента"
    else:
        sql = '''
            SELECT "Клиент",
                    "Наименование клиента",
                    "Код груза",
                    "Наименование груза",
                    "Рейсов 2020",
                    "Рейсов 2021",
                    "Рейсов 2022",
                    "Рейсов 2023"
            FROM dashboard.credibility_gruz_changes_uru
            WHERE "Клиент" = '%s'
        ''' % (client)
        return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

def get_go_rating(client):
    sql2 = '''
        SELECT "Грузоотправитель",
                "Грузоотправитель имя",
                "Договор",
                "Сумма продаж ГО у клиента",
                "Доля ГО у клиента",
                "Результат анализа",
                "Метрика посредничества"
        FROM dashboard.credibility_posrednics_go_rating_uru е
        WHERE "Клиент" = '%s'
    ''' % (client)
    return pd.read_sql(sql2, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

# Фильтры
date_filter = dbc.FormGroup([
    dbc.Label("Период", html_for="date_filter"),
    dcc.DatePickerRange(
        id="date_filter",
        start_date=date(2020,1,1),
        end_date=date.today(),
        display_format='D MMM YYYY'
    )
])
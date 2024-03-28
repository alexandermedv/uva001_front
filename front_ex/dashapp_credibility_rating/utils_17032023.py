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
def get_clients_df(start_date, end_date, client=None):
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
                    "Доля посредничества",
                    max(days_off_cur_sum) AS "Дней просрочки ДЗ", -- максимум за один день
                    max(days_off_cur_count) AS "Случаев просрочки ДЗ", -- максимум за один день
                    max(dept_days_off_sum) AS "Сумма просрочки", --максимальная сумма за один день в выбранном периоде
                    max("Изменение доли основного груза") AS "Изменение доли основного груза",
            max("Разных грузов у клиента") AS "Разных грузов у клиента"
            FROM dashboard.credibility_test_uru
            WHERE "Дата" BETWEEN '%s' AND '%s'
            GROUP BY "Клиент",
                    "Наименование клиента",
                    "Холдинг клиента",
                    "ИНН клиента",
                    "ОГРН клиента",
                    "Дата регистрации клиента",
                    "ОКВЭД",
                    "Доля посредничества"
        ''' % (start_date, end_date)
        df_clients = pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))
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
                    "Доля посредничества",
                    max(days_off_cur_sum) AS "Дней просрочки ДЗ", -- максимум за один день
                    max(days_off_cur_count) AS "Случаев просрочки ДЗ", -- максимум за один день
                    max(dept_days_off_sum) AS "Сумма просрочки", --максимальная сумма за один день в выбранном периоде
                    max("Изменение доли основного груза") AS "Изменение доли основного груза",
            max("Разных грузов у клиента") AS "Разных грузов у клиента"
            FROM dashboard.credibility_test_uru
            WHERE "Дата" BETWEEN '%s' AND '%s'
                AND "Клиент" = '%s'
            GROUP BY "Клиент",
                    "Наименование клиента",
                    "Холдинг клиента",
                    "ИНН клиента",
                    "ОГРН клиента",
                    "Дата регистрации клиента",
                    "ОКВЭД",
                    "Доля посредничества"
        ''' % (start_date, end_date, client)
        df_client = pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))
        return df_client

# Дропдаун для грузоотправителей
def get_list_go(start_date, end_date, client_holding):
    sql2 = '''
        SELECT DISTINCT "ГО (холдинг)", "Метрика посредничества", "Сумма продаж ГО(холдинг) у Клиента"
        FROM dashboard.credibility_posrednics_2_uru
        WHERE "Дата раскредитования" BETWEEN '%s' AND '%s'
            AND "Клиент (холдинг)" = '%s'
        ORDER BY "Метрика посредничества", "Сумма продаж ГО(холдинг) у Клиента" DESC
    ''' % (start_date, end_date, client_holding)
    df_list_go = pd.read_sql(sql2, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))
    return [{"label": i, "value": i} for i in df_list_go['ГО (холдинг)']]

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
        return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))
    
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

# Пока тест - фильтрация
def filter_data(category, sub_category, segment, start_date, end_date, df, province):
    filtered_df = df.copy()
    if category is not None:
        filtered_df = filtered_df[filtered_df["Product Category"] == category]
    if sub_category is not None:
        filtered_df = filtered_df[filtered_df["Product Sub-Category"] == sub_category]
    if segment is not None:
        filtered_df = filtered_df[filtered_df["Customer Segment"] == segment]
    if province is not None:
        if "entry" in province["points"][0].keys():
            if province["points"][0]["entry"] == '':
                filtered_df = filtered_df[filtered_df["Province"] == province["points"][0]["customdata"][0]]
    if start_date is not None:
        if type(start_date) == str:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        filtered_df = filtered_df[filtered_df["Order Date"] >= start_date]
    if end_date is not None:
        if type(end_date) == str:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        filtered_df = filtered_df[filtered_df["Order Date"] <= end_date]
    return filtered_df
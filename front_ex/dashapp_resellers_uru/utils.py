"""Выгрузка данных и вспомогательные функции"""
import os
from sqlalchemy import create_engine
import pandas as pd
from dash import dcc, html
from datetime import date

# Переменные
conn = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)

# Таблица по клиентам
def get_clients_df(client=None):
    """Таблица по клиентам"""
    if client is None:
        sql = '''
            SELECT "id",
                    "Ранг"::integer,
                    "Клиент",
                    "Наименование клиента",
                    "Кол-во рейсов клиента",
                    "Общая сумма клиента (Руб.)",
                    "Средневзвешенное посредничество (Руб.)" AS "Средневзвешенное посредничество",
                    "Доля посредничества",
                    "Отношение продаж клиента к пер. годом ранее" AS "Отношение продаж к годом ранее",
                    "Общий рейтинг"
            FROM dashboard.credibility_posrednics_1_uru
        '''
        df_clients = pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))
        df_clients = df_clients.sort_values(by=["Общий рейтинг"], ascending=False).reset_index(drop=True)
        return df_clients
    else:
        sql = '''
            SELECT "id",
                    "Ранг"::integer,
                    "Клиент",
                    "Наименование клиента",
                    "Кол-во рейсов клиента",
                    "Общая сумма клиента (Руб.)",
                    "Средневзвешенное посредничество (Руб.)" AS "Средневзвешенное посредничество",
                    "Доля посредничества",
                    "Отношение продаж клиента к пер. годом ранее" AS "Отношение продаж к годом ранее",
                    "Общий рейтинг"
            FROM dashboard.credibility_posrednics_1_uru
            WHERE "Клиент" = '%s'
        ''' % (client)
        df_client = pd.read_sql(sql, con=conn)
        return df_client

def get_go_rating(id_client):
    sql2 = '''
        SELECT "Грузоотправитель",
                "Грузоотправитель имя",
                "Договор",
                "Сумма продаж ГО у клиента",
                "Доля ГО у клиента",
                "Результат анализа",
                "Метрика посредничества",
                "Клиент",
                "Наименование клиента"
        FROM dashboard.credibility_posrednics_go_rating_uru е
        WHERE "client_id" = '%s'
    ''' % (id_client)
    temp_data = pd.read_sql(sql2, con=conn)
    return temp_data.loc[0,"Клиент"], temp_data.loc[0, "Наименование клиента"], temp_data.drop(columns=["Клиент", "Наименование клиента"])

def get_data_for_graph(go):
    if go:
        sql3 = '''
            SELECT *
            FROM dashboard.credibility_posrednics_2_uru
            WHERE "Грузоотправитель" = '%s'
        ''' % (go)
    return pd.read_sql(sql3, con=conn)

def get_values_for_levels():
    sql4='''
        SELECT *
        FROM dashboard.credibility_posrednics_lvl_descr
    '''
    sql5='''
        SELECT *
        FROM dashboard.credibility_posrednics_lvl_1_uru
    '''
    sql6='''
        SELECT *
        FROM dashboard.credibility_posrednics_lvl_2_uru
    '''
    df_variables = pd.read_sql(sql4, con=conn)
    df_client_lvl_1 = pd.read_sql(sql5, con=conn)
    df_client_lvl_2 = pd.read_sql(sql6, con=conn)
    return df_variables, df_client_lvl_1, df_client_lvl_2

def query_resellers_logs():
    sql7 = '''
        SELECT *
        FROM dashboard.resellers_log
        ORDER BY to_date("Дата обнаружения", 'DD.MM.YYYY') DESC
    '''
    return pd.read_sql(sql7, con=conn)

def update_postgres_resellers_log(pg):
    pg.to_sql('resellers_log', con=conn, schema='dashboard', if_exists='replace', index=False)
    return True
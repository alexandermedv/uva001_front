"""Выгрузка данных и вспомогательные функции"""
import os
from sqlalchemy import create_engine
import pandas as pd
from dash import dcc, html
from datetime import date

conn = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)

def get_materials_df():
    sql = '''
        SELECT *
        FROM dashboard.zakupki_materials_uru
    '''
    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))

def get_filials_df():
    sql2 = '''
        SELECT *
        FROM dashboard.zakupki_filials_uru
    '''
    return pd.read_sql(sql2, con=conn)

def get_df_grouped_zavod():
    sql3 = '''
        SELECT *
        FROM dashboard.zakupki_grouped_zavod_uru
    '''
    return pd.read_sql(sql3, con=conn)

def get_ekbe_postavshiki_df():
    sql4 = '''
        SELECT *
        FROM dashboard.zakupki_ekbe_postavshiki_uru
    '''
    return pd.read_sql(sql4, con=conn)

def get_df_grouped_zavod_postav():
    sql5 = '''
        SELECT *
        FROM dashboard.zakupki_grouped_zavod_postav_uru
    '''
    return pd.read_sql(sql5, con=conn)

def get_df_pivot_otkl():
    sql6 = '''
        SELECT *
        FROM dashboard.zakupki_pivot_otkl_uru
    '''
    return pd.read_sql(sql6, con=conn)

def get_df_grouped_zavod_for_bar():
    sql7 = '''
        SELECT *
        FROM dashboard.zakupki_grouped_zavod_for_bar_uru
    '''
    return pd.read_sql(sql7, con=conn)

# def get_data_for_graph(go):
#     if go:
#         sql3 = '''
#             SELECT *
#             FROM dashboard.credibility_posrednics_2_uru
#             WHERE "Грузоотправитель" = '%s'
#         ''' % (go)
#     return pd.read_sql(sql3, con=conn)

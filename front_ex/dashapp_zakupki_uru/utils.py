"""Выгрузка данных и вспомогательные функции"""
import os
from sqlalchemy import create_engine
import pandas as pd
from dash import dcc, html
from datetime import date
import plotly.express as px

conn = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)

# clrs - Это цвета для отрисовки графика (Закупки по группам материалов)
clrs1 = px.colors.qualitative.Set1 + px.colors.qualitative.Set2 + px.colors.qualitative.Set3 + px.colors.qualitative.Vivid
clrs = {}
for i, clr in enumerate(clrs1):
    clrs[i] = str(clr)
del clrs1

def get_materials_df():
    sql = '''
        SELECT *
        FROM dashboard.zakupki_materials_uru
    '''
    return pd.read_sql(sql, con=conn, index_col='index')

def get_filials_df():
    sql2 = '''
        SELECT *
        FROM dashboard.zakupki_filials_uru
    '''
    return pd.read_sql(sql2, con=conn)

def get_df_grouped_zavod(postav):
    sql3 = '''
        SELECT *
        FROM dashboard.zakupki_grouped_zavod_uru
        WHERE "Поставщик" = '%s'
    ''' % (postav)
    return pd.read_sql(sql3, con=conn)

def get_ekbe_postavshiki_df():
    sql4 = '''
        SELECT index, id,
            "Поставщик", 
            COALESCE("Поставщик имя", "Наименование поставщик kna1") AS "Поставщик имя",
            "ИНН поставщик", "ОГРН поставщик", "ОКВЭД поставщик",
            "Разных групп материалов",
            "Количество заказа 2022", "Количество заказа 2023", "Количество заказа 2024",
            "Сумма во ВВ 2022", "Сумма во ВВ 2023", "Сумма во ВВ 2024",
            "Последний фин период", "Выручка посл фин период", "Доля ПГК в выручке поставщика"
        FROM dashboard.zakupki_ekbe_postavshiki_uru
    '''
    return pd.read_sql(sql4, con=conn, index_col='index')

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

def get_df_postav_materials_2(postavshik):
    sql8 = '''
        SELECT *
        FROM dashboard.zakupki_postav_materials_2_uru
        WHERE "Поставщик" = '%s'
        ORDER BY "Общяя сумма" DESC
    ''' % (postavshik)
    return pd.read_sql(sql8, con=conn)


postav_materials_2_columns = [
    {"id":"Группа материалов", "name":"Группа материалов"},
    {"id":"Имя группы материалов", "name":"Имя группы материалов"},
    {"id":"Расшифровка группы материалов", "name":"Расшифровка группы материалов"},
    {"id":"Количество заказа 2020", "name":"Кол-во заказа 2020",
             "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
    {"id":"Количество заказа 2021", "name":"Кол-во заказа 2021",
             "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
    {"id":"Количество заказа 2022", "name":"Кол-во заказа 2022",
             "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
    {"id":"Количество заказа 2023", "name":"Кол-во заказа 2023",
             "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
    {"id":"Количество заказа 2024", "name":"Кол-во заказа 2024",
             "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
    {"id":"Сумма во ВВ 2020", "name":"Сумма во ВВ 2020",
             "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
    {"id":"Сумма во ВВ 2021", "name":"Сумма во ВВ 2021",
             "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
    {"id":"Сумма во ВВ 2022", "name":"Сумма во ВВ 2022",
             "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
    {"id":"Сумма во ВВ 2023", "name":"Сумма во ВВ 2023",
             "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
    {"id":"Сумма во ВВ 2024", "name":"Сумма во ВВ 2024",
             "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
]

grouped_zavod_columns = [
    {"id":"Завод", "name":"Завод"},
    {"id":"Завод_название", "name":"Имя завода"},
    {"id":"Поставщик", "name":"Поставщик"},
    {"id":"Дата поставки", "name":"Дата поставки"},
    {"id":"Документ закупки", "name":"Документ закупки"},
    {"id":"Вид документа закупки", "name":"Вид документа закупки"},
    {"id":"Материал", "name":"Материал"},
    {"id":"Наим. материала", "name":"Наим. материала"},
    {"id":"Количество заказа", "name":"Кол-во заказа",
            "type": "numeric", "format": {'specifier': ',.2f',"locale": {"group": " "}}},
    {"id":"ЕИ", "name":"ЕИ"},
    {"id":"Сумма во ВВ", "name":"Сумма во ВВ",
            "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
    {"id":"Цена в закупке(филиал)", "name":"Средняя цена в закупке",
            "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
    {"id":"Средняя цена", "name":"Средняя цена(Материал-Вид ДЗ)",
            "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
    {"id":"Дельта среднего", "name":"Дельта среднего",
            "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
    {"id":"Общее отклонение от среднего", "name":"Общее отклонение от среднего",
            "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
]


style_cell_datatable={
    'height': 'auto',
    'minWidth': '50px', 'maxWidth': '300px',
    'whiteSpace': 'normal',
    'fontSize': 11, 'font-family': 'Arial'
}
style_header_datatable={
    'backgroundColor': '#EFECEC',
    'color': 'black',
    'fontWeight': 'bold'
}
# def get_data_for_graph(go):
#     if go:
#         sql3 = '''
#             SELECT *
#             FROM dashboard.credibility_posrednics_2_uru
#             WHERE "Грузоотправитель" = '%s'
#         ''' % (go)
#     return pd.read_sql(sql3, con=conn)

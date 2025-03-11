""" Интерактивные элементы для отчетов по запчастям."""
import datetime as dt
import numpy as np
from dash.dependencies import Input, Output
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
#import dash_table
#from dash_table.Format import Format, Scheme, Group
#from app.dashes import dashapp1
#from app.raw_sql import dashapp1_non_used_details_udv_filial
import plotly.graph_objects as go
import pandas as pd
#from .layout import layout2
#import string
from ..utils import get_osv_detail_by_dates, get_osv_detail_by_dates2, get_osv_data
from ..utils import get_branch_names, get_detail_type_names, get_warehouse_names
from ..pages import dash_app

#from flask_app import engine_analysis, engine_cons

# def register_callbacks(dashapp1):

#     # Выбор отчета на главной странице
#     @dashapp1.callback(Output('page-content', 'children'),
#                        [Input('url', 'pathname')])
#     def display_page(pathname):
#         if pathname == '/repair_parts/dashboard1':
#             return layout1
#         elif pathname == '/repair_parts/dashboard2':
#             return layout2
#         else:
#             return index_page
#         # You could also return a 404 "URL not found" page here


# Значения списка филиалов
@dash_app.callback(
Output(component_id='dashboard2-dropdown1', component_property='options'),
[Input('dashboard2-tabs', 'value')]
)

def update_dropdown1(tab):
    """Список значений фильтра по филиалам"""
    # df0=pd.read_sql("""
    #             SELECT DISTINCT "Название бизнес-сферы"
    #             FROM sap_s4.osv_94
    #             ORDER BY "Название бизнес-сферы" ASC
    #             """, con=engine_cons)

    if tab is not None:
        df0 = get_branch_names()
        list1 = df0['Название бизнес-сферы'].tolist()
        list2 = ['Все филиалы'] + list1
        df1 = pd.DataFrame(list2,columns=['Название бизнес-сферы'])
    #df['Название бизнес-сферы'] = df['Название бизнес-сферы'].replace('Ярославский филиал', 'ФЯрв')

    return [{'label': i, 'value': i} for i in df1['Название бизнес-сферы']]

# Значения списка типов запчастей
@dash_app.callback(
Output(component_id='dashboard2-dropdown2', component_property='options'),
[Input('dashboard2-tabs', 'value')]
)

def update_dropdown2(tab):
    """Список значение фильтра по типам запчастей"""
    if tab is not None:
        df0 = get_detail_type_names()
        list1 = df0['Группа материалов'].tolist()
        list2 = ['Все запчасти'] + list1
        df1 = pd.DataFrame(list2,columns=['Группа материалов'])
    #df['Название бизнес-сферы'] = df['Название бизнес-сферы'].replace('Ярославский филиал', 'ФЯрв')

    return [{'label': i, 'value': i} for i in df1['Группа материалов']]

# Значения списка складов
@dash_app.callback(
Output(component_id='dashboard2-dropdown3', component_property='options'),
[Input('dashboard2-tabs', 'value'),
Input('dashboard2-dropdown1', 'value')]
)

def update_dropdown3(tab, filial):
    """Список значений фильтра по складам"""
    # df0=pd.read_sql("""
    #             SELECT DISTINCT "КНаименование склада", "Название бизнес-сферы"
    #             FROM sap_s4.osv_94
    #             ORDER BY "КНаименование склада" ASC
    #             """, con=engine_cons)

    if tab is not None:
        df0 = get_warehouse_names()

    branches = []
    if filial == 'Все филиалы':
        branches = df0["Название бизнес-сферы"].unique()
    else:
        branches.append(filial)
    df0 = df0.loc[df0["Название бизнес-сферы"].isin(branches)]

    df0['Название бизнес-сферы'] = df0['Название бизнес-сферы'].replace(
        'Владивостокский филиал', 'ФВлд')
    df0['Название бизнес-сферы'] = df0['Название бизнес-сферы'].replace(
        'Воронежский филиал', 'ФВрж')
    df0['Название бизнес-сферы'] = df0['Название бизнес-сферы'].replace(
        'Екатеринбургский филиал', 'ФЕкб')
    df0['Название бизнес-сферы'] = df0['Название бизнес-сферы'].replace(
        'Иркутский филиал', 'ФИрк')
    df0['Название бизнес-сферы'] = df0['Название бизнес-сферы'].replace(
        'Красноярский филиал', 'ФКрс')
    df0['Название бизнес-сферы'] = df0['Название бизнес-сферы'].replace(
        'Московский филиал', 'ФМск')
    df0['Название бизнес-сферы'] = df0['Название бизнес-сферы'].replace(
        'Нижегородский филиал', 'НжН')
    df0['Название бизнес-сферы'] = df0['Название бизнес-сферы'].replace(
        'Новосибирский филиал', 'ФНвб')
    df0['Название бизнес-сферы'] = df0['Название бизнес-сферы'].replace(
        'Ростовский филиал', 'ФРст')
    df0['Название бизнес-сферы'] = df0['Название бизнес-сферы'].replace(
        'Самарский филиал', 'ФСмр')
    df0['Название бизнес-сферы'] = df0['Название бизнес-сферы'].replace(
        'Санкт-Петербургск.филиал', 'ФСПб')
    df0['Название бизнес-сферы'] = df0['Название бизнес-сферы'].replace(
        'Саратовский филиал', 'ФСрт')
    df0['Название бизнес-сферы'] = df0['Название бизнес-сферы'].replace(
        'Челябинский филиал', 'ФЧлб')
    df0['Название бизнес-сферы'] = df0['Название бизнес-сферы'].replace(
        'Ярославский филиал', 'ФЯрв')

    df0['Название бизнес-сферы'] = df0[
        'Наименование склада'] + " (" + df0['Название бизнес-сферы'] + ")"

    list1 = df0['Название бизнес-сферы'].tolist()
    list2 = ['Все склады'] + list1
    df1 = pd.DataFrame(list2,columns=['label'])

    list3 = df0['Наименование склада'].tolist()
    list4 = ['Все склады'] + list3
    df1['value'] = list4

    return df1.to_dict('records')

# Сумма недостачи за выбранный период
@dash_app.callback(Output(component_id='shortage_amount', component_property='children'),
    [Input('dashboard2-date-picker-range', 'start_date'),
    Input('dashboard2-date-picker-range', 'end_date'),
    Input('dashboard2-dropdown1', 'value'),
    Input('dashboard2-dropdown2', 'value'),
    Input('dashboard2-dropdown3', 'value'),
    Input('dashboard2-tabs', 'value')])

def shortage_amount(start_date, end_date, filial, detail_type, warehouse, tab):
    """Вычисление суммы недостачи"""
    #df0 = get_osv_detail_by_dates(start_date, end_date, debug=False)
    df0 = get_osv_data(start_date, end_date, debug=False)
    #shortage = df0['Изменение за период'].sum()
    branches = []
    if filial == 'Все филиалы':
        branches = df0["Название бизнес-сферы"].unique()
    else:
        branches.append(filial)
    if tab == 'tab-2' or tab == 'tab-3' or tab == 'tab-4':
        df0 = df0.loc[df0["Название бизнес-сферы"].isin(branches)]

    d_type = []
    if detail_type == 'Все запчасти':
        d_type = df0["Группа материалов"].unique()
    else:
        d_type.append(detail_type)
    if tab == 'tab-1' or tab == 'tab-3' or tab == 'tab-4':
        df0 = df0.loc[df0["Группа материалов"].isin(d_type)]

    sklad = []
    if warehouse == 'Все склады':
        sklad = df0["Наименование склада"].unique()
    else:
        sklad.append(warehouse)
    if tab == 'tab-2' or tab == 'tab-4':
        df0 = df0.loc[df0["Наименование склада"].isin(sklad)]
    shortage = '{:,.0f}'.format(round(df0['Изменение за период'].sum())/1000).replace(',', ' ')

    return shortage

# data = None
# d_start = None
# d_end = None

# Построение содержимого выбранной закладки
@dash_app.callback(Output('tab-content', 'children'),
    [Input('dashboard2-date-picker-range', 'start_date'),
    Input('dashboard2-date-picker-range', 'end_date'),
    Input('dashboard2-tabs', 'value'),
    Input('dashboard2-dropdown1', 'value'),
    Input('dashboard2-dropdown2', 'value'),
    Input('dashboard2-dropdown3', 'value'),
    Input('dashboard2-dropdown4', 'value'),
    Input('warehouse_quantity', 'value'),
    Input('ri-level', 'value')])

def render_content(start_date, end_date, tab, filial, detail_type,
 warehouse, sorting, warehouse_quantity, data_level):
    """Построение содержимого выбранной закладки"""
    # global data
    # global d_start
    # global d_end

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    df0 = get_osv_data(start_date, end_date, debug=False)
    df0_left = get_osv_data(dt.datetime.strptime('1900-01-01','%Y-%m-%d'
        ), start_date - dt.timedelta(days=1))

    branches = []
    if filial == 'Все филиалы':
        branches = df0["Название бизнес-сферы"].unique()
    else:
        branches.append(filial)

    d_type = []
    if detail_type == 'Все запчасти':
        d_type = df0["Группа материалов"].unique()
    else:
        d_type.append(detail_type)

    sklad = []
    if warehouse == 'Все склады':
        sklad = df0["Наименование склада"].unique()
    else:
        sklad.append(warehouse)


    # df0['Изменение за период'] = df0['Изменение за период'] / 1000
    # df0['Дебет'] = df0['Дебет'] / 1000
    # df0['Кредит'] = df0['Кредит'] / 1000

    # df0['Аббревиатура филиала'] = df0['Название бизнес-сферы']
    # df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
    #     'Владивостокский филиал', 'ФВлд')
    # df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
    #     'Воронежский филиал', 'ФВрж')
    # df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
    #     'Екатеринбургский филиал', 'ФЕкб')
    # df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
    #     'Иркутский филиал', 'ФИрк')
    # df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
    #     'Красноярский филиал', 'ФКрс')
    # df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
    #     'Московский филиал', 'ФМск')
    # df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
    #     'Нижегородский филиал', 'ФНжН')
    # df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
    #     'Новосибирский филиал', 'ФНвб')
    # df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
    #     'Ростовский филиал', 'ФРст')
    # df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
    #     'Самарский филиал', 'ФСмр')
    # df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
    #     'Санкт-Петербургск.филиал', 'ФСПб')
    # df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
    #     'Саратовский филиал', 'ФСрт')
    # df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
    #     'Челябинский филиал', 'ФЧлб')
    # df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
    #     'Ярославский филиал', 'ФЯрв')

    if tab == 'tab-2':
        """Недостача по филиалам"""
        df0 = df0.loc[df0["Группа материалов"].isin(d_type)]
        df0_left = df0_left.loc[df0_left["Группа материалов"].isin(d_type)]

        df1_left = df0_left.groupby('Название бизнес-сферы').sum()
        df1_left['Название бизнес-сферы'] = df1_left.index
        df1_left = df1_left.reset_index(drop=True)
        df1_left = df1_left[['Название бизнес-сферы', 'Дебет', 'Кредит', 'Количество_дебет', 'Количество_кредит']]

        df1 = df0.groupby('Название бизнес-сферы').sum()
        df1['Название бизнес-сферы'] = df1.index
        df1 = df1.reset_index(drop=True)
        df1 = df1[['Название бизнес-сферы', 'Дебет', 'Кредит', 'Количество_дебет', 'Количество_кредит']]

        df_merged = df1_left.merge(df1, on=['Название бизнес-сферы'], how='outer')
        df_merged = df_merged.fillna(0)
        df_merged['Входящее сальдо'] = df_merged['Дебет_x'] - df_merged['Кредит_x']
        df_merged['Оборот'] = df_merged['Дебет_y'] - df_merged['Кредит_y']
        df_merged['Исходящее сальдо'] = df_merged['Входящее сальдо'] + df_merged['Оборот']
        df_merged['Входящее сальдо, шт.'] = df_merged['Количество_дебет_x'] - df_merged['Количество_кредит_x']
        df_merged['Оборот, шт.'] = df_merged['Количество_дебет_y'] - df_merged['Количество_кредит_y']
        df_merged['Исходящее сальдо, шт.'] = df_merged['Входящее сальдо, шт.'] + df_merged['Оборот, шт.']
        df_merged = df_merged[['Название бизнес-сферы', 'Входящее сальдо', 'Оборот', 'Исходящее сальдо', 'Входящее сальдо, шт.', 'Оборот, шт.', 'Исходящее сальдо, шт.']]

        # df1 = df0.groupby('Название бизнес-сферы').sum()
        # df1['Название бизнес-сферы'] = df1.index
        # df1 = df1.reset_index(drop=True)

        # df2 = df0[['Название бизнес-сферы','Дата проводки']].groupby('Название бизнес-сферы').max()

        # merged1 = df2.merge(df0[['Название бизнес-сферы','Дата проводки', 'cumsum_filial',
        #  'cumsum_filial_count']], on=['Название бизнес-сферы','Дата проводки']).drop_duplicates()

        # df_merged = merged1.merge(df1[['Название бизнес-сферы','Изменение за период',
        #  'Изменение количества']], on = 'Название бизнес-сферы')

        # df_merged.rename(columns={'initial_date':'Дата проводки',
        #                             'Дата проводки_x':'Дата исходящего сальдо',
        #                             'cumsum_filial':'Исходящее сальдо',
        #                             'cumsum_filial_count':'Исходящее сальдо, шт.',
        #                             'Изменение за период':'Оборот',
        #                             'Изменение количества': 'Оборот, шт.',
        #                             'Дата проводки_y':'Дата проводки'}, inplace=True)


        # df_merged['Входящее сальдо'] = df_merged['Исходящее сальдо'] - df_merged['Оборот']
        # df_merged['Входящее сальдо, шт.'] = df_merged[
        #     'Исходящее сальдо, шт.'] - df_merged['Оборот, шт.']

        # df_merged = df_merged[['Название бизнес-сферы', 'Входящее сальдо', 'Входящее сальдо, шт.',
        #  'Оборот', 'Оборот, шт.', 'Исходящее сальдо', 'Исходящее сальдо, шт.']]

        df_merged['Аббревиатура филиала'] = df_merged['Название бизнес-сферы']
        df_merged['Аббревиатура филиала'] = df_merged['Аббревиатура филиала'].replace(
            'Владивостокский филиал', 'ФВлд')
        df_merged['Аббревиатура филиала'] = df_merged['Аббревиатура филиала'].replace(
            'Воронежский филиал', 'ФВрж')
        df_merged['Аббревиатура филиала'] = df_merged['Аббревиатура филиала'].replace(
            'Екатеринбургский филиал', 'ФЕкб')
        df_merged['Аббревиатура филиала'] = df_merged['Аббревиатура филиала'].replace(
            'Иркутский филиал', 'ФИрк')
        df_merged['Аббревиатура филиала'] = df_merged['Аббревиатура филиала'].replace(
            'Красноярский филиал', 'ФКрс')
        df_merged['Аббревиатура филиала'] = df_merged['Аббревиатура филиала'].replace(
            'Московский филиал', 'ФМск')
        df_merged['Аббревиатура филиала'] = df_merged['Аббревиатура филиала'].replace(
            'Нижегородский филиал', 'ФНжН')
        df_merged['Аббревиатура филиала'] = df_merged['Аббревиатура филиала'].replace(
            'Новосибирский филиал', 'ФНвб')
        df_merged['Аббревиатура филиала'] = df_merged['Аббревиатура филиала'].replace(
            'Ростовский филиал', 'ФРст')
        df_merged['Аббревиатура филиала'] = df_merged['Аббревиатура филиала'].replace(
            'Самарский филиал', 'ФСмр')
        df_merged['Аббревиатура филиала'] = df_merged['Аббревиатура филиала'].replace(
            'Санкт-Петербургск.филиал', 'ФСПб')
        df_merged['Аббревиатура филиала'] = df_merged['Аббревиатура филиала'].replace(
            'Саратовский филиал', 'ФСрт')
        df_merged['Аббревиатура филиала'] = df_merged['Аббревиатура филиала'].replace(
            'Челябинский филиал', 'ФЧлб')
        df_merged['Аббревиатура филиала'] = df_merged['Аббревиатура филиала'].replace(
            'Ярославский филиал', 'ФЯрв')

        df_merged = df_merged.fillna(0)
        df_merged = df_merged.sort_values(by=sorting, ascending=True)
        df_merged['Входящее сальдо'] = df_merged['Входящее сальдо'] / 1000
        df_merged['Оборот'] = df_merged['Оборот'] / 1000
        df_merged['Исходящее сальдо'] = df_merged['Исходящее сальдо'] / 1000

        df_merged['Процент входящего сальдо'] = (df_merged['Входящее сальдо']/df_merged[
            'Входящее сальдо'].sum()*100).map('{:,.0f}%'.format)
        df_merged['Процент входящего сальдо, шт.'] = (df_merged['Входящее сальдо, шт.']/df_merged[
            'Входящее сальдо, шт.'].sum()*100).map('{:,.0f}%'.format)
        df_merged['Процент в руб.'] = np.where(df_merged['Оборот'] >= 0, (df_merged[
            'Оборот']/df_merged['Оборот'][df_merged['Оборот']>=0].sum()*100).map('{:,.0f}%'.format),
            (df_merged['Оборот']/df_merged[
            'Оборот'][df_merged['Оборот'] < 0].sum()*100).map('{:,.0f}%'.format))
        df_merged['Процент в шт.'] = np.where(df_merged['Оборот, шт.'] >= 0, (df_merged[
            'Оборот, шт.']/df_merged['Оборот, шт.'][df_merged[
            'Оборот, шт.'] >= 0].sum()*100).map('{:,.0f}%'.format), (df_merged[
            'Оборот, шт.']/df_merged[
            'Оборот, шт.'][df_merged['Оборот, шт.'] < 0].sum()*100).map('{:,.0f}%'.format))
        df_merged['Процент исходящего сальдо'] = (df_merged['Исходящее сальдо']/df_merged[
            'Исходящее сальдо'].sum()*100).map('{:,.0f}%'.format)
        df_merged['Процент исходящего сальдо, шт.'] = (df_merged['Исходящее сальдо, шт.']/df_merged[
            'Исходящее сальдо, шт.'].sum()*100).map('{:,.0f}%'.format)


        x1_data = df_merged['Входящее сальдо'].astype(int).astype(str).tolist()
        x1_text = df_merged['Входящее сальдо'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True) + " (" + df_merged['Процент входящего сальдо'].astype(str) + ")"
        y1_data = df_merged['Аббревиатура филиала'].tolist()

        x2_data = df_merged['Оборот'].astype(int).astype(str).tolist()
        x2_text = df_merged['Оборот'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True) + " (" + df_merged['Процент в руб.'].astype(str) + ")"
        df_merged['Color1'] = np.where(df_merged["Оборот"]<0, "#006B19", "#97151c")
        y2_data = df_merged['Аббревиатура филиала'].tolist()

        x3_data = df_merged['Исходящее сальдо'].astype(int).astype(str).tolist()
        x3_text = df_merged['Исходящее сальдо'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True) + " (" + df_merged['Процент исходящего сальдо'].astype(str) + ")"
        y3_data = df_merged['Аббревиатура филиала'].tolist()

        x4_data = df_merged['Входящее сальдо, шт.'].astype(int).astype(str).tolist()
        x4_text = df_merged['Входящее сальдо, шт.'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)+" (" + df_merged['Процент входящего сальдо, шт.'].astype(str) + ")"
        y4_data = df_merged['Аббревиатура филиала'].tolist()

        x5_data = df_merged['Оборот, шт.'].astype(int).astype(str).tolist()
        x5_text = df_merged['Оборот, шт.'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True) + " (" + df_merged['Процент в шт.'].astype(str) + ")"
        df_merged['Color2'] = np.where(df_merged['Оборот, шт.']<0, "#006B19", "#97151c")
        y5_data = df_merged['Аббревиатура филиала'].tolist()

        x6_data = df_merged['Исходящее сальдо, шт.'].astype(int).astype(str).tolist()
        x6_text = df_merged['Исходящее сальдо, шт.'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)+" (" + df_merged['Процент исходящего сальдо, шт.'].astype(str)+")"
        y6_data = df_merged['Аббревиатура филиала'].tolist()

        # df0_new = df0_new.loc[df0_new["Группа материалов"].isin(d_type)]
        # df1_new = df0_new.groupby('Название бизнес-сферы').sum()

        # x1_data = df1_new['Изменение количества'].astype(int).astype(str).tolist()
        # x1_text = df1_new['Изменение количества'].map('{:,}'.format).astype(str).replace(
        #     ',',' ', regex=True)

        # y1_data = df1_new.index.tolist()

        # df1_new['Color2'] = np.where(df1_new["Изменение количества"]<0, "#006B19", "#97151c")
        #df1['Color2'] = np.where(df1["Изменение количества"]<0, "#006B19", "#97151c")

        content = html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dashboard2-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x1_data,
                                    y=y1_data,
                                    text=x1_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Филиал: %{y} <br>Входящее сальдо, тыс. руб.: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#B4B4B4",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Входящее сальдо, тыс. руб.',
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 70,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns",
                ),
                html.Div([
                    dcc.Graph(
                        id="dashboard2-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x2_data,
                                    y=y2_data,
                                    text=x2_text,
                                    #cliponaxis = False,
                                    hoverinfo='skip',
                                    hovertemplate="""Филиал: %{y} <br>Оборот, тыс. руб.: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": df_merged['Color1'],
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                xaxis = dict(range=[-abs(min(map(float, x2_data))*2 - max(map(float, x2_data))*0.25), max(map(float, x2_data))]),
                                title_text='Оборот, тыс. руб.',
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 70,
                                },

                            ),
                        },
                        config={"displayModeBar": False},
                        style={'align':'left'},
                    ),
                ],
                className="four columns"
                ),
                html.Div([
                    dcc.Graph(
                        id="dashboard2-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x3_data,
                                    y=y3_data,
                                    text=x3_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Филиал: %{y} <br>Исходящее сальдо, тыс. руб.: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#6D6D6D",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Исходящее сальдо, тыс. руб.',
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 70,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns",
                ),

            ], className="row",
            ),
            html.Div([
                html.Div([
                        dcc.Graph(
                        id="dashboard2-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x4_data,
                                    y=y4_data,
                                    text=x4_text,
                                    hoverinfo='skip',
                                    hovertemplate="Филиал: %{y} <br>Входящее сальдо, шт.: %{text}",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#B4B4B4",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Входящее сальдо, шт.',
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 70,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns",
                ),
                html.Div([
                        dcc.Graph(
                        id="dashboard2-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x5_data,
                                    y=y5_data,
                                    text=x5_text,
                                    hoverinfo='skip',
                                    hovertemplate="Филиал: %{y} <br>Оборот, шт.: %{text}",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": df_merged['Color2'],
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Оборот, шт.',
                                xaxis = dict(range=[-abs(min(map(float, x5_data))*2 - max(map(float, x5_data))*0.25), max(map(float, x5_data))]),
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 70,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns",
                ),
                html.Div([
                        dcc.Graph(
                        id="dashboard2-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x6_data,
                                    y=y6_data,
                                    text=x6_text,
                                    hoverinfo='skip',
                                    hovertemplate="Филиал: %{y} <br>Исходящее сальдо, шт.: %{text}",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#6D6D6D",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Исходящее сальдо, шт.',
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 70,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns",
                ),
            ], className="row",
            )
        ])

        return content

    elif tab == 'tab-3':
        """Недостача по типам деталей"""
        df0 = df0.loc[df0["Название бизнес-сферы"].isin(branches)]
        df0_left = df0_left.loc[df0_left["Название бизнес-сферы"].isin(branches)]

        if warehouse != 'Все склады':
            df0 = df0[df0['Наименование склада'].isin([warehouse])]
            df0_left = df0_left[df0_left['Наименование склада'].isin([warehouse])]

        #if not df0.empty:
        # print('df0 =', df0)
        df1_left = df0_left.groupby('Группа материалов').sum()
        df1_left['Группа материалов'] = df1_left.index
        df1_left = df1_left.reset_index(drop=True)
        df1_left = df1_left[['Группа материалов', 'Дебет', 'Кредит', 'Количество_дебет', 'Количество_кредит']]
        # print('df1_left = ', df1_left)

        df1 = df0.groupby('Группа материалов').sum()
        df1['Группа материалов'] = df1.index
        df1 = df1.reset_index(drop=True)
        df1 = df1[['Группа материалов', 'Дебет', 'Кредит', 'Количество_дебет', 'Количество_кредит']]
        # print('df1 =', df1)

        df_merged = df1_left.merge(df1, on=['Группа материалов'], how='outer')
        df_merged = df_merged.fillna(0)
        df_merged['Входящее сальдо'] = df_merged['Дебет_x'] - df_merged['Кредит_x']
        df_merged['Оборот'] = df_merged['Дебет_y'] - df_merged['Кредит_y']
        df_merged['Исходящее сальдо'] = df_merged['Входящее сальдо'] + df_merged['Оборот']
        df_merged['Входящее сальдо, шт.'] = df_merged['Количество_дебет_x'] - df_merged['Количество_кредит_x']
        df_merged['Оборот, шт.'] = df_merged['Количество_дебет_y'] - df_merged['Количество_кредит_y']
        df_merged['Исходящее сальдо, шт.'] = df_merged['Входящее сальдо, шт.'] + df_merged['Оборот, шт.']
        df_merged = df_merged[['Группа материалов', 'Входящее сальдо', 'Оборот', 'Исходящее сальдо', 'Входящее сальдо, шт.', 'Оборот, шт.', 'Исходящее сальдо, шт.']]
        # print('df_merged =', df_merged)

        # df1 = df0.groupby('Группа материалов').sum()
        # df1['Группа материалов'] = df1.index
        # df1 = df1.reset_index(drop=True)
        # df2 = df0[['Группа материалов','Дата проводки']].groupby('Группа материалов').max()
        # merged1 = df2.merge(df0[['Группа материалов','Дата проводки',
        #  'cumsum_det_type', 'cumsum_det_type_count']], on=['Группа материалов',
        #  'Дата проводки']).drop_duplicates()
        # df_merged = merged1.merge(df1[['Группа материалов','Изменение за период',
        #  'Изменение количества']], on = 'Группа материалов')

        # df_merged.rename(columns={'initial_date':'Дата проводки',
        #                             'Дата проводки_x':'Дата исходящего сальдо',
        #                             'cumsum_det_type':'Исходящее сальдо',
        #                             'cumsum_det_type_count':'Исходящее сальдо, шт.',
        #                             'Изменение за период':'Оборот',
        #                             'Изменение количества': 'Оборот, шт.',
        #                             'Дата проводки_y':'Дата проводки'}, inplace=True)

        # df_merged['Входящее сальдо'] = df_merged['Исходящее сальдо'] - df_merged['Оборот']
        # df_merged['Входящее сальдо, шт.'] = df_merged[
        #     'Исходящее сальдо, шт.'] - df_merged['Оборот, шт.']
        # df_merged = df_merged[['Группа материалов', 'Входящее сальдо', 'Входящее сальдо, шт.',
        #  'Оборот', 'Оборот, шт.', 'Исходящее сальдо', 'Исходящее сальдо, шт.']]

        df_merged = df_merged.sort_values(by=sorting, ascending=True)
        df_merged['Входящее сальдо'] = df_merged['Входящее сальдо'] / 1000
        df_merged['Оборот'] = df_merged['Оборот'] / 1000
        df_merged['Исходящее сальдо'] = df_merged['Исходящее сальдо'] / 1000

        df_merged['Процент входящего сальдо в руб.'] = (df_merged['Входящее сальдо']/df_merged[
            'Входящее сальдо'].sum()*100).map('{:,.0f}%'.format)
        df_merged['Процент в руб.']=np.where(df_merged['Оборот']>=0, (df_merged['Оборот']/df_merged[
            'Оборот'][df_merged['Оборот'] >= 0].sum()*100).map('{:,.0f}%'.format),
            (df_merged['Оборот']/df_merged[
            'Оборот'][df_merged['Оборот'] < 0].sum()*100).map('{:,.0f}%'.format))
        df_merged['Процент исходящего сальдо в руб.'] = (df_merged['Исходящее сальдо']/df_merged[
            'Исходящее сальдо'].sum()*100).map('{:,.0f}%'.format)
        df_merged['Процент входящего сальдо в шт.'] = (df_merged['Входящее сальдо, шт.']/df_merged[
            'Входящее сальдо, шт.'].sum()*100).map('{:,.0f}%'.format)
        df_merged['Процент в шт.'] = np.where(df_merged['Оборот, шт.'] >= 0, (df_merged[
            'Оборот, шт.']/df_merged['Оборот, шт.'][df_merged[
            'Оборот, шт.'] >= 0].sum()*100).map('{:,.0f}%'.format),
            (df_merged['Оборот, шт.']/df_merged['Оборот, шт.'][df_merged[
            'Оборот, шт.'] < 0].sum()*100).map('{:,.0f}%'.format))
        df_merged['Процент исходящего сальдо в шт.']=(df_merged['Исходящее сальдо, шт.']/df_merged[
            'Исходящее сальдо, шт.'].sum()*100).map('{:,.0f}%'.format)

        # df0 = df0.loc[df0["Название бизнес-сферы"].isin(branches)]
        # df0 = df0.loc[df0["КНаименование склада"].isin(sklad)]
        # df1 = df0.groupby('Группа материалов').sum()
        # df1['Процент в шт.'] = (df1['Изменение количества']/df1[
        #     'Изменение количества'].sum()*100).map('{:,.0f}%'.format)
        # df1['Процент в руб.'] = (df1['Изменение за период']/df1[
        #     'Изменение за период'].sum()*100).map('{:,.0f}%'.format)
        # df1 = df1.sort_values(by='Изменение за период', ascending=True)

        x1_data = df_merged['Входящее сальдо'].astype(int).astype(str).tolist()
        x1_text = df_merged['Входящее сальдо'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)+" ("+df_merged['Процент входящего сальдо в руб.'].astype(str) + ")"
        y1_data = df_merged['Группа материалов'].tolist()

        x2_data = df_merged['Оборот'].astype(int).astype(str).tolist()
        x2_text = df_merged['Оборот'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True) + " (" + df_merged['Процент в руб.'].astype(str) + ")"
        df_merged['Color1'] = np.where(df_merged["Оборот"]<0, "#006B19", "#97151c")
        y2_data = df_merged['Группа материалов'].tolist()

        x3_data = df_merged['Исходящее сальдо'].astype(int).astype(str).tolist()
        x3_text = df_merged['Исходящее сальдо'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)+" ("+df_merged['Процент исходящего сальдо в руб.'].astype(str)+")"
        y3_data = df_merged['Группа материалов'].tolist()

        x4_data = df_merged['Входящее сальдо, шт.'].astype(int).astype(str).tolist()
        x4_text = df_merged['Входящее сальдо, шт.'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)+" ("+df_merged['Процент входящего сальдо в шт.'].astype(str) + ")"
        y4_data = df_merged['Группа материалов'].tolist()

        x5_data = df_merged['Оборот, шт.'].astype(int).astype(str).tolist()
        x5_text = df_merged['Оборот, шт.'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True) + " (" + df_merged['Процент в шт.'].astype(str) + ")"
        df_merged['Color2'] = np.where(df_merged["Оборот, шт."]<0, "#006B19", "#97151c")
        y5_data = df_merged['Группа материалов'].tolist()

        x6_data = df_merged['Исходящее сальдо, шт.'].astype(int).astype(str).tolist()
        x6_text = df_merged['Исходящее сальдо, шт.'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)+" ("+df_merged['Процент исходящего сальдо в шт.'].astype(str) + ")"
        y6_data = df_merged['Группа материалов'].tolist()

        if not df_merged['Оборот'].empty:
            left = -abs(min(map(float, x2_data))*2 - max(map(float, x2_data))*0.25)
            right = max(map(float, x2_data))
        else:
            left = -1
            right = 1

        if not df_merged['Оборот, шт.'].empty:
            left_col = -abs(min(map(float, x5_data))*2 - max(map(float, x5_data))*0.25)
            right_col = max(map(float, x5_data))
        else:
            left_col = -1
            right_col = 1
            

        content = html.Div([

            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dashboard2-graph2",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x1_data,
                                    y=y1_data,
                                    text=x1_text,
                                    hoverinfo='skip',
                                    hovertemplate="Тип запчасти: %{y} <br>Недостача, шт.: %{text}",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#B4B4B4",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Входящее сальдо, тыс. руб.',
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 200,
                                                    "l": 160,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns"
                ),
                html.Div([
                    dcc.Graph(
                        id="dashboard2-graph2",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x2_data,
                                    y=y2_data,
                                    text=x2_text,
                                    hoverinfo='skip',
                                    hovertemplate="""Тип запчасти: %{y} <br>Недостача,
                                     тыс. руб.: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": df_merged['Color1'],
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Оборот, тыс. руб.',
                                #xaxis = dict(range=[-abs(min(map(float, x2_data))*2 - max(map(float, x2_data))*0.25), max(map(float, x2_data))]),
                                xaxis = dict(range=[left, right]),
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 200,
                                                    "l": 160,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns"
                ),
                html.Div([
                    dcc.Graph(
                        id="dashboard2-graph2",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x3_data,
                                    y=y3_data,
                                    text=x3_text,
                                    hoverinfo='skip',
                                    hovertemplate="Тип запчасти: %{y} <br>Недостача, шт.: %{text}",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#6D6D6D",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Исходящее сальдо, тыс. руб.',
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 200,
                                                    "l": 160,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns"
                ),
            ], className="row",
            ),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dashboard2-graph2",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x4_data,
                                    y=y4_data,
                                    text=x4_text,
                                    hoverinfo='skip',
                                    hovertemplate="Тип запчасти: %{y} <br>Недостача, шт.: %{text}",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#B4B4B4",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Входящее сальдо, шт.',
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 200,
                                                    "l": 160,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns"
                ),
                html.Div([
                    dcc.Graph(
                        id="dashboard2-graph2",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x5_data,
                                    y=y5_data,
                                    text=x5_text,
                                    hoverinfo='skip',
                                    hovertemplate="""Тип запчасти: %{y} <br>Недостача,
                                     тыс. руб.: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": df_merged['Color1'],
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Оборот, шт.',
                                #xaxis = dict(range=[-abs(min(map(float, x5_data))*2 - max(map(float, x5_data))*0.25), max(map(float, x5_data))]),
                                xaxis = dict(range=[left_col, right_col]),
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 200,
                                                    "l": 160,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns"
                ),
                html.Div([
                    dcc.Graph(
                        id="dashboard2-graph2",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x6_data,
                                    y=y6_data,
                                    text=x6_text,
                                    hoverinfo='skip',
                                    hovertemplate="Тип запчасти: %{y} <br>Недостача, шт.: %{text}",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#6D6D6D",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Исходящее сальдо, шт.',
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 200,
                                                    "l": 160,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns"
                ),
            ], className="row",
            ),
        ],
        )
        return content

    elif tab == 'tab-4':
        """Недостача по складам"""
        df0 = df0.loc[df0["Название бизнес-сферы"].isin(branches)]
        df0_left = df0_left.loc[df0_left["Название бизнес-сферы"].isin(branches)]
        df0 = df0.loc[df0["Группа материалов"].isin(d_type)]
        df0_left = df0_left.loc[df0_left["Группа материалов"].isin(d_type)]

        df1_left = df0_left.groupby('Наименование склада').sum()
        df1_left['Наименование склада'] = df1_left.index
        df1_left = df1_left.reset_index(drop=True)
        df1_left = df1_left[['Наименование склада', 'Дебет', 'Кредит', 'Количество_дебет', 'Количество_кредит']]

        df1 = df0.groupby('Наименование склада').sum()
        df1['Наименование склада'] = df1.index
        df1 = df1.reset_index(drop=True)
        df1 = df1[['Наименование склада', 'Дебет', 'Кредит', 'Количество_дебет', 'Количество_кредит']]

        df_merged = df1_left.merge(df1, on=['Наименование склада'], how='outer')
        df_merged = df_merged.fillna(0)
        df_merged['Входящее сальдо'] = df_merged['Дебет_x'] - df_merged['Кредит_x']
        df_merged['Оборот'] = df_merged['Дебет_y'] - df_merged['Кредит_y']
        df_merged['Исходящее сальдо'] = df_merged['Входящее сальдо'] + df_merged['Оборот']
        df_merged['Входящее сальдо, шт.'] = df_merged['Количество_дебет_x'] - df_merged['Количество_кредит_x']
        df_merged['Оборот, шт.'] = df_merged['Количество_дебет_y'] - df_merged['Количество_кредит_y']
        df_merged['Исходящее сальдо, шт.'] = df_merged['Входящее сальдо, шт.'] + df_merged['Оборот, шт.']
        df_merged = df_merged[['Наименование склада', 'Входящее сальдо', 'Оборот', 'Исходящее сальдо', 'Входящее сальдо, шт.', 'Оборот, шт.', 'Исходящее сальдо, шт.']]

        # df0['Наименование склада'] = df0['Наименование склада'] + " (" + df0[
        #     'Аббревиатура филиала'] + ")"

        # df1 = df0.groupby('Наименование склада').sum()
        # df1['Наименование склада'] = df1.index
        # df1 = df1.reset_index(drop=True)
        # df2 = df0[['Наименование склада','Дата проводки']].groupby('Наименование склада').max()
        # merged1 = df2.merge(df0[['Наименование склада','Дата проводки', 'cumsum_sklad',
        #  'cumsum_sklad_count']], on=['Наименование склада','Дата проводки']).drop_duplicates()
        # df_merged = merged1.merge(df1[['Наименование склада','Изменение за период',
        #  'Изменение количества']], on = 'Наименование склада')

        # df_merged.rename(columns={'initial_date':'Дата проводки',
        #                             'Дата проводки_x':'Дата исходящего сальдо',
        #                             'cumsum_sklad':'Исходящее сальдо',
        #                             'cumsum_sklad_count':'Исходящее сальдо, шт.',
        #                             'Изменение за период':'Оборот',
        #                             'Изменение количества': 'Оборот, шт.',
        #                             'Дата проводки_y':'Дата проводки'}, inplace=True)

        # df_merged['Входящее сальдо'] = df_merged['Исходящее сальдо'] - df_merged['Оборот']
        # df_merged['Входящее сальдо, шт.'] = df_merged['Исходящее сальдо, шт.'] - df_merged[
        #     'Оборот, шт.']

        # df_merged = df_merged[['Наименование склада', 'Входящее сальдо', 'Входящее сальдо, шт.',
        # 'Оборот', 'Оборот, шт.', 'Исходящее сальдо', 'Исходящее сальдо, шт.']]

        if warehouse_quantity == '10':
            df_merged = df_merged.sort_values(by=sorting, ascending=False).head(10)
        if warehouse_quantity == '20':
            df_merged = df_merged.sort_values(by=sorting, ascending=False).head(20)
        if warehouse_quantity == '30':
            df_merged = df_merged.sort_values(by=sorting, ascending=False).head(30)
        df_merged = df_merged.sort_values(by=sorting, ascending=True)
        df_merged['Входящее сальдо'] = df_merged['Входящее сальдо'] / 1000
        df_merged['Оборот'] = df_merged['Оборот'] / 1000
        df_merged['Исходящее сальдо'] = df_merged['Исходящее сальдо'] / 1000

        df_merged['Процент входящего сальдо в руб.'] = (df_merged['Входящее сальдо']/df_merged[
            'Входящее сальдо'].sum()*100).map('{:,.0f}%'.format)
        df_merged['Процент в руб.']=np.where(df_merged['Оборот']>=0, (df_merged['Оборот']/df_merged[
            'Оборот'][df_merged['Оборот'] >= 0].sum()*100).map('{:,.0f}%'.format),
            (df_merged['Оборот']/df_merged[
            'Оборот'][df_merged['Оборот'] < 0].sum()*100).map('{:,.0f}%'.format))
        df_merged['Процент исходящего сальдо в руб.'] = (df_merged['Исходящее сальдо']/df_merged[
            'Исходящее сальдо'].sum()*100).map('{:,.0f}%'.format)
        df_merged['Процент входящего сальдо в шт.'] = (df_merged['Входящее сальдо, шт.']/df_merged[
            'Входящее сальдо, шт.'].sum()*100).map('{:,.0f}%'.format)
        df_merged['Процент в шт.'] = np.where(df_merged['Оборот, шт.'] >= 0, (df_merged[
            'Оборот, шт.']/df_merged['Оборот, шт.'][df_merged[
            'Оборот, шт.'] >= 0].sum()*100).map('{:,.0f}%'.format),
            (df_merged['Оборот, шт.']/df_merged[
            'Оборот, шт.'][df_merged['Оборот, шт.'] < 0].sum()*100).map('{:,.0f}%'.format))
        df_merged['Процент исходящего сальдо в шт.']=(df_merged['Исходящее сальдо, шт.']/df_merged[
            'Исходящее сальдо, шт.'].sum()*100).map('{:,.0f}%'.format)

        # df1 = df0.groupby('КНаименование склада').sum()
        # df1 = df1.sort_values('Изменение за период', ascending=False).head(10)

        # df1['Процент в шт.'] = (df1['Изменение количества']/df1[
        #     'Изменение количества'].sum()*100).map('{:,.0f}%'.format)
        # df1['Процент в руб.'] = (df1['Изменение за период']/df1[
        #     'Изменение за период'].sum()*100).map('{:,.0f}%'.format)
        # df1 = df1.sort_values(by='Изменение за период', ascending=True)

        x1_data = df_merged['Входящее сальдо'].astype(int).astype(str).tolist()
        x1_text = df_merged['Входящее сальдо'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)+" ("+df_merged['Процент входящего сальдо в руб.'].astype(str) + ")"
        y1_data = df_merged['Наименование склада'].tolist()

        x2_data = df_merged['Оборот'].astype(int).astype(str).tolist()
        x2_text = df_merged['Оборот'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True) + " (" + df_merged['Процент в руб.'].astype(str) + ")"
        df_merged['Color1'] = np.where(df_merged["Оборот"]<0, "#006B19", "#97151c")
        y2_data = df_merged['Наименование склада'].tolist()

        x3_data = df_merged['Исходящее сальдо'].astype(int).astype(str).tolist()
        x3_text = df_merged['Исходящее сальдо'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)+" ("+df_merged['Процент исходящего сальдо в руб.'].astype(str)+")"
        y3_data = df_merged['Наименование склада'].tolist()

        x4_data = df_merged['Входящее сальдо, шт.'].astype(int).astype(str).tolist()
        x4_text = df_merged['Входящее сальдо, шт.'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)+" ("+df_merged['Процент входящего сальдо в шт.'].astype(str) + ")"
        y4_data = df_merged['Наименование склада'].tolist()

        x5_data = df_merged['Оборот, шт.'].astype(int).astype(str).tolist()
        x5_text = df_merged['Оборот, шт.'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True) + " (" + df_merged['Процент в шт.'].astype(str) + ")"
        df_merged['Color2'] = np.where(df_merged["Оборот, шт."]<0, "#006B19", "#97151c")
        y5_data = df_merged['Наименование склада'].tolist()

        x6_data = df_merged['Исходящее сальдо, шт.'].astype(int).astype(str).tolist()
        x6_text = df_merged['Исходящее сальдо, шт.'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)+" ("+df_merged['Процент исходящего сальдо в шт.'].astype(str) + ")"
        y6_data = df_merged['Наименование склада'].tolist()

        if not df_merged['Оборот'].empty:
            if min(map(float, x2_data)) >= 0:
                left = 0
            else:
                left = -abs(min(map(float, x2_data))*2 - max(map(float, x2_data))*0.25)
            right = max(map(float, x2_data))
        else:
            left = -1
            right = 1

        if not df_merged['Оборот, шт.'].empty:
            if min(map(float, x2_data)) >= 0:
                left_col = 0
            else:
                left_col = -abs(min(map(float, x5_data))*2 - max(map(float, x5_data))*0.25)
            right_col = max(map(float, x5_data))
        else:
            left_col = -1
            right_col = 1

        content = html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dashboard2-graph3",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x1_data,
                                    y=y1_data,
                                    text=x1_text,
                                    hoverinfo='skip',
                                    hovertemplate="Склад: %{y} <br>Входящее сальдо, тыс. руб.: %{text}",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#B4B4B4",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Входящее сальдо, тыс. руб.',
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 200,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns"
                ),
                html.Div([
                    dcc.Graph(
                        id="dashboard2-graph3",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x2_data,
                                    y=y2_data,
                                    text=x2_text,
                                    hoverinfo='skip',
                                    hovertemplate="Склад: %{y} <br>Оборот, тыс. руб.: %{text}",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": df_merged['Color1'],
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Оборот, тыс. руб.',
                                #xaxis = dict(range=[-abs(min(map(float, x2_data))*2 - max(map(float, x2_data))*0.25), max(map(float, x2_data))]),
                                xaxis = dict(range=[left, right]),
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 200,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns"
                ),
                html.Div([
                    dcc.Graph(
                        id="dashboard2-graph3",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x3_data,
                                    y=y3_data,
                                    text=x3_text,
                                    hoverinfo='skip',
                                    hovertemplate="Склад: %{y} <br>Исходящее сальдо, тыс. руб.: %{text}",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#6D6D6D",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Исходящее сальдо, тыс. руб.',
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 200,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns"
                ),
            ], className="row",
            ),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dashboard2-graph3",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x4_data,
                                    y=y4_data,
                                    text=x4_text,
                                    hoverinfo='skip',
                                    hovertemplate="Склад: %{y} <br>Недостача, шт.: %{text}",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#B4B4B4",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Входящее сальдо, шт.',
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 200,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns"
                ),
                html.Div([
                    dcc.Graph(
                        id="dashboard2-graph3",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x5_data,
                                    y=y5_data,
                                    text=x5_text,
                                    hoverinfo='skip',
                                    hovertemplate="Склад: %{y} <br>Недостача, шт.: %{text}",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": df_merged['Color1'],
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Оборот, шт.',
                                #xaxis = dict(range=[-abs(min(map(float, x5_data))*2 - max(map(float, x5_data))*0.25), max(map(float, x5_data))]),
                                xaxis = dict(range=[left_col, right_col]),
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 200,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns"
                ),
                html.Div([
                    dcc.Graph(
                        id="dashboard2-graph3",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x6_data,
                                    y=y6_data,
                                    text=x6_text,
                                    hoverinfo='skip',
                                    hovertemplate="Склад: %{y} <br>Недостача, шт.: %{text}",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#6D6D6D",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Исходящее сальдо, шт.',
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 200,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns"
                ),
            ], className="row",
            )
        ],
        )

        return content
    elif tab == 'tab-1':
        """Динамика недостачи"""
        # global graph_data
        # global d_start
        # global d_end
        # print('graph_data', graph_data)

        # print('Начало периода', start_date)
        # print(end_date)
        # if data is None or (d_start != start_date) or (d_end != end_date):
        #     data = pd.read_sql(sql, engine_cons)
        #     d_start = start_date
        #     d_end = end_date

        # data = get_osv_detail_by_dates(dt.datetime.strptime(start_date,'%Y-%m-%d'
        #   ), dt.datetime.strptime(end_date, '%Y-%m-%d'), debug=False)
        # data_left = get_osv_detail_by_dates(dt.datetime.strptime('1900-01-01','%Y-%m-%d')\
        #     , dt.datetime.strptime(start_date, '%Y-%m-%d') - dt.timedelta(days=1), debug=False)
        # d_start = start_date
        # d_end = end_date



        # graph_data = get_osv_detail_by_dates2(start_date, end_date, debug=False)
        # data_left = get_osv_detail_by_dates2(dt.datetime.strptime('1900-01-01','%Y-%m-%d'
        #     ), start_date - dt.timedelta(days=1), debug=False)

        #         # --> Алгоримт расчета динамического сальдо
        df0['Дата'] = df0['Дата проводки'].apply(lambda x: dt.datetime.strptime(x, '%Y%m%d'))
        df0['Неделя'] = df0['Дата проводки'].apply(lambda x: dt.datetime.strptime(x, '%Y%m%d')).apply(lambda x: x - dt.timedelta(x.weekday()))
        next_month = df0['Дата'].apply(lambda x: x.replace(day=28) + dt.timedelta(days=4))   # this will never fail
        df0['Месяц'] = next_month.apply(lambda x: x - dt.timedelta(days=x.day))

        #df0['Месяц'] = df0['Дата проводки'].apply(lambda x: dt.datetime.strptime(x, '%Y%m%d')).apply(lambda x: x.replace(day=1))

        # graph_data['Дата'] = graph_data[
        #     'Дата ввода'].apply(lambda x: dt.datetime.strptime(x, '%Y%m%d'))
        # graph_data['Неделя'] = graph_data[
        #     'Дата ввода'].apply(lambda x: dt.datetime.strptime(
        #     x, '%Y%m%d')).apply(lambda x: x - dt.timedelta(x.weekday()))
        # graph_data['Месяц'] = graph_data[
        #     'Дата ввода'].apply(lambda x: dt.datetime.strptime(
        #     x, '%Y%m%d')).apply(lambda x: x.replace(day=1))

        # # Добавить условие
        # if data_level == 'День':
        #     graph_data['Дата'] = graph_data['Дата']
        # elif data_level == 'Неделя':
        #     graph_data['Дата'] = graph_data['Неделя']
        # else: graph_data['Дата'] = graph_data['Месяц']
        if filial != 'Все филиалы':
            df0 = df0[df0['Название бизнес-сферы'].isin([filial])]
            df0_left = df0_left[df0_left['Название бизнес-сферы'].isin([filial])]
        if warehouse != 'Все склады':
            df0 = df0[df0['Наименование склада'].isin([warehouse])]
            df0_left = df0_left[df0_left['Наименование склада'].isin([warehouse])]
        if detail_type != 'Все запчасти':
            df0 = df0[df0['Группа материалов'].isin([detail_type])]
            df0_left = df0_left[df0_left['Группа материалов'].isin([detail_type])]
        
        sum_left = df0_left['Изменение за период'].sum()/1000
        count_left = df0_left['Изменение количества'].sum()

        df1 = df0
        if data_level == 'Неделя':
            df1['Дата'] = df1['Неделя']
        elif data_level == 'Месяц':
            df1['Дата'] = df1['Месяц']

        # df1 = graph_data
        # df1_left = data_left

       

        # if filial != 'Все филиалы':
        #     df1 = df1[df1['Филиал'].isin([filial])]
        #     df1_left = data_left[data_left['Филиал'].isin([filial])]
        # if warehouse != 'Все склады':
        #     df1 = df1[df1['Склад'].isin([warehouse])]
        #     df1_left = df1_left[df1_left['Склад'].isin([warehouse])]
        # if detail_type != 'Все запчасти':
        #     df1 = df1[df1['Группа материалов'].isin([detail_type])]
        #     df1_left = data_left[data_left['Группа материалов'].isin([detail_type])]

        # df1['Обороты по дебету'] = df1['Обороты по дебету']/1000
        # df1['Обороты по кредиту'] = df1['Обороты по кредиту']/1000
        # df1_left['Обороты по дебету'] = df1_left['Обороты по дебету']/1000
        # df1_left['Обороты по кредиту'] = df1_left['Обороты по кредиту']/1000
        df1['Дебет'] = df1['Дебет']/1000
        df1['Кредит'] = df1['Кредит']/1000
        df1['cumsum'] = df1['cumsum']/1000

        df2 = df1.groupby(['Дата']).agg({'Дебет':'sum', 'Кредит':'sum'\
            , 'Количество_дебет':'sum', 'Количество_кредит':'sum'})\
                                            .reset_index().sort_values(by = ['Дата'])
        
        df2['Накопительный итог, руб.'] = df2['Дебет'].cumsum() - df2['Кредит'].cumsum() + sum_left
        df2['Накопительный итог, шт.'] = df2['Количество_дебет'].cumsum() - df2['Количество_кредит'].cumsum() + count_left

        # df4 = df1[['Дата', 'Дата проводки']].groupby(['Дата']).max()
        # df5 = df4.merge(df0[['Дата', 'Дата проводки', 'cumsum', 'cumsum_count']], on = ['Дата проводки'], how = 'inner').drop_duplicates()
        # df3 = pd.merge(df2, df5, on = ['Дата'], how = 'inner').drop_duplicates()

        # df3 = df2.merge(df0[['Дата', 'cumsum', 'cumsum_count']], on = ['Дата']).drop_duplicates()

        # df2 = df1.groupby(['Дата']).agg({'Обороты по дебету':'sum', 'Обороты по кредиту':'sum'\
        #     , 'Обороты по дебету, шт':'sum', 'Обороты по кредиту, шт':'sum'})\
        #                                     .reset_index().sort_values(by = ['Дата'])
        # df2_left = df1_left.sum()

        # df2['Обороты по дебету(накоп), руб'] = df2['Обороты по дебету'
        #     ].cumsum() + df2_left['Обороты по дебету']
        # df2['Обороты по кредиту(накоп), руб'] = df2['Обороты по кредиту'
        #     ].cumsum() + df2_left['Обороты по кредиту']
        # df2['Обороты по дебету(накоп), шт'] = df2['Обороты по дебету, шт'
        #     ].cumsum() + df2_left['Обороты по дебету, шт']
        # df2['Обороты по кредиту(накоп), шт'] = df2['Обороты по кредиту, шт'
        #     ].cumsum() + df2_left['Обороты по кредиту, шт']
        # df2['Сальдо, руб'] = df2['Обороты по дебету(накоп), руб'
        #     ] - df2['Обороты по кредиту(накоп), руб']
        # df2['Сальдо, шт'] = df2['Обороты по дебету(накоп), шт'
        #     ] - df2['Обороты по кредиту(накоп), шт']

        # cur_data = df2
        #df3['Дата'] = df3['Дата'] + dt.timedelta(days=-1)

        content = html.Div([

                html.Div([
                    dcc.Graph(
                        id="dashboard2-graph1",
                        config={"displayModeBar": True},
                        figure={
                            'data': [
                                go.Bar(x = df2['Дата'],
                                    y=df2['Дебет'],
                                    textposition='auto',
                                    hoverinfo='skip',
                                    hovertemplate="Дата: %{x}" +
                                        "<br>Обороты по дебету, тыс. руб.: %{y:,.0f}",
                                    marker={
                                        "color": "#97151c",
                                    },
                                    name = 'Обороты по дебету',
                                    yaxis="y1",

                                ),
                                go.Bar(x =df2['Дата'],
                                    y=df2['Кредит'],
                                    hoverinfo='skip',
                                    hovertemplate="Дата: %{x}" +
                                        "<br>Обороты по кредиту, тыс. руб.: %{y:,.0f}",
                                    marker={
                                        "color": "#006B19",
                                    },
                                    name='Обороты по кредиту',
                                    yaxis="y1",
                                ),
                                go.Scatter(x =df2['Дата'],
                                    y=df2['Накопительный итог, руб.'],
                                    hoverinfo='skip',
                                    hovertemplate="Дата: %{x}" + "<br>Исходящее сальдо, тыс. руб.: %{y:,.0f}",
                                    name='Исходящее сальдо',
                                    mode='lines+markers',
                                    line={"color": "#6E6E6E"},
                                    yaxis = "y2"
                                ),
                            ],
                            'layout':go.Layout(
                                title_text='''
                                    Динамика недостачи, тыс. руб.
                                    ''',
                                font={"family": "Raleway", "size": 12},
                                hovermode="closest",
                                legend={
                                    "x": 0.8,
                                    "y": 1.35,
                                    "orientation": "v",
                                    # "yanchor": "bottom",
                                },
                                yaxis=dict(
                                    title="Оборот, тыс. руб."
                                ),
                                yaxis2=dict(
                                    title="Исходящее сальдо, тыс. руб.",
                                    overlaying="y",
                                    side="right",
                                ),
                                xaxis={
                                    "rangeselector": {
                                        "font": {"family": "Raleway", "size": 10},
                                        "buttons": [
                                            {
                                                "count": 1,
                                                "label": "1M",
                                                "step": "month",
                                                "stepmode": "backward",
                                            },
                                            {
                                                "count": 3,
                                                "label": "1Q",
                                                "step": "month",
                                                "stepmode": "backward",
                                            },
                                            {
                                                "count": 6,
                                                "label": "HY",
                                                "step": "month",
                                                "stepmode": "backward",
                                            },
                                            {
                                                "count": 1,
                                                "label": "1Y",
                                                "step": "year",
                                                "stepmode": "backward",
                                            },
                                            {
                                                "count": 1,
                                                "label": "ALL",
                                                "step": "all",
                                                "stepmode": "backward",
                                            },
                                        ]
                                    },
                                    "rangeslider": dict(
                                        visible=True,
                                    ),
                                    "type": "date",
                                },
                            )
                        }
                    ),
                ], className="six columns"
                ),
                html.Div([
                    dcc.Graph(
                    id="graph-2",
                    config={"displayModeBar": True},
                    figure = {
                        'data': [
                            go.Bar(x =df2['Дата'],
                                #y=cur_data['Обороты по дебету(накоп), шт'],
                                y=df2['Количество_дебет'],
                                hoverinfo='skip',
                                hovertemplate="Дата: %{x}" +
                                    "<br>Обороты по дебету, шт.: %{y:,.0f}",
                                marker={
                                    "color": "#97151c",
                                },
                                #name = 'Обороты по дебету(накоп)',
                                name = 'Обороты по дебету',
                                yaxis="y1",

                            ),
                            go.Bar(x =df2['Дата'],
                                #y=cur_data['Обороты по кредиту(накоп), шт'],
                                y=df2['Количество_кредит'],
                                hoverinfo='skip',
                                hovertemplate="Дата: %{x}" +
                                    "<br>Обороты по кредиту, шт.: %{y:,.0f}",
                                marker={
                                    "color": "#006B19",
                                },
                                #name='Обороты по кредиту(накоп)',
                                name='Обороты по кредиту',
                                yaxis="y1",
                            ),
                            go.Scatter(x =df2['Дата'],
                                y=df2['Накопительный итог, шт.'],
                                hoverinfo='skip',
                                hovertemplate="Дата: %{x}" + "<br>Исходящее сальдо, шт.: %{y:,.0f}",
                                name='Исходящее сальдо',
                                mode='lines+markers',
                                line={"color": "#6E6E6E"},
                                # Добавляем вторую ось
                                yaxis="y2",
                            ),
                        ],
                        'layout':go.Layout(
                            title_text='Динамика недостачи, шт.',
                            font={"family": "Raleway", "size": 12},
                            hovermode="closest",
                            legend={
                                "x": 0.8,
                                "y": 1.35,
                                "orientation": "v",
                                # "yanchor": "bottom",
                            },
                            yaxis=dict(
                                title="Оборот, шт."
                            ),
                            yaxis2=dict(
                                title="Исходящее сальдо, шт",
                                overlaying="y",
                                side="right",
                            ),
                            xaxis={
                                "rangeselector": {
                                    "font": {"family": "Raleway", "size": 10},
                                    "buttons": [
                                        {
                                            "count": 3,
                                            "label": "1Q",
                                            "step": "month",
                                            "stepmode": "backward",
                                        },
                                                                {
                                            "count": 6,
                                            "label": "2Q",
                                            "step": "month",
                                            "stepmode": "backward",
                                        },
                                        {
                                            "count": 1,
                                            "label": "1Y",
                                            "step": "year",
                                            "stepmode": "backward",
                                        },
                                        {
                                            "count": 1,
                                            "label": "ALL",
                                            "step": "all",
                                            "stepmode": "backward",
                                        },
                                    ]
                                },
                                "rangeslider": dict(
                                    visible=True,
                                ),
                                "type": "date",
                            },
                        )
                    },
                    ),
                ], className="six columns"
                ),

        ],
        className="row",
        )
        return content


# Настройка видимости фильтров
@dash_app.callback(
    Output(component_id='dashboard2-dropdown1', component_property='style'),
    [Input('dashboard2-tabs', 'value')]
)
def dropdown1_visibility(tab):
    """Настройка видимости фильтра по филиалам"""
    if tab == 'tab-2':
        return {"display":"None"}

@dash_app.callback(
    Output(component_id='name1', component_property='style'),
    [Input('dashboard2-tabs', 'value')]
)
def name1_visibility(tab):
    """Настройка видимости заголовка фильтра по филиалам"""
    if tab == 'tab-2':
        return {"display":"None"}
    else:
        return {"display": "flex",
                    "align-items": "center",
                    "height": "38px",
                    "justify-content": "center"
                        }

@dash_app.callback(
    Output(component_id='dashboard2-dropdown2', component_property='style'),
    [Input('dashboard2-tabs', 'value')]
)
def dropdown2_visibility(tab):
    """Настройка видимости фильтра по типам запчастей"""
    if tab == 'tab-3':
        return {"display":"None"}

@dash_app.callback(
    Output(component_id='name2', component_property='style'),
    [Input('dashboard2-tabs', 'value')]
)
def name2_visibility(tab):
    """Настройка видимости заголовка фильтра по типам запчастей"""
    if tab == 'tab-3':
        return {"display":"None"}
    else:
        return {"display": "flex",
                    "align-items": "center",
                    "height": "38px",
                    "justify-content": "center"
                        }

@dash_app.callback(
    Output(component_id='dashboard2-dropdown3', component_property='style'),
    [Input('dashboard2-tabs', 'value')]
)
def dropdown3_visibility(tab):
    """Настройка видимости фильтра по складам"""
    if tab == 'tab-2' or tab == 'tab-4':
        return {"display":"None"}

@dash_app.callback(
    Output(component_id='name3', component_property='style'),
    [Input('dashboard2-tabs', 'value')]
)
def name3_visibility(tab):
    """Настройка видимости заголовка фильтра по складам"""
    if tab == 'tab-2' or tab == 'tab-4':
        return {"display":"None"}
    else:
        return {"display": "flex",
                    "align-items": "center",
                    "height": "38px",
                    "justify-content": "center"
                        }

@dash_app.callback(
    Output(component_id='dashboard2-dropdown4', component_property='style'),
    [Input('dashboard2-tabs', 'value')]
)
def dropdown4_visibility(tab):
    """Настройка видимости фильтра сортировки"""
    if tab == 'tab-1':
        return {"display":"None"}

@dash_app.callback(
    Output(component_id='name4', component_property='style'),
    [Input('dashboard2-tabs', 'value')]
)
def name4_visibility(tab):
    """Настройка видимости заголовка фильтра сортировки"""
    if tab == 'tab-1':
        return {"display":"None"}
    else:
        return {"display": "flex",
                    "align-items": "center",
                    "height": "38px",
                    "justify-content": "center"
                        }

@dash_app.callback(
    Output(component_id='ri-level', component_property='style'),
    [Input('dashboard2-tabs', 'value')]
)
def radioitems1_visibility(tab):
    """Настройка видимости радиокнопок для выбора день, неделя или месяц"""
    if tab == 'tab-2' or tab == 'tab-3' or tab == 'tab-4':
        return {"display":"None"}

@dash_app.callback(
    Output(component_id='warehouse_quantity', component_property='style'),
    [Input('dashboard2-tabs', 'value')]
)
def radioitems2_visibility(tab):
    """Настройка видимости радиокнопок для выбора количества складов"""
    if tab == 'tab-1' or tab == 'tab-2' or tab == 'tab-3':
        return {"display":"None"}

""" Интерактивные элементы для отчетов по запчастям."""
import datetime as dt
import numpy as np
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
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

# Значения списка филиалов
# @dash_app.callback(
# Output(component_id='dashboard2-dropdown1', component_property='options'),
# [Input('dashboard2-tabs', 'value')]
# )

# def update_dropdown1(tab):
#     """Список значений фильтра по филиалам"""
#     # df0=pd.read_sql("""
#     #             SELECT DISTINCT "Название бизнес-сферы"
#     #             FROM sap_s4.osv_94
#     #             ORDER BY "Название бизнес-сферы" ASC
#     #             """, con=engine_cons)

#     if tab is not None:
#         df0 = get_branch_names()
#         list1 = df0['Название бизнес-сферы'].tolist()
#         list2 = ['Все филиалы'] + list1
#         df1 = pd.DataFrame(list2,columns=['Название бизнес-сферы'])
#     #df['Название бизнес-сферы'] = df['Название бизнес-сферы'].replace('Ярославский филиал', 'ФЯрв')

#     return [{'label': i, 'value': i} for i in df1['Название бизнес-сферы']]


# # Сумма недостачи за выбранный период
# @dash_app.callback(Output(component_id='shortage_amount', component_property='children'),
#     [Input('dashboard2-date-picker-range', 'start_date'),
#     Input('dashboard2-date-picker-range', 'end_date'),
#     Input('dashboard2-dropdown1', 'value'),
#     Input('dashboard2-dropdown2', 'value'),
#     Input('dashboard2-dropdown3', 'value'),
#     Input('dashboard2-tabs', 'value')])

# def shortage_amount(start_date, end_date, filial, detail_type, warehouse, tab):
#     """Вычисление суммы недостачи"""
#     #df0 = get_osv_detail_by_dates(start_date, end_date, debug=False)
#     df0 = get_osv_data(start_date, end_date, debug=False)
#     #shortage = df0['Изменение за период'].sum()
#     branches = []
#     if filial == 'Все филиалы':
#         branches = df0["Название бизнес-сферы"].unique()
#     else:
#         branches.append(filial)
#     if tab == 'tab-2' or tab == 'tab-3' or tab == 'tab-4':
#         df0 = df0.loc[df0["Название бизнес-сферы"].isin(branches)]

#     d_type = []
#     if detail_type == 'Все запчасти':
#         d_type = df0["Группа материалов"].unique()
#     else:
#         d_type.append(detail_type)
#     if tab == 'tab-1' or tab == 'tab-3' or tab == 'tab-4':
#         df0 = df0.loc[df0["Группа материалов"].isin(d_type)]

#     sklad = []
#     if warehouse == 'Все склады':
#         sklad = df0["Наименование склада"].unique()
#     else:
#         sklad.append(warehouse)
#     if tab == 'tab-2' or tab == 'tab-4':
#         df0 = df0.loc[df0["Наименование склада"].isin(sklad)]
#     shortage = '{:,.0f}'.format(round(df0['Изменение за период'].sum())/1000).replace(',', ' ')

#     # return shortage


# Построение содержимого выбранной закладки
@dash_app.callback(Output('tab-content', 'children'),
    [Input('dashboard2-date-picker-range', 'start_date'),
    Input('dashboard2-date-picker-range', 'end_date'),
    Input('dashboard2-tabs', 'value'),
    Input('dashboard2-dropdown1', 'value')])

def render_content(start_date, end_date, tab, filial):
    """Построение содержимого выбранной закладки"""

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)


    if tab == 'tab-1':
        """Содержимое 1 закладки"""
        
    elif tab == 'tab-2':
        """Содержимое 2 закладки"""

    elif tab == 'tab-3':
        """Содержимое 3 закладки"""
        
    elif tab == 'tab-4':
        """Содержимое 4 закладки"""
        

# # Настройка видимости фильтров
# @dash_app.callback(
#     Output(component_id='dashboard2-dropdown1', component_property='style'),
#     [Input('dashboard2-tabs', 'value')]
# )
# def dropdown1_visibility(tab):
#     """Настройка видимости фильтра по филиалам"""
#     if tab == 'tab-2':
#         return {"display":"None"}

# @dash_app.callback(
#     Output(component_id='name1', component_property='style'),
#     [Input('dashboard2-tabs', 'value')]
# )
# def name1_visibility(tab):
#     """Настройка видимости заголовка фильтра по филиалам"""
#     if tab == 'tab-2':
#         return {"display":"None"}
#     else:
#         return {"display": "flex",
#                     "align-items": "center",
#                     "height": "38px",
#                     "justify-content": "center"
#                         }

# @dash_app.callback(
#     Output(component_id='dashboard2-dropdown2', component_property='style'),
#     [Input('dashboard2-tabs', 'value')]
# )
# def dropdown2_visibility(tab):
#     """Настройка видимости фильтра по типам запчастей"""
#     if tab == 'tab-3':
#         return {"display":"None"}

# @dash_app.callback(
#     Output(component_id='name2', component_property='style'),
#     [Input('dashboard2-tabs', 'value')]
# )
# def name2_visibility(tab):
#     """Настройка видимости заголовка фильтра по типам запчастей"""
#     if tab == 'tab-3':
#         return {"display":"None"}
#     else:
#         return {"display": "flex",
#                     "align-items": "center",
#                     "height": "38px",
#                     "justify-content": "center"
#                         }

# @dash_app.callback(
#     Output(component_id='dashboard2-dropdown3', component_property='style'),
#     [Input('dashboard2-tabs', 'value')]
# )
# def dropdown3_visibility(tab):
#     """Настройка видимости фильтра по складам"""
#     if tab == 'tab-2' or tab == 'tab-4':
#         return {"display":"None"}

# @dash_app.callback(
#     Output(component_id='name3', component_property='style'),
#     [Input('dashboard2-tabs', 'value')]
# )
# def name3_visibility(tab):
#     """Настройка видимости заголовка фильтра по складам"""
#     if tab == 'tab-2' or tab == 'tab-4':
#         return {"display":"None"}
#     else:
#         return {"display": "flex",
#                     "align-items": "center",
#                     "height": "38px",
#                     "justify-content": "center"
#                         }

# @dash_app.callback(
#     Output(component_id='dashboard2-dropdown4', component_property='style'),
#     [Input('dashboard2-tabs', 'value')]
# )
# def dropdown4_visibility(tab):
#     """Настройка видимости фильтра сортировки"""
#     if tab == 'tab-1':
#         return {"display":"None"}

# @dash_app.callback(
#     Output(component_id='name4', component_property='style'),
#     [Input('dashboard2-tabs', 'value')]
# )
# def name4_visibility(tab):
#     """Настройка видимости заголовка фильтра сортировки"""
#     if tab == 'tab-1':
#         return {"display":"None"}
#     else:
#         return {"display": "flex",
#                     "align-items": "center",
#                     "height": "38px",
#                     "justify-content": "center"
#                         }

# @dash_app.callback(
#     Output(component_id='ri-level', component_property='style'),
#     [Input('dashboard2-tabs', 'value')]
# )
# def radioitems1_visibility(tab):
#     """Настройка видимости радиокнопок для выбора день, неделя или месяц"""
#     if tab == 'tab-2' or tab == 'tab-3' or tab == 'tab-4':
#         return {"display":"None"}

# @dash_app.callback(
#     Output(component_id='warehouse_quantity', component_property='style'),
#     [Input('dashboard2-tabs', 'value')]
# )
# def radioitems2_visibility(tab):
#     """Настройка видимости радиокнопок для выбора количества складов"""
#     if tab == 'tab-1' or tab == 'tab-2' or tab == 'tab-3':
#         return {"display":"None"}

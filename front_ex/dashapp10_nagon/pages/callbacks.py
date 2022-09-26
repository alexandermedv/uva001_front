""" Интерактивные элементы для отчета по нагону."""
import datetime as dt
import numpy as np
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
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
from ..utils import get_defect, get_defect_count, get_transfer, get_transfer_count
from ..utils import get_repair, get_repair_count, get_sale, get_sale_count
from ..utils import get_nagon_results, get_nagon_dynamics
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


# Количество неотраженных операций
@dash_app.callback(
Output(component_id='nagon_count', component_property='children'),
[Input('dashboard2-date-picker-range', 'start_date'),
Input('dashboard2-date-picker-range', 'end_date')]
)

def update_markdown1(start_date,  end_date):
    """Количество неотраженных операций"""

    df1 = get_nagon_results(start_date,  end_date)
    print('Количество непроведенных операций:', df1['oper_accepted_count'].sum())

    return int(df1['oper_accepted_count'].sum())


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
        """Выбраковка"""
        
        df_defect = get_defect(start_date,  end_date)
        defect_count = get_defect_count(start_date,  end_date)

        content = html.Div([
        html.Output(defect_count),
        html.Div([
            html.Br(),
                    dbc.Row(),
                    html.H6('''Непроведенные операции пересылки''',
                        style={'text-align':'center',
                                'font-size': '16pt',
                                'font-weight': 'bold'}),
                    
                    dash_table.DataTable(
                        # https://dash.plotly.com/datatable/width
                        id='table_defect',                        columns=[{"name": i, "id": i} for i in df_defect.columns],

                        data=df_defect.to_dict('records'),
                        page_size=20,
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            # all three widths are needed
                            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'textAlign': 'left',
                        },
                        # style_cell_conditional=[
                        #     {'if': {'column_id': "Описание недостатка"},
                        #     'width': '20%'},
                        #     {'if': {'column_id': "Мероприятие"},
                        #     'width': '20%'},
                        #     {'if': {'column_id': "Первоначальная дата окончания"},
                        #     'width': '5%'},
                        #     {'if': {'column_id': "Пересмотренная дата окончания"},
                        #     'width': '5%'},
                        #     {'if': {'column_id': "Комментарий"},
                        #     'width': '50%'},
                        # ],
                        export_format='xlsx',
                        export_headers='display',
                        merge_duplicate_headers=True,
                        style_header={
                            'backgroundColor': 'rgb(138,36,50)',
                            'color': 'white',
                            'whiteSpace':'normal',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(230, 230, 230)',
                            }
                        ],
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                        },
                    ),
        ]),
        ])

        return content

    elif tab == 'tab-3':
        """Пересылки"""
        
        df_transfer = get_transfer(start_date,  end_date)
        transfer_count = get_transfer_count(start_date,  end_date)

        content = html.Div([
        html.Output(transfer_count),
        html.Div([
            html.Br(),
                    dbc.Row(),
                    html.H6('''Непроведенные операции пересылки''',
                        style={'text-align':'center',
                                'font-size': '16pt',
                                'font-weight': 'bold'}),
                    
                    dash_table.DataTable(
                        # https://dash.plotly.com/datatable/width
                        id='table_transfer',
                        columns=[{"name": i, "id": i} for i in df_transfer.columns],
                        data=df_transfer.to_dict('records'),
                        page_size=20,
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            # all three widths are needed
                            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'textAlign': 'left',
                        },
                        # style_cell_conditional=[
                        #     {'if': {'column_id': "Описание недостатка"},
                        #     'width': '20%'},
                        #     {'if': {'column_id': "Мероприятие"},
                        #     'width': '20%'},
                        #     {'if': {'column_id': "Первоначальная дата окончания"},
                        #     'width': '5%'},
                        #     {'if': {'column_id': "Пересмотренная дата окончания"},
                        #     'width': '5%'},
                        #     {'if': {'column_id': "Комментарий"},
                        #     'width': '50%'},
                        # ],
                        export_format='xlsx',
                        export_headers='display',
                        merge_duplicate_headers=True,
                        style_header={
                            'backgroundColor': 'rgb(138,36,50)',
                            'color': 'white',
                            'whiteSpace':'normal',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(230, 230, 230)',
                            }
                        ],
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                        },
                    ),
        ]),
        ])

        return content

    elif tab == 'tab-4':
        """Ремонты"""
        
        df_repair = get_repair(start_date,  end_date)
        repair_count = get_repair_count(start_date,  end_date)

        content = html.Div([
        html.Output(repair_count),
        html.Div([
            html.Br(),
                    dbc.Row(),
                    html.H6('''Непроведенные операции ремонтов''',
                        style={'text-align':'center',
                                'font-size': '16pt',
                                'font-weight': 'bold'}),
                    
                    dash_table.DataTable(
                        # https://dash.plotly.com/datatable/width
                        id='table_repair',
                        columns=[{"name": i, "id": i} for i in df_repair.columns],
                        data=df_repair.to_dict('records'),
                        page_size=20,
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            # all three widths are needed
                            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'textAlign': 'left',
                        },
                        # style_cell_conditional=[
                        #     {'if': {'column_id': "Описание недостатка"},
                        #     'width': '20%'},
                        #     {'if': {'column_id': "Мероприятие"},
                        #     'width': '20%'},
                        #     {'if': {'column_id': "Первоначальная дата окончания"},
                        #     'width': '5%'},
                        #     {'if': {'column_id': "Пересмотренная дата окончания"},
                        #     'width': '5%'},
                        #     {'if': {'column_id': "Комментарий"},
                        #     'width': '50%'},
                        # ],
                        export_format='xlsx',
                        export_headers='display',
                        merge_duplicate_headers=True,
                        style_header={
                            'backgroundColor': 'rgb(138,36,50)',
                            'color': 'white',
                            'whiteSpace':'normal',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(230, 230, 230)',
                            }
                        ],
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                        },
                    ),
        ]),
        ])

        return content

    elif tab == 'tab-5':
        """Реализация"""
        
        df_sale = get_sale(start_date,  end_date)
        sale_count = get_sale_count(start_date,  end_date)

        content = html.Div([
        html.Output(sale_count),
        html.Div([
            html.Br(),
                    dbc.Row(),
                    html.H6('''Непроведенные операции реализации''',
                        style={'text-align':'center',
                                'font-size': '16pt',
                                'font-weight': 'bold'}),
                    
                    dash_table.DataTable(
                        # https://dash.plotly.com/datatable/width
                        id='table_sale',
                        columns=[{"name": i, "id": i} for i in df_sale.columns],
                        data=df_sale.to_dict('records'),
                        page_size=20,
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            # all three widths are needed
                            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'textAlign': 'left',
                        },
                        # style_cell_conditional=[
                        #     {'if': {'column_id': "Описание недостатка"},
                        #     'width': '20%'},
                        #     {'if': {'column_id': "Мероприятие"},
                        #     'width': '20%'},
                        #     {'if': {'column_id': "Первоначальная дата окончания"},
                        #     'width': '5%'},
                        #     {'if': {'column_id': "Пересмотренная дата окончания"},
                        #     'width': '5%'},
                        #     {'if': {'column_id': "Комментарий"},
                        #     'width': '50%'},
                        # ],
                        export_format='xlsx',
                        export_headers='display',
                        merge_duplicate_headers=True,
                        style_header={
                            'backgroundColor': 'rgb(138,36,50)',
                            'color': 'white',
                            'whiteSpace':'normal',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(230, 230, 230)',
                            }
                        ],
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                        },
                    ),
        ]),
        ])

        return content

    elif tab == 'tab-6':
        """Сводные результаты"""
        
        df1 = get_nagon_results(start_date,  end_date)
        print('df1 =', df1)

        df_v1 = pd.pivot_table(df1, values='oper_accepted_count', index=['year', 'operation'], columns=['filial_name']).reset_index()
        df_v1.rename(columns = {'Владивостокский филиал' : 'Влд', 'Воронежский филиал' : 'Врж', 'Екатеринбургский филиал' : 'Екб',
                                'Иркутский филиал' : 'Ирк', 'Красноярский филиал ': 'Крс', 'Нижегородский филиал' : 'Нжн',
                                'Новосибирский филиал' : 'Нвб', 'Самарский филиал' : 'Смр', 'Головное отделение' : 'ГО',
                                'Ростовский филиал' : 'Рст', 'Санкт-Петербургский филиал' : 'СПб', 'Саратовский филиал': 'Срт',
                                'Челябинский филиал' : 'Члб', 'Ярославский филиал': 'Ярв'}, inplace = True) 
        print('df_v1 =\n', df_v1)

        df_v2 = pd.pivot_table(df1, values='percentage', index=['year', 'operation'], columns=['filial_name']).reset_index()
        df_v2.rename(columns = {'Владивостокский филиал' : 'Влд', 'Воронежский филиал' : 'Врж', 'Екатеринбургский филиал' : 'Екб',
                                'Иркутский филиал' : 'Ирк', 'Красноярский филиал ': 'Крс', 'Нижегородский филиал' : 'Нжн',
                                'Новосибирский филиал' : 'Нвб', 'Самарский филиал' : 'Смр', 'Головное отделение' : 'ГО',
                                'Ростовский филиал' : 'Рст', 'Санкт-Петербургский филиал' : 'СПб', 'Саратовский филиал': 'Срт',
                                'Челябинский филиал' : 'Члб', 'Ярославский филиал': 'Ярв'}, inplace = True) 
        print('df_v2 =\n', df_v2)

        df_v3 = pd.pivot_table(df1, values='oper_count', index=['year', 'operation'], columns=['filial_name']).reset_index()
        df_v3.rename(columns = {'Владивостокский филиал' : 'Влд', 'Воронежский филиал' : 'Врж', 'Екатеринбургский филиал' : 'Екб',
                                'Иркутский филиал' : 'Ирк', 'Красноярский филиал ': 'Крс', 'Нижегородский филиал' : 'Нжн',
                                'Новосибирский филиал' : 'Нвб', 'Самарский филиал' : 'Смр', 'Головное отделение' : 'ГО',
                                'Ростовский филиал' : 'Рст', 'Санкт-Петербургский филиал' : 'СПб', 'Саратовский филиал': 'Срт',
                                'Челябинский филиал' : 'Члб', 'Ярославский филиал': 'Ярв'}, inplace = True) 
        print('df_v3 =\n', df_v3)
        # sale_count = get_sale_count(start_date,  end_date)

        content = html.Div([
        # html.Output(sale_count),
        html.Div([
            html.Br(),
                    dbc.Row(),
                    html.H6('''Сводные результаты по нагону''',
                        style={'text-align':'center',
                                'font-size': '16pt',
                                'font-weight': 'bold'}),
                    
                    dash_table.DataTable(
                        # https://dash.plotly.com/datatable/width
                        id='table_nagon_not_accepted',
                        columns=[{"name": i, "id": i} for i in df_v1.columns],
                        data=df_v1.to_dict('records'),
                        page_size=20,
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            # all three widths are needed
                            'minWidth': '10px', 'width': '180px', 'maxWidth': '180px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'textAlign': 'left',
                        },
                        # style_cell_conditional=[
                        #     {'if': {'column_id': "Описание недостатка"},
                        #     'width': '20%'},
                        #     {'if': {'column_id': "Мероприятие"},
                        #     'width': '20%'},
                        #     {'if': {'column_id': "Первоначальная дата окончания"},
                        #     'width': '5%'},
                        #     {'if': {'column_id': "Пересмотренная дата окончания"},
                        #     'width': '5%'},
                        #     {'if': {'column_id': "Комментарий"},
                        #     'width': '50%'},
                        # ],
                        export_format='xlsx',
                        export_headers='display',
                        merge_duplicate_headers=True,
                        style_header={
                            'backgroundColor': 'rgb(138,36,50)',
                            'color': 'white',
                            'whiteSpace':'normal',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(230, 230, 230)',
                            }
                        ],
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                        },
                    ),

                    dash_table.DataTable(
                        # https://dash.plotly.com/datatable/width
                        id='table_nagon_all_operations',
                        columns=[{"name": i, "id": i} for i in df_v2.columns],
                        data=df_v2.to_dict('records'),
                        page_size=20,
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            # all three widths are needed
                            'minWidth': '10px', 'width': '180px', 'maxWidth': '180px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'textAlign': 'left',
                        },
                        # style_cell_conditional=[
                        #     {'if': {'column_id': "Описание недостатка"},
                        #     'width': '20%'},
                        #     {'if': {'column_id': "Мероприятие"},
                        #     'width': '20%'},
                        #     {'if': {'column_id': "Первоначальная дата окончания"},
                        #     'width': '5%'},
                        #     {'if': {'column_id': "Пересмотренная дата окончания"},
                        #     'width': '5%'},
                        #     {'if': {'column_id': "Комментарий"},
                        #     'width': '50%'},
                        # ],
                        export_format='xlsx',
                        export_headers='display',
                        merge_duplicate_headers=True,
                        style_header={
                            'backgroundColor': 'rgb(138,36,50)',
                            'color': 'white',
                            'whiteSpace':'normal',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(230, 230, 230)',
                            }
                        ],
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                        },
                    ),

                    dash_table.DataTable(
                        # https://dash.plotly.com/datatable/width
                        id='table_nagon_all_operations',
                        columns=[{"name": i, "id": i} for i in df_v3.columns],
                        data=df_v3.to_dict('records'),
                        page_size=20,
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            # all three widths are needed
                            'minWidth': '10px', 'width': '180px', 'maxWidth': '180px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'textAlign': 'left',
                        },
                        # style_cell_conditional=[
                        #     {'if': {'column_id': "Описание недостатка"},
                        #     'width': '20%'},
                        #     {'if': {'column_id': "Мероприятие"},
                        #     'width': '20%'},
                        #     {'if': {'column_id': "Первоначальная дата окончания"},
                        #     'width': '5%'},
                        #     {'if': {'column_id': "Пересмотренная дата окончания"},
                        #     'width': '5%'},
                        #     {'if': {'column_id': "Комментарий"},
                        #     'width': '50%'},
                        # ],
                        export_format='xlsx',
                        export_headers='display',
                        merge_duplicate_headers=True,
                        style_header={
                            'backgroundColor': 'rgb(138,36,50)',
                            'color': 'white',
                            'whiteSpace':'normal',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(230, 230, 230)',
                            }
                        ],
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                        },
                    ),
        ]),
        ])

        return content

    elif tab == 'tab-1':
        """Динамика нагона по данным УДВ"""
        
        df1 = get_nagon_dynamics(start_date, end_date)
        print('df1 =', df1)
        df1_aggr = df1.groupby(['start_date', 'end_date']).sum().reindex()
        print('df1_aggr =', df1_aggr)

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

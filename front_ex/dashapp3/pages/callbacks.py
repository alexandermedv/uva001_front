""" Интерактивные элементы для отчетов по запчастям."""
import os
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from ..pages import dash_app
from ..utils import utils


# Значения списков конфликтов
@dash_app.callback(
Output(component_id='dropdown1', component_property='options'),
[Input('tabs', 'value')])

def conflict_labels(tab):
    """Значения списка конфликтов на вкладке 2"""

    # conf = pd.read_excel(os.getenv("INITIAL_DIRECTORY") + '/ics/dashapp3/utils/SAP_conflicts.xlsx',
    # sheet_name='Для загрузки')

    conf = pd.read_excel(
     '''./uva001_front/front_ex/dashapp3/utils/SAP_conflicts.xlsx''',
     #os.path.join(APP_PATH, "Data", "aug_latest.xlsm"),
     engine='openpyxl',
     sheet_name='Для загрузки',
    )

    return [{'label': conf.iloc[i]['Название конфликта'],
    'value': conf.iloc[i]['Конфликт']} for i in conf.index]

@dash_app.callback(
Output(component_id='dropdown2', component_property='options'),
[Input('tabs', 'value')])

def conflict_labels1(tab):
    """Значения списка функций на вкладке 6"""

    if tab == 'tab-6':
        func = pd.read_excel(
                os.getenv("INITIAL_DIRECTORY") + '''/ics/dashapp3/utils/SAP_conflicts.xlsx''',
                sheet_name='Функции')

        return [{'label': func.iloc[i]['Функция'],
        'value': func.iloc[i]['Номер_функции']} for i in func.index]
    else:
        return [{'label':'', 'value':''}]

@dash_app.callback(
Output(component_id='dropdown3', component_property='options'),
[Input('tabs', 'value'),
Input('dropdown2', 'value')],)

def conflict_labels2(tab, function1):
    """Значения списка функций на вкладке 6"""

    if tab == 'tab-6':
        func = pd.read_excel(
                os.getenv("INITIAL_DIRECTORY") + '''/ics/dashapp3/utils/SAP_conflicts.xlsx''',
                sheet_name='Конфликты по функциям')

        func = func[func['Номер_функции_1'] == int(function1)]
        func = func.reset_index()

        return [{'label': func.iloc[i]['Функция_2'],
        'value': func.iloc[i]['Номер_функции_2']} for i in func.index]

    else:
        return [{'label':'', 'value':''}]

@dash_app.callback(
Output(component_id='dropdown3', component_property='value'),
[Input('tabs', 'value'),
Input('dropdown2', 'value')],)

def conflict_value(tab, function1):
    """Выбранное значение списка функций на вкладке 6"""

    if tab == 'tab-6':
        func = pd.read_excel(
                os.getenv("INITIAL_DIRECTORY") + '''/ics/dashapp3/utils/SAP_conflicts.xlsx''',
                sheet_name='Конфликты по функциям')

        func = func[func['Номер_функции_1'] == int(function1)]
        func = func.reset_index()

        return func.iloc[0]['Номер_функции_2']
    else:
        return [{'label':'', 'value':''}]


# # Значения списка функций
# @dash_app.callback(
# Output(component_id='dropdown2', component_property='options'),
# [Input('tabs', 'value')])

# # def conflict_labels(tab):
# #     if tab == 'tab-6':
# #         func = pd.read_excel(os.getenv("INITIAL_DIRECTORY") + '/ics/dashapp3/utils/SAP_conflicts.xlsx', sheet_name='Функции')
# #         return [{'label': func.iloc[i]['function'],
# #  'value': func.iloc[i]['function_number']} for i in func.index]


# Построение содержимого выбранной закладки
@dash_app.callback(Output('tab-content', 'children'),
    [Input('tabs', 'value'),
    Input('dropdown1', 'value'),
    Input('dropdown2', 'value'),
    Input('dropdown3', 'value')])

def render_content(tab, conflict, function1, function2):
    """Построение содержимого выбранной закладки"""

    if tab == 'tab-1':
        # Свод

        data = utils.get_summary_data()
        data_quantity = data.groupby('Конфликт').count()
        data_quantity['Полномочия'] = data_quantity.index
        data_quantity['Количество'] = data_quantity['Логин']
        data_quantity = data_quantity[['Полномочия','Логин']]

        content = html.Div([
                html.Div([
                    html.Strong('''Статистика по всем видам конфликтов и наличию критичных
                     полномочий, которые должны быть присвоены только определенным
                     группам пользователей.'''),
                    html.Br([]),
                ], className="row",
                ),
                html.Br([]),

                html.Div([
                    html.P('''Количество учетных записей с конфликтными или критичными
                     полномочиями: '''),
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in data_quantity.columns],
                        data=data_quantity.to_dict('records'),
                        style_table={'overflowX': 'scroll'},
                        page_size=20,
                        style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                        ],
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        }
                    ),
                html.Br([]),
                ], className="row",
                ),

                html.Div([
                    html.P('''Обнаружены следующие учетные записи c конфликтующими или критичными
                     полномочиями: '''),
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in data.columns],
                        data=data.to_dict('records'),
                        style_table={'overflowX': 'scroll'},
                        page_size=20,
                        style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                        ],
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        }
                    ),
                html.Br([]),
                ], className="row",
                ),
            ], style = {'margin': '20px'},
            )

        return content

    elif tab == 'tab-2':
        # Конфликты и критичные полномочия

        # conf = pd.read_excel(
        #     os.getenv("INITIAL_DIRECTORY") + '''/ics/dashapp3/utils/SAP_conflicts.xlsx''',
        #     sheet_name='Для загрузки')

        conf = pd.read_excel(
            '''./uva001_front/front_ex/dashapp3/utils/SAP_conflicts.xlsx''',
            #os.path.join(APP_PATH, "Data", "aug_latest.xlsm"),
            engine='openpyxl',
            sheet_name='Для загрузки',
        )

        if conflict == 'conflict1':
            data = utils.get_conflict1_data()
        elif conflict == 'conflict2':
            data = utils.get_conflict2_data()
        elif conflict == 'conflict3':
            data = utils.get_conflict3_data()
        elif conflict == 'conflict4':
            data = utils.get_conflict4_data()
        elif conflict == 'conflict5':
            data = utils.get_conflict5_data()
        elif conflict == 'conflict6':
            data = utils.get_conflict6_data()
        elif conflict == 'conflict7':
            data = utils.get_conflict7_data()
        elif conflict == 'conflict8':
            data = utils.get_conflict8_data()
        elif conflict == 'conflict9':
            data = utils.get_conflict9_data()
        elif conflict == 'conflict10':
            data = utils.get_conflict10_data()
        elif conflict == 'conflict11':
            data = utils.get_conflict11_data()
        elif conflict == 'conflict12':
            data = utils.get_conflict12_data()
        elif conflict == 'conflict13':
            data = utils.get_conflict13_data()
        elif conflict == 'conflict14':
            data = utils.get_conflict14_data()
        elif conflict == 'conflict15':
            data = utils.get_conflict15_data()
        elif conflict == 'conflict16':
            data = utils.get_conflict16_data()
        elif conflict == 'conflict17':
            data = utils.get_conflict17_data()
        elif conflict == 'conflict18':
            data = utils.get_conflict18_data()

        data_short = data[['Логин', 'Действ. с', 'Действ. по', 'Тип пользователя', 'Группа',
         'ФИО', 'Отдел', 'Функция', 'Конфликт']].drop_duplicates()

        content = html.Div([
                html.Div([
                    html.Strong(conf.loc[conf['Конфликт'] == conflict]["Название конфликта"]),
                    html.Br([]),
                    html.Br([]),
                    html.P(conf.loc[conf['Конфликт'] == conflict]["Описание конфликта"]),
                    # html.P('- S_TCODE (TCD = SU01)'),
                    # html.P('- S_USER_GRP (ACTVT = 01 or 02 or 06 or 22)'),
                    # html.P('- S_USER_PRO (ACTVT = 22)'),
                    # html.P('- S_USER_AGR (ACTVT = 22)'),
                ], className="row",
                ),
                html.Br([]),

                html.Div([
                    html.P('''Обнаружены следующие учетные записи c конфликтующими
                     или критичными полномочиями: '''),
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in data_short.columns],
                        data=data_short.to_dict('records'),
                        style_table={'overflowX': 'scroll'},
                        page_size=20,
                        style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                        ],
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        }
                    ),
                html.Br([]),
                ], className="row",
                ),
                html.Div([
                    html.P('''Данные учетные записи одновременно содержат следующие объекты
                     полномочий, которые являются конфликтующими или чрезмерными:'''),
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in data.columns],
                        data=data.to_dict('records'),
                        style_table={'overflowX': 'scroll'},
                        page_size=20,
                        style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                        ],
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        }
                    ),
                ], className="row",
                ),
            ], style = {'margin': '20px'},
            )

        return content


    elif tab == 'tab-3':
        # Стандартные профили полномочий

        data = utils.get_profiles_data()

        content = html.Div([
                html.Div([
                    html.Strong('''Стандартные привилегированные профили позволяют выполнять
                     критичные настройки системы, выполнять любые действия, корректировать код
                     системы, запускать программы и выполнять другие критичные изменения. В
                     продуктиве не должно быть пользователей, которым присвоены данные профили.'''),
                    html.Br([]),
                ], className="row",
                ),
                html.Br([]),

                html.Div([
                    html.P('''Обнаружены следующие учетные записи со стандартными
                     привилегированными профилями: '''),
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in data.columns],
                        data=data.to_dict('records'),
                        style_table={'overflowX': 'scroll'},
                        page_size=20,
                        style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                        ],
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        }
                    ),
                html.Br([]),
                ], className="row",
                ),

            ], style = {'margin': '20px'},
            )

        return content

    elif tab == 'tab-4':
        # Учетные записи, неактивные в течение 60 и более дней

        data = utils.get_inactive_data()

        content = html.Div([
                html.Div([
                    html.Strong('''Учетные записи, вход под которыми не осуществлялся в течение
                     60 дней и более. Данные учетные записи расходуют лицензии и могут принадлежать
                     уволенным сотрудникам, в частности, сотрудникам, договор ГПХ с которыми
                     прекратился или внешним сотрудникам, которые более не оказывают услуг
                     ПАО "ПГК".'''),
                    html.Br([]),
                ], className="row",
                ),
                html.Br([]),

                html.Div([
                    html.P('''Учетные записи, неактивные в течение 60 и более дней: '''),
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in data.columns],
                        data=data.to_dict('records'),
                        style_table={'overflowX': 'scroll'},
                        page_size=20,
                        style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                        ],
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        }
                    ),
                html.Br([]),
                ], className="row",
                ),

            ], style = {'margin': '20px'},
            )

        return content

    elif tab == 'tab-5':
        # Учетные записи внешних сотрудников, не ограниченные по сроку действия

        data = utils.get_unlimited_time_data()

        content = html.Div([
                html.Div([
                    html.Strong('''При увольнении сотрудника сторонней организации или прекращения
                     договора оказания
                     услуг ПАО "ПГК" часто не получает об этом никакой информации или получает ее с большой задержкой.
                     Компенсирующим контролем является блокировка УЗ, неактивных в течение 60 дней, но данная контрольная 
                     процедура выполняется только перед лицензионным аудитом, ее недостаточно для уменьшения риска несвоевременного
                     прекращения доступа. Поэтому важно сразу устанавливать срок действия учетной записи стороннего сотрудника, он не
                     должен превышать 1 год, чтобы гарантировать актуализацию полномочий хотя бы раз в год.
                    '''),
                    html.Br([]),
                ], className="row",
                ),
                html.Br([]),

                html.Div([
                    html.P('''Учетные записи внешних сотрудников (не входящие в группы ЦА, ЦКР,
                     филиалов, базиса и ИТ-специалистов), для которых не ограничен срок
                     действия: '''),
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in data.columns],
                        data=data.to_dict('records'),
                        style_table={'overflowX': 'scroll'},
                        page_size=20,
                        style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                        ],
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        }
                    ),
                html.Br([]),
                ], className="row",
                ),

            ], style = {'margin': '20px'},
            )

        return content

    elif tab == 'tab-6':
        # Конфликты полномочий на уровне транзакций

        matrix = pd.read_excel(
                os.getenv("INITIAL_DIRECTORY") + '''/ics/dashapp3/utils/SAP_conflicts.xlsx''',
                sheet_name='Critical_segregations')

        func = pd.read_excel(
            os.getenv("INITIAL_DIRECTORY") + '''/ics/dashapp3/utils/SAP_conflicts.xlsx''',
            sheet_name='Функции')
        #return [{'label': func.iloc[i]['function'],
        # 'value': func.iloc[i]['function_number']} for i in func.index]

        transactions = pd.read_excel(
                os.getenv("INITIAL_DIRECTORY") + '''/ics/dashapp3/utils/SAP_conflicts.xlsx''',
                sheet_name='Transactions')

        transactions1 = transactions[transactions['Номер_функции']==int(function1)]
        transactions2 = transactions[transactions['Номер_функции']==int(function2)]
        transactions = pd.merge(transactions1, transactions2, how = 'outer', on = ['Код_транзакции'])

        for trans in transactions1['Код_транзакции']:
            conf_users1 = utils.get_conf_users_data(trans)

        for trans in transactions2['Код_транзакции']:
            conf_users2 = utils.get_conf_users_data(trans)

        conf_users = pd.merge(conf_users1, conf_users2, how = 'inner', on = ['uname'])[['uname', 'agr_name_x', 'agr_name_y', 'to_dat_x', 'to_dat_y']].drop_duplicates()
        conf_users.rename(columns={'uname': 'Логин', 'agr_name_x': 'Роль_1', 'agr_name_y': 'Роль_2', 'to_dat_x': 'Действ_до_1', 'to_dat_y': 'Действ_до_2'}, inplace=True)
        conf_users_short = conf_users[conf_users['Действ_до_1'] == '99991231']
        conf_users_short = conf_users_short[conf_users_short['Действ_до_2'] == '99991231']
        conf_users_short = conf_users_short[['Логин']].drop_duplicates()
        usr02 = utils.get_usr02_data().rename(columns={'bname': 'Логин'})
        user_addrs = utils.get_user_addrs_data().rename(columns={'bname': 'Логин'})
        conf_users_short = pd.merge(conf_users_short, usr02, how = 'inner', on = ['Логин'])[['Логин', 
            'gltgv', 'gltgb', 'class', 'ustyp']].rename(columns={'gltgv': 'Действ_с', 'gltgb': 'Действ_по', 'class': 'Группа', 'ustyp': 'Тип'})
        conf_users_short = pd.merge(conf_users_short, user_addrs, how = 'inner', on = ['Логин'])[['Логин', 
            'Действ_с', 'Действ_по', 'Группа', 'Тип', 'department', 'function']].rename(columns={'department': 'Подразделение', 'function': 'Позиция'})
        conf_roles = conf_users[conf_users['Роль_1'] == conf_users['Роль_2']]
        conf_roles = conf_roles[['Роль_1']].drop_duplicates().rename(columns={'Роль_1': 'Роль'})
        agr_define = utils.get_agr_texts_data()[['agr_name', 'text']].rename(columns={'agr_name': 'Роль', 'text':'Описание_роли'})
        conf_roles = pd.merge(conf_roles, agr_define, how = 'inner', on = ['Роль'])[['Роль', 'Описание_роли']]

        content = html.Div([
                html.Div([
                    html.Strong('''Конфликты полномочий на уровне транзакций
                    '''),
                    html.Br([]),
                ], className="row",
                ),
                html.Br([]),

                # html.Div([
                #     html.P('''Конфликтующие функции:'''),
                #     html.Div([
                #         dash_table.DataTable(
                #             id='table1',
                #             columns=[{"name": i, "id": i} for i in matrix.columns],
                #             data=matrix.to_dict('records'),
                #             style_table={'overflowX': 'scroll'},
                #             page_size=40,
                #             style_data_conditional=[
                #             {
                #                 'if': {'row_index': 'odd'},
                #                 'backgroundColor': 'rgb(248, 248, 248)'
                #             }
                #             ],
                #             style_header={
                #                 'backgroundColor': 'rgb(230, 230, 230)',
                #                 'fontWeight': 'bold'
                #             },
                #         ),
                #     ], className="row",
                #     ),
                # html.Br([]),
                # ], className="row",
                # ),

                html.Div([
                    html.P('''Конфликтующие транзакции:'''),
                    html.Div([
                        dash_table.DataTable(
                            id='table2',
                            columns=[{"name": i, "id": i} for i in transactions1.columns],
                            data=transactions1.to_dict('records'),
                            style_table={'overflowX': 'scroll'},
                            page_size=20,
                            style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }
                            ],
                            style_header={
                                'backgroundColor': 'rgb(230, 230, 230)',
                                'fontWeight': 'bold'
                            },
                        ),
                    ], className="six columns",
                    ),
                    html.Div([
                        dash_table.DataTable(
                            id='table3',
                            columns=[{"name": i, "id": i} for i in transactions2.columns],
                            data=transactions2.to_dict('records'),
                            style_table={'overflowX': 'scroll'},
                            page_size=20,
                            style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }
                            ],
                            style_header={
                                'backgroundColor': 'rgb(230, 230, 230)',
                                'fontWeight': 'bold'
                            },
                        ),
                    ], className="six columns",
                    ),
                html.Br([]),
                ], className="row",
                ),
                html.Div([
                    html.P('''Пользователи, имеющие конфликты полномочий:'''),
                    dash_table.DataTable(
                        id='table4',
                        columns=[{"name": i, "id": i} for i in conf_users_short.columns],
                        data=conf_users_short.to_dict('records'),
                        style_table={'overflowX': 'scroll'},
                        page_size=20,
                        style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                        ],
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        }
                    ),
                html.Br([]),
                ], className="row",
                ),
                html.Div([
                    html.P('''Список конфликтующих ролей по пользователям:'''),
                    dash_table.DataTable(
                        id='table5',
                        columns=[{"name": i, "id": i} for i in conf_users.columns],
                        data=conf_users.to_dict('records'),
                        style_table={'overflowX': 'scroll'},
                        page_size=20,
                        style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                        ],
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        }
                    ),
                html.Br([]),
                ], className="row",
                ),
                html.Div([
                    html.P('''Список ролей, содержащих конфликты полномочий:'''),
                    dash_table.DataTable(
                        id='table6',
                        columns=[{"name": i, "id": i} for i in conf_roles.columns],
                        data=conf_roles.to_dict('records'),
                        style_table={'overflowX': 'scroll'},
                        page_size=20,
                        style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                        ],
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        }
                    ),
                html.Br([]),
                ], className="row",
                ),

                

            ], style = {'margin': '20px'},
            )

        return content

    elif tab == 'tab-7':
        # Критичные действия в системе

        content = html.Div([
                html.Div([
                    html.Strong('''Данная страница еще не разработана.
                    '''),
                    html.Br([]),
                ], className="row",
                ),
                html.Br([]),

            ], style = {'margin': '20px'},
            )

        return content

    elif tab == 'tab-8':
        # Конфликтные роли, которые никому не присвоены

        content = html.Div([
                html.Div([
                    html.Strong('''Данная страница еще не разработана.
                    '''),
                    html.Br([]),
                ], className="row",
                ),
                html.Br([]),

            ], style = {'margin': '20px'},
            )

        return content

    elif tab == 'tab-9':
        # Незаблокированные УЗ уволенных сотрудников

        content = html.Div([
                html.Div([
                    html.Strong('''Для реализации данного теста требуется интеграция с SAP HCM и
                     доступ к данным о сотрудниках ПАО "ПГК" и ООО "ЦКР". 
                    '''),
                    html.Br([]),
                ], className="row",
                ),
                html.Br([]),

            ], style = {'margin': '20px'},
            )

        return content

# Настройка видимости фильтров
@dash_app.callback(
    Output(component_id='dropdown1', component_property='style'),
    [Input('tabs', 'value')]
)
def dropdown1_visibility(tab):
    """Настройка видимости фильтра по конфликтам на вкладке 2"""
    if tab != 'tab-2':
        return {"display":"None"}

@dash_app.callback(
    Output(component_id='dropdown2', component_property='style'),
    [Input('tabs', 'value')]
)
def dropdown1_visibility(tab):
    """Настройка видимости фильтра по конфликтам на вкладке 6"""
    if tab != 'tab-6':
        return {"display":"None"}

@dash_app.callback(
    Output(component_id='dropdown3', component_property='style'),
    [Input('tabs', 'value')]
)
def dropdown1_visibility(tab):
    """Настройка видимости фильтра по конфликтам на вкладке 6"""
    if tab != 'tab-6':
        return {"display":"None"}
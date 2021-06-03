""" Шаблоны для отчетов по запчастям."""
from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
#import dash_table
import pandas as pd
import os

#from flask_app import engine_analysis, engine_cons

def create_layout():
    """Создание шаблона"""

    print('directory:', os.getcwd())
    # func = pd.read_excel(
    #         #os.getenv("INITIAL_DIRECTORY") + '''/ics/dashapp3/utils/SAP_conflicts.xlsx''',
    #         #sheet_name='Функции')
    #         '''./uva001_front/front_ex/dashapp3/utils/SAP_conflicts.xlsx''',
    #         sheet_name='Функции')

    func = pd.read_excel(
     '''./front_ex/dashapp3/utils/SAP_conflicts.xlsx''',
     #os.path.join(APP_PATH, "Data", "aug_latest.xlsm"),
     engine='openpyxl',
     sheet_name='Функции',
    )
    print(func)

    layout2 = html.Div([
        html.Div([
            # Row 1 - Описание отчета
            html.Div([
                html.Div(
                    [
                        html.H5("Отчет о ролях и полномочиях в SAP"),
                        html.Br([]),
                        html.P("\
                            Данный отчет содержит информацию о критичных ролях и полномочиях в SAP, пересечении критичных полномочий.\
                            Отчет построен на основе данных о пользователях SAP S/4.",
                            style={"color": "#ffffff"},
                            className="row",
                        ),
                        html.P(
                            dcc.Markdown("\
                            На " + datetime.now().strftime("%d.%m.%Y") +
                            """ обнаружены следующие конфликты и критичные полномочия, требующие внимания:"""
                            #  + '{0:,}'.format(round(engine_cons.execute(
                            #      """SELECT round(sum("Сумма во внутренней валюте по дебе" -
                            #      "Сумма во внутренней валюте по кред")) AS "Сальдо"
                            #      FROM sap_s4.osv_94""").fetchone()[0]/1000)).replace(',', ' ') +
                            #     "** тыс. руб.",
                                        ),
                            style={"color": "#ffffff"},
                            className="row",
                            ),
                    ], className="product",
                )
            ], className="row",
            ),

            # Row 2 - 1-й ряд фильтров
            html.Div([

                # html.Output('Начало периода:'),

                # html.Br(),

                # dcc.DatePickerSingle(
                #     id='date-picker-single1',
                #     min_date_allowed=date(2000, 1, 1),
                #     max_date_allowed=date(2050, 1, 1),
                #     initial_visible_month=date(2020, 1, 1),
                #     date=date(2020, 1, 1),
                # ),
                # html.Br(),
                # html.Br(),

                # html.Output('Конец периода:'),
                # html.Br(),

                # dcc.DatePickerSingle(
                #     id='date-picker-single2',
                #     min_date_allowed=date(2000, 1, 1),
                #     max_date_allowed=date(2050, 1, 1),
                #     initial_visible_month=date(2020, 1, 1),
                #     date=datetime.now()
                # ),
                # html.Br(),
                # html.Br(),

                # html.Output('Конфликтные/критичные полномочия:'),
                # html.Br(),

                # html.Br(),

                html.Div([
                    dcc.Tabs(id='tabs',
                        value='tab-1',
                        vertical = True,
                        children=[
                        dcc.Tab(label='Свод', value='tab-1', className="tab",),
                        dcc.Tab(label='Конфликты/привилегии на уровне объектов полномочий',
                         value='tab-2', className="tab",),
                        dcc.Tab(label='Стандартные профили', value='tab-3', className="tab",),
                        dcc.Tab(label='УЗ, неактивные в течение 60 и более дней', value='tab-4',
                         className="tab",),
                        dcc.Tab(label='УЗ сторонних сотрудников без срока действия', value='tab-5',
                         className="tab",),
                        dcc.Tab(label='Конфликты на уровне транзакций', value='tab-6',
                         className="tab",),
                        dcc.Tab(label='Критичные действия в системе', value='tab-7',
                         className="tab",),
                        dcc.Tab(label='Конфликтные роли, которые никому не присвоены',
                         value='tab-8', className="tab",),
                        dcc.Tab(label='Незаблокированные УЗ уволенных сотрудников', value='tab-9',
                         className="tab",),
                    ], className="row all-tabs"),
                    #html.Div(id='tabs-example-content')
                ]),
            ], className='two columns',
            style = {'margin': '20px'},
            ),

            html.Div([
                dbc.Navbar([
                    dcc.Dropdown(
                        id='dropdown1',
                        clearable = False,
                        value='conflict1',
                        optionHeight=40,
                        style={
                            # 'width': '80%',
                            # 'display': 'inline-block',
                            'margin': '20px'
                            },
                        className='six columns',
                    ),
                    dcc.Dropdown(
                            id='dropdown2',
                            clearable = False,
                            # options=[{'label': func.iloc[i]['function'],
                            #     'value': func.iloc[i]['function_number']} for i in func.index],
                            value='1',
                            optionHeight=40,
                            style={
                                # 'width': '80%',
                                # 'display': 'inline-block',
                                'margin': '20px'
                                },
                            className='six columns',
                        ),
                    dcc.Dropdown(
                        id='dropdown3',
                        clearable = False,
                        # options=[{'label': func.iloc[i]['function'],
                        #     'value': func.iloc[i]['function_number']} for i in func.index],
                        #value='1',
                        optionHeight=40,
                        style={
                            # 'width': '80%',
                            # 'display': 'inline-block',
                            'margin': '20px'
                            },
                        className='six columns',
                    ),
                ], className = "row",
                ),
            # Row 5 - Содержимое закладки
                html.Div(id='tab-content'),

            ], className='ten columns'),

        ], className="sub_page",
        ),
    ], className="page_landscape_a3",
    )

    return layout2

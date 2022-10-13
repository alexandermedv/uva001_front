from datetime import date, datetime
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd

def create_layout():
    """Создание шаблона"""

    layout2 = html.Div([
        html.H3('Отчеты по запчастям'),
        dcc.Dropdown(
            id='app-1-dropdown',
            options=[
                {'label': 'Отчеты по запчастям - {}'.format(i), 'value': i} for i in [
                    'Отчет по дублям', 'Отчет по неликвидным запчастям', 'Отчет по динамике недостачи в SAP'
                ]
            ]
        ),
        html.Div(id='app-1-display-value'),
        dcc.Link('Перейти к отчетам по ролям и полномочиям в SAP', href='/access_SAP')
    ])

    def get_data_non_used_details_udv():
        #sql = dashapp1_non_used_details_udv()
        sql = 'SELECT * FROM sap_s4.am_t001w'
        df = pd.read_sql(sql, con=engine_analysis)
        return df

    # Шаблон первой страницы с выбором отчетов
    index_page = html.Div([
        dcc.Link('Отчет по неликвидным запчастям', href='/repair_parts/dashboard1'),
        html.Br(),
        dcc.Link('Отчет по динамике недостачи', href='/repair_parts/dashboard2'),
    ])

    dashboard1_description = '''
        ##### Описание отчета
        
        Данный отчет содержит информацию о неликвидных запчастях по системам УДВ и SAP в разрезе филиалов и типов запчастей.  
        Неликвидными считаются запчасти, с которыми в течение периода более 180 дней не выполняется никаких операций.
        ***
        '''

    dashboard1_distribution = '''
        ##### Распределение неликвидных запчастей по филиалам
        '''

    dashboard1_table = '''
        ##### Список неликвидных запчастей
        '''



    # Отчет по неликвидным запчастям
    layout1 = html.Div([
        dbc.Navbar(
                dbc.NavbarBrand(html.Div("УВА. Отчет по неликвидным запчастям.", style={'fontSize': 25})),
            color='rgb(149, 55, 53)', dark=True),
        dbc.Navbar([
            html.Div('Выберите систему:', className='two columns', style={'color': 'white'}),

            # html.Label('Выберите систему:'),
            #     dcc.RadioItems(id='radioitems_system',
            # options=[
            #     {'label': 'УДВ', 'value': 'УДВ'},
            #     {'label': 'SAP', 'value': 'SAP'},
            # ],
            # value='УДВ',
            # labelStyle={'display': 'inline-block'}
            # ),

            html.Div(dcc.Dropdown(id='dropdown_system',
                                        style={'width': '100px'},
                                        options=[{'label':'УДВ', 'value': 'УДВ'}, {'label':'SAP', 'value': 'SAP'} ],
                                        value= 'УДВ',
                                        clearable=False,
                                        className='four columns'))
            # ,html.Div('Выберите тип запчастей:', className='two columns', style={'color': 'white'})
            # ,html.Div(dcc.Dropdown(id='detail_type',
            #                             style={'width': '250px'},
            #                             options=[{'label':'Колесная пара', 'value':'KP'},
            #                                      {'label':'Боковые рамы', 'value':'RB'},
            #                                      {'label':'Надрессорные балки', 'value':'BN'},
            #                                      {'label':'Поглощающие аппараты', 'value':'PA'}]), className='four columns')
        ], dark=True, sticky="top", color='rgb(71, 71, 71)'),

        # Описание отчета
        html.Div([
            dcc.Markdown(children=dashboard1_description)
        ]),

        # Гистограмма неликвидных запчастей по филиалам
        html.Div([
            dcc.Markdown(children=dashboard1_distribution)
        ]),
        html.Div([
            dbc.Col(dcc.Graph(id='graph1'))
            ], className='row'),

        # Таблица со списком неликвидных запчастей
        html.Div([
            dcc.Markdown(children=dashboard1_table)
        ]),
        html.Div([
            dbc.Col(dash_table.DataTable(id='table1',
                                        editable=True,
                                        filter_action="native",
                                        sort_action="native",
                                        sort_mode="multi",
                                        column_selectable="single",
                                        selected_columns=[],
                                        selected_rows=[],
                                        page_action="native",
                                        page_current= 0,
                                        page_size= 15
            ))
        ], className='eleven columns')

        ])

    return layout1
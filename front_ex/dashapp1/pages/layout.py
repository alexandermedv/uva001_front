""" Шаблоны для отчетов по запчастям."""
from datetime import date
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from . import engine_cons
from ..utils import get_max_date
#import dash_table
#import pandas as pd

#from flask_app import engine_analysis, engine_cons

def create_layout():
    """Создание шаблона"""
    layout2 = html.Div([
        html.Div([
            # Row 1 - Описание отчета
            html.Div([
                html.Div(
                    [
                        html.H5("Отчет о размере и динамике недостачи номерных деталей"),
                        html.Br([]),
                        html.P("\
                            Данный отчет содержит информацию о динамике недостачи номерных деталей и недостаче на указанную дату в разрезе филиалов, типов запчастей и складов.\
                            Отчет построен на основе данных по счету 9402110000 - Недостачи по НзЧ (номерной) в SAP S/4.",
                            style={"color": "#ffffff"},
                            className="row",
                        ),
                        html.P(
                            dcc.Markdown("\
                            На **" + get_max_date().strftime("%d.%m.%Y") +
                            "** размер недостачи по данным SAP составляет **"
                             + '{0:,}'.format(round(engine_cons.execute(
                                 """SELECT round(sum("Сумма во внутренней валюте по дебе" -
                                 "Сумма во внутренней валюте по кред")) AS "Сальдо"
                                 FROM sap_s4.osv_94""").fetchone()[0]/1000)).replace(',', ' ') +
                                "** тыс. руб.",
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
                dbc.Navbar([
                    html.Div(
                        html.Output('Дата:'),
                        className='one column',
                        style={"display": "flex",
                        "align-items": "center",
                        "height": "38px"
                            }
                            ),
                    dcc.DatePickerRange(
                        id='dashboard2-date-picker-range',
                        min_date_allowed=date(2000, 1, 1),
                        max_date_allowed=date(2050, 1, 1),
                        initial_visible_month=date(2020, 1, 1),
                        start_date=date(2020, 1, 1),
                        end_date=get_max_date().strftime("%m.%d.%Y"),
                        number_of_months_shown = 3,
                        updatemode = 'singledate',
                        display_format='DD.MM.YYYY',
                        start_date_placeholder_text='Начало периода',
                        end_date_placeholder_text='Конец периода',
                    className='four columns'),

                    html.Div(
                        html.Output('Изменение недостачи за период, тыс. руб.:'),
                    className='five columns',
                    style={"display": "flex",
                        "align-items": "center",
                        "height": "38px"
                            }),
                    html.Div(
                        html.B(
                            html.Output(id='shortage_amount'),
                            ),
                    className='two columns',
                                style={"border-style": "groove",
                                    "border-radius": "5px",
                                    "height": "38px",
                                    "display": "flex",
                                    "align-items": "center",
                                    "justify-content": "center"
                                    }
                            ),
                ],)
            ], className="row",
                    ),

            # Row 3 - 2-й ряд фильтров
            html.Div(
                html.Br(),
                style={"height":"5px"}),
            html.Div([
                dbc.Navbar([
                    html.Div(
                        html.Output('Филиал:'),
                        id = 'name1',
                        className='two columns',
                        style={"display": "flex",
                        "align-items": "center",
                        "height": "38px",
                        "justify-content": "center"
                            }
                            ),
                    dcc.Dropdown(
                        id="dashboard2-dropdown1",
                        value='Все филиалы',
                        clearable=False,
                        style={"display": "flex",
                            "justify-content": "center"},
                        #multi=True,
                        className='three columns'),

                    html.Div(
                        html.Output('Тип запчасти:'),
                        id = 'name2',
                        className='two columns',
                        style={"display": "flex",
                        "align-items": "center",
                        "justify-content": "center",
                        "height": "38px"
                            }
                            ),
                    dcc.Dropdown(
                            id="dashboard2-dropdown2",
                            value='Все запчасти',
                            clearable=False,
                            style={"display": "flex",
                                "justify-content": "center"},
                            className='two columns',
                                ),

                    html.Div(
                        html.Output('Склад:'),
                        id = 'name3',
                        className='one column',
                        style={"display": "flex",
                        "align-items": "center",
                        "justify-content": "center",
                        "height": "38px"
                            }
                            ),
                    dcc.Dropdown(
                        id="dashboard2-dropdown3",
                        value='Все склады',
                        clearable=False,
                        className='three columns',
                        style={"display": "flex",
                            "justify-content": "center"}),

                    ],),

                    html.Div(
                        html.Output('Сортировка:'),
                        id = 'name4',
                        className='two columns',
                        style={"display": "flex",
                        "align-items": "center",
                        "justify-content": "right",
                        "height": "38px"
                            }
                    ),
                    dcc.Dropdown(
                        id="dashboard2-dropdown4",
                        options=[
                            {'label': 'Входящее сальдо',
                            'value': 'Входящее сальдо'},
                            {'label': 'Оборот', 'value': 'Оборот'},
                            {'label': 'Исходящее сальдо',
                            'value': 'Исходящее сальдо'},
                            {'label': 'Входящее сальдо, шт.', 'value': 'Входящее сальдо, шт.'},
                            {'label': 'Оборот, шт.', 'value': 'Оборот, шт.'},
                            {'label': 'Исходящее сальдо, шт.', 'value': 'Исходящее сальдо, шт.'}
                        ],
                        value='Оборот',
                        clearable=False,
                        className='two columns',

                    )
                ], className="row",
                ),


            html.Div([
                html.Div([
                    dcc.RadioItems(
                        options=[
                            {'label': i, 'value': i}
                            for i in ['Месяц', 'Неделя', 'День']
                        ],
                        value="Месяц",
                        id = 'ri-level',
                        labelStyle={'display': 'inline-block',
                                    "height": "20px"},
                        # style={"display": "flex",
                        #    "align-items": "center",
                        #    "height": "20px"}
                    ),
                ],
                className = 'three columns'
                ),
                html.Div([
                    dcc.RadioItems(
                        options=[
                            {'label': i, 'value': i}
                            for i in ['10', '20', '30']
                        ],
                        value="10",
                        id = 'warehouse_quantity',
                        labelStyle={'display': 'inline-block',
                                    "height": "20px"},
                        # style={"display": "flex",
                        #    "align-items": "center",
                        #    "height": "20px"}
                    ),
                ],
                className = 'three columns'
                ),
            ], className="row",
            ),

            # Row 4 - Закладки

            html.Div([
                dcc.Tabs(id='dashboard2-tabs', value='tab-1', children=[
                    dcc.Tab(label='Динамика недостачи', value='tab-1', className="tab",),
                    dcc.Tab(label='По филиалам', value='tab-2', className="tab",),
                    dcc.Tab(label='По типам запчастей', value='tab-3', className="tab",),
                    dcc.Tab(label='По складам', value='tab-4', className="tab",),
                ], className="row all-tabs"),
                #html.Div(id='tabs-example-content')
            ]),

            # Row 5 - Содержимое закладки
            html.Div(id='tab-content'),
        ], className="sub_page",
                ),
    ], className="page_landscape_a3",
    )

    return layout2

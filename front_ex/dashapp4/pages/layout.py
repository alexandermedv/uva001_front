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
                        html.H5("Отчет о дебиторской задолженности и лимитах"),
                        html.Br([]),
                        html.P("\
                            Данный отчет содержит информацию о динамике дебиторской задолженности и превышениях лимита в разрезе договоров.\
                            Отчет построен на основе данных по счету ... в SAP S/4.",
                            style={"color": "#ffffff"},
                            className="row",
                        ),
                        html.P(
                            dcc.Markdown("\
                            На **" + get_max_date().strftime("%d.%m.%Y") +
                            "** размер дебиторской задолженности по данным SAP составляет XXXXXXX**"
                            #  + '{0:,}'.format(round(engine_cons.execute(
                            #      """SELECT round(sum("Сумма во внутренней валюте по дебе" -
                            #      "Сумма во внутренней валюте по кред")) AS "Сальдо"
                            #      FROM sap_s4.osv_94""").fetchone()[0]/1000)).replace(',', ' ') +
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
                        html.Output('Изменение дебиторской задолженности за период, тыс. руб.:'),
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
                style={"height":"5px"}
                ),

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
                        id="dashboard4-dropdown1",
                        options=[{'label': 'Все филиалы',
                            'value': 'Все филиалы'}],
                        value='Все филиалы',
                        clearable=False,
                        # style={"display": "flex",
                        #     "justify-content": "right"},
                        #multi=True,
                        className='two columns'
                    ),
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
                        id="dashboard4-dropdown2",
                        options=[
                            {'label': 'Входящее сальдо',
                            'value': 'Входящее сальдо'},
                            {'label': 'Оборот', 'value': 'Оборот'},
                            {'label': 'Исходящее сальдо',
                            'value': 'Исходящее сальдо'},
                        ],
                        value='Оборот',
                        clearable=False,
                        className='two columns',
                    ),
                ],
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

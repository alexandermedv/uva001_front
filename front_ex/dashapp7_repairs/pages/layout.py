""" Шаблоны для отчета по ремонтам."""
from datetime import date
import datetime
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# from . import engine_cons
from ..utils import get_max_date
from sqlalchemy import create_engine
import front_ex.config as config

#import dash_table
#import pandas as pd

#from flask_app import engine_analysis, engine_cons

def create_layout():
    """Создание шаблона"""
    # engine_cons = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    layout = html.Div([
        html.Div([
            # Row 1 - Описание отчета
            html.Div([
                html.Div(
                    [
                        html.H5("Отчет по ремонтам"),
                        html.Br([]),
                        html.P("\
                            Данный отчет содержит информацию о статистике выполненных плановых и внеплановых ремонтов ПС.\
                            Отчет построен на основе данных о ремонтах в SAP S4.",
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
                        id='dashboard7-date-picker-range',
                        min_date_allowed=date(2000, 1, 1),
                        max_date_allowed=date(2050, 1, 1),
                        initial_visible_month=date(2021, 4, 1),
                        start_date=date(2021, 1, 1),
                        end_date=date(2021, 9, 30),
                        # end_date=get_max_date().strftime("%m.%d.%Y"),
                        # end_date=datetime.datetime.now().strftime("%m.%d.%Y"),
                        number_of_months_shown = 3,
                        updatemode = 'singledate',
                        display_format='DD.MM.YYYY',
                        start_date_placeholder_text='Начало периода',
                        end_date_placeholder_text='Конец периода',
                    className='four columns'),

                    html.Div(
                        html.Output('Количество посреднических рейсов:'),
                    className='two columns',
                    style={"display": "flex",
                        "align-items": "center",
                        "height": "38px"
                            }),
                    html.Div(
                        html.B(
                            html.Output(id='resellers_amount'),
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

                    html.Div(
                        html.Output('Доля посреднических рейсов:'),
                    className='two columns',
                    style={"display": "flex",
                        "align-items": "center",
                        "height": "38px"
                            }),
                    html.Div(
                        html.B(
                            html.Output(id='resellers_share'),
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
                    
                    # html.Div(
                    #     html.Output('Всего рейсов за период:'),
                    # className='five columns',
                    # style={"display": "flex",
                    #     "align-items": "center",
                    #     "height": "38px"
                    #         }),
                    # html.Div(
                    #     html.B(
                    #         html.Output(id='transportations_count'),
                    #         ),
                    # className='two columns',
                    #             style={"border-style": "groove",
                    #                 "border-radius": "5px",
                    #                 "height": "38px",
                    #                 "display": "flex",
                    #                 "align-items": "center",
                    #                 "justify-content": "center"
                    #                 }
                    #         ),
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
                        className='one column',
                        style={"display": "flex",
                        "align-items": "center",
                        "height": "38px",
                        "justify-content": "center"
                            }
                            ),
                    dcc.Dropdown(
                        id="dashboard5-dropdown1",
                        value='Все филиалы',
                        clearable=False,
                        style={"display": "block",
                            "justify-content": "center"},
                        #multi=True,
                        className='four columns'),

                    html.Div(
                        html.Output('Группа грузов:'),
                        id = 'name2',
                        className='two columns',
                        style={"display": "flex",
                        "align-items": "center",
                        "justify-content": "center",
                        "height": "38px"
                            }
                            ),
                    dcc.Dropdown(
                            id="dashboard5-dropdown2",
                            value='Все грузы',
                            clearable=False,
                            style={"display": "block",
                                "justify-content": "center"},
                            className='two columns',
                                ),

                    html.Div(
                        html.Output('РПС:'),
                        id = 'name3',
                        className='two columns',
                        style={"display": "flex",
                        "align-items": "center",
                        "justify-content": "center",
                        "height": "38px"
                            }
                            ),
                    dcc.Dropdown(
                        id="dashboard5-dropdown3",
                        value='Все РПС',
                        clearable=False,
                        className='two columns',
                        style={"display": "block",
                            "justify-content": "center"}),

                    ],),

                ], className="row",
                ),

            # 3 ряд фильтров

            html.Div(
                html.Br(),
                style={"height":"5px"}),
            html.Div([
                dbc.Navbar([       
                    html.Div(
                        html.Output('Сортировка:'),
                        id = 'name4',
                        className='two columns',
                        style={"display": "flex",
                        "align-items": "center",
                        "justify-content": "left",
                        "height": "38px"
                            }
                    ),
                    dcc.Dropdown(
                        id="dashboard5-dropdown4",
                        options=[
                            {'label': 'Количество посред рейсов, шт.', 'value': 'Количество посреднических рейсов'},
                            {'label': 'Доля по количеству', 'value': 'Доля по количеству'},
                            {'label': 'Количество, шт.', 'value': 'Количество рейсов'},
                            {'label': 'Сумма посред рейсов, руб.', 'value': 'Сумма посреднических рейсов, руб.'},
                            {'label': 'Доля по сумме', 'value': 'Доля по сумме'},
                            {'label': 'Сумма, руб.', 'value': 'Сумма, руб.'},
                        ],
                        value='Количество посреднических рейсов',
                        clearable=False,
                        className='three columns',

                    )

                    ],),
                ], className="row",
                ),

            # Row 5 - Графики
            html.Div(id='graphs'),
        ], className="sub_page",
        ),
    ], className="page_landscape_a3",
    )

    return layout

""" Шаблоны для отчетов по запчастям."""
from datetime import date
import datetime
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
import dash_bootstrap_components as dbc
# from . import engine_cons
from ..utils import get_max_date, get_resellers_count
from sqlalchemy import create_engine
# import front_ex.config as config

#import dash_table
#import pandas as pd

#from flask_app import engine_analysis, engine_cons

def create_layout():
    """Создание шаблона"""
    # engine_cons = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
    layout = html.Div([
        html.Div([
            # Row 1 - Описание отчета
            html.Div([
                html.Div(
                    [
                        html.H5("Отчет по анализу грузовой базы на предмет наличия посредников"),
                        html.Br([]),
                        html.P("\
                            Отчет построен на основе данных о рейсах из SAP TM и данных о заказчиках из SAP S/4.\
                            Данные о связях между компаниями выгружены из внешнего источника Spark-interfax (демо-версия API).",
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
                        id='dashboard5-date-picker-range',
                        min_date_allowed=date(2000, 1, 1),
                        max_date_allowed=date(2050, 1, 1),
                        initial_visible_month=date(2021, 4, 1),
                        start_date=date(2022, 1, 1),
                        end_date=date(2022, 12, 31),
                        # end_date=get_max_date().strftime("%m.%d.%Y"),
                        # end_date=datetime.datetime.now().strftime("%m.%d.%Y"),
                        number_of_months_shown = 3,
                        updatemode = 'singledate',
                        display_format='DD.MM.YYYY',
                        start_date_placeholder_text='Начало периода',
                        end_date_placeholder_text='Конец периода',
                    className='four columns'),

                    html.Div(
                        html.Output('Кол-во посредн. рейсов:'),
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
                        html.Output('Доля посреднических рейсов, % (в шт.):'),
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
                    
                ],)
            ], className="row",
            ),

            # Row 3 - Второй ряд значений
            html.Div(
                html.Br(),
                style={"height":"5px"}),
            html.Div([
                dbc.Navbar([
                    html.Div(
                        html.Output('Кол-во клиентов-посредников'),
                        className='two columns',
                        style={"display": "flex",
                        "align-items": "center",
                        "height": "38px"
                            }
                            ),
                    html.Div(
                        html.B(
                            html.Output(id='resellers_count'),
                            ),
                    className='three columns',
                                style={"border-style": "groove",
                                    "border-radius": "5px",
                                    "height": "38px",
                                    "display": "flex",
                                    "align-items": "center",
                                    "justify-content": "center"
                                    }
                    ),

                    html.Div(
                        html.Output('Сумма посредн. рейсов, руб.'),
                    className='two columns',
                    style={"display": "flex",
                        "align-items": "center",
                        "height": "38px"
                            }),
                    html.Div(
                        html.B(
                            html.Output(id='resellers_amount_money'),
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
                        html.Output('Доля посреднических рейсов, % (в руб.)'),
                    className='two columns',
                    style={"display": "flex",
                        "align-items": "center",
                        "height": "38px"
                            }),
                    html.Div(
                        html.B(
                            html.Output(id='resellers_share_money'),
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

            # Row 4 - 2-й ряд фильтров
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
                        className='three columns'),

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


            # html.Div([
            #     html.Div([
            #         dcc.RadioItems(
            #             options=[
            #                 {'label': i, 'value': i}
            #                 for i in ['Месяц', 'Неделя', 'День']
            #             ],
            #             value="Месяц",
            #             id = 'ri-level',
            #             labelStyle={'display': 'inline-block',
            #                         "height": "20px"},
            #             # style={"display": "flex",
            #             #    "align-items": "center",
            #             #    "height": "20px"}
            #         ),
            #     ],
            #     className = 'three columns'
            #     ),
            #     html.Div([
            #         dcc.RadioItems(
            #             options=[
            #                 {'label': i, 'value': i}
            #                 for i in ['10', '20', '30']
            #             ],
            #             value="10",
            #             id = 'warehouse_quantity',
            #             labelStyle={'display': 'inline-block',
            #                         "height": "20px"},
            #             # style={"display": "flex",
            #             #    "align-items": "center",
            #             #    "height": "20px"}
            #         ),
            #     ],
            #     className = 'three columns'
            #     ),
            # ], className="row",
            # ),

            # Row 4 - Закладки

            html.Div([
                dcc.Tabs(id='dashboard5-tabs', value='tab-1', children=[
                    dcc.Tab(label='ТОП посредников', value='tab-1', className="tab",),
                    dcc.Tab(label='По филиалам', value='tab-2', className="tab",),
                    dcc.Tab(label='По РПС', value='tab-3', className="tab",),
                    dcc.Tab(label='По типам грузов', value='tab-4', className="tab",),
                    dcc.Tab(label='Динамика', value='tab-5', className="tab",),
                ], className="row all-tabs"),
                #html.Div(id='tabs-example-content')
            ]),

            # Row 5 - Содержимое закладки
            html.Div(id='tab-content'),
        ], className="sub_page",
        ),
    ], className="page_landscape_a3",
    )

    return layout

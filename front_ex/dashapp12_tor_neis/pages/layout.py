""" Шаблоны для отчета по ремонтам."""
from datetime import date
import datetime
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# from . import engine_cons

from ..utils import get_tors, get_tors_by_contr, get_tors_by_client, get_tors_count, get_tors_count_nk
from sqlalchemy import create_engine
# import front_ex.config as config

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
                        html.H5("Аналитика по некачественным ремонтам вагонов"),
                        html.Br([]),
                        html.P("\
                            Данный отчет содержит информацию о статистике выполненных некачественных ремонтов ПС.\
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
                        id='dashboard12-date-picker-range',
                        min_date_allowed=date(2000, 1, 1),
                        max_date_allowed=date(2050, 1, 1),
                        initial_visible_month=date(2022, 4, 1),
                        start_date=date(2019, 1, 1),
                        end_date=date(2023, 12, 31),
                        number_of_months_shown = 3,
                        updatemode = 'singledate',
                        display_format='DD.MM.YYYY',
                        start_date_placeholder_text='Начало периода',
                        end_date_placeholder_text='Конец периода',
                    className='four columns'),

                    html.Div(
                        html.Output('Количество ремонтов:'),
                        className='two columns',
                        style={"display": "flex",
                        "align-items": "center",
                        "height": "38px"
                            },
                            ),
                    html.Div(
                        html.B(
                            html.Output(id='tors_amount'),
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
                        html.Output('Количество некач. ремонтов:'),
                        className='two columns',
                        style={"display": "flex",
                        "align-items": "center",
                        "height": "38px"
                            },
                            ),
                    html.Div(
                        html.B(
                            html.Output(id='tors_amount_nk'),
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
            
 
           html.Div([
                dcc.Tabs(id='dashboard12-tabs', value='tab-1', children=[
                    dcc.Tab(label='Графики', value='tab-1', className="tab",),
                    #dcc.Tab(label='Справочник', value='tab-2', className="tab",),
                ], className="row all-tabs"),
                #html.Div(id='tabs-example-content')
            ]),

                # Row 5 - Графики
            html.Div(id='tab-content'),
        ], className="sub_page",
        ),
    ], className="page_landscape_a3",
    )

    return layout

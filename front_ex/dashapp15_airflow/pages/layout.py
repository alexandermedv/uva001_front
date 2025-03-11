""" Шаблоны для отчетов по запчастям."""
from datetime import date
import datetime as dt
import datetime
from weakref import ref
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
import dash_bootstrap_components as dbc

from sqlalchemy import create_engine

def create_layout():
    """Создание шаблона"""
    # engine_cons = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
    print(dt.datetime.now().replace(minute=0) - dt.timedelta(days=15))
    layout = html.Div([
        html.Div([
            # Row 2 - 1-й ряд фильтров
            html.Div(className="row", children=[
                dcc.DatePickerRange(
                    id='d15-date-picker-range',
                    # min_date_allowed= dt.datetime.now().date(),
                    # max_date_allowed=dt.datetime.now().date(),
                    # initial_visible_month=date(2021, 4, 1),
                    start_date=dt.datetime.now()  - dt.timedelta(days=15), 
                    # Последний день предыдущего месяца
                    end_date=dt.datetime.now(), 
                    # number_of_months_shown = 3,
                    # updatemode = 'singledate',
                    display_format='DD.MM.YYYY HH:00',
                    start_date_placeholder_text='Начало периода',
                    end_date_placeholder_text='Конец периода',
                    className='col-6',
                ),
            ]),
            html.Div([
                dcc.Tabs(id='dashboard15-tabs', value='tab-1', children=[
                    dcc.Tab(label='Airflow', value='tab-1', className="tab",),
                    dcc.Tab(label='База данных', value='tab-4', className="tab",),
                    dcc.Tab(label='Описание', value='tab-3', className="tab",),
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

""" Шаблоны для отчетов по запчастям."""
from datetime import date
import datetime as dt
import datetime
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# from . import engine_cons
# from ..utils import get_max_date, get_resellers_count
from sqlalchemy import create_engine
import front_ex.config as config


#from flask_app import engine_analysis, engine_cons
from ..utils import get_trans_empty_by_railway_penalty

def create_layout():
    """Создание шаблона"""
    # engine_cons = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    layout = html.Div([
        html.Div([
            # Row 1 - Описание отчета
            html.Div([
                html.Div(
                    [
                        html.H5("Отчет о нарушении срока доставки порожних вагонов ПАО ПГК"),
                        # html.Br([]),
                        html.P("\
                            Данный отчет содержит информацию о количестве порожних рейсов.\
                            Отчет построен на основе данных SAP TM по внутренним перевозкам." ,
                            style={"color": "#ffffff"},
                            className="row",
                        ),
                        html.Br(),
                        html.P("*Расчёт отклонения срока доставки производился без учета затрат времени на ТОР.",
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
                        style={"display": "flex", "align-items": "center", "height": "38px"}
                    ),
                    dcc.DatePickerRange(
                        id='dashboard8-date-picker-range',
                        min_date_allowed=date(2000, 1, 1),
                        max_date_allowed=date(2050, 1, 1),
                        initial_visible_month=date(2021, 4, 1),
                        start_date=date(2021, 1, 1),
                        # Последний день предыдущего месяца
                        end_date=(dt.date.today() - dt.timedelta(days=1)).replace(day=1) - dt.timedelta(days=1),
                        # end_date=get_max_date().strftime("%m.%d.%Y"),
                        # end_date=datetime.datetime.now().strftime("%m.%d.%Y"),
                        number_of_months_shown = 3,
                        updatemode = 'singledate',
                        display_format='DD.MM.YYYY',
                        start_date_placeholder_text='Начало периода',
                        end_date_placeholder_text='Конец периода',
                        className='four columns'
                    ),
                    html.Div(
                        html.Output('Дорога:'),
                        className='one column',
                        style={"display": "flex",  "align-items": "center", "height": "38px"},
                        id = 'name1',
                    ),
                    dcc.Dropdown(
                        id="dashboard8-dropdown1-in-railway",
                        value='',
                        clearable=False,
                        style={"display": "block",
                            "justify-content": "center"},
                        options=[{'label': i, 'value': i} for i in [''] + get_trans_empty_by_railway_penalty()['Дорога назначения'].unique().tolist()],
                        #multi=True,
                        className='three columns'),
                    html.Button('Выгрузить', id='download-report-button', n_clicks=0),
                    html.Output(id='link1', className='one column', hidden=True),
                    html.Output(id='download_callback', hidden=True)
                ])
            ], className="row",
            ),
            html.Div([
                dcc.Tabs(id='dashboard8-tabs', value='tab-1', children=[
                    dcc.Tab(label='Общие', value='tab-1', className="tab",),
                    dcc.Tab(label='По РПС', value='tab-4', className="tab",),
                    dcc.Tab(label='По дорогам назначения', value='tab-2', className="tab",),
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

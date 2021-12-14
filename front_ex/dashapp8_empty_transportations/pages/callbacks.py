""" Интерактивные элементы для отчетов по запчастям."""
import datetime as dt
import numpy as np
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import dash_table
import dash
import plotly.express as px
from dateutil import relativedelta

from ..pages import dash_app
# Первая закладка
from ..utils import get_trans_empty_by_type, get_trans_empty_by_money, get_trans_empty_by_type_month, get_trans_empty_by_money_month
# Вторая закладка
from ..utils import get_raiways, get_trans_empty_all, get_trans_empty_by_railway_delay, get_trans_empty_by_railway_mean_delay, get_trans_empty_by_railway_penalty
from ..utils import get_tab4_trans_empty_delay_by_rps, get_tab4_trans_empty_penalty_by_rps, get_tab4_trans_empty_mean_delay_by_rps
from ..utils import external_railway, get_tab1_trans_empty_by_delay_stat

# pie_colors = (px.colors.sequential.Burg + px.colors.sequential.amp )[::-1]
pie_colors = [ 
    # 'rgb(60, 9, 17)',
    #  'rgb(89, 13, 31)',
    'rgb(120, 14, 40)',
    'rgb(149, 19, 39)',
    'rgb(172, 44, 36)',
    'rgb(186, 74, 47)',
    'rgb(196, 102, 73)',
    'rgb(205, 129, 103)',
    'rgb(213, 156, 137)',
    'rgb(221, 182, 170)',
    'rgb(230, 209, 203)',
    #  'rgb(103, 32, 68)',
    #  'rgb(139, 48, 88)',
    #  'rgb(173, 70, 108)',
    'rgb(204, 96, 125)',
    'rgb(227, 129, 145)',
    'rgb(244, 163, 168)',
    'rgb(255, 198, 196)',
    'rgb(230, 209, 203)',
    'rgb(241, 236, 236)',]

def get_rps_name(rps):
    dict = {'ПВ':'Полувагоны', 
        'КР':'Крытые', 
        'ЦМВ':'Цементовозы', 
        'ПЛ':'Платформы', 
        'ЦС':'Цистерны', 
        'ФИТ':'Фитинговые пл.', 
        'ОКТ':'Окатышевозы', 
        'МВЗ':'Минераловозы', 
        'ПР':'Прочие'
    }
    rps_name = dict.get(rps)
    return rps_name

# Вычисление списка дорог
@dash_app.callback(
    Output(component_id='dashboard8-dropdown1-in-railway', component_property='options'),
    [Input('dashboard8-date-picker-range', 'start_date'),
     Input('dashboard8-date-picker-range', 'end_date'),
     Input('dashboard8-tabs', 'value')]
)
def update_dropdown1(start_date, end_date, tab):
    """Список значений по дорогам"""
    trans_empty_by_railway_penalty = get_trans_empty_by_railway_penalty()
    return [{'label': i, 'value': i} for i in [''] + trans_empty_by_railway_penalty['Дорога назначения'].unique().tolist()]

# Скрытие фильтра по дорогам по выбору закладки 
@dash_app.callback(Output('dashboard8-dropdown1-in-railway', 'style'), [Input('dashboard8-tabs', 'value'),])
def hide_graph(input):
    if (input !='tab-2') & (input != 'tab-3'):
        return {'display':'block'}
    else:
        return {'display':'none'}

# Скрытие фильтра по дорогам по выбору закладки 
@dash_app.callback(Output('name1', 'style'), [Input('dashboard8-tabs', 'value'),])
def hide_graph(input):
    if (input !='tab-2') & (input != 'tab-3'):
        return {'display':'block'}
    else:
        return {'display':'none'}

# Построение содержимого выбранной закладки
@dash_app.callback(Output('tab-content', 'children'),
                   [Input('dashboard8-tabs', 'value'),
                   Input('dashboard8-date-picker-range', 'start_date'),
                   Input('dashboard8-date-picker-range', 'end_date'),
                   Input('dashboard8-dropdown1-in-railway', 'value')
                   ])
def render_content(tab, start_date, end_date, railway):
    """Построение содержимого выбранной закладки"""

    # start_date = pd.to_datetime(start_date)
    # end_date = pd.to_datetime(end_date)
    
    if tab == 'tab-1':
        """Динамика"""
        # Закладка динамика
        trans_empty_by_type = get_trans_empty_by_type(railway=railway, start_date=start_date, end_date=end_date)
        trans_empty_by_money = get_trans_empty_by_money(railway=railway, start_date=start_date, end_date=end_date)
        trans_empty_by_type_month = get_trans_empty_by_type_month(railway=railway, start_date=start_date, end_date=end_date)
        trans_empty_by_money_month = get_trans_empty_by_money_month(railway=railway, start_date=start_date, end_date=end_date)
        tab1_trans_empty_by_delay_stat = get_tab1_trans_empty_by_delay_stat(railway=railway, start_date=start_date, end_date=end_date)
        
        content = html.Div([
            # Первая линия
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dash8-tab-1-pie1",
                        figure={
                            "data": [go.Pie(labels=trans_empty_by_type['Тип'],
                                values=trans_empty_by_type["Кол-во вагонорейсов"],
                                marker={"colors": ["#D3D3D3",  "#97151c", "#191970",]}, 
                                # hovertext=trans_empty_by_type["Кол-во вагонорейсов"].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                hoverinfo='skip',
                                hovertemplate = '%{label} - %{text}',
                                text = trans_empty_by_type["Кол-во вагонорейсов"].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                rotation = -5,
                                # textfont = dict(color = '#ffffff')
                            ),],
                            "layout": go.Layout(
                                autosize=True,
                                font = dict(size=12),
                                title_text='Общее кол-во порожних вагонорейсов, шт. <br> (плательщик, грузоотправитель, грузополучатель ПАО "ПКГ")',
                                margin={"r": 0, "t": 100, "b": 20, "l": 70, },
                            ),
                        },
                        # config={"displayModeBar": False},
                    ),
                ], className="six columns",
                ),
                html.Div([
                    dcc.Graph(
                        id="dash8-tab-1-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=trans_empty_by_type_month[(trans_empty_by_type_month['Тип'] == 'С просрочкой') & (trans_empty_by_type_month['Месяц'].apply(lambda x: x.year) == dt.date.today().year - 1)]["Месяц"].apply(lambda x: x.replace(x.year+1)).tolist(),
                                    y=trans_empty_by_type_month[(trans_empty_by_type_month['Тип'] == 'С просрочкой') & (trans_empty_by_type_month['Месяц'].apply(lambda x: x.year) == dt.date.today().year - 1)]["Кол-во вагонорейсов"].tolist(),
                                    text=trans_empty_by_type_month[(trans_empty_by_type_month['Тип'] == 'С просрочкой') & (trans_empty_by_type_month['Месяц'].apply(lambda x: x.year) == dt.date.today().year - 1)]["Кол-во вагонорейсов"]\
                                        .map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True).tolist(),
                                    textfont = dict(color = '#ffffff'),
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Кол-во вагонорейсов с просрочкой в прошлом году: %{text}""",
                                    name = dt.date.today().year - 1 ,

                                    orientation='v',
                                    textposition='auto',
                                    constraintext='outside',
                                    marker={
                                        "color": "#808080",
                                        # "line": {
                                        #     "color": "#97151c",
                                        #     "width": 2,
                                        # },
                                    },
                                ),
                                go.Bar(
                                    x=trans_empty_by_type_month[(trans_empty_by_type_month['Тип'] == 'С просрочкой') & (trans_empty_by_type_month['Месяц'].apply(lambda x: x.year) == dt.date.today().year)]["Месяц"].tolist(),
                                    y=trans_empty_by_type_month[(trans_empty_by_type_month['Тип'] == 'С просрочкой') & (trans_empty_by_type_month['Месяц'].apply(lambda x: x.year) == dt.date.today().year)]["Кол-во вагонорейсов"].tolist(),
                                    text=trans_empty_by_type_month[(trans_empty_by_type_month['Тип'] == 'С просрочкой') & (trans_empty_by_type_month['Месяц'].apply(lambda x: x.year) == dt.date.today().year)]["Кол-во вагонорейсов"]\
                                        .map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True).tolist(),
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Кол-во вагонорейсов с просрочкой: %{text}""",
                                    name = dt.date.today().year,

                                    orientation='v',
                                    textposition='auto',
                                    constraintext='outside',

                                    marker={
                                        "color": "#97151c",
                                        "line": {
                                            "color": "#97151c",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                # barmode = 'stack', 
                                barmode = 'group',
                                title_text='Кол-во порожних вагонорейсов с просрочкой помесячно, ваг.',
                                margin={"r": 0, "t": 50, "b": 20, "l": 70, },
                            ),
                        },
                        config={"displayModeBar": False},
                    ),
                ], className="six columns",
                ),            
            ], className="row"),
            # Вторая линия
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dash8-tab1-pie2",
                        figure={
                            "data": [go.Pie(labels=trans_empty_by_money['Тип'], 
                            values=trans_empty_by_money['Рассчитанная сумма'].apply(lambda x: int(x/1000)), 
                             marker={"colors": ["#808080","#97151c", "#D3D3D3",]},
                            #  темно-синий "#191970",
                             hoverinfo='skip',
                             hovertemplate = '%{label} - %{text}',
                             text = trans_empty_by_money['Рассчитанная сумма'].apply(lambda x: int(x/1000)).map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                             textfont = dict(color = '#ffffff'),
                             )],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Сумма пени, исходя <br> из рассчитанной суммы тарифа в SAP, тыс. руб.',
                                margin={
                                    "r": 0, "t": 100, "b": 20, "l": 70,
                                },
                            ),
                        },
                        # config={"displayModeBar": False},
                    ),
                ], className="six columns",
                ),
                html.Div([
                    dcc.Graph(
                        id="dash8-tab1-graph2",
                        figure={
                            "data": [
                                go.Scatter(
                                    x=trans_empty_by_money_month[trans_empty_by_money_month['Месяц'].apply(lambda x: x.year) == dt.date.today().year]["Месяц"].tolist(),
                                    y=trans_empty_by_money_month[trans_empty_by_money_month['Месяц'].apply(lambda x: x.year) == dt.date.today().year]["Оценка пени"].apply(lambda x: int(x/1000)).tolist(),
                                    text=trans_empty_by_money_month[trans_empty_by_money_month['Месяц'].apply(lambda x: x.year) == dt.date.today().year]["Оценка пени"].apply(lambda x: int(x/1000))\
                                        .map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True).tolist(),
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Оценка пени: %{text} тыс. руб.""",
                                    name=dt.date.today().year,
            
                                    # orientation='v',
                                    # textposition='auto',
                                    marker={
                                        "color": "#97151c",
                                        "line": {
                                            "color": "#97151c",
                                            "width": 2,
                                        },
                                    },
                                ),
                                go.Scatter(
                                    x=trans_empty_by_money_month[trans_empty_by_money_month['Месяц'].apply(lambda x: x.year) == dt.date.today().year - 1]["Месяц"].apply(lambda x: x.replace(x.year+1)).tolist(),
                                    y=trans_empty_by_money_month[trans_empty_by_money_month['Месяц'].apply(lambda x: x.year) == dt.date.today().year - 1]["Оценка пени"].apply(lambda x: int(x/1000)).tolist(),
                                    text=trans_empty_by_money_month[trans_empty_by_money_month['Месяц'].apply(lambda x: x.year) == dt.date.today().year - 1]["Оценка пени"].apply(lambda x: int(x/1000))\
                                        .map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True).tolist(),
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Оценка пени: %{text} тыс. руб.""",
                                    name=dt.date.today().year - 1,
            
                                    # orientation='v',
                                    # textposition='auto',
                                    marker={
                                        "color": "#D3D3D3",
                                        "line": {
                                            "color": "#97151c",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                barmode = 'stack', 
                                title_text='Динамика пени за просрочку <br> (оценкa без учета времени простоя в ТОР), тыс. руб.',
                                # Рассчет при условии 6% от рассчитанной суммы тарифа, но не более 50%
                                # margin={"r": 0, "t": 50, "b": 20, "l": 70, },
                                annotations = [dict(showarrow=False, text='test', font=dict(size=10),  x=0.5,  y=-0.5, xref='paper', yref='paper', xshift=-1
                                , yshift=-5, align="left")]
                            ),
                        },
                        config={"displayModeBar": False},
                    ),
                ], className="six columns",
                ),
            ], className="row"),
            html.Div([
                html.Div([
                    html.P("За несоблюдение сроков доставки грузов перевозчик уплачивает пени в соответствии со ст. 97 Устава ЖТД РФ. Размер пени за каждые сутки просрочки составит 6% платы за перевозку, а максимальный размер ответственности – 50%, если перевозчик не докажет, что груз пришёл с опозданием не по его вине.",
                            # style={"color": "#ffffff"},
                            style={"fontSize": "12px"},
                            className="row",
                    ),
                ], className='six columns'),
                html.Div([
                    html.P('')
                ], className='six columns'),
            ], className="row"),

            # Статистика по просрочке
            # html.Div([
            #     html.Div([
            #         dcc.Graph(
            #             id="dash8-tab-1-pie3",
            #             figure={
            #                 "data": [go.Pie(labels=tab1_trans_empty_by_delay_stat['Дней просрочки, суток'], 
            #                     values=tab1_trans_empty_by_delay_stat["Кол-во вагонорейсов"],
            #                     marker={"colors": px.colors.qualitative.Set3}, 
            #                     # hovertext=trans_empty_by_type["Кол-во вагонорейсов"].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
            #                     hoverinfo='skip',
            #                     hovertemplate = '%{label} - %{text}',
            #                     text = tab1_trans_empty_by_delay_stat["Кол-во вагонорейсов"].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
            #                     # textfont = dict(color = '#ffffff')
            #                 ),],
            #                 "layout": go.Layout(
            #                     autosize=True,
            #                     font = dict(size=12),
            #                     title_text='Статистика по дням просрочки, суток',
            #                     margin={"r": 0, "t": 100, "b": 20, "l": 70, },
            #                 ),
            #             },
            #             # config={"displayModeBar": False},
            #         ),
            #     ], className="six columns",
            #     ),           
            # ], className="row")
        ])
        return content
    elif tab == 'tab-2':
        """По дорогам"""
        trans_empty_by_railway_delay = get_trans_empty_by_railway_delay(start_date=start_date, end_date=end_date)
        trans_empty_by_railway_penalty = get_trans_empty_by_railway_penalty(start_date=start_date, end_date=end_date)
        trans_empty_by_railway_mean_delay = get_trans_empty_by_railway_mean_delay(start_date=start_date, end_date=end_date)
        
        # Tab-2 pie content вагонорейсы
        internal_delay = trans_empty_by_railway_delay
        internal_delay['Вагонорейсы с просрочкой, %'] = internal_delay['Кол-во вагонорейсов с просрочкой']/internal_delay['Кол-во вагонорейсов с просрочкой'].sum()
        
        # Tab-2 pie content рубли
        internal_penalty = trans_empty_by_railway_penalty
        # internal_penalty['Оценка пени, %'] = internal_penalty['Оценка пени']/internal_penalty['Оценка пени'].sum()

        content = html.Div([
            html.Div([ 
                html.Div([
                    dcc.Graph(
                        id="dashboard8-pie1",
                        figure={
                            "data": [go.Pie(labels=internal_penalty['Дорога назначения'], 
                                # values=internal_delay['Вагонорейсы с просрочкой, %'],
                                values=internal_delay['Кол-во вагонорейсов с просрочкой'],
                                # marker=dict(colors=pie_colors),
                                marker=dict(colors=px.colors.qualitative.Antique),                                
                                text = internal_delay['Кол-во вагонорейсов с просрочкой'].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                rotation = 90,
                                hoverinfo='skip',
                                hovertemplate = '%{label} - %{text}',
                                name='',
                            )],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Структура по вагонорейсам с просрочкой, шт.',
                                margin={"r": 0, "t": 50, "b": 20, "l": 70, },
                            ),
                        },
                        # config={"displayModeBar": False},
                    ),
                ], className="six columns",
                ),
                html.Div([
                    dcc.Graph(
                        id="dashboard8-pie2",
                        figure={
                            "data": [go.Pie(labels=internal_penalty['Дорога назначения'], 
                                values=internal_penalty['Оценка пени'].apply(lambda x: int(x/1000)),
                                text = internal_penalty['Оценка пени'].apply(lambda x: int(x/1000)).map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                # marker=dict(colors=pie_colors),
                                marker=dict(colors=px.colors.qualitative.Antique), 
                                hoverinfo='skip',
                                hovertemplate = '%{label} - %{text}',
                                rotation = 90,
                            )],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Структура по оценке пени, тыс. руб.',
                                margin={"r": 0, "t": 50, "b": 20, "l": 70, },
                            ),
                        },
                        # config={"displayModeBar": False},
                    ),
                ], className="six columns",
                ),
            
            ], className="row"),
            
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dash8-2-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=internal_delay["Кол-во вагонорейсов с просрочкой"].tolist(),
                                    y=internal_delay["Дор. назн."].tolist(),
                                    text=internal_delay["Кол-во вагонорейсов с просрочкой"].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True).tolist(),
                                    hoverinfo='skip',
                                    customdata = internal_delay['Дорога назначения'].tolist(),
                                    hovertemplate= """Дорога: %{customdata} <br> Кол-во вагонорейсов с просрочкой: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    constraintext='outside',
                                    marker={
                                        "color": "rgb(175, 100, 88)",
                                        # "color": "#B4B4B4",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                yaxis={"autorange":"reversed"},
                                autosize=True,
                                title_text='Кол-во вагонорейсов с просрочкой, шт.',
                                margin={"r": 0, "t": 50, "b": 20, "l": 70, },
                            ),
                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns",
                ),
            
                html.Div([
                    dcc.Graph(
                        id="dash8-2-graph2",
                        figure={
                            "data": [
                                go.Bar(
                                    x=internal_penalty["Оценка пени"].apply(lambda x: int(x/1000)).tolist(),
                                    y=internal_penalty["Дор. назн."].tolist(),
                                    text=internal_penalty["Оценка пени"].apply(lambda x: int(x/1000)).map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True).tolist(),
                                    customdata=internal_penalty["Дорога назначения"].tolist(),
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Дорога: %{customdata} <br> Оценка пени: %{text} тыс. руб.""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    constraintext='outside',
                                    marker={
                                        "color": "rgb(175, 100, 88)",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                yaxis={"autorange":"reversed"},
                                title_text='Оценка пени, тыс. руб.',
                                margin={"r": 0, "t": 50, "b": 20, "l": 70, },
                            ),
                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns",
                ),
            
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph3",
                        figure={
                            "data": [
                                go.Bar(
                                    x=trans_empty_by_railway_mean_delay["Средняя просрочка, сут"],
                                    y=trans_empty_by_railway_mean_delay["Дор. назн."],
                                    text=trans_empty_by_railway_mean_delay["Средняя просрочка, сут"].map('{:,.1f}'.format).astype(str).replace(',', ' ', regex=True).astype(str),
                                    hoverinfo='skip',
                                    customdata=trans_empty_by_railway_mean_delay["Дорога назначения"],
                                    hovertemplate=
                                    """Дорога: %{customdata} <br> Средняя просрочка: %{text} суток""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    constraintext='outside',
                                    marker={
                                        "color": "rgb(175, 100, 88)",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Средняя просрочка, сут.',
                                margin={
                                    "r": 0, "t": 50, "b": 20, "l": 70,
                                },
                            ),
                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns",
                ),
             ], className="row"),
        ])
        return content
    elif tab == 'tab-3':
        content = html.Div([
            html.Div([html.P('')], className = 'row'),
            html.Div([
                html.P("Оборот вагонов зависит от скорости продвижения вагонов, выгрузки и погрузки."),
                html.P("Перевозчики обязаны доставлять грузы по назначению и в установленные сроки согласно ст. 33 Устав ЖДТ РФ. Вагон считается доставленным в срок, если до истечения указанного в транспортной железнодорожной накладной срока доставки (с учетом корректировки в соответствии с правилами исчисления сроков доставки грузов, порожних грузовых вагонов железнодорожным транспортом) перевозчик обеспечил подачу на пути под ГО."), 
                html.Br(),
                html.P("Данные из выгрузки вагонорейсов и дашборда могут использоваться:"),
                # html.Br(),
                html.P("    - в качестве понимания количества порожних вагонов с нарушением срока доставки и контроля за объемом пени, подлежащих выставлению."),
                # html.Br(),
                html.P("    - как рычаг воздействия на перевозчика, т.е. в целях получения преференций от перевозчика (РЖД) для повышения эффективности вагонного парка, при условии не выставление ему пени."),
            ], className="row")
        ],)
        return content
    elif tab == 'tab-4':
        """По РПС"""
        trans_empty_by_railway_delay = get_tab4_trans_empty_delay_by_rps(railway=railway, start_date=start_date, end_date=end_date)
        trans_empty_by_railway_penalty = get_tab4_trans_empty_penalty_by_rps(railway=railway, start_date=start_date, end_date=end_date)
        trans_empty_by_railway_mean_delay = get_tab4_trans_empty_mean_delay_by_rps(railway=railway, start_date=start_date, end_date=end_date)
        
        # Tab-2 pie content вагонорейсы
        internal_delay = trans_empty_by_railway_delay

        # Tab-2 pie content рубли
        internal_penalty = trans_empty_by_railway_penalty

        content = html.Div([
            html.Div([ 
                html.Div([
                    dcc.Graph(
                        id="dashboard8-pie1",
                        figure={
                            "data": [go.Pie(labels=internal_delay['РПС'], 
                                values=internal_delay['Кол-во вагонорейсов с просрочкой'],
                                # marker=dict(colors=pie_colors),
                                text = internal_delay['Кол-во вагонорейсов с просрочкой'].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                marker=dict(colors=px.colors.qualitative.Antique), 
                                hoverinfo='skip',
                                customdata=internal_penalty['РПС'].apply(lambda x: get_rps_name(x)),
                                hovertemplate = 'РПС: %{customdata} <br> %{label} - %{text}',
                                name='',
                                rotation=90,
                            )],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Структура по вагонорейсам с просрочкой, шт.',
                                margin={"r": 0, "t": 50, "b": 20, "l": 70, },
                            ),
                        },
                        # config={"displayModeBar": False},
                    ),
                ], className="six columns",
                ),
                html.Div([
                    dcc.Graph(
                        id="dashboard8-pie2",
                        figure={
                            "data": [go.Pie(labels=internal_penalty['РПС'], 
                                values=internal_penalty['Оценка пени'].apply(lambda x: int(x/1000)),
                                # marker=dict(colors=pie_colors),
                                marker=dict(colors=px.colors.qualitative.Antique), 
                                text = internal_penalty['Оценка пени'].apply(lambda x: int(x/1000)).map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                hoverinfo='skip',
                                customdata=internal_penalty['РПС'].apply(lambda x: get_rps_name(x)),
                                hovertemplate = 'РПС: %{customdata} <br> %{label} - %{text}',
                                name='',
                                rotation=90,
                            )],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Структура по оценке пени, тыс. руб.',
                                margin={"r": 0, "t": 50, "b": 20, "l": 70, },
                            ),
                        },
                        # config={"displayModeBar": False},
                    ),
                ], className="six columns",
                ),
            
            ], className="row"),
            
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dash8-2-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=internal_delay["Кол-во вагонорейсов с просрочкой"].tolist(),
                                    y=internal_delay["РПС"].tolist(),
                                    text=internal_delay["Кол-во вагонорейсов с просрочкой"].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True).tolist(),
                                    hoverinfo='skip',
                                    customdata=internal_delay['РПС'].apply(lambda x: get_rps_name(x)),
                                    hovertemplate=
                                    """РПС: %{customdata} <br> Кол-во вагонорейсов с просрочкой: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "rgb(175, 100, 88)",
                                        # "color": "#B4B4B4",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                yaxis={"autorange":"reversed"},
                                autosize=True,
                                title_text='Кол-во вагонорейсов с просрочкой, шт.',
                                margin={"r": 0, "t": 50, "b": 20, "l": 70, },
                            ),
                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns",
                ),
            
                html.Div([
                    dcc.Graph(
                        id="dash8-2-graph2",
                        figure={
                            "data": [
                                go.Bar(
                                    x=internal_penalty["Оценка пени"].apply(lambda x: int(x/1000)).tolist(),
                                    y=internal_penalty["РПС"].tolist(),
                                    text=internal_penalty["Оценка пени"].apply(lambda x: int(x/1000)).map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True).tolist(),
                                    hoverinfo='skip',
                                    customdata=internal_penalty['РПС'].apply(lambda x: get_rps_name(x)),
                                    hovertemplate=
                                    """РПС: %{customdata} <br> Оценка пени: %{text} тыс. руб.""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "rgb(175, 100, 88)",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                yaxis={"autorange":"reversed"},
                                title_text='Оценка пени, тыс. руб.',
                                margin={"r": 0, "t": 50, "b": 20, "l": 70, },
                            ),
                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns",
                ),
            
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph3",
                        figure={
                            "data": [
                                go.Bar(
                                    x=trans_empty_by_railway_mean_delay["Средняя просрочка, сут"],
                                    y=trans_empty_by_railway_mean_delay["РПС"],
                                    text=trans_empty_by_railway_mean_delay["Средняя просрочка, сут"].map('{:,.1f}'.format).astype(str).replace(',', ' ', regex=True).astype(str),
                                    hoverinfo='skip',
                                    customdata=trans_empty_by_railway_mean_delay['РПС'].apply(lambda x: get_rps_name(x)),
                                    hovertemplate=
                                    """РПС: %{customdata} <br> Средняя просрочка: %{text} суток""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "rgb(175, 100, 88)",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Средняя просрочка, сут.',
                                margin={
                                    "r": 0, "t": 50, "b": 20, "l": 70,
                                },
                            ),
                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns",
                ),
             ], className="row"),
        ])
        return content
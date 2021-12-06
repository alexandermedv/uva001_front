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

from ..pages import dash_app
# Первая закладка
from ..utils import get_trans_empty_by_type, get_trans_empty_by_money, get_trans_empty_by_type_month, get_trans_empty_by_money_month
# Вторая закладка
from ..utils import get_raiways, get_trans_empty_all, get_trans_empty_by_railway_delay, get_trans_empty_by_railway_mean_delay, get_trans_empty_by_railway_penalty
from ..utils import external_railway

# Вычисление списка дорог
@dash_app.callback(
    Output(component_id='dashboard8-dropdown1-in-railway', component_property='options'),
    [Input('dashboard5-date-picker-range', 'start_date'),
     Input('dashboard5-date-picker-range', 'end_date'),
    #  Input('dashboard5-dropdown1', 'value'),
    # Input('dashboard5-dropdown2', 'value'),
    #  Input('dashboard5-dropdown3', 'value'),
     Input('dashboard5-tabs', 'value')]
)
def update_dropdown1(start_date, end_date, tab):
    """Список значений по дорогам"""
    trans_empty_by_railway_penalty = get_trans_empty_by_railway_penalty()
    # print({'label': i, 'value': i} for i in [''] + trans_empty_by_railway_penalty['Дорога назначения'].unique().tolist())
    return [{'label': i, 'value': i} for i in [''] + trans_empty_by_railway_penalty['Дорога назначения'].unique().tolist()]

# Скрытие фильтра по дорогам по выбору закладки 
@dash_app.callback(Output('dashboard8-dropdown1-in-railway', 'style'), [Input('dashboard8-tabs', 'value'),])
def hide_graph(input):
    if input != 'tab-2':
        return {'display':'block'}
    else:
        return {'display':'none'}

# Скрытие фильтра по дорогам по выбору закладки 
@dash_app.callback(Output('name1', 'style'), [Input('dashboard8-tabs', 'value'),])
def hide_graph(input):
    if input != 'tab-2':
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
        
        content = html.Div([
            # Первая линия
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dash8-tab-1-pie1",
                        figure={
                            "data": [go.Pie(labels=trans_empty_by_type['Тип'], values=trans_empty_by_type["Кол-во вагонорейсов"],
                                marker={"colors": ["#D3D3D3",  "#97151c", "#191970",]}, 
                                # hovertext=trans_empty_by_type["Кол-во вагонорейсов"].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                hoverinfo='skip',
                                hovertemplate = '%{label} - %{text}',
                                text = trans_empty_by_type["Кол-во вагонорейсов"].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True)
                            ),],
                            "layout": go.Layout(
                                autosize=True,
                                font = dict(size=12),
                                title_text='Кол-во порожних вагонорейсов, шт. <br> (плательщик, грузоотправитель, грузополучатель ПАО "ПКГ")',
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
                                    x=trans_empty_by_type_month[trans_empty_by_type_month['Тип'] == 'Без просрочки']["Месяц"].tolist(),
                                    y=trans_empty_by_type_month[trans_empty_by_type_month['Тип'] == 'Без просрочки']["Кол-во вагонорейсов"].tolist(),
                                    text=trans_empty_by_type_month[trans_empty_by_type_month['Тип'] == 'Без просрочки']["Кол-во вагонорейсов"]\
                                        .map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True).tolist(),
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Кол-во вагонорейсов с просрочкой: %{text}""",
                                    name = 'Без просрочки',
                                    # trans_empty_by_type_month['Тип'],
                                    orientation='v',
                                    textposition='auto',
                                    marker={
                                        "color": "#D3D3D3",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                                go.Bar(
                                    x=trans_empty_by_type_month[trans_empty_by_type_month['Тип'] == 'С просрочкой']["Месяц"].tolist(),
                                    y=trans_empty_by_type_month[trans_empty_by_type_month['Тип'] == 'С просрочкой']["Кол-во вагонорейсов"].tolist(),
                                    text=trans_empty_by_type_month[trans_empty_by_type_month['Тип'] == 'С просрочкой']["Кол-во вагонорейсов"]\
                                        .map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True).tolist(),
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Кол-во вагонорейсов без просрочки: %{text}""",
                                    name = 'С просрочкой',
                                    # trans_empty_by_type_month['Тип'],
                                    orientation='v',
                                    textposition='auto',
                                    marker={
                                        "color" : "#97151c",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                barmode = 'stack', 
                                title_text='Кол-во порожних вагонорейсов помесячно, ваг.',
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
                            "data": [go.Pie(labels=trans_empty_by_money['Тип'], values=trans_empty_by_money['Рассчитанная сумма'], 
                             marker={"colors": ["#97151c", "#808080", "#D3D3D3", ]},
                            #  темно-синий "#191970",
                             hoverinfo='skip',
                             hovertemplate = '%{label} - %{text}',
                             text = trans_empty_by_money['Рассчитанная сумма'].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True)
                             )],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Сумма пени, исходя из рассчитанной суммы тарифа в SAP, руб.',
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
                                    x=trans_empty_by_money_month["Месяц"].tolist(),
                                    y=trans_empty_by_money_month["Оценка пени"].tolist(),
                                    text=trans_empty_by_money_month["Оценка пени"]\
                                        .map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True).tolist(),
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Оценка пени: %{text}""",
                                    name='Без просрочки',
            
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
                                title_text='Динамика пени за просрочку <br> (оценкa без учета времени простоя в ТОР), руб.',
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
        ])
        return content
    elif tab == 'tab-2':
        """По дорогам"""
        trans_empty_by_railway_delay = get_trans_empty_by_railway_delay()
        trans_empty_by_railway_penalty = get_trans_empty_by_railway_penalty()
        trans_empty_by_railway_mean_delay = get_trans_empty_by_railway_mean_delay()
        
        # Tab-2 pie content вагонорейсы
        internal_delay = trans_empty_by_railway_delay
        internal_delay['Вагонорейсы с просрочкой, %'] = internal_delay['Кол-во вагонорейсов с просрочкой']/internal_delay['Кол-во вагонорейсов с просрочкой'].sum()
        
        # Убрать экспорт-импортные дороги
        #[~trans_empty_by_railway_delay['Дорога назначения'].isin(external_railway)].copy()

        # Tab-2 pie content рубли
        internal_penalty = trans_empty_by_railway_penalty[~trans_empty_by_railway_penalty['Дорога назначения'].isin(external_railway)].copy()
        internal_penalty['Оценка пени, %'] = internal_penalty['Оценка пени']/internal_penalty['Оценка пени'].sum()

        content = html.Div([
            html.Div([ 
                html.Div([
                    dcc.Graph(
                        id="dashboard8-pie1",
                        figure={
                            "data": [go.Pie(labels=internal_penalty['Дорога назначения'], 
                                values=internal_delay['Вагонорейсы с просрочкой, %'],
                                marker=dict(colors=px.colors.sequential.amp + px.colors.sequential.Burg),
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
                            "data": [go.Pie(labels=internal_penalty['Дорога назначения'], values=internal_penalty['Оценка пени, %'],
                                marker=dict(colors=px.colors.sequential.amp + px.colors.sequential.Burg),
                            )],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Структура по оценке пени, руб.',
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
                                    hovertemplate=
                                    """Кол-во вагонорейсов с просрочкой: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#97151c",
                                        # "color": "#B4B4B4",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
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
                                    x=internal_penalty["Оценка пени"].tolist(),
                                    y=internal_penalty["Дор. назн."].tolist(),
                                    text=internal_penalty["Оценка пени"].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True).tolist(),
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Оценка пени: %{text} руб.""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#97151c",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Оценка пени, руб.',
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
                                    hovertemplate=
                                    """Средняя просрочка: %{text} суток""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#97151c",
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
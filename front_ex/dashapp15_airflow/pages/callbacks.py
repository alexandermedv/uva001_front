""" Интерактивные элементы для отчетов по запчастям."""
import datetime as dt
import os
import numpy as np
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import dash_table
import plotly.express as px
from dateutil import relativedelta
from pprint import pprint
import dash_table.FormatTemplate as FormatTemplate

# from dash import dash_table


import requests

from ..pages import dash_app
# Первая закладка
from ..utils import dag_load_daily

from ..utils import get_trans_empty_by_type, get_trans_empty_by_money, get_trans_empty_by_type_month, get_trans_empty_by_money_month
# Вторая закладка
from ..utils import get_raiways, get_trans_empty_all, get_trans_empty_by_railway_delay, get_trans_empty_by_railway_mean_delay, get_trans_empty_by_railway_penalty
from ..utils import get_tab4_trans_empty_delay_by_rps, get_tab4_trans_empty_penalty_by_rps, get_tab4_trans_empty_mean_delay_by_rps
from ..utils import external_railway, get_tab1_trans_empty_by_delay_stat

def dag_load_daily_bars():
    bars = []
    dags_load_hours_by_day = dag_load_daily()
                                                             
    for dag_id in dags_load_hours_by_day[dags_load_hours_by_day['date'] >= dt.datetime.strptime('2023-10-01', '%Y-%m-%d').date()]['dag_id'].unique():
        # print(dag_id, flush=True)

        bars.append(go.Bar(x=dags_load_hours_by_day[(dags_load_hours_by_day['date'] >= dt.datetime.strptime('2023-10-01', '%Y-%m-%d').date()) 
                                              & (dags_load_hours_by_day['dag_id']==dag_id)]['date'],
            y=dags_load_hours_by_day[(dags_load_hours_by_day['date'] >= dt.datetime.strptime('2023-10-01', '%Y-%m-%d').date()) 
                                              & (dags_load_hours_by_day['dag_id']==dag_id)]['duration_hours'],
            text = dag_id,
            # hovertemplate=
            #     """Кол-во вагонорейсов с просрочкой в прошлом году: %{text}""",
            # name = dt.date.today().year - 1 ,
            name = dag_id,
        ),)
    return bars

def data_bars(df, column):
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [
        ((df[column].max() - df[column].min()) * i) + df[column].min()
        for i in bounds
    ]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        styles.append({
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'background': (
                """
                    linear-gradient(90deg,
                    rgb(174,202,197) 0%,
                    rgb(174,202,197) {max_bound_percentage}%,
                    white {max_bound_percentage}%,
                    white 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
                    #0074D9 0%,
                    #0074D9 {max_bound_percentage}%,
            'paddingBottom': 2,
            'paddingTop': 2
        })

    return styles

pie_colors_failed = [ 
    'rgb(172, 59, 70)',
    'rgb(101,102,105)',
   ]


# Построение содержимого выбранной закладки
@dash_app.callback(Output('tab-content', 'children'),
                   [Input('dashboard15-tabs', 'value'),
                   Input('d15-date-picker-range', 'start_date'),
                   Input('d15-date-picker-range', 'end_date'),
                #    Input('dashboard8-dropdown1-in-railway', 'value')
                   ])
def render_content(tab, start_date, end_date):
    """Построение содержимого выбранной закладки"""

    # start_date = pd.to_datetime(start_date)
    # end_date = pd.to_datetime(end_date)
    
    if tab == 'tab-1':
        """Общие"""
        # Закладка общие
        dags_load_hours_by_day = dag_load_daily()
        dash4_cols=['dag_id','owners','duration_hours']
        # print(dags_load_hours_by_day[(dags_load_hours_by_day['date'] == dt.datetime.strptime('2023-10-11', '%Y-%m-%d').date())
        #                         & (dags_load_hours_by_day['state']=='failed')][['dag_id', 'owners', 'duration_hours']])

        content = html.Div([
            # Первая линия
            html.Div(className="row", children=[
                html.Div(className="col-4", children=[
                    dcc.Graph(
                        id="dash15-tab-1-pie1",
                        figure={
                            "data": [
                                go.Pie(
                                    values=dags_load_hours_by_day[(dags_load_hours_by_day['date'] == dt.datetime.strptime('2023-10-11', '%Y-%m-%d').date())]
                                       .groupby('state').agg(state_cnt=('dag_id', lambda x: x.nunique()))['state_cnt'],        
                                    textinfo='label+value+percent', 
                                    hole=.6,
                                    labels=dags_load_hours_by_day[(dags_load_hours_by_day['date'] == dt.datetime.strptime('2023-10-11', '%Y-%m-%d').date())]
                                       .groupby('state').agg(state_cnt=('dag_id', lambda x: x.nunique())).reset_index()['state'],
                                    marker=dict(colors=pie_colors_failed),
                            ),],
                            "layout": go.Layout(
                                autosize=True,
                                annotations=[dict(text='<b>Всего: {}</b>'
                                                    .format(len(dags_load_hours_by_day[(dags_load_hours_by_day['date'] == dt.datetime.strptime('2023-10-11', '%Y-%m-%d').date())]['dag_id'].unique())), 
                                                    x=0.5, y=0.5, font_size=18, showarrow=False)],
                                font = dict(size=11),
                                title_text='Статистика исполнения задач на вчера',
                                hovermode=False,
                                # margin={"r": 0, "t": 100, "b": 20, "l": 70, },
                                # legend=dict(orientation="h", yanchor="top", y=1.02, xanchor="right", x=0)
                            ),
                        },
                        # config={"displayModeBar": False},
                    ),
                ]),
                html.Div(className="col-8", children=[
                    dcc.Graph(
                        id="dash15-tab-1-graph1",
                        figure={
                            "data": 
                                dag_load_daily_bars(),
                            # dag_load_daily_bars(),
                            "layout": go.Layout(
                                autosize=True,
                                barmode = 'stack', 
                                # barmode = 'group',
                                title_text='Подневная загрузка - общий объем исполнения задач в часах',
                                # margin={"r": 0, "t": 50, "b": 20, "l": 70, },
                                # legend=dict(orientation="h"), 
                                hovermode = 'closest',
                            ),
                        },
                        config={"displayModeBar": False},
                    ),
                ]),            
            ]),

            # Вторая линия -------------------------------------------------------------------------------------------
            # Невыполненные на вчера задачи
            html.Div(className="row", children=[
                html.Div(className="col-4", children=[
                    dash_table.DataTable(
                        id = "dash_15_data_failed",
                        columns =  [
                            {"name": 'dag_id', "id": 'dag_id'},
                            {"name": 'owners', "id": 'owners'},
                            {"name": 'duration_hours', "id": 'duration_hours', 'type': 'numeric', 'format': dict(specifier='.2f')},                                                  
                        ],
                        data=dags_load_hours_by_day[(dags_load_hours_by_day['date'] == dt.datetime.strptime('2023-10-11', '%Y-%m-%d').date())
                                & (dags_load_hours_by_day['state']=='failed')][['dag_id', 'owners', 'duration_hours']].to_dict('records'),
                        editable=False,
                        sort_action='native',
                        filter_action='native',
                        style_cell={'textAlign': 'left', 'fontSize':12, 'font-family':'verdana'},
                        style_as_list_view=True,

                #         # title_text='Невыполненные на вчера задачи',
                    )
                ]),
                html.Div(className="col-4", children=[
                    dash_table.DataTable(
                        id = "dash_15_datatable",
                        columns =  [
                            {"name": 'dag_id', "id": 'dag_id'},
                            {"name": 'owners', "id": 'owners'},
                            {"name": 'duration_hours', "id": 'duration_hours', 'type': 'numeric', 'format': dict(specifier='.2f')},                                                  
                                    ],
                        data=dags_load_hours_by_day[(dags_load_hours_by_day['date'] == dt.datetime.strptime('2023-10-11', '%Y-%m-%d').date())
                                                    & (dags_load_hours_by_day['duration_hours']>0)][dash4_cols].sort_values(by='duration_hours', ascending=False).to_dict('records'),
                        editable=False,
                        sort_action='native',
                        style_data_conditional=(
                            data_bars(dags_load_hours_by_day[(dags_load_hours_by_day['date'] == dt.datetime.strptime('2023-10-11', '%Y-%m-%d').date())
                                                    & (dags_load_hours_by_day['duration_hours']>0)][dash4_cols].sort_values(by='duration_hours', ascending=False), 'duration_hours')
                        ),
                        filter_action='native',
                        style_cell={'textAlign': 'left', 'fontSize':12, 'font-family':'verdana'},
                        style_as_list_view=True,
                        # style_cell_conditional=[
                        #     {
                        #         'if': {'column_id': 'duration_hours'},
                        #         'color': 'rgb(94,144,134)'
                        #     }
                        # ]
                    )
                ]),
                html.Div(className="col-4", children=[
                    dash_table.DataTable(
                        id = "dash_15_datatable2",
                        columns =  [
                            {"name": 'owners', "id": 'owners'},
                            {"name": 'dag_id', "id": 'dag_id'},
                            {"name": 'duration_hours', "id": 'duration_hours', 'type': 'numeric', 'format': dict(specifier='.2f')},                                                  
                                    ],
                        data=dags_load_hours_by_day[(dags_load_hours_by_day['date'] == dt.datetime.strptime('2023-10-11', '%Y-%m-%d').date())
                                                    & (dags_load_hours_by_day['duration_hours']>0)].groupby('owners')
                                                    .agg(dag_id=('dag_id', 'count'), duration_hours=('duration_hours', 'sum')).reset_index()
                                                    .sort_values(by='duration_hours', ascending=False).to_dict('records'),
                        editable=False,
                        sort_action='native',
                        style_data_conditional=(
                            data_bars(dags_load_hours_by_day[(dags_load_hours_by_day['date'] == dt.datetime.strptime('2023-10-11', '%Y-%m-%d').date())
                                                    & (dags_load_hours_by_day['duration_hours']>0)].groupby('owners')
                                                    .agg(dag_id=('dag_id', 'count'), duration_hours=('duration_hours', 'sum')).reset_index()
                                                    .sort_values(by='duration_hours', ascending=False), 'duration_hours')
                        ),
                        filter_action='native',
                        style_cell={'textAlign': 'left', 'fontSize':12, 'font-family':'verdana'},
                        style_as_list_view=True,
                    )
                ]),
            ]),
        ])
        return content
    
    # elif tab == 'tab-2':
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
    # elif tab == 'tab-3':
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
                html.P("    - как рычаг воздействия на перевозчика, т.е. в целях получения преференций от перевозчика (РЖД) для повышения эффективности вагонного парка, при условии не выставления ему пени."),
            ], className="row")
        ],)
        return content
    # elif tab == 'tab-4':
        """По РПС"""
        internal_delay = get_tab4_trans_empty_delay_by_rps(railway=railway, start_date=start_date, end_date=end_date)
        internal_penalty = get_tab4_trans_empty_penalty_by_rps(railway=railway, start_date=start_date, end_date=end_date)
        trans_empty_by_railway_mean_delay = get_tab4_trans_empty_mean_delay_by_rps(railway=railway, start_date=start_date, end_date=end_date)
        
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
                                customdata=internal_delay['РПС'].apply(lambda x: get_rps_name(x)),
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

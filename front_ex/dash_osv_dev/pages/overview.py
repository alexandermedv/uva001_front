import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Output, Input, State

import datetime as dt   
from ..pages import dash_app

from ..utils import Header, get_osv_detail, get_osv_detail_by_dates 

def create_layout(app, start_date = None, end_date=None, debug=False):
    if start_date == None: df = get_osv_detail().sort_values(by=['Дата ввода'])

    mindate = dt.datetime.strptime(df['Дата ввода'].min(), '%Y%m%d').date()
    maxdate = dt.datetime.strptime(df['Дата ввода'].max(), '%Y%m%d').date()

    # Page layouts
    layout = html.Div(
        [
            html.Div(
                [
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Динамика недостачи в филиале"], className="subtitle padded"
                                    ),
                                    html.Div([
                                        dcc.DatePickerSingle(
                                            id = "osv_datepicker_startdate",
                                            display_format = 'DD.MM.YYYY',
                                            date = mindate,
                                        ),
                                        html.P("-", style = {"display":"inline-block","margin-right":"10px","margin-left":"10px"}),
                                        dcc.DatePickerSingle(
                                            id = "osv_datepicker_enddate",
                                            display_format = 'DD.MM.YYYY', 
                                            date = maxdate,
                                        ),
                                    ], className = "single row"),
                                    html.Div(
                                        [
                                            dcc.Dropdown(
                                                options=[
                                                    {'label': i, 'value': i}
                                                    for i in ['Safe', 'Danger!!']
                                                ],
                                                # style = {"display":"inline-block"},
                                                id='dd-filial', 
                                                className = 'four columns'
                        
                                            ),
                                            dcc.Dropdown(
                                                options=[
                                                    {'label': i, 'value': i}
                                                    for i in ['Safe', 'Danger!!']
                                                ],
                                                # style = {"display":"inline-block"},
                                                id='dd-stock',
                                                className = 'four columns'
                                            ),
                                            dcc.Dropdown(
                                                options=[
                                                    {'label': i, 'value': i}
                                                    for i in ['Safe', 'Danger!!']
                                                ],
                                                # style = {"display":"inline-block"},
                                                id='dd-material', 
                                                className = 'four columns'
                                            ),
                                        ],
                                        className="row"    
                                    ),
                                    html.Div(
                                        [
                                            dcc.RadioItems(
                                                options=[
                                                    {'label': i, 'value': i}
                                                    for i in ['Месяц', 'Неделя', 'День']
                                                ],
                                                id = 'ri-level',
                                                labelStyle={'display': 'inline-block'}
                                            )
                                        ],
                                        className = 'row'
                                    ),
                                    html.Div(
                                        id = "div-graph-1"
                                    ),
                                ],
                                # className="six columns",
                                className="twelve columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
    return layout

data = None

@dash_app.callback(
    Output('div-graph-1', 'children'),
    [Input('osv_datepicker_startdate', 'date'), 
    Input('osv_datepicker_enddate', 'date')])
    # Input('filter1', 'data')])
def update_graph1(start_date, end_date):
    global data
    global d_start
    global d_end
    # global filter1
    # print('data', data)

    if data is None or (d_start != start_date) or (d_end != end_date): 
        data = get_osv_detail_by_dates(dt.datetime.strptime(start_date,'%Y-%m-%d'), dt.datetime.strptime(end_date, '%Y-%m-%d'), debug=False)
        d_start = start_date
        d_end = end_date

    # if filter1 != input_filter1: current_data = current_data.loc[input_filter] 
    # if filter2 != input_filter2: current_data = current_data.loc[input_filter] 

    # --> Алгоримт расчета динамического сальдо
    data['Дата'] = data['Дата ввода'].apply(lambda x: dt.datetime.strptime(x, '%Y%m%d'))
    data['Неделя'] = data['Дата ввода'].apply(lambda x: dt.datetime.strptime(x, '%Y%m%d')).apply(lambda x: x - dt.timedelta(x.weekday()))
    data['Месяц'] = data['Дата ввода'].apply(lambda x: dt.datetime.strptime(x, '%Y%m%d')).apply(lambda x: x.replace(day=1))

    # Добавить условие
    data['Дата'] = data['Дата']

    df2 = data.groupby(['Дата']).agg({'Обороты по дебету':'sum', 'Обороты по кредиту':'sum'\
                                          , 'Обороты по дебету, шт':'sum', 'Обороты по кредиту, шт':'sum'})\
                                        .reset_index().sort_values(by = ['Дата']) 
    df2['Обороты по дебету(накоп), руб'] = df2['Обороты по дебету'].cumsum()
    df2['Обороты по кредиту(накоп), руб'] = df2['Обороты по кредиту'].cumsum()
    df2['Обороты по дебету(накоп), шт'] = df2['Обороты по дебету, шт'].cumsum()
    df2['Обороты по кредиту(накоп), шт'] = df2['Обороты по кредиту, шт'].cumsum()
    df2['Сальдо, руб'] = df2['Обороты по дебету(накоп), руб'] - df2['Обороты по кредиту(накоп), руб']
    df2['Сальдо, шт'] = df2['Обороты по дебету(накоп), шт'] - df2['Обороты по кредиту(накоп), шт']   
    
    # <-- Алгоримт расчета динамического сальдо

    cur_data = df2

    fig1 = {
        'data': [
            go.Bar(x =cur_data['Дата'],
                y=cur_data['Обороты по дебету(накоп), руб'],
                marker={
                    "color" : "#808080",
                },
                name = 'Обороты по дебету(накоп), руб',
                yaxis="y1", 
               
            ),
            go.Bar(x =cur_data['Дата'],
                y=cur_data['Обороты по кредиту(накоп), руб'],
                marker={
                    "color": "#bbbbbb",
                },
                name='Обороты по кредиту(накоп), руб',                         
                yaxis="y1",
            ),
            go.Scatter(x =cur_data['Дата'], 
                y=cur_data['Сальдо, руб'],
                name='Сальдо',
                mode='lines+markers',
                line={"color": "#97151c"}, 
                # Добавляем вторую ось  
                yaxis="y2", 
            ), 
        ],
        'layout':go.Layout(
            font={"family": "Raleway", "size": 12},
            hovermode="closest",
            legend={
                "x": 0.7,
                "y": 1.35,
                "orientation": "v",
                # "yanchor": "bottom",
            },
            yaxis=dict(
                title="Обороты, руб"
            ),
            yaxis2=dict(
                title="Сальдо, руб",
                overlaying="y",
                side="right",
            ),
            xaxis={
                "rangeselector": {
                    "font": {"family": "Raleway", "size": 10},
                    "buttons": [
                        {
                            "count": 3,
                            "label": "1Q",
                            "step": "month",
                            "stepmode": "backward",
                        },
                                                {                        
                            "count": 6,
                            "label": "2Q",
                            "step": "month",
                            "stepmode": "backward",
                        },
                        {
                            "count": 1,
                            "label": "1Y",
                            "step": "year",
                            "stepmode": "backward",
                        },
                        {
                            "count": 1,
                            "label": "ALL",
                            "step": "all",
                            "stepmode": "backward",
                        },
                    ]
                },
                "rangeslider": dict(
                    visible=True,
                ),
                "type": "date",
            },
        )
    }

    # График в штуках
    fig2 = {
        'data': [
            go.Bar(x =cur_data['Дата'],
                y=cur_data['Обороты по дебету(накоп), шт'],
                marker={
                    "color" : "#808080",
                },
                name = 'Обороты по дебету(накоп), шт',
                yaxis="y1", 
               
            ),
            go.Bar(x =cur_data['Дата'],
                y=cur_data['Обороты по кредиту(накоп), шт'],
                marker={
                    "color": "#bbbbbb",
                },
                name='Обороты по кредиту(накоп), шт',                         
                yaxis="y1",
            ),
            go.Scatter(x =cur_data['Дата'], 
                y=cur_data['Сальдо, шт'],
                name='Сальдо',
                mode='lines+markers',
                line={"color": "#97151c"}, 
                # Добавляем вторую ось  
                yaxis="y2", 
            ), 
        ],
        'layout':go.Layout(
            font={"family": "Raleway", "size": 12},
            hovermode="closest",
            legend={
                "x": 0.7,
                "y": 1.35,
                "orientation": "v",
                # "yanchor": "bottom",
            },
            yaxis=dict(
                title="Обороты, шт"
            ),
            yaxis2=dict(
                title="Сальдо, шт",
                overlaying="y",
                side="right",
            ),
            xaxis={
                "rangeselector": {
                    "font": {"family": "Raleway", "size": 10},
                    "buttons": [
                        {
                            "count": 3,
                            "label": "1Q",
                            "step": "month",
                            "stepmode": "backward",
                        },
                                                {                        
                            "count": 6,
                            "label": "2Q",
                            "step": "month",
                            "stepmode": "backward",
                        },
                        {
                            "count": 1,
                            "label": "1Y",
                            "step": "year",
                            "stepmode": "backward",
                        },
                        {
                            "count": 1,
                            "label": "ALL",
                            "step": "all",
                            "stepmode": "backward",
                        },
                    ]
                },
                "rangeslider": dict(
                    visible=True,
                ),
                "type": "date",
            },
        )
    }

    div = [
        dcc.Graph(
            id="graph-1",
            config={"displayModeBar": True},
            figure = fig1,
        ),
        dcc.Graph(
            id="graph-2",
            config={"displayModeBar": True},
            figure = fig2,
        ),
    ]    
    return div
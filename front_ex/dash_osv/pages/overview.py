import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Output, Input, State

import pandas as pd
import os
import datetime as dt   
from ..pages import dash_app

from ..utils import Header, get_osv_detail, get_osv_detail_by_dates 

# Данные
data = None
d_start = None
d_end = None

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
                                        html.Button ('Выгрузить', 'id_button_download')
                                    ], className = "single row"),
                                    html.Div(
                                        [
                                            dcc.Dropdown(
                                                id='dd-filial', 
                                                className = 'four columns',
                                                value = 'Все',
                                                clearable = False,
                                            ),
                                            dcc.Dropdown(
                                                id='dd-stock',
                                                className = 'four columns',
                                                clearable = False,
                                                value = 'Все'
                                            ),
                                            dcc.Dropdown(
                                                id='dd-material', 
                                                className = 'four columns',
                                                clearable = False,
                                                value = 'Все'
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
                                                value="Месяц",
                                                id = 'ri-level',
                                                labelStyle={'display': 'inline-block'}
                                            )
                                        ],
                                        className = 'row'
                                    ),
                                    html.Div(
                                        id = "div-graph-1", 
                                        className = 'row'
                                    ),
                                    html.Div(
                                        html.Div(),
                                        id = 'Output',
                                        className = 'row'
                                    )
                                ],
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

data_excel = None

@dash_app.callback(Output('Output', 'value'), [Input('id_button_download', 'n_clicks')])
def down_data(n_click):
    global data_excel

    wr = pd.ExcelWriter('//home//locadm//git//uva000_front_ex//SAP_ОСВ.xlsx')
    # print(os.listdir('//home//locadm//git//uva000_front_ex'))

    data_excel.to_excel(wr, sheet_name = 'ОСВ_94_тест', encoding = 'utf-8', index = False)
    wr.save()
    wr.close()

    return n_click

@dash_app.callback(
    Output('dd-filial', 'options'),
    [Input('osv_datepicker_startdate', 'date'), 
    Input('osv_datepicker_enddate', 'date')])
def get_filial_options(start_date, end_date):
    global data
    if data is None: 
        data = get_osv_detail_by_dates(dt.datetime.strptime(start_date,'%Y-%m-%d'), dt.datetime.strptime(end_date, '%Y-%m-%d'), debug=False)
    lf = ['Все'] + data['Филиал'].unique().tolist()
    return [{'label': i, 'value': i} for i in lf]
@dash_app.callback(
    Output('dd-stock', 'options'),
    [Input('osv_datepicker_startdate', 'date'), 
    Input('osv_datepicker_enddate', 'date')])
def get_stock_options(start_date, end_date):
    global data
    if data is None: 
        data = get_osv_detail_by_dates(dt.datetime.strptime(start_date,'%Y-%m-%d'), dt.datetime.strptime(end_date, '%Y-%m-%d'), debug=False)
    lf = ['Все'] + data['Склад'].unique().tolist()
    return [{'label': i, 'value': i} for i in lf]
@dash_app.callback(
    Output('dd-material', 'options'),
    [Input('osv_datepicker_startdate', 'date'), 
    Input('osv_datepicker_enddate', 'date')])
def get_material_options(start_date, end_date):
    global data
    if data is None: 
        data = get_osv_detail_by_dates(dt.datetime.strptime(start_date,'%Y-%m-%d'), dt.datetime.strptime(end_date, '%Y-%m-%d'), debug=False)
    lf = ['Все'] + data['Группа материалов'].unique().tolist()
    return [{'label': i, 'value': i} for i in lf]
@dash_app.callback(
    Output('div-graph-1', 'children'),
    [Input('osv_datepicker_startdate', 'date'), 
    Input('osv_datepicker_enddate', 'date'),
    Input('ri-level', 'value'),
    Input('dd-filial', 'value'), 
    Input('dd-stock', 'value'), 
    Input('dd-material', 'value')])
def update_graph1(start_date, end_date, data_level, filial, stock, material):
    global data
    global d_start
    global d_end
    # global filter1
    # print('data', data)
    global data_excel

    print('data_level',data_level)
 
    # if data is None or (d_start != start_date) or (d_end != end_date): 
    data = get_osv_detail_by_dates(dt.datetime.strptime(start_date,'%Y-%m-%d'), dt.datetime.strptime(end_date, '%Y-%m-%d'), debug=False)
    data_left = get_osv_detail_by_dates(dt.datetime.strptime('1900-01-01','%Y-%m-%d')\
        , dt.datetime.strptime(start_date, '%Y-%m-%d') - dt.timedelta(days=1), debug=False)
    d_start = start_date
    d_end = end_date

    # if filter1 != input_filter1: current_data = current_data.loc[input_filter] 
    # if filter2 != input_filter2: current_data = current_data.loc[input_filter] 

    # --> Алгоримт расчета динамического сальдо
    data['Дата'] = data['Дата ввода'].apply(lambda x: dt.datetime.strptime(x, '%Y%m%d'))
    data['Неделя'] = data['Дата ввода'].apply(lambda x: dt.datetime.strptime(x, '%Y%m%d')).apply(lambda x: x - dt.timedelta(x.weekday()))
    data['Месяц'] = data['Дата ввода'].apply(lambda x: dt.datetime.strptime(x, '%Y%m%d')).apply(lambda x: x.replace(day=1))

    # Добавить условие
    if data_level == 'День':
        data['Дата'] = data['Дата']
    elif data_level == 'Неделя':
        data['Дата'] = data['Неделя']
    else: data['Дата'] = data['Месяц']

    # Фильтры
    df1 = data
    df1_left = data_left

    if filial != 'Все':
        df1 = data[data['Филиал'].isin([filial])]
        df1_left = data_left[data_left['Филиал'].isin([filial])]
    if stock != 'Все':
        df1 = df1[df1['Склад'].isin([stock])]
        df1_left = df1_left[df1_left['Склад'].isin([stock])]
    if material != 'Все':
        df1 = data[data['Группа материалов'].isin([material])]
        df1_left = data_left[data_left['Группа материалов'].isin([material])]

    df2 = df1.groupby(['Дата', 'Филиал']).agg({'Обороты по дебету':'sum', 'Обороты по кредиту':'sum'\
                                          , 'Обороты по дебету, шт':'sum', 'Обороты по кредиту, шт':'sum'})\
                                        .reset_index().sort_values(by = ['Дата']) 

    df2_left = df1_left.sum()

    df2['Обороты по дебету(накоп), руб'] = df2['Обороты по дебету'].cumsum() + df2_left['Обороты по дебету']
    df2['Обороты по кредиту(накоп), руб'] = df2['Обороты по кредиту'].cumsum() + df2_left['Обороты по кредиту']
    df2['Обороты по дебету(накоп), шт'] = df2['Обороты по дебету, шт'].cumsum() + df2_left['Обороты по дебету, шт']
    df2['Обороты по кредиту(накоп), шт'] = df2['Обороты по кредиту, шт'].cumsum() + df2_left['Обороты по кредиту, шт']
 
    df2['Сальдо, руб'] = df2['Обороты по дебету(накоп), руб'] - df2['Обороты по кредиту(накоп), руб']
    df2['Сальдо, шт'] = df2['Обороты по дебету(накоп), шт'] - df2['Обороты по кредиту(накоп), шт']   
    
    df2['Обороты по дебету'] = df2['Обороты по дебету']*1000
    df2['Обороты по кредиту'] = df2['Обороты по кредиту']*1000

    # print('Входящее сальдо', df2_left['Обороты по дебету'] - df2_left['Обороты по кредиту'])
    # <-- Алгоримт расчета динамического сальдо
    data_excel = df2
    print(df2.info()    )

    df2 = df1.groupby(['Дата']).agg({'Обороты по дебету':'sum', 'Обороты по кредиту':'sum'\
                                        , 'Обороты по дебету, шт':'sum', 'Обороты по кредиту, шт':'sum'})\
                                    .reset_index().sort_values(by = ['Дата']) 

    df2_left = df1_left.sum()

    df2['Обороты по дебету(накоп), руб'] = df2['Обороты по дебету'].cumsum() + df2_left['Обороты по дебету']
    df2['Обороты по кредиту(накоп), руб'] = df2['Обороты по кредиту'].cumsum() + df2_left['Обороты по кредиту']
    df2['Обороты по дебету(накоп), шт'] = df2['Обороты по дебету, шт'].cumsum() + df2_left['Обороты по дебету, шт']
    df2['Обороты по кредиту(накоп), шт'] = df2['Обороты по кредиту, шт'].cumsum() + df2_left['Обороты по кредиту, шт']
    df2['Сальдо, руб'] = df2['Обороты по дебету(накоп), руб'] - df2['Обороты по кредиту(накоп), руб']
    df2['Сальдо, шт'] = df2['Обороты по дебету(накоп), шт'] - df2['Обороты по кредиту(накоп), шт']   

    cur_data = df2

    fig1 = {
        'data': [
            go.Bar(x =cur_data['Дата'],
                y=cur_data['Обороты по дебету'],
                marker={
                    "color" : "#808080",
                },
                name = 'Обороты по дебету',
                yaxis="y1", 
               
            ),
            go.Bar(x =cur_data['Дата'],
                y=cur_data['Обороты по кредиту'],
                marker={
                    "color": "#bbbbbb",
                },
                name='Обороты по кредиту',                         
                yaxis="y1",
            ),
            go.Scatter(x =cur_data['Дата'], 
                y=cur_data['Сальдо, руб'],
                name='Сальдо',
                mode='lines+markers',
                line={"color": "#97151c"}, 
                # Добавляем вторую ось  
                # yaxis="y2", 
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
                            "count": 1,
                            "label": "1M",
                            "step": "month",
                            "stepmode": "backward",
                        },
                        {
                            "count": 3,
                            "label": "1Q",
                            "step": "month",
                            "stepmode": "backward",
                        },
                        {                        
                            "count": 6,
                            "label": "HY",
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
                # yaxis="y2", 
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
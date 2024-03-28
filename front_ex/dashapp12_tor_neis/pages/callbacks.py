""" Интерактивные элементы для отчетов."""
import datetime as dt
import numpy as np
#from PIL import Image
from dash.dependencies import Input, Output
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
import plotly.graph_objects as go
import pandas as pd
# import dash_table
from dash import dash_table
import dash
# from .layout import layout
#import string
from ..pages import dash_app
from ..utils import get_tors
from ..utils import get_tors_count
from ..utils import get_tors_count_speed
from ..utils import get_tors_count_nk
from ..utils import get_top_tors_by_contr
from ..utils import get_tors_by_contr_bubl


# Количество ремонтов за выбранный период
@dash_app.callback(Output(component_id='tors_amount', component_property='children'),
                   [Input('dashboard12-date-picker-range', 'start_date'),
                   Input('dashboard12-date-picker-range', 'end_date'),])

def tors_amount(start_date, end_date):
    """Вычисление количества ремонтов"""
    df0 = get_tors_count(start_date, end_date)
    print('df0 =', df0)
    return df0['Количество ремонтов'].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True)


@dash_app.callback(Output(component_id='tors_amount_nk', component_property='children'),
                   [Input('dashboard12-date-picker-range', 'start_date'),
                   Input('dashboard12-date-picker-range', 'end_date'),])

def tors_amount_nk(start_date, end_date):
    """Вычисление количества некачественных ремонтов"""
    df1 = get_tors_count_nk(start_date, end_date)
    print('df1 =', df1)
    return df1['Количество некач ремонтов'].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True)


# Первая линия
# Первый график по ремонтам
@dash_app.callback(
     Output('tab-content', 'children'),
     [Input('dashboard12-tabs', 'value'),
      Input('dashboard12-date-picker-range', 'start_date'),
      Input('dashboard12-date-picker-range', 'end_date')]
 )

def render_content(tab, start_date, end_date):
    """Первый график общему количеству"""
    if tab == 'tab-1':
        print('Запустился callback с графиками')
        df2 = get_tors(start_date, end_date)
        print('df2 =', df2)

        df3 = get_top_tors_by_contr(start_date, end_date)
        #df4 = get_top_tors_by_client(start_date, end_date)
        df5 = get_tors(start_date, end_date)
        df6 = get_tors_count_speed(start_date, end_date)
        print('df6 =', df6)

        x1_data = df3['Процент']
        x1_text = df3['Процент'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)
        x2_data = df3['Контрагент'].tolist()
        y1_data = df3['Контрагент'].tolist()
        y2_data = df3['Некачественный']
        y3_data = df3['Качественные']

        #x2_data = df4['Процент']
        #x2_text = df4['Процент'].map('{:,.0f}'.format).astype(str).replace(
        #    ',',' ', regex=True)
        #y2_data = df4['Наименование Депо'].tolist()

        df7 = get_tors_by_contr_bubl(start_date, end_date)

        #cbar = Image.open('cat.png')


    content = html.Div([
            html.Div([
                    html.Br(),
                    html.H6('''Сводная информация по ремонтам''',
                        style={'text-align':'center',
                                'font-size': '16pt',
                                'font-weight': 'bold'}),
                    html.Br([]),
                    dash_table.DataTable(
                        id='dashboard12-tables',
                        columns=[{"name": i, "id": i} for i in df2.columns],
                        data=df2.to_dict('records'),
                        page_size=2000,
                        style_table={'overflowY': 'scroll'},
                        style_cell={
                            # all three widths are needed
                            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'textAlign': 'left',
                        },
                        export_format='xlsx',
                        export_headers='display',
                        merge_duplicate_headers=True,
                        style_header={
                            'backgroundColor': 'rgb(200, 200, 200)',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(230, 230, 230)',
                            }
                        ],
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                        },
                        style_cell_conditional =[
                            {'if':{'column_id': 'Год'},
                            'width':'5%'},
                            {'if':{'column_id': 'Качественные'},
                            'width':'20%'},
                            {'if':{'column_id': 'Некачественные'},
                            'width':'20%'},
                            {'if':{'column_id': 'Всего'},
                            'width':'20%'},
                        ],
                    ),
                ], className="row"),

            html.Div([
                dcc.Graph(
                    id="dashboard12-graph1",
                    config={"displayModeBar": True},
                    figure={
                        'data': [
                            go.Scatter(x=df5['Год'],
                                y=df5['Некачественные'],
                                hoverinfo='skip',
                                hovertemplate="Дата: %{x}" + "<br>Количество ремонтов, шт.: %{y:,.0f}",
                                name='Динамика некачественных ремонтов',
                                mode='lines+markers',
                                line={"color": "#d30909"}, #6E6E6E
                                yaxis = "y2"
                            ),
                            go.Scatter(x=df5['Год'],
                                y=df5['Общее количество'],
                                hoverinfo='skip',
                                hovertemplate="Дата: %{x}" + "<br>Количество ремонтов, шт.: %{y:,.0f}",
                                name='Общее количество ремонтов',
                                mode='lines+markers',
                                line={"color": "#09d3d3"}, #6E6E6E
                                yaxis = "y2"
                            ),                                                           
                        ],
                        'layout':go.Layout(
                            autosize=True,
                            title_text='Динамика ремонтов, шт.',
                            margin={
                                                "r": 0,
                                                "t": 50,
                                                "b": 20,
                                                "l": 50,
                                },
                            #title_text='''
                            #    Динамика некачественных ремонтов, шт.
                            #    ''',
                            font={"family": "Raleway", "size": 12},
                            hovermode="closest",
                            legend={
                                "x": 0.8,
                                "y": 1.35, 
                                "orientation": "v",
                                # "yanchor": "bottom",
                            },
                            yaxis=dict(
                                title="Количество ремонтов, шт."
                              
                            ),
                            yaxis2=dict(
                                title="Количество ремонтов, шт.",
                                overlaying="y2",
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
                                # "rangeslider": dict(
                                #     visible=True,
                                # ),
                                "type": "date",
                            },
                        )
                    }
                ),
            ], className="six columns"
            ),
                
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Graph(
                            id="dashboard12-graph4",
                            figure={
                                "data": [
                                    #go.Figure(
                                        go.Indicator(
                                        mode = "gauge+number",
                                        value = df6['Некачественные'][0],
                                        domain = {'x': [0, 1], 'y': [0, 1]},
                                        gauge = {'axis': {'range': [None, df6['Общее количество'][0],], 'tickwidth': 1, 'tickcolor': "darkblue"},
                                                'bar': {'color': "#d30909"},
                                                'bgcolor': "lightgray"},),
                                         #),
                                    ],
                                    "layout": go.Layout(
                                        autosize=True,
                                        title_text='Доля некачественных ремонтов',
                                        margin={
                                                    "r": 50,
                                                    "t": 100,
                                                    "b": 20,
                                                    "l": 120,
                                            },

                                    ),

                                },
                                config={"displayModeBar": False},

                            ),
                        ], className="six columns"),
                        html.Div([
                        dcc.Graph(
                            id="dashboard12-graph5",
                            figure={
                                "data": [
                                    #go.Figure(
                                        go.Pie(
                                        labels=["Контрагенты, выполнившие более 10% ремонтов некачественно","Контрагенты, выполнившие менее 10% ремонтов некачественно"],
                                        values=[df7['Некачественные'][0],df7['Качественные'][0]],
                                        hole = 0.7,
                                        marker={"colors": ['#97151c','#D3D3D3']},
                                         ),
                                    ],
                                    "layout": go.Layout(
                                        autosize=True,
                                        title_text='Анализ контрагентов',
                                        margin={
                                                    "r": 50,
                                                    "t": 100,
                                                    "b": 20,
                                                    "l": 120,
                                            },

                                    ),

                                },
                                config={"displayModeBar": False},

                            ),
                        ], className="twelve columns"),
                        html.Div([
                    dcc.Graph(
                        id="dashboard12-graph2",
                        figure={
                            "data": [
                                go.Bar(
                                    x=df3['Контрагент'],
                                    y=df3['Некачественный'],
                                    xaxis='x1',
                                    text=x1_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Ремонты: %{y} <br>Процент некачественных ремонтов: %{text}""",
                                    name='Некачественные',
                                    #orientation='h',
                                    #textposition='auto',
                                    marker={
                                        "color": "#97151c",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                                go.Bar(
                                    x=df3['Контрагент'],
                                    y=df3['Качественные'],
                                    xaxis='x1',
                                    text=x1_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Ремонты: %{y} <br>Процент некачественных ремонтов: %{text}""",
                                    name='Качественные',
                                    #orientation='h',
                                    #textposition='auto',
                                    marker={
                                        "color": "#D3D3D3",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                barmode='stack',
                                title_text='ТОП-10 контрагентов',
                                plot_bgcolor='white',
                                paper_bgcolor='white',
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 100,
                                                    "l": 100,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="twelve columns"),
                #html.Div([
                #cbar
                #]),
            ],),
          ],),
        ],)
    return content



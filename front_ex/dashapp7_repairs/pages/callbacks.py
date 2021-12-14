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
# from .layout import layout
#import string
from ..pages import dash_app
from ..utils import get_bad_tors_912, get_bad_tors_913, get_top_tors_by_rps_pr
from ..utils import get_tors_by_rps, get_tors_by_rps_pr
from ..utils import get_tors_by_type
from ..utils import get_top_tors_by_rps
from ..utils import get_top_tors_by_type
from ..utils import get_avg_tors
from ..utils import get_tors_count
from ..utils import get_kodneis_info


# Количество ремонтов за выбранный период
@dash_app.callback(Output(component_id='tors_amount', component_property='children'),
                   [Input('dashboard7-date-picker-range', 'start_date'),
                   Input('dashboard7-date-picker-range', 'end_date'),])

def tors_amount(start_date, end_date):
    """Вычисление количества ремонтов"""
    df0 = get_tors_count(start_date, end_date)
    print('df0 =', df0)
    return df0['Количество ремонтов'].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True)


# Первая линия
# Первый график по ремонтам
@dash_app.callback(
    Output('tab-content', 'children'),
    [Input('dashboard7-tabs', 'value'),
     Input('dashboard7-date-picker-range', 'start_date'),
     Input('dashboard7-date-picker-range', 'end_date')]
)
def render_content(tab, start_date, end_date):
    """Первый график по ремонтам - по РПС"""
    if tab == 'tab-1':
        print('Запустился callback с графиками')
        df1 = get_tors_by_rps(start_date, end_date)
        df1['Total', 'Прочие', 'ДР']= 15
        df1['Total', 'Прочие', 'КР']= 25
        df1['Total', 'Прочие', 'ТР-1']= 35
        df1['Total', 'Прочие', 'ТР-2']= 45
        print('df1 =', df1)

        y1_data = df1['Количество ремонтов'][df1['Вид ремонта'] == 'ДР']
        x1_text = df1['Количество ремонтов'][df1['Вид ремонта'] == 'ДР']
        x1_data = df1['РПС'][df1['Вид ремонта'] == 'ДР']

        y2_data = df1['Количество ремонтов'][df1['Вид ремонта'] == 'КР']
        x2_text = df1['Количество ремонтов'][df1['Вид ремонта'] == 'КР']
        x2_data = df1['РПС'][df1['Вид ремонта'] == 'КР']

        y3_data = df1['Количество ремонтов'][df1['Вид ремонта'] == 'ТР-1']
        x3_text = df1['Количество ремонтов'][df1['Вид ремонта'] == 'ТР-1']
        x3_data = df1['РПС'][df1['Вид ремонта'] == 'ТР-1']

        y4_data = df1['Количество ремонтов'][df1['Вид ремонта'] == 'ТР-2']
        x4_text = df1['Количество ремонтов'][df1['Вид ремонта'] == 'ТР-2']
        x4_data = df1['РПС'][df1['Вид ремонта'] == 'ТР-2']


        df5 = get_tors_by_type(start_date=start_date, end_date=end_date)
        print('df5 =', df5)


        print('Запустился callback с графиками')
        df2 = get_tors_by_rps_pr(start_date, end_date).sort_values(by='РПС', ascending=True)
        df2['Total', 'Прочие', 'ДР']= 15
        df2['Total', 'Прочие', 'КР']= 25
        df2['Total', 'Прочие', 'ТР-1']= 35
        df2['Total', 'Прочие', 'ТР-2']= 45
        print('df2 =', df2)
        y5_data = df2['Количество ремонтов'][df2['Вид ремонта'] == 'ДР']
        x5_text = df2['Количество ремонтов'][df2['Вид ремонта'] == 'ДР']
        x5_data = df2['РПС'][df2['Вид ремонта'] == 'ДР']

        y6_data = df2['Количество ремонтов'][df2['Вид ремонта'] == 'КР']
        x6_text = df2['Количество ремонтов'][df2['Вид ремонта'] == 'КР']
        x6_data = df2['РПС'][df2['Вид ремонта'] == 'КР']

        y7_data = df2['Количество ремонтов'][df2['Вид ремонта'] == 'ТР-1']
        x7_text = df2['Количество ремонтов'][df2['Вид ремонта'] == 'ТР-1']
        x7_data = df2['РПС'][df2['Вид ремонта'] == 'ТР-1']

        y8_data = df2['Количество ремонтов'][df2['Вид ремонта'] == 'ТР-2']
        x8_text = df2['Количество ремонтов'][df2['Вид ремонта'] == 'ТР-2']
        x8_data = df2['РПС'][df2['Вид ремонта'] == 'ТР-2']



        print('Запустился callback с графиками')
        df3 = get_avg_tors(start_date, end_date)
        print('df3 =', df3)

        x9_data = df3['Средняя длительность'].astype(str).tolist()
        x9_text = df3['Средняя длительность']
        y9_data = df3['Вид ремонта'].tolist()
        print(df3)
        x10_data = df3['Плановая длительность'].astype(str).tolist()
        x10_text = df3['Плановая длительность']
        y10_data = df3['Вид ремонта'].tolist()


        print('Запустился callback с графиками')
        df4 = get_top_tors_by_type(start_date, end_date)
        print('df4 =', df4)

        x11_data = df4['Количество'].astype(str).tolist()
        x11_text = df4['Код неисправности2'].astype(str).tolist()
        y11_data = df4['Код неисправности3']

        print('Запустился callback с графиками')
        df6 = get_top_tors_by_rps(start_date, end_date).sort_values(by='РПС', ascending=False)
        print('df6 =', df6)

        x12_data = df6['Количество'].astype(str).tolist()
        x12_text = df6['Код неисправности2'].astype(str).tolist()
        y12_data = df6['Код неисправности3']

        print('Запустился callback с графиками')
        df7 = get_top_tors_by_rps_pr(start_date, end_date).sort_values(by='РПС', ascending=False)
        print('df7 =', df7)

        x13_data = df7['Количество'].astype(str).tolist()
        x13_text = df7['Код неисправности2'].astype(str).tolist()
        y13_data = df7['Код неисправности3']

        df8 = get_bad_tors_912(start_date=start_date, end_date=end_date)
        print('df8 =', df8)

        df9 = get_bad_tors_913(start_date=start_date, end_date=end_date)
        print('df9 =', df9)

        sum3 = sum(map(int, df8["Количество"]))

        sum4 = sum(map(int, df9["Количество"]))

        content = html.Div([
            html.Div([
                dcc.Graph(
                    id="dashboard7-graph1",
                    figure={
                        "data": [
                            go.Bar(
                                x=x3_data,
                                y=y3_data.map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                text=x3_text.map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                hoverinfo='skip',
                                hovertemplate=
                                    """Кол-во ремонтов ТР-1: %{y}""",
                                name = 'ТР-1',
                                orientation='v',
                                textposition='outside',
                                constraintext='outside',
                                marker={
                                    "color": "#C17A75",
                                },
                            ),
                            go.Bar(
                                x=x4_data,
                                y=y4_data.map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                text=x4_text.map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                hoverinfo='skip',
                                hovertemplate=
                                    """Кол-во ремонтов ТР-2: %{y}""",
                                name = 'ТР-2',
                                orientation='v',
                                textposition='outside',
                                constraintext='outside',
                                marker={
                                    "color": "#8A2432",
                                },
                            ),
                            go.Bar(
                                x=x1_data,
                                y=y1_data.map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                text=x1_text.map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                hoverinfo='skip',
                                hovertemplate=
                                    """Кол-во ремонтов ДР: %{y}""",
                                name = 'ДР',
                                orientation='v',
                                textposition='outside',
                                constraintext='outside',
                                marker={
                                    "color": "#D9D9D9",
                                },
                            ),
                            go.Bar(
                                x=x2_data,
                                y=y2_data.map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                text=x2_text.map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                hoverinfo='skip',
                                hovertemplate=
                                    """Кол-во ремонтов КР: %{y}""",
                                name = 'КР',
                                orientation='v',
                                textposition='outside',
                                constraintext='outside',
                                marker={
                                    "color": "#7E7E7E",
                                },
                            ),
                        ],
                        "layout": go.Layout(
                            autosize=True,
                            title_text='Ремонты по РПС, шт.',
                            margin={
                                                "r": 0,
                                                "t": 50,
                                                "b": 20,
                                                "l": 70,
                            },

                        ),

                    },
                ),
                ], className='six columns'),

            html.Div([
                dcc.Graph(
                    id="dashboard7-graph2",
                    figure={
                        "data": [
                            go.Bar(
                                x=x7_data,
                                y=y7_data.map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                text=x7_text.map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                hoverinfo='skip',
                                hovertemplate=
                                    """Кол-во ремонтов ТР-1: %{y}""",
                                name = 'ТР-1',
                                orientation='v',
                                textposition='outside',
                                constraintext='outside',
                                marker={
                                    "color": "#C17A75",
                                },
                            ),
                            go.Bar(
                                x=x8_data,
                                y=y8_data.map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                text=x8_text.map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                hoverinfo='skip',
                                hovertemplate=
                                    """Кол-во ремонтов ТР-2: %{y}""",
                                name = 'ТР-2',
                                orientation='v',
                                textposition='outside',
                                constraintext='outside',
                                marker={
                                    "color": "#8A2432",
                                },
                            ),
                            go.Bar(
                                x=x5_data,
                                y=y5_data.map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                text=x5_text.map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                hoverinfo='skip',
                                hovertemplate=
                                    """Кол-во ремонтов ДР: %{y}""",
                                name = 'ДР',
                                orientation='v',
                                textposition='outside',
                                constraintext='outside',
                                marker={
                                    "color": "#D9D9D9",
                                },
                            ),
                            go.Bar(
                                x=x6_data,
                                y=y6_data.map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                text=x6_text.map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                hoverinfo='skip',
                                hovertemplate=
                                    """Кол-во ремонтов КР: %{y}""",
                                name = 'КР',
                                orientation='v',
                                textposition='outside',
                                constraintext='outside',
                                marker={
                                    "color": "#7E7E7E",
                                },
                            ),
                        ],
                        "layout": go.Layout(
                            autosize=True,
                            title_text='Ремонты по РПС: раскрытие прочих, шт.',
                            margin={
                                                "r": 0,
                                                "t": 50,
                                                "b": 20,
                                                "l": 70,
                            },

                        ),

                    },
                ),
                ], className='six columns'),

            html.Div([
                dcc.Graph(
                    id="dash7-pie1",
                    figure={
                        "data": [go.Pie(labels=df5['Вид ремонта'], values=df5["Количество ремонтов"],
                            marker={"colors": ["#D9D9D9","#7E7E7E","#C17A75",  "#8A2432"]}, 
                            hoverinfo='skip',
                            hovertemplate = '%{label} - %{text}',
                            text = df5["Количество ремонтов"].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True)
                        ),],
                        "layout": go.Layout(
                            autosize=True,
                            font = dict(size=12),
                            title_text='Количество ремонтов по виду, шт.',
                            margin={"r": 0, "t": 100, "b": 20, "l": 70, },
                        ),
                    },
                    # config={"displayModeBar": False},
                ),
            ], className="six columns"),

            html.Div([
                dcc.Graph(
                    id="dashboard7-graph3",
                    figure={
                        "data": [
                            go.Bar(
                                x=x9_data,
                                y=y9_data,
                                text=x9_text.map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True),
                                hoverinfo='skip',
                                #hovertemplate=
                                #    """фактическое время: %{y}""",
                                name = 'Фактическое время',
                                orientation='h',
                                textposition='auto',
                                constraintext='outside',
                                marker={
                                    "color": "#8A2432",
                                },
                            ),
                            go.Bar(
                                x=x10_data,
                                y=y10_data,
                                text=x10_text,
                                hoverinfo='skip',
                                #hovertemplate=
                                #    """ожидаемое время: %{y}""",
                                name = 'Ожидаемое время',
                                orientation='h',
                                textposition='auto',
                                constraintext='outside',
                                marker={
                                    "color": "#D9D9D9",
                                },
                            ),
                        ],
                        "layout": go.Layout(
                            autosize=True,
                            title_text='Средняя продолжительность ремонта, сут.',
                            margin={
                                                "r": 0,
                                                "t": 50,
                                                "b": 20,
                                                "l": 70,
                            },

                        ),

                    },
                ),
            ], className='six columns'),

            html.Div([
                dcc.Graph(
                    id="dashboard7-graph4",
                    figure={
                        "data": [
                            go.Bar(
                                x=x11_data,
                                y=y11_data,
                                text=x11_text,
                                hoverinfo='skip',
                                hovertemplate=
                                    """<br>Количество ремонтов: %{x}""",
                                name='',
                                orientation='h',
                                textposition='outside',
                                marker={
                                    "color": ["#7E7E7E","#979797","#C5C5C5","#D9D9D9","#D2D2D2","#E1E1E1","#C17A75","#C39491","#D9C4C2","#8A2432","#9F5C66","#C9AAAE"],
                                    "line": {
                                        "color": "rgb(255, 255, 255)",
                                        "width": 2,
                                    },
                                },
                            ),
                        ],
                        "layout": go.Layout(
                            autosize=True,
                            title_text='Топ-3 кода неисправности по видам ремонтов, шт.',
                            margin={
                                                "r": 0,
                                                "t": 50,
                                                "b": 20,
                                                "l": 150,
                            },

                        ),

                    },
                    config={"displayModeBar": False},
                ),
            ], className="six columns"),  
            html.Div([
                dcc.Graph(
                    id="dashboard7-graph5",
                    figure={
                        "data": [
                            go.Bar(
                                x=x12_data,
                                y=y12_data,
                                text=x12_text,
                                hoverinfo='skip',
                                hovertemplate=
                                    """<br>Количество ремонтов: %{x}""",
                                name='',
                                orientation='h',
                                textposition='outside',
                                marker={
                                    "color": ["#656669","#9B9B9D","#9B9B9D","#730031","#A45979","#D5B2C1","#083B40","#5E7F83","#B4C4C5"],
                                    "line": {
                                        "color": "rgb(255, 255, 255)",
                                        "width": 2,
                                    },
                                },
                            ),
                        ],
                        "layout": go.Layout(
                            autosize=True,
                            title_text='Топ-3 кода неисправности по РПС, шт.',
                            margin={
                                                "r": 0,
                                                "t": 50,
                                                "b": 20,
                                                "l": 150,
                            },

                        ),

                    },
                    config={"displayModeBar": False},
                ),
            ], className="six columns"),
            html.Div([
                dcc.Graph(
                    id="dashboard7-graph6",
                    figure={
                        "data": [
                            go.Bar(
                                x=x13_data,
                                y=y13_data,
                                text=x13_text,
                                #layout_yaxis_range=[0,2000],
                                hoverinfo='skip',
                                hovertemplate=
                                    """<br>Количество ремонтов: %{x}""",
                                name='',
                                orientation='h',
                                textposition='outside',
                                marker={
                                    "color": ["#470023","#875970","#C7B2BD","#8A2432","#B3707A","#DCBDC1","#AC3B46","#C97F87","#E6C4C7","#C17A75","#D7A8A5","#ECD7D5","#D97A6B","#E6A89F","#F4D7D2","#F27C8D","#F7AAB5","#FBD7DD","#F4ACBA","#F8C9D2","#FCE6EA"],
                                    "line": {
                                        "color": "rgb(255, 255, 255)",
                                        "width": 2,
                                    },
                                },
                            ),
                        ],
                        "layout": go.Layout(
                            autosize=True,
                            xaxis_range=[0,1800],
                            title_text='Топ-3 кода неисправности по РПС: раскрытие прочих, шт.',
                            margin={
                                                "r": 0,
                                                "t": 50,
                                                "b": 20,
                                                "l": 150,
                            },

                        ),

                    },
                    config={"displayModeBar": False},
                ),
            ], className="twelve columns"),   
            html.Div([
                dcc.Graph(
                    id="dash7-pie2",
                    figure={
                        "data": [go.Pie(labels=df8['РПС'], values=df8["Количество"], sort=False,
                            marker={"colors": ["#083B40","#730031","#470023", "#8A2432","#AC3B46","#C17A75","#D97A6B","#F27C8D","#F4ACBA"]}, 
                            hoverinfo='skip',
                            hovertemplate = '%{label} - %{text}',
                            text = df8["Количество"].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True)
                        ),],
                        "layout": go.Layout(
                            autosize=True,
                            font = dict(size=12),
                            title_text=f'''Количество некачественных ремонтов 912 - {sum3} шт.''',
                            margin={"r": 0, "t": 120, "b": 80, "l": 70, },
                        ),
                    },
                    # config={"displayModeBar": False},
                ),
            ], className="six columns"),   
            html.Div([
                dcc.Graph(
                    id="dash7-pie3",
                    figure={
                        "data": [go.Pie(labels=df9['РПС'], values=df9["Количество"], sort=False,
                            #color_discrete_map={'КР':'#083B40',
                            #         'ПВ':'#730031',
                            #         'ЗРВ':'#470023',
                            #         'МВЗ':'#8A2432',
                            #         'ОКТ':'#AC3B46',
                            #         'ПЛ':'#C17A75',
                            #         'ФИТ':'#D97A6B',
                            #         'ЦМВ':'#F27C8D',
                            #         'ЦС':'#F4ACBA'},
                            marker={"colors": ["#083B40","#730031","#470023", "#8A2432","#AC3B46","#C17A75","#D97A6B","#F27C8D","#F4ACBA"]}, 
                            hoverinfo='skip',
                            hovertemplate = '%{label} - %{text}',
                            text = df9["Количество"].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True)
                        ),],
                        "layout": go.Layout(
                            autosize=True,
                            font = dict(size=12),
                            title_text=f'''Количество некачественных ремонтов 913 - {sum4} шт.''',
                            margin={"r": 0, "t": 120, "b": 80, "l": 70, },
                        ),
                    },
                    # config={"displayModeBar": False},
                ),
            ], className="six columns"),   
        ],),
        return content     

    elif tab == 'tab-2':
        print('tab-2')
        df10 = get_kodneis_info()
        print('df10 =', df10)

        content = html.Div([
            html.Div([
                    html.Br(),
                    html.H6('''Справочник кодов неисправности''',
                        style={'text-align':'center',
                                'font-size': '16pt',
                                'font-weight': 'bold'}),
                    html.Br([]),
                    dash_table.DataTable(
                        id='dashboard7-tabs',
                        columns=[{"name": i, "id": i} for i in df10.columns],
                        data=df10.to_dict('records'),
                        page_size=20,
                        style_table={'overflowX': 'auto'},
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
                    ),
                ], className="row"),
        ],)
        return content  







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
from ..pages import dash_app
from ..utils import get_get_open_ap_by_groups_182, get_get_open_ap_by_groups_365, get_get_open_ap_by_groups_366
from ..utils import get_incoming_ap, get_increase_ap, get_decrease_ap, get_outcoming_ap, get_high_ap_issues


# Построение содержимого выбранной закладки

def render_content():
    """Построение содержимого дашборда"""

    print('Запуск вкладки 1')
    df1 = get_get_open_ap_by_groups_182()
    print('df1 =', df1)
    # df1 = get_monitoring().sort_values(by=s, ascending=True)

    kol = 0

    x1_data = df1['count'][df1['issue_risk_level']=='Низкий'].astype(str).tolist()
    x1_text = df1['count'][df1['issue_risk_level']=='Низкий'].astype(str)
    y1_data = df1['issue_group'][df1['issue_risk_level']=='Низкий'].tolist()
    print('x1_data =', x1_data)
    print('y1_data =', y1_data)

    x2_data = df1['count'][df1['issue_risk_level']=='Средний'].astype(str).tolist()
    x2_text = df1['count'][df1['issue_risk_level']=='Средний'].astype(str)
    y2_data = df1['issue_group'][df1['issue_risk_level']=='Средний'].tolist()
    print('x2_data =', x2_data)
    print('y2_data =', y2_data)

    x3_data = df1['count'][df1['issue_risk_level']=='Высокий'].astype(str).tolist()
    x3_text = df1['count'][df1['issue_risk_level']=='Высокий'].astype(str)
    y3_data = df1['issue_group'][df1['issue_risk_level']=='Высокий'].tolist()
    print('x3_data =', x3_data)
    print('y3_data =', y3_data)

    print('x1_data =', x1_data)
    print('sum(x1_data) =', sum(map(int, x1_data)))
    sum1 = sum(map(int, x1_data)) + sum(map(int, x2_data)) + sum(map(int, x3_data))

    df1 = get_get_open_ap_by_groups_365()

    x4_data = df1['count'][df1['issue_risk_level']=='Низкий'].astype(str).tolist()
    x4_text = df1['count'][df1['issue_risk_level']=='Низкий'].astype(str)
    y4_data = df1['issue_group'][df1['issue_risk_level']=='Низкий'].tolist()

    x5_data = df1['count'][df1['issue_risk_level']=='Средний'].astype(str).tolist()
    x5_text = df1['count'][df1['issue_risk_level']=='Средний'].astype(str)
    y5_data = df1['issue_group'][df1['issue_risk_level']=='Средний'].tolist()

    x6_data = df1['count'][df1['issue_risk_level']=='Высокий'].astype(str).tolist()
    x6_text = df1['count'][df1['issue_risk_level']=='Высокий'].astype(str)
    y6_data = df1['issue_group'][df1['issue_risk_level']=='Высокий'].tolist()

    print('df2 =', df1)
    sum2 = sum(map(int, x4_data)) + sum(map(int, x5_data)) + sum(map(int, x6_data))


    df1 = get_get_open_ap_by_groups_366()

    x7_data = df1['count'][df1['issue_risk_level']=='Низкий'].astype(str).tolist()
    x7_text = df1['count'][df1['issue_risk_level']=='Низкий'].astype(str)
    y7_data = df1['issue_group'][df1['issue_risk_level']=='Низкий'].tolist()

    x8_data = df1['count'][df1['issue_risk_level']=='Средний'].astype(str).tolist()
    x8_text = df1['count'][df1['issue_risk_level']=='Средний'].astype(str)
    y8_data = df1['issue_group'][df1['issue_risk_level']=='Средний'].tolist()

    x9_data = df1['count'][df1['issue_risk_level']=='Высокий'].astype(str).tolist()
    x9_text = df1['count'][df1['issue_risk_level']=='Высокий'].astype(str)
    y9_data = df1['issue_group'][df1['issue_risk_level']=='Высокий'].tolist()

    print('df3 =', df1)

    sum3 = sum(map(int, x7_data)) + sum(map(int, x8_data)) + sum(map(int, x9_data))

    incoming_ap = get_incoming_ap()
    increase_ap = get_increase_ap()
    decrease_ap = get_decrease_ap()
    outcoming_ap = get_outcoming_ap()

    y11 = incoming_ap[incoming_ap['issue_risk_level'] == 'Высокий']['count'].iloc[0]
    y12 = increase_ap[increase_ap['issue_risk_level'] == 'Высокий']['count'].iloc[0]
    y13 = (-1)*decrease_ap[decrease_ap['issue_risk_level'] == 'Высокий']['count'].iloc[0]
    y14 = (-1)*outcoming_ap[outcoming_ap['issue_risk_level'] == 'Высокий']['count'].iloc[0]

    y21 = incoming_ap[incoming_ap['issue_risk_level'] == 'Средний']['count'].iloc[0]
    y22 = increase_ap[increase_ap['issue_risk_level'] == 'Средний']['count'].iloc[0]
    y23 = (-1)*decrease_ap[decrease_ap['issue_risk_level'] == 'Средний']['count'].iloc[0]
    y24 = (-1)*outcoming_ap[outcoming_ap['issue_risk_level'] == 'Средний']['count'].iloc[0]

    y31 = incoming_ap[incoming_ap['issue_risk_level'] == 'Низкий']['count'].iloc[0]
    y32 = increase_ap[increase_ap['issue_risk_level'] == 'Низкий']['count'].iloc[0]
    y33 = (-1)*decrease_ap[decrease_ap['issue_risk_level'] == 'Низкий']['count'].iloc[0]
    y34 = (-1)*outcoming_ap[outcoming_ap['issue_risk_level'] == 'Низкий']['count'].iloc[0]

    high_ap = get_high_ap_issues()

    content = html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Br([]),
                    html.H6('''Количество недостатков по областям риска и длительностям устранения, шт.''',
                        style={'text-align':'center',
                            'font-size': '16pt',
                            'font-weight': 'bold'}),
                    html.Br([]),

                    dcc.Graph(
                        id="dashboard6-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x1_data,
                                    y=y1_data,
                                    text=x1_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Риск: Низкий <br>Количество недостатков: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": 'rgb(112,149,51)',
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                                go.Bar(
                                    x=x2_data,
                                    y=y2_data,
                                    text=x2_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Риск: Средний <br>Количество недостатков: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": 'rgb(250,216,89)',
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                                go.Bar(
                                    x=x3_data,
                                    y=y3_data,
                                    text=x3_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Риск: Высокий <br>Количество недостатков: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": 'rgb(138,36,50)',
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                barmode='stack',
                                height=200,
                                title_text=f'''До 6 месяцев – {sum1} недостатков ({round(sum1/(sum1+sum2+sum3)*100)}%)''',
                                margin={
                                                    "r": 50,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 150,
                                },
                                showlegend=False,

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                    html.Br([]),
    
                    dcc.Graph(
                        id="dashboard6-graph2",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x4_data,
                                    y=y4_data,
                                    text=x4_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Риск: Низкий <br>Количество недостатков: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": 'rgb(112,149,51)',
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                                go.Bar(
                                    x=x5_data,
                                    y=y5_data,
                                    text=x5_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Риск: Средний <br>Количество недостатков: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": 'rgb(250,216,89)',
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                                go.Bar(
                                    x=x6_data,
                                    y=y6_data,
                                    text=x6_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Риск: Высокий <br>Количество недостатков: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": 'rgb(138,36,50)',
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                # autosize=True,
                                height=200,
                                barmode='stack',
                                title_text=f'''от 6 месяцев до 1 года – {sum2} недостатков ({round(sum2/(sum1+sum2+sum3)*100)}%)''',
                                margin={
                                                    "r": 50,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 150,
                                },
                                showlegend=False,

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                    html.Br([]),
    
                    dcc.Graph(
                        id="dashboard6-graph3",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x7_data,
                                    y=y7_data,
                                    text=x7_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Риск: Низкий <br>Количество недостатков: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": 'rgb(112,149,51)',
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                                go.Bar(
                                    x=x8_data,
                                    y=y8_data,
                                    text=x8_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Риск: Средний <br>Количество недостатков: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": 'rgb(250,216,89)',
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                                go.Bar(
                                    x=x9_data,
                                    y=y9_data,
                                    text=x9_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Риск: Высокий <br>Количество недостатков: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": 'rgb(138,36,50)',
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                height=200,
                                barmode='stack',
                                title_text=f'''более 1 года – {sum3} недостатков ({round(sum3/(sum1+sum2+sum3)*100)}%)''',
                                margin={
                                                    "r": 50,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 150,
                                },
                                showlegend=False,
                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                    html.Br([]),
                ], className="six columns"),

                html.Div([
                    html.Br([]),
                    html.H6('''Динамика выявленных недостатков по уровню значимости                      ''',
                        style={'text-align':'center',
                            'font-size': '16pt',
                            'font-weight': 'bold'}),
                    html.Br([]),

                    dcc.Graph(
                        id="dashboard6-graph4",
                        figure={
                            "data": [
                                go.Waterfall(
                                    measure = ['relative', 'relative', 'relative', 'relative'],
                                    x=["Мониторинг <br>на 01.04.2021", "Выявлено по <br>проверкам 2021", "Сняты с контроля <br>на 30.11.2021", "Мониторинг <br>на 30.11.2021"],
                                    y=[y11, y12, y13, y14],
                                    # y=[49, 43, -23, -69],
                                    increasing = {"marker":{"color":"rgb(138,36,50)"}},
                                    decreasing = {"marker":{"color":"rgb(197, 116, 137)"}},
                                    textposition = "inside",
                                    cliponaxis = False,
                                    connector={'visible': False},
                                    text=[y11, y12, y13, (-1)*y14],
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Количество недостатков: %{text}""",
                                    name='Недостатки',
                                    orientation='v',
                                ),
                                
                            ],
                            "layout": go.Layout(
                                # autosize=True,
                                height=200,
                                barmode='stack',
                                xaxis = {'tickangle': 0},
                                title_text='Высокий уровень',
                                margin={
                                                    "r": 10,
                                                    "t": 50,
                                                    "b": 40,
                                                    "l": 20,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                    html.Br([]),

                    dcc.Graph(
                        id="dashboard6-graph5",
                        figure={
                            "data": [
                                go.Waterfall(
                                    measure = ['relative', 'relative', 'relative', 'relative'],
                                    x=["Мониторинг <br>на 01.04.2021", "Выявлено по <br>проверкам 2021", "Сняты с контроля <br>на 30.11.2021", "Мониторинг <br>на 30.11.2021"],
                                    y=[y21, y22, y23, y24],
                                    # y=[49, 43, -23, -69],
                                    increasing = {"marker":{"color":"rgb(250,216,89)"}},
                                    decreasing = {"marker":{"color":"rgb(251, 231, 152)"}},
                                    textposition = "inside",
                                    connector={'visible': False},
                                    text=[y21, y22, y23, (-1)*y24],
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Количество недостатков: %{text}""",
                                    name='Недостатки',
                                    orientation='v',
                                ),
                                
                            ],
                            "layout": go.Layout(
                                # autosize=True,
                                height=200,
                                barmode='stack',
                                title_text='Средний уровень',
                                margin={
                                                    "r": 10,
                                                    "t": 50,
                                                    "b": 40,
                                                    "l": 20,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                    html.Br([]),

                    dcc.Graph(
                        id="dashboard6-graph6",
                        figure={
                            "data": [
                                go.Waterfall(
                                    measure = ['relative', 'relative', 'relative', 'relative'],
                                    x=["Мониторинг <br>на 01.04.2021", "Выявлено по <br>проверкам 2021", "Сняты с контроля <br>на 30.11.2021", "Мониторинг <br>на 30.11.2021"],
                                    y=[y31, y32, y33, y34],
                                    # y=[49, 43, -23, -69],
                                    increasing = {"marker":{"color":"rgb(112,149,51)"}},
                                    decreasing = {"marker":{"color":"rgb(169, 191, 133)"}},
                                    textposition = "inside",
                                    connector={'visible': False},
                                    text=[y31, y32, y33, (-1)*y34],
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Количество недостатков: %{text}""",
                                    name='Недостатки',
                                    orientation='v',
                                ),
                                
                            ],
                            "layout": go.Layout(
                                # autosize=True,
                                height=200,
                                barmode='stack',
                                title_text='Низкий уровень',
                                margin={
                                                    "r": 10,
                                                    "t": 50,
                                                    "b": 40,
                                                    "l": 20,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="six columns"),
            ], className="row"),

            html.Div([
                html.Div([
                    html.H6(f'''Итого: {sum1+sum2+sum3} открытых недостатка''',
                    style={'text-align':'center',
                            'font-size': '16pt',
                            'font-weight': 'bold'}),
                ], className="five columns"),
                html.Div([
                    html.H6('''Итого:''',
                    style={'text-align':'center',
                            'font-size': '16pt',
                            'font-weight': 'bold'}),
                ], className="one column"),
                html.Div([
                    html.H6(y11+y21+y31,
                    style={'text-align':'center',
                            'font-size': '16pt',
                            'font-weight': 'bold'}),
                ], className="two columns"),
                html.Div([
                    html.H6(y12+y22+y32,
                    style={'text-align':'center',
                            'font-size': '16pt',
                            'font-weight': 'bold'}),
                ], className="one column"),
                html.Div([
                    html.H6(y13+y23+y33,
                    style={'text-align':'center',
                            'font-size': '16pt',
                            'font-weight': 'bold'}),
                ], className="two columns"),
                html.Div([
                    html.H6(-y14-y24-y34,
                    style={'text-align':'center',
                            'font-size': '16pt',
                            'font-weight': 'bold'}),
                ], className="one column"),
            ], className="row"),

            html.Div([
                html.Br(),
                html.H6('''Недостатки высокого уровня значимости''',
                    style={'text-align':'center',
                            'font-size': '16pt',
                            'font-weight': 'bold'}),
                html.Br([]),
                dash_table.DataTable(
                    # https://dash.plotly.com/datatable/width
                    id='high_ap_issues_table',
                    columns=[{"name": i, "id": i} for i in high_ap.columns],
                    data=high_ap.to_dict('records'),
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
        ], className="row"),
    ])

    return content

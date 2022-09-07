""" Шаблоны для отчетов по запчастям."""
import os
import numpy as np
from pathlib import Path
from datetime import date
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# from . import engine_cons
# from ..utils import get_max_date
from sqlalchemy import create_engine

import dash_table
import pandas as pd

from . import radar
from ..utils import  get_risk_table
#from flask_app import engine_analysis, engine_cons

# Добавление пазов для модуле
# sys.path.append('/opt/airflow')
# os.path.abspath(Path(__file__).parents[1])
# Адрес файла
# print(Path(__file__), flush=True)
# Адрес проекта
# print(os.getcwd()+'/front_ex/files', flush=True)

# секция настройки радара


import plotly.graph_objects as go
# from IPython.core.debugger import set_trace
# import seaborn as sns


# path_xlsx = os.getcwd()+'/front_ex/files/reestr_risk.xlsx' 
risks=get_risk_table()
risks_cols = ['Номер', 'Категория', 'Описание', 'Вероятность', 'Ущерб']
# risks = pd.read_excel(path_xlsx, engine='openpyxl', header=1)
# print(risks.head(3), flush=True)
risks.columns = risks_cols

params = [
    'Weight', 'Torque', 'Width', 'Height',
    'Efficiency', 'Power', 'Displacement'
]

def create_layout():
    """Создание шаблона"""
    # engine_cons = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    layout = html.Div([
        html.Div([
            html.Div([
                dcc.Graph(
                        id="dash8-tab-1-graph1",
                        figure={
                            "data": [
                                go.Scatterpolargl(
                                    hovertext=radar.hover_text,
                                    showlegend=False,
                                    hoverinfo="text",
                                    r = radar.trial_1_r,
                                    theta = radar.trial_1_theta,
                                    name = "Риск",
                                    mode="markers+text", 
                                    marker=dict(size=radar.p*radar.koef_resize_markers*np.array(radar.marker_size), 
                                        color ='rgb(217,217,217)', 
                                    #                 Прозрачность
                                        opacity=1,
                                        line=dict(color='grey'),
                                    ),
                                    #     hover_data={'r':False},
                                    text = radar.ball_text, 
                                    hoverlabel=dict(
                                        bgcolor='rgb(0,0,0)'
                                    )
                                    #     textfont = dict(color='black', size = 15),
                                ), 
                                go.Barpolar(
                                    r = radar.bar_r,
                                    theta = radar.bar_theta,
                                    name='Группы рисков',
                                    hovertext=radar.hover_sec_text,
                                    hoverinfo="text",
                                    marker=dict(color=radar.bar_color, 
                                                line=dict(width=1)
                                            ),
                                    showlegend=False
                                    #     marker=dict(color='frequency')
                                ),
                            ],
                            "layout": go.Layout(
                                height=radar.p*100, 
                                # width=100+100,
                                # height=fig.layout.height*p, 
                                # width=(fig.layout.width-100)*p+100  ,#900, 
                                autosize=True,
                                margin=dict(l=0, r=0, t=0, b=0),

                                polar_bargap=0, 
    
                                polar = dict(
                                    bgcolor ='White',# "rgb(223, 0, 0)",
                                        radialaxis = dict(showticklabels=False, 
                                                        ticks='',# opacity=1,
                                                        showgrid=False,
                                                        showline=False,
                                                        layer='below traces',
                                                        linecolor = 'White'
                                #                                   linewidth = 3,
                                                        ),
                                        angularaxis = dict(showticklabels=False, 
                                                        showgrid=False,
                                                        ticks='',
                                                        linecolor = 'White',
                                #                             gridwidth = 3,
                                #                              linewidth = 3,
                                        ),
                                    ),
                                # autosize=True,
                                # # barmode = 'stack', 
                                # barmode = 'group',
                                # title_text='Кол-во порожних вагонорейсов с просрочкой помесячно, ваг.',
                                # margin={"r": 0, "t": 50, "b": 20, "l": 70, },
                            ),
                        },
                        config = {'displayModeBar': False}
                ),            
            ], style={'width': radar.p*100, 'display': 'inline-block'}),
            html.Div([
                dash_table.DataTable(
                    id='table-risks',
                    columns=(
                        [{"name":i, "id":i} for i in risks_cols]
                    ),
                     data= risks.to_dict(orient='records'),
                    # columns=[{'id': c, 'name': c} for c in df.columns],
                    # page_action='none',
                    filter_action="native",
                    # filter_action='custom',
                    # filter_query='',
                    sort_action='native',
                    sort_mode='multi',
                    row_selectable='multi',
                    selected_rows=risks.index.tolist(),
                    page_action='native',
                    style_table={'height': 530, 
                            # 'width':800,
                            'overflowY': 'auto',
                            'lineHeight': '30px'},

                    editable=True,
                    merge_duplicate_headers=True,
                    style_header={
                                'backgroundColor': 'rgb(138,36,50)',
                                'color': 'white',
                                'whiteSpace':'normal',
                                'fontWeight': 'bold',
                                'font_size': '16px'
                    },
                    style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(230, 230, 230)',
                                }
                    ],
                    # fixed_rows={'headers': True},
                    style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'font_size': '12px',
                            'line-height': 0.9
                            # 'width': '100px',
                            # 'maxWidth': '100px',
                            # 'minWidth': '100px',
                        },
                    style_cell={
                            'minWidth': 10, 'maxWidth': 95, 'width': 10,'textAlign': 'left'
                        },
                    page_size=100,
                    export_format='xlsx',
                    # editable=True
                ),
                # html.Div([
                #     dash_table.DataTable(
                #             # https://dash.plotly.com/datatable/width
                #             id='table_defect',
                #             columns=[{"name": i, "id": i} for i in ['1', '2', '3']],
                #             data={'1': '1', '2': '1', '3': '1'},
                #             page_size=20,
                #             style_table={'overflowX': 'auto'},
                #             style_cell={
                #                 # all three widths are needed
                #                 'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                #                 'overflow': 'hidden',
                #                 'textOverflow': 'ellipsis',
                #                 'textAlign': 'left',
                #             },
                #             # style_cell_conditional=[
                #             #     {'if': {'column_id': "Описание недостатка"},
                #             #     'width': '20%'},
                #             #     {'if': {'column_id': "Мероприятие"},
                #             #     'width': '20%'},
                #             #     {'if': {'column_id': "Первоначальная дата окончания"},
                #             #     'width': '5%'},
                #             #     {'if': {'column_id': "Пересмотренная дата окончания"},
                #             #     'width': '5%'},
                #             #     {'if': {'column_id': "Комментарий"},
                #             #     'width': '50%'},
                #             # ],
                #             export_format='xlsx',
                #             export_headers='display',
                #             merge_duplicate_headers=True,
                #             style_header={
                #                 'backgroundColor': 'rgb(138,36,50)',
                #                 'color': 'white',
                #                 'whiteSpace':'normal',
                #                 'fontWeight': 'bold'
                #             },
                #             style_data_conditional=[
                #                 {
                #                     'if': {'row_index': 'odd'},
                #                     'backgroundColor': 'rgb(230, 230, 230)',
                #                 }
                #             ],
                #             style_data={
                #                 'whiteSpace': 'normal',
                #                 'height': 'auto',
                #             },
                #     ),]),
            ], style={'display': 'inline-block', 'width': '49%',
             'verticalAlign': 'top','margin-right': '1px','margin-left': '1px',} ),

            # # Row 4 - Закладки
            # html.Div([
            #     dcc.Tabs(id='dashboard2-tabs', value='tab-1', children=[
            #         dcc.Tab(label='Динамика недостачи', value='tab-1', className="tab",),
            #         dcc.Tab(label='По филиалам', value='tab-2', className="tab",),
            #         dcc.Tab(label='По типам запчастей', value='tab-3', className="tab",),
            #         dcc.Tab(label='По складам', value='tab-4', className="tab",),
            #     ], className="row all-tabs"),
            #     #html.Div(id='tabs-example-content')
            # ]),

            # Row 5 - Содержимое закладки
            # html.Div(id='tab-content'),
        ], className="sub_page", #style={'flex-basis': '45%', 'vertical-align': 'middle'}#'display': 'inline-block',}
                ),
    ], className="page_landscape_a3",
    )

    return layout

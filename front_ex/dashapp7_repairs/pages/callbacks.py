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
from ..utils import get_rps
from ..utils import get_tors_by_rps
from ..utils import get_tors_by_type
from ..utils import get_top_tors_by_rps
from ..utils import get_top_tors_by_type
from ..utils import get_avg_tors
from ..utils import get_tors_count
from ..utils import get_all_rps



# Количество посреднических рейсов за выбранный период
@dash_app.callback(Output(component_id='tors_amount', component_property='children'),
                   [Input('dashboard7-date-picker-range', 'start_date'),
                   Input('dashboard7-date-picker-range', 'end_date'),
                   Input('dashboard7-dropdown1', 'value'),
                   Input('dashboard7-dropdown2', 'value'),
                   Input('dashboard7-dropdown3', 'value'),
                   Input('dashboard7-tabs', 'value')])
def tors_amount(start_date, end_date, rps):
    """Вычисление количества посреднических рейсов"""


    if rps == 'Все РПС':
        rod = tuple(get_all_rps(start_date, end_date)['Род подвижного состава'].dropna())
    else:
        rod = (rps, rps)

    df0 = get_tors_count(start_date, end_date, rod)

    return df0['Количество'][0]

# Значения списка РПС
@dash_app.callback(
    Output(component_id='dashboard7-dropdown3', component_property='options'),
    [Input('dashboard7-date-picker-range', 'start_date'),
     Input('dashboard7-date-picker-range', 'end_date'),
     Input('dashboard7-dropdown1', 'value'),
     Input('dashboard7-dropdown2', 'value'),
     Input('dashboard7-dropdown3', 'value'),
     Input('dashboard7-tabs', 'value')]
)
def update_dropdown3(start_date, end_date):
    """Список значений фильтра по РПС"""

    if tab is not None:
        df0 = get_rps(start_date, end_date)
        list1 = df0['Род подвижного состава'].tolist()
        list2 = ['Все РПС'] + list1
        df1 = pd.DataFrame(list2, columns=['Род подвижного состава'])

    return [{'label': i, 'value': i} for i in df1['Род подвижного состава']]


# Построение содержимого выбранной закладки
@dash_app.callback(Output('tab-content', 'children'),
                   [Input('dashboard7-tabs', 'value'),
                   Input('dashboard7-date-picker-range', 'start_date'),
                   Input('dashboard7-date-picker-range', 'end_date'),
                   Input('dashboard7-dropdown1', 'value'),
                   Input('dashboard7-dropdown2', 'value'),
                   Input('dashboard7-dropdown3', 'value'),
                   Input('dashboard7-dropdown4', 'value')])
def render_content(tab, start_date, end_date, rps):
    """Построение содержимого выбранной закладки"""

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)


    if rps == 'Все РПС':
        rod = tuple(get_all_rps(start_date, end_date)['Род подвижного состава'].dropna())
    else:
        rod = (rps, rps)

    if tab == 'tab-1':
        """Вкладка ТОП посредников"""

        tors_rps = get_tors_by_rps(start_date=start_date, end_date=end_date)
        tors_type = get_tors_by_type(start_date=start_date, end_date=end_date)
        top_tors_rps = get_top_tors_by_rps(start_date=start_date, end_date=end_date)
        top_tors_type = get_top_tors_by_type(start_date=start_date, end_date=end_date)
        avg_tors = get_avg_tors(start_date=start_date, end_date=end_date)

        content = html.Div([
            # Первая линия
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dash7-pie1",
                        figure={
                            "data": [go.Pie(labels=tors_type['Вид ремонта'], values=tors_type["Количество ремонтов"],
                                marker={"colors": ["#D3D3D3",  "#97151c", "#191970",]}, 
                                hoverinfo='skip',
                                hovertemplate = '%{label} - %{text}',
                                text = tors_type["Количество ремонтов"].map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True)
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
                ], className="six columns",
                ),
                html.Div([
                    dcc.Graph(
                        id="dash7-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=tors_rps[(tors_rps['Вид ремонта'] == 'КР')]["РПС"].tolist(),
                                    y=tors_rps[(tors_rps['Вид ремонта'] == 'КР')]["Количество ремонтов"].tolist(),
                                    text=tors_rps[(tors_rps['Вид ремонта'] == 'КР')]["Количество ремонтов"]\
                                        .map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True).tolist(),
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Кол-во ремонтов: %{text}""",
                                    name = dt.date.today().year - 1 ,

                                    orientation='v',
                                    textposition='auto',
                                    constraintext='outside',
                                    marker={
                                        "color": "#808080",
                                        
                                    },
                                ),
                                go.Bar(
                                    x=tors_rps[(tors_rps['Вид ремонта'] == 'ДР')]["РПС"].tolist(),
                                    y=tors_rps[(tors_rps['Вид ремонта'] == 'ДР')]["Количество ремонтов"].tolist(),
                                    text=tors_rps[(tors_rps['Вид ремонта'] == 'ДР')]["Количество ремонтов"]\

                                        .map('{:,.0f}'.format).astype(str).replace(',', ' ', regex=True).tolist(),
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Кол-во ремонтов: %{text}""",
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
                                title_text='Кол-во ремонтов по РПС, шт.',
                                margin={"r": 0, "t": 50, "b": 20, "l": 70, },
                            ),
                        },
                        config={"displayModeBar": False},
                    ),
                ], className="six columns",
                ),            
            ], className="row"),
            ])
        return content
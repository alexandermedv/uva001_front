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
from ..utils import get_branch_names, get_cargo_names, get_rps
from ..utils import get_resellers_by_branches, get_resellers_by_rps
from ..utils import get_resellers_count, get_resellers_table
from ..utils import get_top_resellers, get_resellers_share, get_resellers_cargo
from ..utils import get_all_branch_names, get_all_cargo_names, get_all_rps


# Количество посреднических рейсов за выбранный период
@dash_app.callback(Output(component_id='resellers_amount', component_property='children'),
                   [Input('dashboard5-date-picker-range', 'start_date'),
                   Input('dashboard5-date-picker-range', 'end_date'),
                   Input('dashboard5-dropdown1', 'value'),
                   Input('dashboard5-dropdown2', 'value'),
                   Input('dashboard5-dropdown3', 'value'),
                   Input('dashboard5-tabs', 'value')])
def resellers_amount(start_date, end_date, filial, cargo, rps, tab):
    """Вычисление количества посреднических рейсов"""

    if filial == 'Все филиалы':
        branches = tuple(get_all_branch_names(start_date, end_date)['Наименование филиала'].dropna())
    else:
        branches = (filial, filial)

    if rps == 'Все РПС':
        rod = tuple(get_all_rps(start_date, end_date)['Род подвижного состава'].dropna())
    else:
        rod = (rps, rps)

    if cargo == 'Все грузы':
        gruz = tuple(get_all_cargo_names(start_date, end_date)['Название груза ЕТСНГ'].dropna())
    else:
        gruz = (cargo, cargo)

    df0 = get_resellers_count(start_date, end_date, branches, gruz, rod)

    return df0['Количество'][0]


# Доля посреднических рейсов за выбранный период
@dash_app.callback(Output(component_id='resellers_share', component_property='children'),
                   [Input('dashboard5-date-picker-range', 'start_date'),
                   Input('dashboard5-date-picker-range', 'end_date'),
                   Input('dashboard5-dropdown1', 'value'),
                   Input('dashboard5-dropdown2', 'value'),
                   Input('dashboard5-dropdown3', 'value'),
                   Input('dashboard5-tabs', 'value')])
def resellers_share(start_date, end_date, filial, cargo, rps, tab):
    """Вычисление доли посреднических рейсов"""

    if filial == 'Все филиалы':
        branches = tuple(get_all_branch_names(start_date, end_date)['Наименование филиала'].dropna())
    else:
        branches = (filial, filial)

    if rps == 'Все РПС':
        rod = tuple(get_all_rps(start_date, end_date)['Род подвижного состава'].dropna())
    else:
        rod = (rps, rps)

    if cargo == 'Все грузы':
        gruz = tuple(get_all_cargo_names(start_date, end_date)['Название груза ЕТСНГ'].dropna())
    else:
        gruz = (cargo, cargo)

    return get_resellers_share(start_date, end_date, branches, gruz, rod)


# Значения списка филиалов
@dash_app.callback(
    Output(component_id='dashboard5-dropdown1', component_property='options'),
    [Input('dashboard5-date-picker-range', 'start_date'),
     Input('dashboard5-date-picker-range', 'end_date'),
     Input('dashboard5-dropdown1', 'value'),
     Input('dashboard5-dropdown2', 'value'),
     Input('dashboard5-dropdown3', 'value'),
     Input('dashboard5-tabs', 'value')]
)
def update_dropdown1(start_date, end_date, filial, cargo, rps, tab):
    """Список значений фильтра по филиалам"""

    if cargo == 'Все грузы':
        gruz = tuple(get_all_cargo_names(start_date, end_date)['Название груза ЕТСНГ'].dropna())
    else:
        gruz = (cargo, cargo)

    if rps == 'Все РПС':
        rod = tuple(get_all_rps(start_date, end_date)['Род подвижного состава'].dropna())
    else:
        rod = (rps, rps)

    if tab is not None:
        df0 = get_branch_names(start_date, end_date, gruz, rod)
        list1 = df0['Наименование филиала'].tolist()
        list2 = ['Все филиалы'] + list1
        df1 = pd.DataFrame(list2, columns=['Наименование филиала'])

    return [{'label': i, 'value': i} for i in df1['Наименование филиала']]


# Значения списка групп грузов
@dash_app.callback(
    Output(component_id='dashboard5-dropdown2', component_property='options'),
    [Input('dashboard5-date-picker-range', 'start_date'),
     Input('dashboard5-date-picker-range', 'end_date'),
     Input('dashboard5-dropdown1', 'value'),
     Input('dashboard5-dropdown2', 'value'),
     Input('dashboard5-dropdown3', 'value'),
     Input('dashboard5-tabs', 'value')]
)
def update_dropdown2(start_date, end_date, filial, cargo, rps, tab):
    """Список значений фильтра по группам грузов"""

    if filial == 'Все филиалы':
        branches = tuple(get_all_branch_names(start_date, end_date)['Наименование филиала'].dropna())
    else:
        branches = (filial, filial)

    if rps == 'Все РПС':
        rod = tuple(get_all_rps(start_date, end_date)['Род подвижного состава'].dropna())
    else:
        rod = (rps, rps)
    if tab is not None:
        df0 = get_cargo_names(start_date, end_date, branches, rod)
        list1 = df0['Название груза ЕТСНГ'].tolist()
        list2 = ['Все грузы'] + list1
        df1 = pd.DataFrame(list2, columns=['Название груза ЕТСНГ'])

    return [{'label': i, 'value': i} for i in df1['Название груза ЕТСНГ']]


# Значения списка РПС
@dash_app.callback(
    Output(component_id='dashboard5-dropdown3', component_property='options'),
    [Input('dashboard5-date-picker-range', 'start_date'),
     Input('dashboard5-date-picker-range', 'end_date'),
     Input('dashboard5-dropdown1', 'value'),
     Input('dashboard5-dropdown2', 'value'),
     Input('dashboard5-dropdown3', 'value'),
     Input('dashboard5-tabs', 'value')]
)
def update_dropdown3(start_date, end_date, filial, cargo, rps, tab):
    """Список значений фильтра по РПС"""

    if filial == 'Все филиалы':
        branches = tuple(get_all_branch_names(start_date, end_date)['Наименование филиала'].dropna())
    else:
        branches = (filial, filial)
    if cargo == 'Все грузы':
        gruz = tuple(get_all_cargo_names(start_date, end_date)['Название груза ЕТСНГ'].dropna())
    else:
        gruz = (cargo, cargo)
    if tab is not None:
        df0 = get_rps(start_date, end_date, branches, gruz)
        list1 = df0['Род подвижного состава'].tolist()
        list2 = ['Все РПС'] + list1
        df1 = pd.DataFrame(list2, columns=['Род подвижного состава'])

    return [{'label': i, 'value': i} for i in df1['Род подвижного состава']]


# Построение содержимого выбранной закладки
@dash_app.callback(Output('tab-content', 'children'),
                   [Input('dashboard5-tabs', 'value'),
                   Input('dashboard5-date-picker-range', 'start_date'),
                   Input('dashboard5-date-picker-range', 'end_date'),
                   Input('dashboard5-dropdown1', 'value'),
                   Input('dashboard5-dropdown2', 'value'),
                   Input('dashboard5-dropdown3', 'value'),
                   Input('dashboard5-dropdown4', 'value')])
def render_content(tab, start_date, end_date, filial, cargo,
                   rps, sorting):
    """Построение содержимого выбранной закладки"""

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    if filial == 'Все филиалы':
        branches = tuple(get_all_branch_names(start_date, end_date)['Наименование филиала'].dropna())
    else:
        branches = (filial, filial)

    if rps == 'Все РПС':
        rod = tuple(get_all_rps(start_date, end_date)['Род подвижного состава'].dropna())
    else:
        rod = (rps, rps)

    if cargo == 'Все грузы':
        gruz = tuple(get_all_cargo_names(start_date, end_date)['Название груза ЕТСНГ'].dropna())
    else:
        gruz = (cargo, cargo)

    if tab == 'tab-1':
        """Вкладка ТОП посредников"""

        if sorting == 'Количество':
            s = 'Количество посреднических рейсов'
        elif sorting == 'Доля по количеству':
            s = 'Доля посреднических рейсов'
        df1 = get_top_resellers(start_date, end_date, branches, gruz, rod, sorting).sort_values(by=s, ascending=True)

        x1_data = df1['Количество посреднических рейсов'].astype(str).tolist()
        x1_text = df1['Количество посреднических рейсов'].astype(str)
        y1_data = df1['Название заказчика'].tolist()

        x2_data = df1['Доля посреднических рейсов'].astype(str).tolist()
        x2_text = df1['Доля посреднических рейсов'].astype(str) + "%"
        y2_data = df1['Название заказчика'].tolist()

        content = html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x1_data,
                                    y=y1_data,
                                    text=x1_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Контрагент: %{y} <br>Количество посреднических рейсов: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#B4B4B4",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Количество посреднических рейсов, шт.',
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
                        id="dashboard5-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x2_data,
                                    y=y2_data,
                                    text=x2_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Контрагент: %{y} <br>Доля посреднических рейсов: %{text}""",
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
                                title_text='Доля посреднических рейсов, %',
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
            ], className="row"),
        ])
        return content

    elif tab == 'tab-2':
        """Вкладка По филиалам"""

        if sorting == 'Количество':
            s = 'Количество посреднических рейсов'
        elif sorting == 'Доля по количеству':
            s = 'Доля посреднических рейсов'
        df0 = get_resellers_by_branches(start_date, end_date, branches, gruz, rod, sorting)

        df0['Аббревиатура филиала'] = df0['Наименование филиала']
        df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
            'ПГК - Владивостокский филиал', 'ФВлд')
        df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
            'ПГК - Воронежский филиал', 'ФВрж')
        df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
            'ПГК - Екатеринбургский филиал', 'ФЕкб')
        df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
            'ПГК - Иркутский филиал', 'ФИрк')
        df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
            'ПГК - Красноярский филиал', 'ФКрс')
        df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
            'ПГК - Московский филиал', 'ФМск')
        df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
            'ПГК - Нижегородский филиал', 'ФНжН')
        df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
            'ПГК - Новосибирский филиал', 'ФНвб')
        df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
            'ПГК - Ростовский филиал', 'ФРст')
        df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
            'ПГК - Самарский филиал', 'ФСмр')
        df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
            'ПГК - Санкт-Петербургский филиал', 'ФСПб')
        df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
            'ПГК - Саратовский филиал', 'ФСрт')
        df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
            'ПГК - Челябинский филиал', 'ФЧлб')
        df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
            'ПГК - Ярославский филиал', 'ФЯрв')
        df0['Аббревиатура филиала'] = df0['Аббревиатура филиала'].replace(
            'ПГК - Центральный Аппарат', 'ЦА')

        x1_data = df0['Количество посреднических рейсов'].astype(str).tolist()
        x1_text = df0['Количество посреднических рейсов'].astype(str)
        y1_data = df0['Аббревиатура филиала'].tolist()

        x2_data = df0['Доля посреднических рейсов'].astype(str).tolist()
        x2_text = df0['Доля посреднических рейсов'].astype(str) + "%"
        y2_data = df0['Аббревиатура филиала'].tolist()

        content = html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x1_data,
                                    y=y1_data,
                                    text=x1_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Филиал: %{y} <br>Количество посреднических рейсов: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#B4B4B4",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Количество посреднических рейсов, шт.',
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 70,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns",
                ),
            ]),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x2_data,
                                    y=y2_data,
                                    text=x2_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Филиал: %{y} <br>% посреднических рейсов: %{text}""",
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
                                title_text='Количество посреднических рейсов, %',
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 70,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns",
                ),
            ]),
        ])
        return content

    elif tab == 'tab-3':
        """Количество посреднических рейсов по РПС"""

        if sorting == 'Количество':
            s = 'Количество посреднических рейсов'
        elif sorting == 'Доля по количеству':
            s = 'Доля посреднических рейсов'
        df0 = get_resellers_by_rps(start_date, end_date, branches, gruz, rod, sorting)

        x1_data = df0['Количество посреднических рейсов'].astype(str).tolist()
        x1_text = df0['Количество посреднических рейсов'].astype(str)
        y1_data = df0['Род подвижного состава'].tolist()

        x2_data = df0['Доля посреднических рейсов'].astype(str).tolist()
        x2_text = df0['Доля посреднических рейсов'].astype(str) + "%"
        y2_data = df0['Род подвижного состава'].tolist()

        content = html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x1_data,
                                    y=y1_data,
                                    text=x1_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """РПС: %{y} <br>Количество посреднических рейсов: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#B4B4B4",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Количество посреднических рейсов, шт.',
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 70,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns",
                ),
            ]),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x2_data,
                                    y=y2_data,
                                    text=x2_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """РПС: %{y} <br>% посреднических рейсов: %{text}""",
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
                                title_text='Количество посреднических рейсов, %',
                                margin={
                                                    "r": 0,
                                                    "t": 50,
                                                    "b": 20,
                                                    "l": 70,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns",
                ),
            ]),
        ])
        return content

    elif tab == 'tab-4':
        """Вкладка По типам грузов"""

        if sorting == 'Количество':
            s = 'Количество посреднических рейсов'
        elif sorting == 'Доля по количеству':
            s = 'Доля посреднических рейсов'

        if sorting == 'Количество':
            s = 'Количество посреднических рейсов'
        elif sorting == 'Доля по количеству':
            s = 'Доля посреднических рейсов'
        df1 = get_resellers_cargo(start_date, end_date, branches, gruz, rod, sorting).sort_values(by=s, ascending=True)

        x1_data = df1['Количество посреднических рейсов'].astype(str).tolist()
        x1_text = df1['Количество посреднических рейсов'].astype(str)
        y1_data = df1['Название груза ЕТСНГ'].tolist()

        x2_data = df1['Доля посреднических рейсов'].astype(str).tolist()
        x2_text = df1['Доля посреднических рейсов'].astype(str) + "%"
        y2_data = df1['Название груза ЕТСНГ'].tolist()

        content = html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x1_data,
                                    y=y1_data,
                                    text=x1_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Груз: %{y} <br>Количество посреднических рейсов: %{text}""",
                                    name='',
                                    orientation='h',
                                    textposition='auto',
                                    marker={
                                        "color": "#B4B4B4",
                                        "line": {
                                            "color": "rgb(255, 255, 255)",
                                            "width": 2,
                                        },
                                    },
                                ),
                            ],
                            "layout": go.Layout(
                                autosize=True,
                                title_text='Количество посреднических рейсов, шт.',
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
                        id="dashboard5-graph1",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x2_data,
                                    y=y2_data,
                                    text=x2_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Груз: %{y} <br>Доля посреднических рейсов: %{text}""",
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
                                title_text='Доля посреднических рейсов, %',
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
            ], className="row"),
        ])
        return content

    elif tab == 'tab-5':
        """Динамика"""

        if sorting == 'Количество':
            s = 'Количество посреднических рейсов'
        elif sorting == 'Доля по количеству':
            s = 'Доля посреднических рейсов'
        df0 = get_resellers_table(start_date, end_date, branches, gruz, rod)

        content = html.Div([
            html.Div([
                html.Div([
                    html.Br(),
                    dash_table.DataTable(
                        id='resellers_table',
                        columns=[{"name": i, "id": i} for i in df0.columns],
                        data=df0.to_dict('records'),
                        page_size=10,
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            # all three widths are needed
                            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                        },
                        export_format='xlsx',
                        export_headers='display',
                        merge_duplicate_headers=True,
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        },
                    ),
                ]),
            ], className="row"),
        ])
        return content

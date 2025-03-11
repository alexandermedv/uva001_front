""" Интерактивные элементы для отчетов по запчастям."""
import datetime as dt
import numpy as np
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
from ..utils import get_branch_names, get_cargo_names, get_rps
from ..utils import get_resellers_by_branches, get_resellers_by_rps
from ..utils import get_resellers_count, get_resellers_table
from ..utils import get_top_resellers, get_resellers_share, get_resellers_cargo
from ..utils import get_all_branch_names, get_all_cargo_names, get_all_rps
from ..utils import get_resellers_dynamics


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

    result = '{:,.0f}'.format(df0['Количество'][0]).replace(',', ' ')

    return result


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

        if sorting == 'Количество посреднических рейсов':
            s = 'Количество посреднических рейсов'
        elif sorting == 'Доля по количеству':
            s = 'Доля посреднических рейсов'
        elif sorting == 'Количество рейсов':
            s = 'Количество рейсов'
        elif sorting == 'Сумма посреднических рейсов, руб.':
            s = 'Стоимость посреднических рейсов'
        elif sorting == 'Доля по сумме':
            s = 'Доля ст посреднических рейсов'
        elif sorting == 'Сумма, руб.':
            s = 'Стоимость рейсов'
        df1 = get_top_resellers(start_date, end_date, branches, gruz, rod, sorting).sort_values(by=s, ascending=True)

        x1_data = df1['Количество посреднических рейсов'].astype(str).tolist()
        x1_text = df1['Количество посреднических рейсов'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)
        y1_data = df1['Название заказчика'].tolist()

        x2_data = df1['Доля посреднических рейсов'].astype(str).tolist()
        x2_text = df1['Доля посреднических рейсов'].astype(str) + "%"
        y2_data = df1['Название заказчика'].tolist()

        x3_data = df1['Количество рейсов'].astype(str).tolist()
        x3_text = df1['Количество рейсов'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)
        y3_data = df1['Название заказчика'].tolist()

        x4_data = df1['Стоимость посреднических рейсов'].astype(str).tolist()
        x4_text = df1['Стоимость посреднических рейсов'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)
        y4_data = df1['Название заказчика'].tolist()

        x5_data = df1['Доля ст посреднических рейсов'].astype(str).tolist()
        x5_text = df1['Доля ст посреднических рейсов'].astype(str) + "%"
        y5_data = df1['Название заказчика'].tolist()

        x6_data = df1['Стоимость рейсов'].astype(str).tolist()
        x6_text = df1['Стоимость рейсов'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)
        y6_data = df1['Название заказчика'].tolist()

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
                                        """Контрагент: %{y} <br>Количество посреднических рейсов: %{y}""",
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
                ], className="four columns"),
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph2",
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
                ], className="four columns"),
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph3",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x3_data,
                                    y=y3_data,
                                    text=x3_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Контрагент: %{y} <br>Количество рейсов: %{text}""",
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
                                title_text='Количество рейсов, шт.',
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
                ], className="four columns"),

            ], className="row"),

            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph4",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x4_data,
                                    y=y4_data,
                                    text=x4_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                        """Контрагент: %{y} <br>Стоимость посреднических рейсов: %{text}""",
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
                                title_text='Стоимость посреднических рейсов, руб.',
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
                ], className="four columns"),
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph5",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x5_data,
                                    y=y5_data,
                                    text=x5_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Контрагент: %{y} <br>Доля стоимости посреднических рейсов: %{text}""",
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
                                title_text='Доля стоимости посреднических рейсов, %',
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
                ], className="four columns"),
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph6",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x6_data,
                                    y=y6_data,
                                    text=x6_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Контрагент: %{y} <br>Стоимость рейсов: %{text}""",
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
                                title_text='Стоимость рейсов, руб.',
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
                ], className="four columns"),

            ], className="row"),
        ])
        return content

    elif tab == 'tab-2':
        """Вкладка По филиалам"""

        # if sorting == 'Количество посреднических рейсов':
        #     s = 'Количество посреднических рейсов'
        # elif sorting == 'Доля по количеству':
        #     s = 'Доля посреднических рейсов'
        # elif sorting == 'Количество рейсов':
        #     s = 'Количество рейсов'
        # elif sorting == 'Сумма посреднических рейсов, руб.':
        #     s = 'Стоимость посреднических рейсов'
        # elif sorting == 'Доля по сумме':
        #     s = 'Доля ст посреднических рейсов'
        # elif sorting == 'Сумма, руб.':
        #     s = 'Стоимость рейсов'
        df1 = get_resellers_by_branches(start_date, end_date, branches, gruz, rod, sorting)

        df1['Аббревиатура филиала'] = df1['Наименование филиала']
        df1['Аббревиатура филиала'] = df1['Аббревиатура филиала'].replace(
            'ПГК - Владивостокский филиал', 'ФВлд')
        df1['Аббревиатура филиала'] = df1['Аббревиатура филиала'].replace(
            'ПГК - Воронежский филиал', 'ФВрж')
        df1['Аббревиатура филиала'] = df1['Аббревиатура филиала'].replace(
            'ПГК - Екатеринбургский филиал', 'ФЕкб')
        df1['Аббревиатура филиала'] = df1['Аббревиатура филиала'].replace(
            'ПГК - Иркутский филиал', 'ФИрк')
        df1['Аббревиатура филиала'] = df1['Аббревиатура филиала'].replace(
            'ПГК - Красноярский филиал', 'ФКрс')
        df1['Аббревиатура филиала'] = df1['Аббревиатура филиала'].replace(
            'ПГК - Московский филиал', 'ФМск')
        df1['Аббревиатура филиала'] = df1['Аббревиатура филиала'].replace(
            'ПГК - Нижегородский филиал', 'ФНжН')
        df1['Аббревиатура филиала'] = df1['Аббревиатура филиала'].replace(
            'ПГК - Новосибирский филиал', 'ФНвб')
        df1['Аббревиатура филиала'] = df1['Аббревиатура филиала'].replace(
            'ПГК - Ростовский филиал', 'ФРст')
        df1['Аббревиатура филиала'] = df1['Аббревиатура филиала'].replace(
            'ПГК - Самарский филиал', 'ФСмр')
        df1['Аббревиатура филиала'] = df1['Аббревиатура филиала'].replace(
            'ПГК - Санкт-Петербургский филиал', 'ФСПб')
        df1['Аббревиатура филиала'] = df1['Аббревиатура филиала'].replace(
            'ПГК - Саратовский филиал', 'ФСрт')
        df1['Аббревиатура филиала'] = df1['Аббревиатура филиала'].replace(
            'ПГК - Челябинский филиал', 'ФЧлб')
        df1['Аббревиатура филиала'] = df1['Аббревиатура филиала'].replace(
            'ПГК - Ярославский филиал', 'ФЯрв')
        df1['Аббревиатура филиала'] = df1['Аббревиатура филиала'].replace(
            'ПГК - Центральный Аппарат', 'ЦА')

        x1_data = df1['Количество посреднических рейсов'].astype(str).tolist()
        x1_text = df1['Количество посреднических рейсов'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)
        y1_data = df1['Аббревиатура филиала'].tolist()

        x2_data = df1['Доля посреднических рейсов'].astype(str).tolist()
        x2_text = df1['Доля посреднических рейсов'].astype(str) + "%"
        y2_data = df1['Аббревиатура филиала'].tolist()

        x3_data = df1['Количество рейсов'].astype(str).tolist()
        x3_text = df1['Количество рейсов'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)
        y3_data = df1['Аббревиатура филиала'].tolist()

        x4_data = df1['Стоимость посреднических рейсов'].astype(str).tolist()
        x4_text = df1['Стоимость посреднических рейсов'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)
        y4_data = df1['Аббревиатура филиала'].tolist()

        x5_data = df1['Доля ст посреднических рейсов'].astype(str).tolist()
        x5_text = df1['Доля ст посреднических рейсов'].astype(str) + "%"
        y5_data = df1['Аббревиатура филиала'].tolist()

        x6_data = df1['Стоимость рейсов'].astype(str).tolist()
        x6_text = df1['Стоимость рейсов'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)
        y6_data = df1['Аббревиатура филиала'].tolist()

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
            
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph3",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x3_data,
                                    y=y3_data,
                                    text=x3_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Филиал: %{y} <br>Количество рейсов: %{text}""",
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
                                title_text='Количество рейсов, шт.',
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
            ], className="row"),

            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph4",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x4_data,
                                    y=y4_data,
                                    text=x4_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Филиал: %{y} <br>Стоимость посреднических рейсов: %{text}""",
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
                                title_text='Стоимость посреднических рейсов, руб.',
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
            
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph5",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x5_data,
                                    y=y5_data,
                                    text=x5_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Филиал: %{y} <br>% стоимости посреднических рейсов: %{text}""",
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
                                                    "l": 70,
                                },

                            ),

                        },
                        config={"displayModeBar": False},
                    ),
                ], className="four columns",
                ),
            
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph6",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x6_data,
                                    y=y6_data,
                                    text=x6_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Филиал: %{y} <br>Стоимость рейсов: %{text}""",
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
                                title_text='Стоимость рейсов, руб.',
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
            ], className="row"),

        ])
        return content

    elif tab == 'tab-3':
        """Количество посреднических рейсов по РПС"""

        # if sorting == 'Количество':
        #     s = 'Количество посреднических рейсов'
        # elif sorting == 'Доля по количеству':
        #     s = 'Доля посреднических рейсов'
        df1 = get_resellers_by_rps(start_date, end_date, branches, gruz, rod, sorting)

        x1_data = df1['Количество посреднических рейсов'].astype(str).tolist()
        x1_text = df1['Количество посреднических рейсов'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)
        y1_data = df1['Род подвижного состава'].tolist()

        x2_data = df1['Доля посреднических рейсов'].astype(str).tolist()
        x2_text = df1['Доля посреднических рейсов'].astype(str) + "%"
        y2_data = df1['Род подвижного состава'].tolist()

        x3_data = df1['Количество рейсов'].astype(str).tolist()
        x3_text = df1['Количество рейсов'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)
        y3_data = df1['Род подвижного состава'].tolist()

        x4_data = df1['Стоимость посреднических рейсов'].astype(str).tolist()
        x4_text = df1['Стоимость посреднических рейсов'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)
        y4_data = df1['Род подвижного состава'].tolist()

        x5_data = df1['Доля ст посреднических рейсов'].astype(str).tolist()
        x5_text = df1['Доля ст посреднических рейсов'].astype(str) + "%"
        y5_data = df1['Род подвижного состава'].tolist()

        x6_data = df1['Стоимость рейсов'].astype(str).tolist()
        x6_text = df1['Стоимость рейсов'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)
        y6_data = df1['Род подвижного состава'].tolist()

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

                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph3",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x3_data,
                                    y=y3_data,
                                    text=x3_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """РПС: %{y} <br>Количество рейсов: %{text}""",
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
                                title_text='Количество рейсов, шт.',
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

            ], className="row"),

            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph4",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x4_data,
                                    y=y4_data,
                                    text=x4_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """РПС: %{y} <br>Стоимость посреднических рейсов: %{text}""",
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
                                title_text='Стоимость посреднических рейсов, руб.',
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
            
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph5",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x5_data,
                                    y=y5_data,
                                    text=x5_text,
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
                                title_text='Доля посреднических рейсов, %',
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

                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph6",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x6_data,
                                    y=y6_data,
                                    text=x6_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """РПС: %{y} <br>Стоимость рейсов: %{text}""",
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
                                title_text='Стоимость рейсов, руб.',
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

            ], className="row"),
        ])
        return content

    elif tab == 'tab-4':
        """Вкладка По типам грузов"""

        if sorting == 'Количество посреднических рейсов':
            s = 'Количество посреднических рейсов'
        elif sorting == 'Доля по количеству':
            s = 'Доля посреднических рейсов'
        elif sorting == 'Количество рейсов':
            s = 'Количество рейсов'
        elif sorting == 'Сумма посреднических рейсов, руб.':
            s = 'Стоимость посреднических рейсов'
        elif sorting == 'Доля по сумме':
            s = 'Доля ст посреднических рейсов'
        elif sorting == 'Сумма, руб.':
            s = 'Стоимость рейсов'
        df1 = get_resellers_cargo(start_date, end_date, branches, gruz, rod, sorting).sort_values(by=s, ascending=True)

        x1_data = df1['Количество посреднических рейсов'].astype(str).tolist()
        x1_text = df1['Количество посреднических рейсов'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)
        y1_data = df1['Название груза ЕТСНГ'].tolist()

        x2_data = df1['Доля посреднических рейсов'].astype(str).tolist()
        x2_text = df1['Доля посреднических рейсов'].astype(str) + "%"
        y2_data = df1['Название груза ЕТСНГ'].tolist()

        x3_data = df1['Количество рейсов'].astype(str).tolist()
        x3_text = df1['Количество рейсов'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)
        y3_data = df1['Название груза ЕТСНГ'].tolist()

        x4_data = df1['Стоимость посреднических рейсов'].astype(str).tolist()
        x4_text = df1['Стоимость посреднических рейсов'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)
        y4_data = df1['Название груза ЕТСНГ'].tolist()

        x5_data = df1['Доля ст посреднических рейсов'].astype(str).tolist()
        x5_text = df1['Доля ст посреднических рейсов'].astype(str) + "%"
        y5_data = df1['Название груза ЕТСНГ'].tolist()

        x6_data = df1['Стоимость рейсов'].astype(str).tolist()
        x6_text = df1['Стоимость рейсов'].map('{:,.0f}'.format).astype(str).replace(
            ',',' ', regex=True)
        y6_data = df1['Название груза ЕТСНГ'].tolist()

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
                ], className="four columns"),

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
                ], className="four columns"),

                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph3",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x3_data,
                                    y=y3_data,
                                    text=x3_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Груз: %{y} <br>Количество рейсов: %{text}""",
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
                                title_text='Количество рейсов, шт.',
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
                ], className="four columns"),

            ], className="row"),

            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph4",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x4_data,
                                    y=y4_data,
                                    text=x4_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Груз: %{y} <br>Стоимость посреднических рейсов: %{text}""",
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
                                title_text='Стоимость посреднических рейсов, руб.',
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
                ], className="four columns"),

                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph5",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x5_data,
                                    y=y5_data,
                                    text=x5_text,
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
                ], className="four columns"),

                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph6",
                        figure={
                            "data": [
                                go.Bar(
                                    x=x6_data,
                                    y=y6_data,
                                    text=x6_text,
                                    hoverinfo='skip',
                                    hovertemplate=
                                    """Груз: %{y} <br>Стоимость рейсов: %{text}""",
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
                                title_text='Стоимость рейсов, руб.',
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
                ], className="four columns"),

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

        df1 = get_resellers_dynamics(start_date, end_date, branches, gruz, rod)

        content = html.Div([
            # html.Div([
            #     html.Div([
            #         html.Br(),
            #         dash_table.DataTable(
            #             id='resellers_table',
            #             columns=[{"name": i, "id": i} for i in df0.columns],
            #             data=df0.to_dict('records'),
            #             page_size=10,
            #             style_table={'overflowX': 'auto'},
            #             style_cell={
            #                 # all three widths are needed
            #                 'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
            #                 'overflow': 'hidden',
            #                 'textOverflow': 'ellipsis',
            #             },
            #             export_format='xlsx',
            #             export_headers='display',
            #             merge_duplicate_headers=True,
            #             style_header={
            #                 'backgroundColor': 'rgb(230, 230, 230)',
            #                 'fontWeight': 'bold'
            #             },
            #         ),
            #     ]),
            # ], className="row"),

            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph1",
                        config={"displayModeBar": True},
                        figure={
                            'data': [
                                # go.Bar(x = df1['Начало месяца'],
                                #     y=df1['Количество рейсов'],
                                #     textposition='auto',
                                #     hoverinfo='skip',
                                #     hovertemplate="Дата: %{x}" +
                                #         "<br>Обороты по дебету, тыс. руб.: %{y:,.0f}",
                                #     marker={
                                #         "color": "#97151c",
                                #     },
                                #     name = 'Обороты по дебету',
                                #     yaxis="y1",

                                # ),
                                # go.Bar(x = df1['Месяц'],
                                #     y = df1['Количество рейсов'],
                                #     hoverinfo='skip',
                                #     hovertemplate="Дата: %{x}" +
                                #         "<br>Обороты по кредиту, тыс. руб.: %{y:,.0f}",
                                #     marker={
                                #         "color": "#006B19",
                                #     },
                                #     name='Обороты по кредиту',
                                #     yaxis="y1",
                                # ),
                                go.Scatter(x=df1['Начало месяца'],
                                    y=df1['Количество посред рейсов'],
                                    hoverinfo='skip',
                                    hovertemplate="Дата: %{x}" + "<br>Количество рейсов, шт.: %{y:,.0f}",
                                    name='Динамика посреднических рейсов',
                                    mode='lines+markers',
                                    line={"color": "#6E6E6E"},
                                    yaxis = "y2"
                                ),
                                # go.Scatter(x=df1['Начало месяца'],
                                #     y=df1['Количество рейсов'],
                                #     hoverinfo='skip',
                                #     hovertemplate="Дата: %{x}" + "<br>Количество рейсов, шт.: %{y:,.0f}",
                                #     name='Динамика посреднических рейсов',
                                #     mode='lines+markers',
                                #     line={"color": "#6E6E6E"},
                                #     yaxis = "y2"
                                # ),
                            ],
                            'layout':go.Layout(
                                title_text='''
                                    Динамика посреднических рейсов, шт.
                                    ''',
                                font={"family": "Raleway", "size": 12},
                                hovermode="closest",
                                legend={
                                    "x": 0.8,
                                    "y": 1.35,
                                    "orientation": "v",
                                    # "yanchor": "bottom",
                                },
                                yaxis=dict(
                                    title="Количество рейсов, шт."
                                ),
                                yaxis2=dict(
                                    title="Количество рейсов, шт.",
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
                    dcc.Graph(
                        id="dashboard5-graph2",
                        config={"displayModeBar": True},
                        figure={
                            'data': [
                                go.Scatter(x=df1['Начало месяца'],
                                    y=df1['Доля посред рейсов в шт'],
                                    hoverinfo='skip',
                                    hovertemplate="Дата: %{x}" + "<br>Доля посред рейсов, %: %{y:,.0f}",
                                    name='Доля посреднических рейсов в шт',
                                    mode='lines+markers',
                                    line={"color": "#6E6E6E"},
                                    yaxis = "y2"
                                ),
                            ],
                            'layout':go.Layout(
                                title_text='''
                                    Доля посреднических рейсов в шт.
                                    ''',
                                font={"family": "Raleway", "size": 12},
                                hovermode="closest",
                                legend={
                                    "x": 0.8,
                                    "y": 1.35,
                                    "orientation": "v",
                                },
                                yaxis=dict(
                                    title="Доля посред рейсов, %"
                                ),
                                yaxis2=dict(
                                    title="Количество рейсов, шт.",
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
            ], className="row"
            ),

            html.Div([
                html.Div([
                    dcc.Graph(
                        id="dashboard5-graph3",
                        config={"displayModeBar": True},
                        figure={
                            'data': [
                                go.Scatter(x=df1['Начало месяца'],
                                    y=df1['Стоимость посред рейсов'],
                                    hoverinfo='skip',
                                    hovertemplate="Дата: %{x}" + "<br>Стоимость рейсов, руб.: %{y:,.0f}",
                                    name='Количество посреднических рейсов',
                                    mode='lines+markers',
                                    line={"color": "#6E6E6E"},
                                    yaxis = "y2"
                                ),
                            ],
                            'layout':go.Layout(
                                title_text='''
                                    Динамика посреднических рейсов, руб.
                                    ''',
                                font={"family": "Raleway", "size": 12},
                                hovermode="closest",
                                legend={
                                    "x": 0.8,
                                    "y": 1.35,
                                    "orientation": "v",
                                },
                                yaxis=dict(
                                    title="Стоимость посред рейсов, руб."
                                ),
                                yaxis2=dict(
                                    title="Стоимость посред рейсов, руб.",
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
                    dcc.Graph(
                        id="dashboard5-graph4",
                        config={"displayModeBar": True},
                        figure={
                            'data': [
                                go.Scatter(x=df1['Начало месяца'],
                                    y=df1['Доля посред рейсов в руб'],
                                    hoverinfo='skip',
                                    hovertemplate="Дата: %{x}" + "<br>Доля посред рейсов, %: %{y:,.0f}",
                                    name='Доля посреднических рейсов в руб',
                                    mode='lines+markers',
                                    line={"color": "#6E6E6E"},
                                    yaxis = "y2"
                                ),
                            ],
                            'layout':go.Layout(
                                title_text='''
                                    Доля посреднических рейсов в руб.
                                    ''',
                                font={"family": "Raleway", "size": 12},
                                hovermode="closest",
                                legend={
                                    "x": 0.8,
                                    "y": 1.35,
                                    "orientation": "v",
                                },
                                yaxis=dict(
                                    title="Доля посред рейсов, %"
                                ),
                                yaxis2=dict(
                                    title="Доля посред рейсов, %",
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
                                    # "rangeslider": dict(
                                    #     visible=True,
                                    # ),
                                    "type": "date",
                                },
                            ),
                        }
                    ),
                ], className="six columns"
                ),
            ], className="row"),
        ])
        return content

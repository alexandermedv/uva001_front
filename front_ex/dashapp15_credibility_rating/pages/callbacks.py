""" Интерактивные элементы для отчета"""
import datetime as dt
import numpy as np
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import dash_table
import dash
from dash import no_update
from ..pages import dash_app
from ..utils import get_gruzes_df, get_list_go, get_go_posrednics_graph, min_date, max_date  #get_clients_df, date_filter

@dash_app.callback(
    (
        Output('client_card_body','children'),
        Output('table', 'style_data_conditional'),
        Output('gruzes_table', 'data'),
        Output('go_dd', 'options'),
        Output('go_dd', 'value')
    ),
    Input('table', 'derived_virtual_selected_row_ids'),
    State('table', 'derived_virtual_data'),
    State('table', 'derived_virtual_selected_rows'),
    prevent_initial_call=True)
def update_table_data(selected_row_ids, data, selected_rows): #, selected_cells, active_cell 
    if selected_rows:
        # Работа с выделенной строкой в dash.datatable
        dff = pd.DataFrame(data)
        dff = dff[dff['Клиент']==selected_row_ids[0]].reset_index(drop=True)
        gruzes_df = get_gruzes_df(client=selected_row_ids[0])
        # Карточка клиента
        client_card = dbc.Card(
            dbc.CardBody(
                [
                    html.Label(
                        dff['Наименование клиента'],
                        style={'font-size': 14,
                               'font-family': 'Arial',
                                'text-align': 'left',
                                'color': '#808080'},
                    ),
                    html.P('Состоит в холдинге: {}'.format(dff['Холдинг клиента'][0])),
                    html.P('ИНН: {}, ОКПО: {}'.format(dff['ИНН клиента'][0], dff['ОГРН клиента'][0])),
                    html.P(dff['ОКВЭД']),
                    html.P('Дата регистрации: {}'.format(dff['Дата регистрации клиента'][0])),
                ]
            )
        )
        # Опции для дропдауна и График посредничества 
        go_list = get_list_go(start_date=min_date, end_date=max_date, client=dff['Клиент'][0])
        return (
            client_card,
            [
                {
                    "if": {
                        "filter_query": "{{id}} = '{}'".format(i)
                    },
                    "backgroundColor": "rgba(0, 116, 217, 0.3)",
                    "border": "1px solid rgb(0, 116, 217)",
                } for i in (selected_row_ids)
            ]
            +[
                {
                    "if": {
                        "state": "selected"  # 'active' | 'selected'
                    },
                    "backgroundColor": "rgba(0, 116, 217, 0.3)",
                    "border": "1px solid rgb(0, 116, 217)",
                }
            ],
            gruzes_df.to_dict('rows'),
            go_list, # Дропдаун по грузоотправителям
            go_list[0] # выбирается первый ГО
        )
    else:
        df_zero = pd.DataFrame(columns=['Наименование груза', 'Рейсов 2020', 'Рейсов 2021', 'Рейсов 2022', 'Рейсов 2023'])
        client_card = dbc.CardBody(
            [
                html.Label(
                    "Кликни клиента на таблице и получишь информацию о нем",
                    style={'font-size': 14,
                            'text-align': 'left',
                            'color': '#808080'},
                ),
            ], className="border border-5"
        )
        return (client_card, 
                #"Click the table", 
                no_update, 
                df_zero.to_dict('rows'),
                no_update,
                no_update)

# График посредники 
@dash_app.callback(
    Output('graph_posrednics', 'figure'),
    Input('go_dd', 'value'),
    State('table', 'derived_virtual_data'),
    State('table', 'derived_virtual_selected_row_ids'))
def update_graph(go, data, selected_row_ids):
    # Тут нужно разрулить ситуацию, когда data is None
    if selected_row_ids is None:
        print('------------------selected_row_ids is None')
        raise dash.exceptions.PreventUpdate
    else: 
        dff2 = pd.DataFrame(data)
        dff2 = dff2[dff2['Клиент']==selected_row_ids[0]].reset_index(drop=True)
        client = dff2['Клиент'][0]
        try:
            gh = go['value']
        except:
            gh = go
        df_posrednics_graph = get_go_posrednics_graph(go=gh)
        fig = px.scatter(df_posrednics_graph, 
                        x='Дата раскредитования', y='Сумма услуги общая', 
                        category_orders={'Клиент': [client, list(df_posrednics_graph['Клиент'].unique()).remove(client)]}, # Эта строчка нужна, чтобы выбранный клиент всегда красился в один цвет(синий)
                        color="Клиент",
                        #trendline='ols', 
                        title='<b>Распределение вагоноотправок по ГО:</b> <br />  %s' % gh,
                        #height=600
                        )
        fig.update_layout(
            legend=dict(
            orientation="h",
            xanchor="center",
            yanchor="top",
            y=-0.15,
            x=0.5,
            #itemwidth=70,
            title_font_color='#730031',
            title_font_family="Arial",
            font=dict(
                family="Arial",
                size=12,
                color="black"
            )),
            #plot_bgcolor='#EFECEC'
        )
        return fig
""" Интерактивные элементы для отчета"""
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import dcc, html, dash_table, no_update
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
#import pandas as pd
from ..pages import dash_app
from ..utils import get_clients_df, get_gruzes_df, get_go_rating, min_date, max_date  #get_clients_df, date_filter, get_go_posrednics_graph

@dash_app.callback(
    (
        Output('table', 'style_data_conditional'),
        Output('client_card_body','children'),
        Output('gruzes_table', 'data'),
        Output('go_rating_table', 'data'),
        Output('pie_profit', 'figure'),
    ),
    Input('table', 'active_cell'),
    prevent_initial_call=True)
def update_table_data(active_cell): #, selected_cells, active_cell 
    if active_cell:
        # Работа с выделенной строкой в dash.datatable
        active_row_id = active_cell['row_id'] if active_cell else None
        active_visible_row_id = active_cell['row'] if active_cell else None
        client, dff = get_clients_df(client_id=active_row_id)
        # client = df_clients.loc[active_row_id]['Клиент']
        # dff = df_clients[df_clients['Клиент']==client].reset_index(drop=True)
        gruzes_df = get_gruzes_df(client)
        go_rating = get_go_rating(client)
        # Карточка клиента
        client_card_body = dbc.CardBody(
                    [
                        html.Label(
                            dff['Наименование клиента'],
                            style={'font-size': 14,
                                    'font-family': 'Arial',
                                    'text-align': 'left',
                                },
                        ),
                        html.P('Состоит в холдинге: {}'.format(dff['Холдинг клиента'][0])),
                        html.P('ИНН: {}, ОКПО: {}'.format(dff['ИНН клиента'][0], dff['ОГРН клиента'][0])),
                        html.P(dff['ОКВЭД']),
                        html.P('Дата регистрации: {}'.format(dff['Дата регистрации клиента'][0])),
                        html.P('Последний фин период (СПАРК): {}'.format(dff['Последний фин период'][0])),
                        html.P('Выручка посл фин период(СПАРК): {}'.format(dff['Выручка посл фин период'][0])),
                    ]
                )
        # Карточка доходности ДО
        profit_do = px.pie(names=['Критичные','Минимальные', 'Нормативные', 'Целевые'],
                    values=[dff['ДО критичн'][0], 
                            dff['ДО миним'][0], 
                            dff['ДО норматив'][0], 
                            dff['ДО целев'][0]],
                    color_discrete_sequence=['#D2042D', '#C0C0C0', '#FCD975', '#287233'],
                    title=dff['Наименование клиента'][0],
                    hole=0.85, 
                    category_orders={"names":['Критичные','Минимальные', 'Нормативные', 'Целевые']})
        profit_do.update_traces(textinfo='value+label', 
                        textposition="outside")
        profit_do.update_layout(showlegend=False,
                        #plot_bgcolor= '#FFFFF0', paper_bgcolor= '#FFFFF0'
                        )
        profit_do.add_annotation(x=0.5, y=0.5, text='ДО: Отправки', showarrow=False)
        # Опции для дропдауна и График посредничества 
        #go_list = get_list_go(start_date=min_date, end_date=max_date, client=dff['Клиент'][0])
        return (
            [
                {
                    "if": {
                        "row_index": active_visible_row_id
                    },
                    "backgroundColor": "#EFECEC", #"rgb(232, 255, 255)",
                    "border": "1px solid darkgray", #rgb(0, 116, 217)
                } #for i in (active_row_id)
            ]
            +[
                {
                    "if": {
                        "state": "active"  # 'active' | 'selected'
                    },
                    "backgroundColor": "rgba(255, 99, 71, 0.2)", #"rgba(0, 116, 217, 0.3)"
                    "border": "1px solid darkgray", #"1px solid rgb(0, 116, 217)",
                }
            ], 
            client_card_body,
            gruzes_df.to_dict('records'),
            go_rating.to_dict('records'),
            profit_do,
        )
    else:
        raise PreventUpdate
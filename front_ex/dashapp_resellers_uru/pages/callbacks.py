""" Интерактивные элементы для отчета"""
import datetime as dt
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash
from dash import dash_table, no_update, html, dcc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from ..pages import dash_app
from ..utils import  get_go_rating, get_data_for_graph, query_resellers_logs, update_postgres_resellers_log, min_date, max_date  #get_clients_df, date_filter, get_go_posrednics_graph, get_gruzes_df,
from ..pages.layout import df_client

# Глобальная переменная, нужна для того, чтобы не активировать пересчет, при активации той же строки таблицы клиентов.
cl_last_row, go_last_row = -1, -1

@dash_app.callback(
    (
            Output('client_table', 'style_data_conditional'),
            Output('client_id', 'children'),
            Output('client_name', 'children'),
            Output('client_info', 'children'),
            Output("go_rating", "page_current"),
            Output("go_rating", "data"),
            Output('go_rating', 'active_cell'),
            Output('go_rating', "selected_cells")
            #Output('client_info', 'children'),
    ),
    [
        Input('client_table', 'active_cell'),
    ],
    prevent_initial_call=True
)
def update_style_data(active_cell):
    #input_triggered = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    #if input_triggered == "client_table":
    if active_cell is None:
        raise PreventUpdate
    
    active_row_id = active_cell['row_id'] if active_cell else None
    active_visible_row_id = active_cell['row'] if active_cell else None

    global cl_last_row
        
    if active_row_id is None:
        return (no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update)
    elif active_row_id == cl_last_row: # Если выделенная строка не изменилась с прошлого клика
        return (no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update)
    else:
        cl_last_row = active_row_id
        client = df_client.loc[int(active_row_id)]['Клиент']
        client_name = df_client.loc[int(active_row_id)]['Наименование клиента']
        data_go = get_go_rating(client)
        # Это индексирование нужно для того чтобы в dash можно было выбирать строку
        data_go['id'] = data_go.index
        page_cur = 0
        go = data_go.loc[0,'Грузоотправитель']
        active_cell_go = None

        #hld_cl, fit = df_fit.loc[df_fit["Клиент"] ==client, ['Клиент (холдинг)', 'Доля ФИТ(%)']].min()
        return (
            # Стили для таблицы по Клиентам
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
            client, 
            'Клиент: '+str(client_name),
            [
                dcc.ConfirmDialogProvider(
                    id='danger_client_go_in_logs',
                    children=dbc.Button('Отправить клиента в логи', outline=True, color="danger"),
                                        #className="btn btn-danger"),
                    message='Вы хотите добавить клиента {} ({}) в таблицу с логами. Продолжить?'.format(client_name, client)
                ),
                html.Div(id='placeholder_2', children=[]),
            ],
            page_cur, # page-current для ГО
            data_go.to_dict('records'), # Построение рейтинга ГО и Список ГО для выбранного Клиента
            active_cell_go, # Если мы меняем выбор Клиента, то в таблице с ГО активную строку обнуляем
            [], # selected_cells обнуляем
            # # Доп инфо по выбранным клиенту и ГО
            # [
            #     html.H4(id='current_client_name', children=client_name),
            #     html.H4(id='current_client', children=client),
            #     #html.H4(df_client.loc[int(active_row_id)]['Наименование клиента'] + " (" + client +")"),
            #     html.P(f'Холдинг клиента: {hld_cl}'),
            #     html.P(f'Доля фитинговых перевозок: {fit} %'),
            #     dcc.ConfirmDialogProvider(
            #         id='danger_client_go_in_logs',
            #         children=dbc.Button('Отправить клиента в логи', outline=True, color="danger"),
            #                              #className="btn btn-danger"),
            #         message='Вы хотите добавить клиента {} ({}) в таблицу с логами. Продолжить?'.format(client_name, client)
            #     ),
            #     html.Div(id='placeholder_2', children=[]),
            # ], 
            # [
            #     html.P("Выбран грузоотправитель"),
            #     html.H4(go_name),
            #     html.H4(go),
            # ], 
        )
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Активная ячейка в рейтинге ГО
@dash_app.callback(
    (
        Output("graph_go_cl", "figure"),
        Output("go_rating", "style_data_conditional"), 
        Output("go_id", "children"),
        Output("go_name", "children"),
    ),
    [
        Input('go_rating', 'active_cell'),
        State('go_rating', 'data'),
        State('client_id', 'children'),
    ],
    prevent_initial_call=True
)
def update_style_data(active_cell_go, data_go, client):
    if client is None:
        raise PreventUpdate
    
    active_row_go_id = active_cell_go['row_id'] if active_cell_go is not None else None
    active_visible_row_go_id = active_cell_go['row'] if active_cell_go is not None else None
        
    global go_last_row

    if active_row_go_id is None:
        go_last_row = -1
        return (no_update, [], "Грузоотправитель не выбран", "Кликните по таблице ниже")#no_update, 
    elif active_row_go_id == go_last_row:
        return (no_update, no_update, no_update, no_update)
    else:
        #print('active_row_go_id, go_last_row = ', active_row_go_id, go_last_row)
        go_last_row = active_row_go_id
        go_id = data_go[int(active_row_go_id)]['Грузоотправитель']
        go_name = 'Грузоотправитель: ' + str(data_go[int(active_row_go_id)]['Грузоотправитель имя'])

        #hld_cl, fit = df_fit.loc[df_fit["Клиент"] ==client, ['Клиент (холдинг)', 'Доля ФИТ(%)']].min()
        df_temp = get_data_for_graph(go_id)
        df2_grouped_balak = pd.DataFrame(df_temp)
        fig = px.scatter(df2_grouped_balak, 
                         x="Дата раскредитования", y="Сумма услуги общая", 
                         #category_orders={'Клиент': [client, list(df2_grouped_balak['Клиент'].unique()).remove(client)]},
                         color='Наименование клиента',#"Клиент",
                         hover_name='Наименование клиента',
                         render_mode="svg",
                         #trendline='ols', 
                         title='<b>Распределение вагоноотправок </b> %s' % go_name + " (" + go_id +")",
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
            plot_bgcolor='#EFECEC'
        )
        return (
            fig,
            #Стили для таблицы ГО
            [
                {
                    "if": {
                        "row_index": active_visible_row_go_id
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
            go_id, 
            go_name,
        )
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@dash_app.callback(Output('pg_datatable', 'children'),
              [Input('interval_pg', 'n_intervals')])
def populate_datatable(n_intervals):
    df_resellers_logs_2 = query_resellers_logs()
    return [
        dash_table.DataTable(id='resellers_logs_2',
            columns=[
                {"name":"Дата обнаружения", "id":"Дата обнаружения"},
                {"name":"Клиент", "id":"Клиент"},
                {"name":"Наименование клиента", "id":"Наименование клиента"},
                {"name":"Комментарий", "id":"Комментарий", "editable":True, "fillspace":True},
            ],
            data=df_resellers_logs_2.to_dict('records'),
            page_size=5,
            filter_action="native",
            style_as_list_view=True,
            export_format='xlsx',
            export_headers='display',
            style_cell={
                'height': 'auto',
                #'minWidth': '160px', 'width': '180px', 'maxWidth': '200px',
                'whiteSpace': 'normal', 'fontSize': 11, 'font-family': 'Arial'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': ['Наименование клиента', 'Комментарий']},
                    'textAlign': 'left'
                },
                {
                    'if': {'column_id': ['Дата обнаружения','Клиент','Наименование клиента']},
                     'width': '20%'
                },
            ],
            style_header={
                'backgroundColor': '#EFECEC',
                'color': 'black',
                'fontWeight': 'bold'
            }
        )
    ]

# Отправить выбранного клиента в логи . P.s. кнопка "danger_client_go_in_logs" пока не работает. Возможно библиотеки python устарели. вернуться позже 
@dash_app.callback(
    [
        Output('placeholder_2', 'children'), 
        Output('resellers_logs_2', 'data'),
    ],
    [Input('danger_client_go_in_logs', 'submit_n_clicks'),],
    [State('resellers_logs_2', 'data'), 
     #State('current_client', 'children'),
     #State('current_client_name', 'children')
     State('client_id', 'children'),
     State('client_name', 'children'),
    ],
    prevent_initial_call=True
)
def client_to_logs(n_clicks_2, dataset_2, client, client_name):
    if n_clicks_2 is None:
        raise PreventUpdate
    elif client:
        print('Кнопка добавить в логи начала работу. Client =', client)
        try:
            pg_2 = pd.DataFrame(dataset_2, columns=['Дата обнаружения','Клиент','Наименование клиента','Комментарий'])
            if client in list(pg_2['Клиент']):
                output_placeholder = [html.Plaintext("Клиент {} уже есть в логах".format(client),
                                style={'color': 'red', 'font-weight': 'bold', 'font-size': 'large'})]
                print('клиент есть в логах')
                return output_placeholder, no_update
            else:
                #Если столбцы в таблице dashboard.resellers_log поменяются, то этот метод может работать некорректно
                pg_2.loc[-1, ['Дата обнаружения', 'Клиент','Наименование клиента', 'Комментарий']] = [dt.datetime.today().strftime('%d.%m.%Y'), client, client_name, None]
                pg_2.index+=1
                pg_2 = pg_2.sort_index()
                update_postgres_resellers_log(pg_2)
                output_placeholder = [html.Plaintext("Клиент {} добавлен в логи".format(client_name),
                        style={'color': 'green', 'font-weight': 'bold', 'font-size': 'large'})]
                return output_placeholder, pg_2.to_dict('records')
        except:
            no_output = [html.Plaintext("Клиент {} не был добавлен".format(client_name), style={'margin': "0px"})]
            return no_output, no_update
    else:
        print('факап. client =', client)
        
# Сохранение комментария в таблицу Postgres
@dash_app.callback(
    [Output('placeholder', 'children'), 
     Output("store", "data")],
    [Input('save_to_postgres', 'n_clicks'),],
    [State('resellers_logs_2', 'data'), 
     State('store', 'data')],
)
def df_to_postgres(n_clicks, dataset, s):
    output = html.Plaintext("Данные загружены в БД.",
                            style={'color': 'green', 'font-weight': 'bold', 'font-size': 'large'})
    no_output = html.Plaintext("", style={'margin': "0px"})

    input_triggered = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

    if input_triggered == "save_to_postgres":
        s = 6
        pg = pd.DataFrame(dataset)
        update_postgres_resellers_log(pg)
        return output, s
    elif s == 0:
        return no_output, s
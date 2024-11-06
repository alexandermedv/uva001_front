from datetime import date
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.dash_table.Format import Format, Scheme, Group
from ..utils import get_clients_df, get_values_for_levels

def create_layout():
    df_client = get_clients_df()

    df_variables, df_client_lvl_1, df_client_lvl_2 = get_values_for_levels()
    x_line_1 = df_variables.loc[df_variables['Переменная']=='x_line_1','Значение'].min()
    x_line_2 = df_variables.loc[df_variables['Переменная']=='x_line_2','Значение'].min()
    y_line_1 = df_variables.loc[df_variables['Переменная']=='y_line_1','Значение'].min()
    y_line_2 = df_variables.loc[df_variables['Переменная']=='y_line_2']['Значение'].min()
    max_x_1 = df_client_lvl_1['Доля посредничества'].max() 
    max_y_1 = df_client_lvl_1['Кол-во рейсов клиента'].max()
    max_x_2 = df_client_lvl_2['Доля посредничества'].max() 
    max_y_2 = df_client_lvl_2['Кол-во рейсов клиента'].max()

    fig_lvl_1 = go.Figure()
    fig_lvl_1.add_traces(
        px.scatter(df_client_lvl_1, x = 'Доля посредничества', y='Кол-во рейсов клиента', 
                color='point_color', color_discrete_map = {'red':'rgb(255,0,0)', 'green':'rgb(0,255,0)', 'darkgreen':'rgb(0,150,0)', 'blue':'rgb(0,0,255)', 'grey':'rgb(128,128,128)', 'yellow':'rgb(255, 204,0)'},
                hover_name='Наименование клиента', hover_data = {'point_color':False, 'Клиент':True}
                ).data,
    )
    fig_lvl_1.update_yaxes(type='log', title='Количество рейсов (log)')
    fig_lvl_1.update_xaxes(title='Доля посредничества')
    fig_lvl_1.add_trace(go.Scatter(x=[x_line_1, x_line_1], y=[0,max_y_1], 
                                mode='lines', line=dict(color="blue", width=1)))
    fig_lvl_1.add_trace(go.Scatter(x=[0,max_x_1], y=[y_line_1, y_line_1], 
                                mode='lines', line=dict(color="blue", width=1)))
    fig_lvl_1.update_layout(title='Метрика посредничества за 180 дней <br><sup>Клиенты, выделенные красным, требуют дополнительного анализа</sup>', 
                            margin=dict(r=0),
                        showlegend=False, height=700)

    fig_lvl_2 = go.Figure()
    fig_lvl_2.add_traces(
        px.scatter(df_client_lvl_2, x = 'Доля посредничества', y='Кол-во рейсов клиента', 
                color='point_color', color_discrete_map = {'red':'rgb(255,0,0)', 'green':'rgb(0,255,0)', 'darkgreen':'rgb(0,150,0)', 'blue':'rgb(0,0,255)', 'grey':'rgb(128,128,128)', 'yellow':'rgb(255, 204,0)'},
                hover_name='Наименование клиента', hover_data = {'point_color':False, 'Клиент':True}
                ).data,
    )
    fig_lvl_2.update_yaxes(type='log', title='Количество рейсов (log)')
    fig_lvl_2.update_xaxes(title='Доля посредничества')
    fig_lvl_2.add_trace(go.Scatter(x=[x_line_2, x_line_2], y=[0,max_y_2], 
                                mode='lines', line=dict(color="blue", width=1)))
    fig_lvl_2.add_trace(go.Scatter(x=[0,max_x_2], y=[y_line_2, y_line_2], 
                                mode='lines', line=dict(color="blue", width=1)))
    fig_lvl_2.update_layout(title='Метрика посредничества за 360 дней <br><sup>Клиенты, выделенные красным, требуют дополнительного анализа</sup>', 
                            margin=dict(r=0),
                        showlegend=False, height=700)
    
    layout = html.Div([
        html.Div([
            html.Div(
                children=dash_table.DataTable(
                    id='client_table',
                    columns=[
                        {"name": "Ранг", "id": "Ранг"},
                        {"name": "Клиент", "id": "Клиент"},
                        {"name": "Наименование клиента", "id": "Наименование клиента"},
                        {"name": "Кол-во рейсов клиента", "id": "Кол-во рейсов клиента", "type": "numeric",
                            "format": {'specifier': ',.0f',
                                        "locale": {"group": " "}}},
                        {"name": "Общая сумма клиента (Руб.)", "id": "Общая сумма клиента (Руб.)", "type": "numeric",
                            "format": {'specifier': ',.0f',
                                        "locale": {"group": " "}}},
                        {"name": "Средневзвешенное посредничество (Руб.)", "id": "Средневзвешенное посредничество", "type": "numeric",
                            "format": {'specifier': ',.0f',
                                        "locale": {"group": " "}}},
                        {"name": "Доля посредничества", "id": "Доля посредничества", "type": "numeric",
                            "format": {'specifier': ',.0%'}},
                        {"name": "Отношение продаж клиента к пер. годом ранее", "id": "Отношение продаж к годом ранее", 
                                "type": "numeric", "format": {'specifier': ',.2f'}},
                        {"name": "Общий рейтинг", "id": "Общий рейтинг",
                                "type": "numeric",
                            "format": {'specifier': ',.2f'}},
                    ],
                    data=df_client.to_dict('records'), 
                    page_size=10,
                    filter_action="native", sort_action="native",
                    export_format='xlsx', export_headers='display',
                    style_as_list_view=True,
                    style_cell_conditional=[
                        {
                            'if': {'column_id': ['Наименование клиента']},#, 'Ранг'
                            'textAlign': 'left'
                        },
                        {
                            'if': {'column_id': 'Ранг'},
                                'width': '50px'
                        },
                        {
                            'if': {'column_id': 'Кол-во рейсов клиента'},
                            'width': '150px'
                        },
                        {
                            'if': {'column_id': ['Общая сумма клиента (Руб.)', 'Средневзвешенное посредничество (Руб.)', 
                                                    'Отношение продаж клиента к пер. годом ранее']},
                                'width': '180px'
                        },
                    ],
                    style_cell={
                        #'height': 'auto',
                        'minWidth': '50px', 'maxWidth': '300px',
                        'whiteSpace': 'normal',
                        'fontSize': 10, 'font-family': 'Arial',
                        #'overflow': 'hidden', 'textOverflow': 'ellipsis', 
                    },
                    #style_table={"height": "500px", "overflowY": "hidden"},
                    style_header={
                        'backgroundColor': '#EFECEC',
                        'color': 'black',
                        'fontWeight': 'bold',
                        'height':'70px'
                    },
                    #fixed_rows={'headers': True},
                ),
                style=dict(margin=dict(b=0),)
            ),
            html.Hr(),
            # 2-й большой блок
            html.Div(className='row', children=
                [
                    html.Div(id='client_current_card', children = 
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        dbc.CardImg(
                                                            src="./assets/Лого ПГК серый.png",
                                                            className="img-fluid rounded-start",
                                                            style={"opacity": 0.4, "maxHeight": "225px", "maxWidth": "149"},
                                                        ),
                                                        className="col-md-4",
                                                    ),
                                                    dbc.Col(
                                                        dbc.CardBody(
                                                            [
                                                                html.Div(
                                                                    children=[
                                                                        html.H6("Клиент:"),
                                                                        html.H6("Клиент не выбран", id='client_name', style={'color':'red'}),
                                                                        html.H6("Кликните по таблице выше", id='client_id'),
                                                                        html.Br(),
                                                                        html.Div(id='client_info'),
                                                                        ]
                                                                    ),
                                                            ]
                                                        ),
                                                        className="col-md-8",
                                                    ),
                                                ],
                                            ),
                                        ]
                                    ),
                                    dbc.CardFooter(
                                        'Чтобы выбрать другого клиента, нажмите на него в таблице выше',
                                        className="card-text text-muted",
                                    ),
                                ],
                                className="h-100",
                            ),
                        ], className='six columns',
                    ),
                    html.Div(id='go_current_card', children = 
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H6("Грузоотправитель:"),
                                            html.H6("Грузоотправитель не выбран", id = 'go_name', style={'color': 'red'}),
                                            html.H6("Кликните по таблице ниже", id = 'go_id')
                                        ]
                                    ),
                                    #className="col-md-8",
                                    dbc.CardFooter(
                                        'Чтобы выбрать грузоотправителя, нажмите на него в таблице ниже',
                                        className="card-text text-muted",
                                    ),
                                ],
                                className="h-100",
                            ),
                        ], 
                        className='six columns',
                    ),
                ],
            ),
            html.Hr(style={'color':'#730031'}),
            # 3 Блок (график по распределению вагоноотправок по ГО)
            html.Div(className='row', children=
                [
                    html.Div(className='six columns', children=
                        [
                            dash_table.DataTable(id="go_rating", 
                                columns=[
                                    {"name":"Грузоотправитель", "id": "Грузоотправитель"},
                                    {"name":"Грузоотправитель имя", "id": "Грузоотправитель имя"},
                                    {"name":"Договор", "id": "Договор"},
                                    {"name":"Сумма продаж ГО у клиента", "id": "Сумма продаж ГО у клиента", 
                                            "type": "numeric", "format": {'specifier': ',.0f',
                                                                            "locale": {"group": " "}}},
                                    {"name":"Доля ГО у клиента", "id": "Доля ГО у клиента", 
                                            "type": "numeric", "format": {'specifier': ',.0%'}},
                                    {"name":"Результат анализа СПАРК", "id": "Результат анализа"},
                                    {"name":"Метрика посредничества", "id": "Метрика посредничества", 
                                                    "type": "numeric", "format": {'specifier': ',.0%'}},
                                ],
                                page_size=10,
                                sort_action="native", filter_action="native",
                                export_format='xlsx', export_headers='display', 
                                style_as_list_view=True,
                                style_cell_conditional=[
                                    {
                                        'if': {'column_id': 'Грузоотправитель'},
                                        'textAlign': 'left',
                                        'width': '10%'
                                    },
                                    {
                                        'if': {'column_id': ['Метрика посредничества', 'Сумма продаж ГО у клиента']},
                                        'width': '15%'
                                    },
                                ],
                                style_cell={
                                    'height': 'auto', 'maxheight': '50px',
                                    'minWidth': '50px', 'maxWidth': '300px',
                                    'whiteSpace': 'normal',
                                    'fontSize': 10, 'font-family': 'Arial'
                                    },
                                style_header={
                                    'backgroundColor': '#EFECEC',
                                    'color': 'black',
                                    'fontWeight': 'bold',
                                    'fontSize': 10, 'font-family': 'Arial'
                                }
                            )
                        ]
                    ),
                    html.Div(className='six columns', children=
                        [
                            dcc.Graph(id='graph_go_cl'),
                        ],
                    )
                ]
            ),
            # Блок с логированием посредников
            html.Div(className='row', children=
                [
                    html.Div(className='ten columns', children=
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.Article('Логи потенциальных посредников: '),
                                            dcc.Interval(id='interval_pg', interval=86400000, n_intervals=0), # Активация раз в день
                                            html.Div(id='pg_datatable', children=[]),
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    html.Div(className='two columns', children=[
                    html.P('Измените комментарий в таблице, нажмите Enter и кнопку ниже:'),
                    dbc.Button("Загрузить комментарии в БД", id='save_to_postgres', 
                                outline=True, color="secondary", className="me-1"),
                        # Create notification when saving to postgre
                    html.Div(id='placeholder', children=[]),
                    dcc.Store(id="store", data=0), #Тест для загрузки в postgres
                    #dcc.Interval(id='interval', interval=1000), #???
                    ]),
                ], 
                 style={'background-color': '#EFECEC',  #f6f8ff
                                            'padding': '30px'}
            ),

            # Level 1 и Level 2
            html.Div(className='row',children=
                [
                    html.Div(className='six columns', children=[]),#card_lvl_1
                    html.Div(className='six columns', children=[]),#card_lvl_2
                ]
            ),

            # Графики
            html.Div(className='row',children=
                [
                    html.Div(className='six columns', children=
                        [
                            dcc.Graph(figure=fig_lvl_1),
                            html.Article('   Клиент отправляется в логи, при выполнении следующих условий: '),
                            html.Article('   - Количество рейсов клиента за 180 последних дней >= {}'.format(y_line_1)),
                            html.Article('   - Доля посредничества клиента >= {}'.format(x_line_1)),
                            html.Article('   -------------------------------------------'),
                            html.Article('   Количество клиентов: {}'.format(len(df_client_lvl_1[df_client_lvl_1['point_color']=='red']))),
                        ]
                    ),
                    html.Div(className='six columns', children=
                        [
                            dcc.Graph(figure=fig_lvl_2),
                            html.Article('Клиент отправляется в логи, при выполнении следующих условий: '),
                            html.Article('- Количество рейсов клиента за 360 последних дней >= {}'.format(y_line_2)),
                            html.Article('- Доля посредничества клиента >= {}'.format(x_line_2)),
                            html.Article('-------------------------------------------'),
                            html.Article('Количество клиентов: {}'.format(len(df_client_lvl_2[df_client_lvl_2['point_color']=='red']))),
                        ]
                    ),
                ],
                style={'margin-left': '15px'}
            ),
            
            html.Hr(style={'color':'#730031'}),
        ], className="sub_page",)
    ], className="page_landscape_a3",)

    return layout
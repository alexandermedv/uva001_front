from datetime import date
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Format, Scheme, Group
from ..utils import get_clients_df, flag_gruz, flag_posr, flag_profit

#min_date = date(2021,1,1)
#max_date = date.today()

card_height_s = '18rem'
card_height = '36rem'

df_clients = get_clients_df() # min_date, max_date
#spark_extended_report['Дата регистрации клиента'] = pd.to_datetime(spark_extended_report['Дата регистрации клиента'], errors='coerce', format='%Y-%m-%d')

gruzes_card =  dbc.Card(
    [
        dbc.CardHeader("🚚 Изменения грузовой базы клиента", style={'fontWeight': 'bold','font-family': 'Arial', 'font-size': 14}),
        dbc.CardBody(
            dash_table.DataTable(
                id='gruzes_table',
                columns=[#{'name': 'Клиент', 'id': 'Клиент', 'type': 'text'},
                            #{'name': 'Наименование клиента', 'id': 'Наименование клиента', 'type': 'text'},
                            #{'name': 'Код груза', 'id': 'Код груза', 'type': 'text'},
                            {'name': 'Груз', 'id': 'Наименование груза', 'type': 'text'},
                            {'name': 'Рейсов 2020', 'id': 'Рейсов 2020', 'type': 'numeric', "format": {'specifier': ',.0f', "locale": {"group": " "}}},
                            {'name': 'Рейсов 2021', 'id': 'Рейсов 2021', 'type': 'numeric', "format": {'specifier': ',.0f', "locale": {"group": " "}}},
                            {'name': 'Рейсов 2022', 'id': 'Рейсов 2022', 'type': 'numeric', "format": {'specifier': ',.0f', "locale": {"group": " "}}},
                            {'name': 'Рейсов 2023', 'id': 'Рейсов 2023', 'type': 'numeric', "format": {'specifier': ',.0f', "locale": {"group": " "}}},
                            {'name': 'Рейсов 2024', 'id': 'Рейсов 2024', 'type': 'numeric', "format": {'specifier': ',.0f', "locale": {"group": " "}}},
                            ],
                style_as_list_view=True,
                sort_action="native",
                style_cell={
                    'width': '20px',
                    'minWidth': '20px',
                    'maxWidth': '20px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'text-align': 'right',
                    'font-family': 'Arial',
                    'fontSize': 10, 
                },
                style_cell_conditional=[
                        # Выравнивание текста в таблице слева
                        {
                            'if': {'column_id': 'Наименование груза'},
                            'textAlign': 'left',
                            'width': '50px','minWidth': '50px','maxWidth': '50px',
                        }# for c in ['Клиент', 'Наименование клиента', 'Холдинг клиента', 'ОКВЭД']
                    ],
                style_header={
                    'backgroundColor': '#EFECEC',
                    'fontWeight': 'bold',
                    #'text-align': 'left',
                    'font-family': 'Arial',
                    'font-size': 10,
                },
                page_action='native',
                style_table={'height': card_height, 'overflowY': 'auto'},
            ),
        ), 
    ]
)

debitors_card = dbc.Card(
    [
        dbc.CardHeader("ДЗ клиента", style={'fontWeight': 'bold','font-family': 'Arial', 'font-size': 14}),
        dbc.CardBody(
            [
                html.Label("Информация по дебиторской задолженности находится в разработке",
                            style={'font-size': 14,
                                    'text-align': 'left',
                                    'color': '#808080'},
                        ),
            ]#, className="border border-5"
        ),
    ]
)

client_card = dbc.Card(
    [
        dbc.CardHeader('Информация о клиенте',style={'fontWeight': 'bold','font-family': 'Arial', 'font-size': 14}),
        dbc.CardBody(id ='client_card_body', children=
            [
                html.Label("Для выбора клиента кликните по таблице выше",
                            style={'font-size': 14,
                                    'text-align': 'left',
                                    'color': '#808080'},
                        ),
            ], style={'height':card_height}
        ),
    ]
)

posredniki_card = dbc.Card(
    [
        dbc.CardHeader('⭐ Анализ посредничества грузоотправителей по выбранному клиенту',style={'fontWeight': 'bold','font-family': 'Arial', 'font-size': 14}),
        dbc.CardBody(
            dash_table.DataTable(
                id='go_rating_table',
                columns=[
                    {"name":"Грузоотправитель", "id": "Грузоотправитель"},
                    {"name":"Грузоотправитель имя", "id": "Грузоотправитель имя"},
                    #{"name":"Договор", "id": "Договор"},
                    {"name":"Продажи ГО у клиента", "id": "Сумма продаж ГО у клиента", 
                        "type": "numeric", "format": {'specifier': ',.0f', "locale": {"group": " "}}},
                    {"name":"Доля ГО у клиента", "id": "Доля ГО у клиента", 
                        "type": "numeric", "format": {'specifier': ',.0%'}},
                    {"name":"Анализ СПАРК", "id": "Результат анализа"},
                    # {"name":"Метрика посредничества", "id": "Метрика посредничества", 
                    #             "type": "numeric", "format": {'specifier': ',.0%'}},
                ],
                style_as_list_view=True,
                sort_action="native",
                style_cell={
                    'width': '20px', 'minWidth': '20px','maxWidth': '20px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'text-align': 'right',
                    'font-family': 'Arial', 'fontSize': 10, 
                },
                style_cell_conditional=[
                    # Выравнивание текста в таблице слева
                    {
                        'if': {'column_id': ['Грузоотправитель', 'Грузоотправитель имя']},
                        'textAlign': 'left',
                    },
                    {
                        'if': {'column_id': ['Грузоотправитель имя']},
                        'width': '35px','minWidth': '35px','maxWidth': '35px',
                    },
                ],
                style_header={
                    'backgroundColor': '#EFECEC',
                    'fontWeight': 'bold',
                    'overflowY': 'auto',
                    'font-family': 'Arial',
                    'font-size': 10,
                },
                page_action='native',
                page_size=10,
                #fixed_rows={'headers': True},
                #style_table={'height': card_height, 'overflowY': 'auto', 'margin-right': '0px'},
            ), style={'height':card_height}
        )
    ], style={'margin-right': '0px'}
)

profit_card = dbc.Card([
    dbc.CardHeader('💰 ДО: Доходность с 1 января 2023',style={'fontWeight': 'bold','font-family': 'Arial', 'font-size': 14}),
    dbc.CardBody(children=[dcc.Graph(id='pie_profit', style={'height':card_height})])  
])

cards_1 = html.Div(className='row',children=
    [
        html.Div(client_card, className='five columns'),#client_card_body
        html.Div(posredniki_card, className='seven columns'),
    ], #style={'max-height': card_height, 'width':'100%', 'margin-right': '0px'}
)

cards_2 = html.Div(className='row',
    children=[
        html.Div(profit_card, className='five columns'),
        html.Div(gruzes_card, className='seven columns'),
    ], #style={'max-height': card_height}
)

cards_3 = html.Div(className='row', 
    children=[
        html.Div(debitors_card, className='five_columns'),
        html.Div(className='seven columns'),
    ]
)

def create_layout():
    """Создание шаблона"""
    # engine_cons = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128)
    layout = html.Div([
        html.Div(className='row', children=
            [
                html.Article('''В таблице собраны данные из разных источников.
                                Данные по доходности выгружены из BW за период с 1 января 2023 по последнее воскресенье.
                            В столбце "Флаги" отмечаются алерты со следующими настройками:
                            ⭐ - Доля посредничества >= {:.0f}% ;
                            🚚 - Изменение доли основного груза >= {:.0f}% ;
                            💰 - Доля критичнодоходности >= {:.0f}% ; '''.format(flag_posr*100, flag_gruz*100, flag_profit*100),
                        style={'background-color': '#FFFFF0', 'padding': '30px', 'fontSize': 10, 'font-family': 'Arial'}
                ),
                dbc.Card(
                    dash_table.DataTable(
                        id='table',
                        columns=[
                            {'name': 'Клиент', 'id': 'Клиент', 'type': 'text'},
                            {'name': 'Наименование клиента', 'id': 'Наименование клиента', 'type': 'text'},
                            {'name': 'Кол-во рейсов ТМ', 'id': 'Кол-во рейсов ТМ', 'type': 'numeric', 'format': Format(scheme=Scheme.decimal_integer, group=Group.yes, groups=3, precision=2, group_delimiter=' ')},
                            #{'name': 'Холдинг клиента', 'id': 'Холдинг клиента', 'type': 'text'},
                            {'name': 'ДО: Доходность 2023', 'id': 'ДО: Доходность', 'type': 'numeric', 'format': Format(scheme=Scheme.decimal_integer, group=Group.yes, groups=3, precision=2, group_delimiter=' ')},
                            {'name': 'СХ: Доходность 2023', 'id': 'СХ: Доходность', 'type': 'numeric', 'format': Format(scheme=Scheme.decimal_integer, group=Group.yes, groups=3, precision=2, group_delimiter=' ')},
                            {'name': 'Доля посредничества', 'id': 'Доля посредничества', 'type':'numeric', 'format': Format(scheme=Scheme.percentage, precision=0)},
                            # {'name': 'Случаев просрочки ДЗ', 'id': 'Случаев просрочки ДЗ', 'type': 'numeric', 'format': Format(scheme=Scheme.decimal_integer, group=Group.yes, groups=3, precision=2, group_delimiter=' ')},
                            # {'name': 'Дней просрочки ДЗ', 'id': 'Дней просрочки ДЗ', 'type': 'numeric', 'format': Format(scheme=Scheme.decimal_integer, group=Group.yes, groups=3, precision=2, group_delimiter=' ')},
                            # {'name': 'Сумма просрочки', 'id': 'Сумма просрочки', 'type': 'numeric', 'format': Format(scheme=Scheme.decimal_integer, group=Group.yes, groups=3, precision=2, group_delimiter=' ')},
                            # {'name': 'Изменение доли основного груза 🚚', 'id': 'Изменение доли основного груза', 'type': 'numeric',  'format': Format(scheme=Scheme.percentage, precision=0)},
                            {'name': 'Разных грузов у клиента', 'id': 'Разных грузов у клиента', 'type': 'numeric'},
                            {'name': 'Флаги', 'id': 'Флаги', 'type': 'text'},
                        ],
                        data=df_clients.to_dict('records'), 
                        page_action='native', page_size=10,
                        filter_action="native",
                        sort_action="native",
                        style_as_list_view=True,
                        #selected_rows=[0], # Сразу активирована первая строка в таблице
                        style_cell_conditional=[
                            # Выравнивание текста в таблице слева
                            {
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['Наименование клиента'] #'Клиент', , 'Холдинг клиента'
                        ],
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        },
                        style_cell={
                            'overflow': 'hidden', 'textOverflow': 'ellipsis', 'maxWidth': 0,
                            'padding': '5px', 
                            'minWidth': 45, 'maxWidth': 120, 'width': 45,
                            'fontSize': 10, 'font-family': 'Arial'
                        },
                    )
                )
            ]
        ),
        html.Br(),
        cards_1,
        html.Br(),
        cards_2,    
        html.Br(),
        #cards_3,
    ], className="page_landscape_a3",)

    return layout

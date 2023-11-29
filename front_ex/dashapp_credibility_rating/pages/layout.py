from datetime import date
import datetime
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from ..utils import get_clients_df, date_filter
from sqlalchemy import create_engine
import dash_table
from dash_table.Format import Format, Scheme, Group

min_date = date(2020,1,1)
max_date = date.today()
flag_posr = 0.8
flag_gruz = 0.8
flag_profit = 0.8
card_height_s = '18rem'
card_height = '36rem'

df_clients = get_clients_df() # min_date, max_date
#spark_extended_report['Дата регистрации клиента'] = pd.to_datetime(spark_extended_report['Дата регистрации клиента'], errors='coerce', format='%Y-%m-%d')
df_clients['Флаги'] = ''
df_clients.loc[df_clients['Доля посредничества']>=flag_posr, 'Флаги'] += '⭐'
df_clients.loc[df_clients['Изменение доли основного груза']>=flag_gruz, 'Флаги'] += '🚚'
df_clients.loc[df_clients['Доля критичнодоходности']>=flag_profit, 'Флаги'] += '💰'

# Это индексирование нужно для того чтобы в dash можно было выбирать строку
df_clients['id'] = df_clients.index

gruzes_card =  dbc.Card(
    dbc.CardBody(
        [
            html.Label(
                "Изменения грузовой базы клиента",
                style={'font-size': 18,
                        'text-align': 'left'},
            ),
            dash_table.DataTable(
                id='gruzes_table',
                columns=[#{'name': 'Клиент', 'id': 'Клиент', 'type': 'text'},
                            #{'name': 'Наименование клиента', 'id': 'Наименование клиента', 'type': 'text'},
                            #{'name': 'Код груза', 'id': 'Код груза', 'type': 'text'},
                            {'name': 'Груз', 'id': 'Наименование груза', 'type': 'text'},
                            {'name': 'Рейсов 2020', 'id': 'Рейсов 2020', 'type': 'numeric'},
                            {'name': 'Рейсов 2021', 'id': 'Рейсов 2021', 'type': 'numeric'},
                            {'name': 'Рейсов 2022', 'id': 'Рейсов 2022', 'type': 'numeric'},
                            {'name': 'Рейсов 2023', 'id': 'Рейсов 2023', 'type': 'numeric'},
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
                            'width': '50px',
                            'minWidth': '50px',
                            'maxWidth': '50px',
                        }# for c in ['Клиент', 'Наименование клиента', 'Холдинг клиента', 'ОКВЭД']
                    ],
                style_header={
                    'backgroundColor': '#EFECEC',
                    'fontWeight': 'bold',
                    'text-align': 'left',
                    'font-family': 'Arial',
                    'font-size': 10,
                },
                page_action='native',
                style_table={'height': card_height, 'overflowY': 'auto'},
            ),
        ]#, className="border border-5"
    ), 
)

debitors_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Label(
                    "ДЗ клиента",
                    style={'font-size': 18,
                            'text-align': 'left'},
                ),
                html.Label("Информация по дебиторской задолженности находится в разработке",
                            style={'font-size': 14,
                                    'text-align': 'left',
                                    'color': '#808080'},
                        ),
            ]#, className="border border-5"
        ),
    ]
)

posredniki_card = dbc.Card(
    dbc.CardBody(
        [
            html.Label(
                "Анализ посредничества грузоотправителей по выбранному клиенту",
                className='card-title',
                style={'font-size': 18, 'text-align': 'left'},
            ),
            dash_table.DataTable(
                id='go_rating_table',
                columns=[
                    {"name":"Грузоотправитель", "id": "Грузоотправитель"},
                    {"name":"Грузоотправитель имя", "id": "Грузоотправитель имя"},
                    #{"name":"Договор", "id": "Договор"},
                    {"name":"Продажи ГО у клиента", "id": "Сумма продаж ГО у клиента", 
                        "type": "numeric", "format": {'specifier': ',.0f',
                                                                        "locale": {"group": " "}}},
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
                }, #'font-family':'Arial'
                style_cell_conditional=[
                    # Выравнивание текста в таблице слева
                    {
                        'if': {'column_id': ['Грузоотправитель']},
                        'textAlign': 'left',
                    },
                    {
                        'if': {'column_id': ['Грузоотправитель имя']},
                        'textAlign': 'left',
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
                #fixed_rows={'headers': True},
                style_table={'height': card_height, 'overflowY': 'auto', 'margin-right': '0px'},
            )
        ], style={'margin-right': '0px'}
    ), style={'margin-right': '0px'}
)

profit_card = dbc.Card([
    dbc.CardHeader('ДО: Доходность с 1 января 2023',style={'fontWeight': 'bold','font-family': 'Arial', 'font-size': 18}),
    dbc.CardBody(children=[dcc.Graph(id='pie_profit', style={'height':card_height})])  
])

cards_1 = html.Div(className='row',
    children=[
        html.Div(
            [
                html.Label(
                        "Информация о клиенте",
                        style={'font-size': 18,
                                'text-align': 'left'},
                    ),
                html.Div(id='client_card_body'),
            ],
            className='five columns'),
        html.Div(posredniki_card, className='seven columns'),
    ], style={'max-height': card_height, 'width':'100%', 'margin-right': '0px'}
)

cards_2 = html.Div(className='row',
    children=[
        html.Div(profit_card, className='five columns'),
        html.Div(gruzes_card, className='seven columns'),
    ], style={'max-height': card_height}
)

cards_3 = html.Div(className='row', 
    children=[
        html.Div(debitors_card, className='five_columns'),
        html.Div(className='five columns'),
    ]
)

def create_layout():
    """Создание шаблона"""
    # engine_cons = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    layout = html.Div([
        html.Div([
            # Row 1 - Фильтры отчета   
            dbc.Row(
                dbc.Navbar(
                [
                    html.Div('Начало периода:', 
                        style={'width': '15%', 
                        'display': 'inline-block', 'marginBottom': 15, 'margin-left': 30,'marginTop': 25,
                        'color': '#7E0046'}
                    ),
                    dcc.DatePickerSingle(
                        clearable=True,
                        id='filtr_str_date',
                        date=min_date,
                        min_date_allowed=min_date,
                        max_date_allowed=max_date,
                        initial_visible_month=min_date,
                        number_of_months_shown = 3,
                        display_format='DD.MM.YYYY',
                        style={'width': '20%', 'display': 'inline-block'}
                    ),
                    html.Div('Конец периода:', 
                        style={'width': '15%', 'display': 'inline-block', 'color': '#7E0046'}
                    ),
                    dcc.DatePickerSingle(
                        clearable=True,
                        id='filtr_end_date',
                        date=max_date,
                        min_date_allowed=min_date,
                        max_date_allowed=max_date,
                        initial_visible_month=min_date,
                        number_of_months_shown = 3,
                        display_format='DD.MM.YYYY',
                        style={'width': '20%', 'display': 'inline-block'}
                    ),
                    html.Button('Выбрать', id='submit-val', n_clicks=0,
                        style={'width': '15%',  'background-color': 'white', 'display': 'inline-block', 'color':'#7E0046',})
                ], style={'background-image': 'linear-gradient(to bottom right, #D3D3D3, #A9A9A9)'}
                ), 
            style={'margin-bottom': '16px'}
            ),
            # Row 3 - Табличка
            dbc.Row([
                #html.Strong('''Рейтинг: '''),
                html.Article('''В таблице собраны данные из разных источников.
                             Данные по доходности выгружены из BW за период с 1 января 2023 по последнее воскресенье.
                            В столбце "Флаги" отмечаются алерты со следующими настройками:
                            ⭐ - Доля посредничества >= {:.0f}% ;
                            🚚 - Изменение доли основного груза >= {:.0f}% ;
                            💰 - Доля критичнодоходности >= {:.0f}% ; '''.format(flag_posr*100, flag_gruz*100, flag_profit*100),
                     style={'background-color': '#FFFFF0', 'padding': '30px', 'fontSize': 10, 'font-family': 'Arial'}),

                dash_table.DataTable(
                    id='table',
                    columns=[
                        {'name': 'Клиент', 'id': 'Клиент', 'type': 'text'},
                        {'name': 'Наименование клиента', 'id': 'Наименование клиента', 'type': 'text'},
                        {'name': 'Холдинг клиента', 'id': 'Холдинг клиента', 'type': 'text'},
                        {'name': 'ДО: Доходность 2023', 'id': 'ДО: Доходность', 'type': 'numeric', 'format': Format(scheme=Scheme.decimal_integer, group=Group.yes, groups=3, precision=2, group_delimiter=' ')},
                        {'name': 'СХ: Доходность 2023', 'id': 'СХ: Доходность', 'type': 'numeric', 'format': Format(scheme=Scheme.decimal_integer, group=Group.yes, groups=3, precision=2, group_delimiter=' ')},
                        {'name': 'Доля посредничества ⭐', 'id': 'Доля посредничества', 'type':'numeric', 'format': Format(scheme=Scheme.percentage, precision=0)},
                        # {'name': 'Случаев просрочки ДЗ', 'id': 'Случаев просрочки ДЗ', 'type': 'numeric', 'format': Format(scheme=Scheme.decimal_integer, group=Group.yes, groups=3, precision=2, group_delimiter=' ')},
                        # {'name': 'Дней просрочки ДЗ', 'id': 'Дней просрочки ДЗ', 'type': 'numeric', 'format': Format(scheme=Scheme.decimal_integer, group=Group.yes, groups=3, precision=2, group_delimiter=' ')},
                        # {'name': 'Сумма просрочки', 'id': 'Сумма просрочки', 'type': 'numeric', 'format': Format(scheme=Scheme.decimal_integer, group=Group.yes, groups=3, precision=2, group_delimiter=' ')},
                        {'name': 'Изменение доли основного груза 🚚', 'id': 'Изменение доли основного груза', 'type': 'numeric',  'format': Format(scheme=Scheme.percentage, precision=0)},
                        {'name': 'Разных грузов у клиента', 'id': 'Разных грузов у клиента', 'type': 'numeric'},
                        {'name': 'Флаги', 'id': 'Флаги', 'type': 'text'},
                    ],
                    data=df_clients.to_dict('rows'), 
                    page_size=10,
                    filter_action="native",
                    sort_action="native",
                    style_as_list_view=True,
                    #selected_rows=[0], # Сразу активирована первая строка в таблице
                    style_cell_conditional=[
                        # Выравнивание текста в таблице слева
                        {
                            'if': {'column_id': c},
                            'textAlign': 'left'
                        } for c in ['Наименование клиента', 'Холдинг клиента'] #'Клиент', 
                    ],
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    style_cell={
                        'overflow': 'hidden', 'textOverflow': 'ellipsis', 'maxWidth': 0,
                        'padding': '5px', 
                        'minWidth': 45, 'maxWidth': 120, 'width': 45,
                        'fontSize': 11, 'font-family': 'Arial'
                    },
                    style_table={'max-height': card_height},
                    # Расшифровка строки в выпадающей подсказке
                    # tooltip_data=[
                    #     {
                    #         column: {'value': str(value), 'type': 'markdown'}
                    #         for column, value in row.items()
                    #     } for row in df_clients[['Наименование клиента', 'ОКВЭД']].to_dict('records')
                    # ],
                    # tooltip_delay=0,
                    # tooltip_duration=None,
                ),]
                ),
            html.Hr(style={'color':'#730031'}),
            # Row 4
            cards_1,
            html.Hr(style={'color':'#730031'}),
            html.Br(),
            cards_2,
            html.Hr(style={'color':'#730031'}),
            html.Br(),        
            cards_3,
            # Row 5 -
            #dbc.Alert(id='tbl_out')
        ], className="sub_page",)
    ], className="page_landscape_a3",)

    return layout

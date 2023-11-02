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
card_height_s = '18rem'
card_height = '34rem'

df_clients = get_clients_df() # min_date, max_date
#spark_extended_report['Дата регистрации клиента'] = pd.to_datetime(spark_extended_report['Дата регистрации клиента'], errors='coerce', format='%Y-%m-%d')
df_clients['Звезды'] = '⭐'
df_clients.loc[1, 'Звезды'] = '🔺'
df_clients['id'] = df_clients['Клиент']
df_clients.set_index('id', inplace=True, drop=False)

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
                style_cell={
                    'width': '20px',
                    'minWidth': '20px',
                    'maxWidth': '20px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'text-align': 'right',
                    'font-family': 'Arial',
                    'fontSize': 11, 
                }, #'font-family':'Arial'
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
                    'font-size': 11,
                },
                page_action='none',
                style_table={'height': '24rem', 'overflowY': 'auto'},
            ),
        ]#, className="border border-5"
    ), 
)

debitors_card = dbc.Card(
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
)

posredniki_card = dbc.Card(
    dbc.CardBody(
        [
            html.Label(
                "Анализ посредничества",
                className='card-title',
                style={'font-size': 18,
                        'text-align': 'left'},
            ),
            html.Label(
                "Выберите ГО:",
                style={'font-size': 14,
                        'text-align': 'left',
                        'color': '#808080'},
            ),
            dcc.Dropdown(
                id="go_dd", 
                #placeholder='Выберите Грузоотправителя (холдинг):'
            ),
            dcc.Graph(id='graph_posrednics')
        ]#, className="border border-5"
    ), 
)

cards_1 = html.Div(
    [
        html.Div(
            [
                html.Label(
                        "Информация о клиенте",
                        style={'font-size': 18,
                                'text-align': 'left'},
                    ),
                html.Div(id='client_card_body'),
            ],
            className='six columns'),
        html.Div(posredniki_card, 
                 className='six columns'),
    ], className='row'
)

cards_2 = html.Div(
    [
        html.Div(gruzes_card, className='six columns'),
        html.Div(debitors_card, className='six columns'),
    ], className='row'
)

def create_layout():
    """Создание шаблона"""
    # engine_cons = create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8')
    layout = html.Div([
        html.Div([
            # Row 1 - Описание отчета
            # dbc.Row([
            #     html.Div(
            #         [
            #             html.H5("Рейтинг добросовестности клиентов"),
            #         ], className="product",
            #     )
            # ], style={'margin-top': '8px', 'margin-bottom': '0px'}
            # ),
            # Row 2 - Фильтры отчета   
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
                html.Strong('''Рейтинг: '''),
                dash_table.DataTable(
                    id='table',
                    columns=[
                        {'name': 'Клиент', 'id': 'Клиент', 'type': 'text'},
                        {'name': 'Наименование клиента', 'id': 'Наименование клиента', 'type': 'text'},
                        {'name': 'Холдинг клиента', 'id': 'Холдинг клиента', 'type': 'text'},
                        {'name': 'Доля посредничества', 'id': 'Доля посредничества', 'type':'numeric', 'format': Format(scheme=Scheme.percentage, precision=0)},
                        # {'name': 'Случаев просрочки ДЗ', 'id': 'Случаев просрочки ДЗ', 'type': 'numeric', 'format': Format(scheme=Scheme.decimal_integer, group=Group.yes, groups=3, precision=2, group_delimiter=' ')},
                        # {'name': 'Дней просрочки ДЗ', 'id': 'Дней просрочки ДЗ', 'type': 'numeric', 'format': Format(scheme=Scheme.decimal_integer, group=Group.yes, groups=3, precision=2, group_delimiter=' ')},
                        # {'name': 'Сумма просрочки', 'id': 'Сумма просрочки', 'type': 'numeric', 'format': Format(scheme=Scheme.decimal_integer, group=Group.yes, groups=3, precision=2, group_delimiter=' ')},
                        {'name': 'Изменение доли основного груза', 'id': 'Изменение доли основного груза', 'type': 'numeric',  'format': Format(scheme=Scheme.percentage, precision=0)},
                        {'name': 'Разных грузов у клиента', 'id': 'Разных грузов у клиента', 'type': 'numeric'},
                        {'name': 'Звезды', 'id': 'Звезды', 'type': 'text'},
                    ],
                    data=df_clients.to_dict('rows'), 
                    row_selectable='single',
                    cell_selectable=True,
                    selected_rows=[0], # Сразу активирована первая строка в таблице
                    #page_action="native",
                    #page_size=10,
                    filter_action="native",
                    #sort_action="native",
                    #sort_mode="multi",
                    style_cell_conditional=[
                        # Выравнивание текста в таблице слева
                        {
                            'if': {'column_id': c},
                            'textAlign': 'left'
                        } for c in ['Клиент', 'Наименование клиента', 'Холдинг клиента', 'ОКВЭД']
                    ],
                    style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    },
                    # {
                    #     "if": {
                    #         "state": "active"  # 'active' | 'selected'
                    #     },
                    #     "backgroundColor": "rgba(0, 116, 217, 0.3)",
                    #     "border": "1px solid rgb(0, 116, 217)",
                    # },
                    # {
                    #     "if": {
                    #         "state": "selected"  # 'active' | 'selected'
                    #     },
                    #     "backgroundColor": "rgba(0, 116, 217, 0.3)",
                    #     "border": "1px solid rgb(0, 116, 217)",
                    # }
                    ],
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    # Таблица без вертикальных линий
                    style_as_list_view=True,
                    #
                    virtualization=True,
                    # Фиксируем шапку
                    #fixed_rows={'headers': True},
                    # Расстояние между строками 
                    style_cell={
                        'overflow': 'hidden', 'textOverflow': 'ellipsis', 'maxWidth': 0,
                        'padding': '5px', 
                        'minWidth': 45, 'maxWidth': 120, 'width': 45,
                        'fontSize': 11, 'font-family': 'Arial'
                    },
                    style_table={'height': 400},
                    # Расшифровка строки в выпадающей подсказке
                    tooltip_data=[
                        {
                            column: {'value': str(value), 'type': 'markdown'}
                            for column, value in row.items()
                        } for row in df_clients[['Наименование клиента', 'ОКВЭД']].to_dict('records')
                    ],
                    tooltip_delay=0,
                    tooltip_duration=None,
                ),]
                ),
            # Row 4
            cards_1,
            html.Br(),
            cards_2,
            html.Br(),
            # Row 5 -
            #dbc.Alert(id='tbl_out')
        ], className="sub_page",)
    ], className="page_landscape_a3",)

    return layout

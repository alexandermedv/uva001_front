from datetime import date
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.dash_table.Format import Format, Scheme, Group
from ..utils import get_materials_df, get_filials_df, get_ekbe_postavshiki_df, get_df_grouped_zavod_postav, get_df_grouped_zavod_for_bar, style_cell_datatable, style_header_datatable #get_df_grouped_zavod

# Перенос дашборда по закупкам на портал

materials = get_materials_df()
material_dict = materials[['Материал', 'Наим. материала']].drop_duplicates().set_index('Материал')['Наим. материала']
material_dict = material_dict.to_dict()
filials = get_filials_df()
filials_names_list = filials[['Завод', 'Завод_название']].drop_duplicates()
filials_names={filials_names_list.loc[i, 'Завод']:filials_names_list.loc[i, 'Завод_название'] for i in range(len(filials_names_list))}
#df_grouped_zavod = get_df_grouped_zavod()
ekbe_postavshiki = get_ekbe_postavshiki_df()
df_grouped_zavod_postav = get_df_grouped_zavod_postav()
df_grouped_zavod_for_bar = get_df_grouped_zavod_for_bar()

def create_layout():
    layout = html.Div([
        html.Div([
            dcc.Tabs(
                [
                    dcc.Tab(
                        html.Div(
                            [
                                html.Br(),
                                dash_table.DataTable(
                                    id='postav_table',
                                    columns = [
                                        {"id":"Поставщик", "name":"Поставщик"},
                                        {"id":"Поставщик имя", "name":"Наименование поставщик"},
                                        {"id":"ИНН поставщик", "name":"ИНН поставщик"},
                                        {"id":"ОГРН поставщик", "name":"ОГРН поставщик"},
                                        {"id":"ОКВЭД поставщик", "name":"ОКВЭД поставщик"},
                                        {"id":"Разных групп материалов", "name":"Разных групп материалов",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                        {"id":"Количество заказа 2022", "name":"Кол-во заказа 2022",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                        {"id":"Количество заказа 2023", "name":"Кол-во заказа 2023",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                        {"id":"Количество заказа 2024", "name":"Кол-во заказа 2024",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                        {"id":"Сумма во ВВ 2022", "name":"Сумма во ВВ 2022",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                        {"id":"Сумма во ВВ 2023", "name":"Сумма во ВВ 2023",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                        {"id":"Сумма во ВВ 2024", "name":"Сумма во ВВ 2024",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                        {"id":"Последний фин период", "name":"Последний фин период", "type": "numeric"},
                                        {"id":"Выручка посл фин период", "name":"Выручка посл фин период",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                        {"id":"Доля ПГК в выручке поставщика", "name":"Доля ПГК в выручке поставщика",
                                                "type": "numeric", "format": {'specifier': ',.0%'}},
                                    ],
                                    data=ekbe_postavshiki.to_dict('records'),
                                    page_size=10,
                                    filter_action="native",
                                    sort_action="native",
                                    export_format='xlsx',
                                    style_cell= style_cell_datatable,
                                    style_header= style_header_datatable
                                ),
                                html.Div(id='postav_materials_table', children=[]),
                            ]
                        ),
                        label="Поставщики",
                        className="tab",
                    ),
                    dcc.Tab(
                        html.Div(
                            [
                                html.Br(),
                                dash_table.DataTable(id = 'deviation_means_table', 
                                    data=materials.to_dict('records'),
                                    columns=[
                                        {"id": "Материал", "name": "Материал"},
                                        {"id":"Наим. материала", "name":"Наим. материала"},
                                        {"id":"Разница средних", "name":"Разница средней цены",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                        {"id":"Доля последнего года к первому", "name":"Доля последнего года к первому",
                                                "type": "numeric", "format": {'specifier': ',.0%', "locale": {"group": " "}}},
                                        # {"id":"Количество заказа 2020", "name":"Кол-во заказа 2020",
                                        #         "type": "numeric", "format": {'specifier': ',.2f',"locale": {"group": " "}}},
                                        {"id":"Количество заказа 2021", "name":"Кол-во 2021",
                                                "type": "numeric", "format": {'specifier': ',.2f',"locale": {"group": " "}}},
                                        {"id":"Количество заказа 2022", "name":"Кол-во 2022",
                                                "type": "numeric", "format": {'specifier': ',.2f',"locale": {"group": " "}}},
                                        {"id":"Количество заказа 2023", "name":"Кол-во 2023",
                                                "type": "numeric", "format": {'specifier': ',.2f',"locale": {"group": " "}}},
                                        {"id":"Количество заказа 2024", "name":"Кол-во 2024",
                                                "type": "numeric", "format": {'specifier': ',.2f',"locale": {"group": " "}}},
                                        # {"id":"Сумма во ВВ 2020", "name":"Сумма 2020",
                                        #         "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                        {"id":"Сумма во ВВ 2021", "name":"Сумма 2021",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                        {"id":"Сумма во ВВ 2022", "name":"Сумма 2022",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                        {"id":"Сумма во ВВ 2023", "name":"Сумма 2023",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                        {"id":"Сумма во ВВ 2024", "name":"Сумма 2024",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                    ],
                                    page_size=12,
                                    sort_action="native",
                                    filter_action="native",
                                    export_format='xlsx',
                                    export_headers='display',
                                    #style_as_list_view=True,
                                    style_cell_conditional=[
                                        {
                                            'if': {'column_id': 'Наим. материала'},
                                            'textAlign': 'left',
                                        },
                                        {
                                            'if': {'column_id': ['Наим. материала', 'Количество заказа 2024', 'Сумма во ВВ 2024', 'Доля последнего года к первому']},
                                            'borderRight': '1px solid rgb(167,166,166)',
                                        },
                                    ],
                                    style_cell= style_cell_datatable,
                                    style_header= style_header_datatable
                                ),
                                html.Article('Для каждого материала посчитано количество и сумма закупок за каждый год по дате поставки материала. Количество заказа в данном случае подразумевается как "Количество закупаемой продукции/услуг" за соответствующий год. Нажмите на таблицу, чтобы выбрать материал.'),
                                html.Hr(style={'color':'#730031'}),
                                dcc.Graph(id="materials_price", ),
                                html.Article('На графике каждая точка отражает информацию по закупкам выбранного материала в конкретный день у одного поставщика. Разные поставщики выделены разным цветом. По оси Y отражается средняя цена закупок за этот день у одного поставщика. А размер точки - количество закупаемой продукции/услуги. Наведи курсор на точку для более детальной информации. Линия на графие отражает динамику средней цены закупки. Она строится методом скользящей средней на основе последних пяти закупок. Количество закупаемой продукции не влияет на этот тренд(чтобы самые большие закупки не отвлекали на себя всю среднюю цену).'),
                                html.Hr(style={'color':'#730031'}),
                            ],
                        ),
                        label="Материалы",
                        className="tab",
                        #active_label_style={"color": "#FB79B3"}, Будет работать начиная с dcc ver 2.11
                    ),
                    dcc.Tab(
                        html.Div(
                            [
                                html.Br(),
                                dash_table.DataTable(
                                    id='filials_table',
                                    columns=[
                                        {"id":"Завод", "name":"Завод"},
                                        {"id":"Завод_название", "name":"Завод_название"},
                                        {"id":"id филиала", "name":"id филиала"},
                                        {"id":"Общее отклонение от среднего", "name":"Общее отклонение от среднего",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                        {"id":"Сумма во ВВ", "name":"Сумма во ВВ",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                        {"id":"Кол-во ВО", "name":"Кол-во ВО",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                        {"id":"Стоимость вагоноотправок", "name":"Стоимость вагоноотправок",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                    ],
                                    data = filials.to_dict('records'),
                                    page_size=11,
                                    filter_action="native",
                                    sort_action="native",
                                    style_cell= style_cell_datatable,
                                    style_header= style_header_datatable
                                ),
                                html.Div(id='name_zavod', className='row'),
                                html.Br(),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Graph(id='filials_hist')
                                            ], 
                                            className='col-4'
                                        ),
                                        
                                        html.Div(
                                            id='zavod_for_bar',
                                            className='col-8'
                                        )
                                    ], 
                                    className='row'
                                ),
                                html.Hr(),
                                # html.Div(
                                #     [
                                #         html.Div(html.H4('Выберите вид документа закупки:'), 
                                #                 className='col-2'),
                                #         html.Div(
                                #             dcc.Dropdown(id='vid_zak_dd', 
                                #                     options=df_grouped_zavod['Вид документа закупки'].unique(),  #[df_grouped_zavod['Вид документа закупки']!='ZUZD']
                                #                     value='ZUPR'#df_grouped_zavod.loc[0,'Вид документа закупки']
                                #             ), 
                                #             className='col'),
                                #     ],
                                #     className='row'
                                # ),
                                # html.Div(id='vid_zak_df')
                                
                            ]
                        ),
                        label="Филиалы(заводы)",
                        className="tab",
                    ),
                    dcc.Tab(
                        html.Div(
                            [
                                html.Br(),
                                dash_table.DataTable(
                                    columns = [
                                        {"id":"Завод", "name":"Завод"},
                                        {"id":"Завод_название", "name":"Завод_название"},
                                        {"id":"Поставщик", "name":"Поставщик"},
                                        {"id":"Поставщик имя", "name":"Наименование поставщик"},
                                        {"id":"Сумма во ВВ 2022", "name":"Сумма заказа 2022",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                        {"id":"Сумма во ВВ 2023", "name":"Сумма 2023",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                        {"id":"Сумма во ВВ 2024", "name":"Сумма 2024",
                                                "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                                    ],
                                    data=df_grouped_zavod_postav.to_dict(orient='records'),
                                    page_size=20,
                                    filter_action="native",
                                    sort_action="native",
                                    export_format='xlsx',
                                    style_cell= style_cell_datatable,
                                    style_header= style_header_datatable
                                ),
                            ]
                        ),
                        label="Поставщики в разрезе филиалов",
                        className="tab",
                    ),
                    dcc.Tab(html.Div(
                            [
                                html.Hr(),
                                html.H5('Данные:'),
                                html.Article('За основу взятые следующие таблицы из SAP S4: EKBE(История к документу закупки), EKKO(Заголовок док зак), EKPO(Позиция док зак), EKET(График поставок).'),
                                html.Article('Оставляем только те документы закупок, у которых есть несторнированный 101-й вид движения в MSEG'),
                                html.Article('Убираем документы закупок, где Количество заказа равно нулю'),
                                html.Article('Вид закупок(ekko."BSART") из списка: NB, ZUPR(Закупка прочих услуг ТМЦ), ZP01(Материалы).'),
                                html.Br(),
                                html.H5('Сравнение средних цен:'),
                                html.Article('Средняя цена в закупке сравнивается со средней ценой по группировке: (Вид документа закупки)-(Материал)-(ЕИ)'),
                                html.Article('При этом из расчета средних исключены поставщики: ПГК Диджитал (0001015926), ПГК Центральная Азия (0002000388), ЦКР (0001008149), ЦКР ИТ (0001012161)'),
                                html.Article(''),
                                html.Br(),
                                html.Br(),
                                html.H5('Наблюдения:'),
                                html.Article('Поставщик 0001004888  ООО "ВТОРМЕТПРОМ" - Деятельность автомобильного грузового транспорта. Вся его выручка это ПГК'),
                                html.Article('Поставщик 0001010426  ООО "ЧЕРНОБРОВКИНА" - Вся выручка за 2022г это ПГК'),
                                html.Article('Также у следующих поставщиков доля выручки от ПГК больше 80% за год или близко: 0001001480 , 0001002163 , 0001010143 , 0001003383 , 0001006771 , 0001013111 , 0001013359 , 0001015535 , 0001011495 , 0001004874'),
                                html.Article(' Поставщик и сотрудник Марина Кашина(P070000828) - Много командировок?'),
                                html.Article(' Поставщик и сотрудник АЛЕКСАНДР ЗАМЯТКИН(P070000321) - посмотреть'),
                                html.Article(' Поставщик и сотрудник ЕВГЕНИЯ ШПАК(P070000426) - закупка ноутбуков'),
                                html.Br(),
                                html.H5('На будущее:'),
                                html.Article('Проверить поставщиков, у которых много разных групп материалов.'),
                                html.Article('Посмотреть поставщиков, у которых доля ПГК в выручке из СПАРК > 50%'),
                                html.Article('Обновить данные СПАРК'),

                                html.Article('Из ekko подтянуть договоры'),
                                

                            ]
                        ),
                        label="Описание",
                        className="tab",
                    ),
                ], className="row all-tabs"
            ),
        ], className="sub_page",)
    ], className="page_landscape_a3",)

    return layout
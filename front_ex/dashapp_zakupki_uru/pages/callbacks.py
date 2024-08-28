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
from ..pages.layout import materials, material_dict, filials, filials_names, df_grouped_zavod_for_bar
from ..utils import get_df_pivot_otkl

df_pivot_otkl = get_df_pivot_otkl()

# Стиль активной строки
def style_active_row(active_visible_row_id):
    return ([
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
                "backgroundColor": "rgba(232, 212, 205, 0.7)", #"rgba(0, 116, 217, 0.3)" rgba(255, 99, 71, 0.2)
                "border": "1px solid darkgray", #"1px solid rgb(0, 116, 217)",
            }
    ])

# Выбор материала
@dash_app.callback(
    (
        Output('deviation_means_table', 'style_data_conditional'),
        Output("materials_price", 'figure'),
    ),
    [
        Input('deviation_means_table', 'active_cell'),
    ],
    prevent_initial_call=True
)
def update_style_data(active_cell):
    input_triggered = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    if active_cell is None:
        raise PreventUpdate
    
    active_row_id = active_cell['row_id'] if active_cell else None
    active_visible_row_id = active_cell['row'] if active_cell else None
        
    if active_row_id is None:
        return (no_update, no_update)
    else:
        material = materials.loc[int(active_row_id)]['Материал']
        data_material = df_pivot_otkl[df_pivot_otkl['Материал']==material].reset_index(drop=True)
        #print('data_material.info = ',  data_material.info())
        if len(data_material)>0:
            fig = px.scatter(data_material, 
                  x='Дата поставки', y='Средняя цена_день',
                  color='Поставщик имя',
                  size='size_marker',
                  hover_data = {'Поставщик имя':True, 'size_marker':False, 'Количество заказа':True},
                  #trendline="expanding", trendline_scope="overall", trendline_color_override="grey") # expanding - расширенное среднее (накопление за все время)
                  trendline="rolling",trendline_scope="overall", trendline_options=dict(window=5), trendline_color_override="grey") # скользящее среднее ( window = n - это среднее по последним n)
            fig.update_layout(
                title='Динамика средней цены по материалу: {} ({})'.format(material, material_dict[material]),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",#'#EFECEC'
                #annotations=[dict(text='Тут будет<br>аннотация', x=0.5, y=0.5, font_size=20, showarrow=False)]
            )
            fig.update_traces(marker_sizemin=3, selector=dict(type='scatter'))
            return (style_active_row(active_visible_row_id), fig)
        else:
            return (style_active_row(active_visible_row_id), [])

@dash_app.callback(
    (
        Output('filials_table', 'style_data_conditional'),
        Output('name_zavod', 'children'),
        Output('filials_hist', 'figure'),
        Output('zavod_for_bar', 'children'),
    ),
    
    Input('filials_table', 'active_cell')
)
def analytics_for_current_zavod(active_cell):
    input_triggered = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    if active_cell is None:
        raise PreventUpdate
    
    active_row_id = active_cell['row_id'] if active_cell else None
    active_visible_row_id = active_cell['row'] if active_cell else None
        
    if active_row_id is None:
        return (no_update, no_update, no_update, no_update)
    else:
        zavod = filials.loc[int(active_row_id)]['Завод']
        fig=px.bar(df_grouped_zavod_for_bar[df_grouped_zavod_for_bar['Завод']==zavod], 
            x='Вид документа закупки', 
            y='Сумма во ВВ', 
            color='Вид документа закупки',
            color_discrete_map=dict({'NB':'#C17A75', 'ZP01':'#D9D9D9', 'ZUPR':'#7E7E7E'}),
            text = df_grouped_zavod_for_bar[df_grouped_zavod_for_bar['Завод']==zavod]['Доля по виду док.'].apply(lambda x: '{0:1.0f}%'.format(100*x))
        )
        fig.update_layout(title='Закупки завода: {}'.format(filials_names[zavod]),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
            showlegend=False
        )
        
        #Таблица
        table_zavod_vidz = dash_table.DataTable(
            data=df_grouped_zavod_for_bar[(df_grouped_zavod_for_bar['Завод']==zavod)].to_dict('records'),
                columns=[
                    {"id":"Завод", "name":"Завод"},
                    {"id":"Завод_название", "name":"Завод_название"},
                    {"id":"Вид документа закупки", "name":"Вид документа закупки"},
                    {"id":"Количество заказа", "name":"Количество заказа",
                            "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                    {"id":"Сумма во ВВ", "name":"Сумма во ВВ",
                            "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                    {"id":"Ср.цена вид-завод", "name":"Ср.цена вид-завод",
                            "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                    {"id":"Средняя цена по виду зак.", "name":"Средняя цена по виду зак.",
                            "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                    {"id":"Дельта среднего", "name":"Дельта среднего",
                            "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
                    {"id":"Общее отклонение от среднего", "name":"Общее отклонение от среднего",
                            "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}}
                ],
            style_cell={
                'height': 'auto',
                'minWidth': '50px', 'maxWidth': '300px',
                'whiteSpace': 'normal',
                'fontSize': 11, 'font-family': 'Arial'
            },
            #style_cell_conditional=style_cell_conditional,
            style_header={
                'backgroundColor': '#EFECEC',
                'color': 'black',
                'fontWeight': 'bold'
            }
    )
    return style_active_row(active_visible_row_id), html.H5('Выбран завод {}: {}'.format(zavod, filials_names[zavod])), fig, table_zavod_vidz

# @app.callback(
#     Output('vid_zak_df', 'children'),
#     [
#         Input('fil_dd', 'value'),
#         Input('vid_zak_dd', 'value'),
#     ]
# )
# def vid_zak_df(zavod, vid):
#     if len(df_grouped_zavod[(df_grouped_zavod['Завод']==zavod) &\
#                                                (df_grouped_zavod['Вид документа закупки']==vid)]) >= 1000000:
#         return html.H4('Для завода {} с видом закупки {} строк больше миллиона. Выберите другой завод или вид закупки'\
#                        .format(zavod, vid))
#     else:
#         return dash_table.DataTable(data=df_grouped_zavod[(df_grouped_zavod['Завод']==zavod) &\
#                                                    (df_grouped_zavod['Вид документа закупки']==vid)]\
#                                     .sort_values(by='Общее отклонение от среднего', ascending=False).to_dict('records'),
#                              columns=[
#                                  {"id":"Завод", "name":"Завод"},
#                                  {"id":"Завод_название", "name":"Завод_название"},
#                                  {"id":"Вид документа закупки", "name":"Вид документа закупки"},
#                                  {"id":"Документ закупки", "name":"Документ закупки"},
#                                  {"id":"Материал", "name":"Материал"},
#                                  {"id":"Наим. материала", "name":"Наим. материала"},
#                                  {"id":"Количество заказа", "name":"Количество заказа",
#                                           "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
#                                  {"id":"ЕИ", "name":"ЕИ"},
#                                  {"id":"Сумма во ВВ", "name":"Сумма во ВВ",
#                                           "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
#                                  {"id":"Цена в закупке(филиал)", "name":"Цена в закупке(филиал)",
#                                           "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
#                                  {"id":"Средняя цена", "name":"Средняя цена",
#                                           "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
#                                  {"id":"Дельта среднего", "name":"Дельта среднего",
#                                           "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}},
#                                  {"id":"Общее отклонение от среднего", "name":"Общее отклонение от среднего",
#                                           "type": "numeric", "format": {'specifier': ',.0f',"locale": {"group": " "}}}
#                              ],
#                             page_size=20,
#                             filter_action='native',
#                             sort_action='native',
#                             export_format='xlsx',
#                             style_cell={
#                                 'height': 'auto',
#                                 'minWidth': '50px', 'maxWidth': '300px',
#                                 'whiteSpace': 'normal',
#                                 'fontSize': 11, 'font-family': 'Arial'
#                             },
#                             style_cell_conditional=style_cell_conditional,
#                             style_header={
#                                 'backgroundColor': '#EFECEC',
#                                 'color': 'black',
#                                 'fontWeight': 'bold'
#                             }
#                             )


# # Выбор поставщика
# @app.callback(
#     Output('postav_table', 'style_data_conditional'),
#     Output('postav_materials_table', 'children'),
#     Input('postav_table', 'active_cell'),
#     prevent_initial_call=True
# )
# def update_style_data_2(active_cell):
#     input_triggered = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
#     if active_cell is None:
#         raise PreventUpdate
    
#     active_row_id = active_cell['row_id'] if active_cell else None
#     active_visible_row_id = active_cell['row'] if active_cell else None
        
#     if active_row_id is None:
#         return (no_update, no_update)
#     else:
#         postav = ekbe_postavshiki.loc[int(active_row_id), 'Поставщик']
#         data_temp = postav_materials_2[postav_materials_2['Поставщик']==postav].reset_index(drop=True)
#         if len(data_temp)>0:
#             div_childr = [
#                 html.H5('Разбивка по группам грузов для поставщика: {}({})'.format(postav_dict[postav], postav)),
#                 dash_table.DataTable(
#                     columns = postav_materials_2_columns,
#                     data=data_temp.to_dict('records'),
#                     page_size=20,
#                     filter_action='native',
#                     sort_action='native',
#                     export_format='xlsx',
#                     style_cell={
#                         'height': 'auto',
#                         'minWidth': '50px', 'maxWidth': '300px',
#                         'whiteSpace': 'normal',
#                         'fontSize': 11, 'font-family': 'Arial'
#                     },
#                     #style_cell_conditional=style_cell_conditional,
#                     style_header={
#                         'backgroundColor': '#EFECEC',
#                         'color': 'black',
#                         'fontWeight': 'bold'
#                     },
#                 ),
#             ]
#             return (style_active_row(active_visible_row_id), div_childr)
#         else:
#             return (style_active_row(active_visible_row_id), [])


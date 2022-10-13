""" Интерактивные элементы для отчетов по запчастям."""
import datetime as dt
# from sre_parse import State
import numpy as np
from dash.dependencies import Input, Output,State
import dash
import dash_core_components as dcc
import dash_html_components as html
#import dash_table
#from dash_table.Format import Format, Scheme, Group
#from app.dashes import dashapp1
#from app.raw_sql import dashapp1_non_used_details_udv_filial
import plotly.graph_objects as go
import pandas as pd
#from .layout import layout2
#import string
# from ..utils import get_osv_detail_by_dates, get_osv_detail_by_dates2, get_osv_data
# from ..utils import get_branch_names, get_detail_type_names, get_warehouse_names
from ..pages import dash_app
from . import radar
#Показывает шарик на радаре соответствуюший выбраной ячейки в таблице 
# Перрерисовывать таблицу по выбраным ячейкам
@dash_app.callback( 
    [
        Output('dash8-tab-1-graph1', 'figure')
    ],
    [
        Input('table-risks', 'active_cell'),
        Input('table-risks', 'selected_rows'),

    ],
    [
        State('dash8-tab-1-graph1', 'figure'),
        State('table-risks', 'derived_viewport_data'), 
        State('table-risks', 'data'),         
        ],  prevent_initial_call=True, background=True
)
def show_marker(a_c,s_r,f,d_w_d,d):
    ctx=dash.callback_context
    if ctx.triggered[0]['prop_id']=='table-risks.active_cell':
        if a_c and (a_c['column'] in [0,2]):
            i0=f['data'][0]['text'].index(str(d_w_d[a_c['row']]['Номер']))
            f['data'][0]['marker']['color']=['rgb(217,217,217)' if i!=i0 else 'rgb(255,255,102)'  for i in range(len(f['data'][0]['r']))]
        else:
            f['data'][0]['marker']['color']=['rgb(217,217,217)'  for i in range(len(f['data'][0]['r']))]
    elif ctx.triggered[0]['prop_id']=='table-risks.selected_rows':
        mask=[1 if i in s_r else 0 for i in range(len(d))]
        bar_theta,bar_r,bar_bound,hover_sec_text,ball_text,trial_1_r,\
            trial_1_theta,marker_size,hover_text,bar_color=radar.main0(pd.DataFrame(d),  radar.bigest_size,radar.b,radar.koef,radar.koef_r,radar.try_resize_radius_bounds,radar.resize_balles, mask)
        if a_c and (a_c['column'] in [0,2]) and (str(d_w_d[a_c['row']]['Номер']) in ball_text):
            i0=ball_text.index(str(d_w_d[a_c['row']]['Номер']))
            f['data'][0]['marker']['color']=['rgb(217,217,217)' if i!=i0 else 'rgb(255,255,102)'  for i in range(len(ball_text))]
        else:
            f['data'][0]['marker']['color']=['rgb(217,217,217)'  for i in range(len(ball_text))]

        f['data'][0]['marker']['size']=radar.p*radar.koef_resize_markers*np.array(marker_size)
        f['data'][0]['text']=[ str (i) for i in ball_text]
        f['data'][0]['theta']=trial_1_theta
        f['data'][0]['r']=trial_1_r
        f['data'][0]['hovertext']=hover_text
        f['data'][1]['hovertext']=hover_sec_text
        f['data'][1]['theta']=bar_theta
        f['data'][1]['r']=bar_r
        f['data'][1]['marker']['color']=bar_color
                                        
    else:
        raise dash.exceptions.PreventUpdate
    return [f]

# Select all
@dash_app.callback( 
    [
        Output('table-risks', 'selected_rows'),
        Output('checklist_select_all', 'value'),
    ],
    [
        Input('checklist_select_all', 'value'),
        Input('table-risks', 'selected_rows'),
    ],
    [
        State('table-risks', 'data'), 
        ],  prevent_initial_call=True, background=True
)
def sellect_all(v,s_r,d):
    ctx=dash.callback_context
    if ctx.triggered[0]['prop_id']=='checklist_select_all.value':
            if v==[]:
                return [[],v]
            else:
                return [[i for i in range (len(d))],v]
    else:
        if ((v==[]) & (len(s_r)!=len(d))) | ((v!=[]) & (len(s_r)==len(d))) :
            raise dash.exceptions.PreventUpdate
        elif len(s_r)!=len(d):
            return [s_r,[]]
        else:
            return [s_r,['Select all']]


# @dash_app.callback( 
#     [
#         Output('table-risks', 'selected_rows'),
#     ],
#     [
#         Input('checklist_select_all', 'value'),
#     ],
#     [
#         State('table-risks', 'selected_rows'),  
#         State('table-risks', 'data'), 
#         ],  prevent_initial_call=True, background=True
# )
# def sellect_all(v,s_r,d):
#     ctx=dash.callback_context
#     if v==[]:
#         return [[]]
#     else:
#         return [[i for i in range (len(d))]]
# # unSelect all
# @dash_app.callback( 
#     [
#         Output('checklist_select_all', 'value'),
#     ],
#     [
#         Input('table-risks', 'selected_rows'),  
#     ],
#     [
 
#         State('table-risks', 'data'), 
#         State('checklist_select_all', 'value'),
#         ],  prevent_initial_call=True, background=True
# )
# def unsellect_all(s_r,d,v):
#     ctx=dash.callback_context
#     if ((v==[]) & (len(s_r)!=len(d))) | ((v!=[]) & (len(s_r)==len(d))) :
#         raise dash.exceptions.PreventUpdate
#     elif len(s_r)!=len(d):
#         return [[]]
#     else:
#          [['Select all']]
# #     bar_theta,bar_r,bar_bound,hover_sec_text,ball_text,trial_1_r,
# trial_1_theta,marker_size,hover_text,bar_color=radar.main0(d,s_r)
    
#   
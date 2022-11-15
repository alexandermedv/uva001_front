import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Output, Input, State
# from dash.dash_table.Format import Format, Group
import dash_bootstrap_components as dbc
import dash_table
from datetime import date
import pandas as pd
import os
from functools import lru_cache
import pyhdb
import datetime as dt
from datetime import datetime
import numpy as np
import dash
from sqlalchemy import create_engine
from . import dash_app as app
from ..utils import  get_credit_data, get_credit_data_bseg, get_saldo_bseg, get_distinct_comp_bseg, get_credit_data_all, get_credit_data_clients#get_credit_data_filials,
# from .utils import get_limit_oper_client_zuonr_data, get_limit1, get_limit
def sum_nonlimit(s , n=0.13):
    if n in s.values:
        return n
    else:
        return s.sum()
def get_matrix_stat_1(df3_1, s_d=None, e_d=None, tol_dept=1):
    if s_d is not None:
        df3_1=df3_1[df3_1['date']>=s_d]
    if e_d is not None:
        df3_1=df3_1[df3_1['date']<=e_d]
    if df3_1.shape[0]==0:
        return pd.DataFrame()
    df3_1=df3_1.sort_values([ 'id_rcm', 'client_name','date'])
    df6=pd.DataFrame()
    i0=0
    res=0
    dg_n=0
    for dg, dt, dp in df3_1[[ 'id_rcm', 'date','dept_over_lim']].values:
        if dg_n==0:
            # set_trace()
            dg_n=dg
            m=dp
        elif  dg_n!=dg:
            # set_trace()
            # print(dg)
            df6_1=pd.DataFrame({'id_rcm': [dg_n],
            'res': [res],
            'max': [m]})
            df6=pd.concat([df6, df6_1], ignore_index=True)
            if (dp>0):
                res=1
                i0=dp
            else:
                i0=0
            m=dp
            dg_n=dg
        else:
            if (i0==0) & (dp>0):
                res=res+1
                i0=dp
            elif (dp==0):
                i0=0
            if dp>m:
                m=dp
    df6_1=pd.DataFrame({'id_rcm': [dg_n],
            'res': [res],
            'max': [m]})
    df6=pd.concat([df6, df6_1], ignore_index=True)
    col0=[i  for i in ['client_name', 
        'dog_number','yur_hold',
       # 'date',  
        'dinamic_saldo', 'lim_sum',
       'dept_over_lim', #'rating', 'garanty',
       'res','max'] if (i in df3_1.columns) | (i in df6.columns )]
    
    # df3_1=df3_1[[ i for i in df3_1.columns if i not in ['rating', 'garanty']]]
    # df3_1=df3_1.loc[df3_1['date']==df3_1['date'].max(),].merge(df6, left_on='id_rcm', right_on='id_rcm')[col0].sort_values(['dept_over_lim','dinamic_saldo', ],  ascending=False)

    return df3_1.loc[(df3_1['date']==df3_1['date'].max()) & (df3_1['dinamic_saldo']>tol_dept)].merge(df6, left_on='id_rcm', right_on='id_rcm')[col0].sort_values(['dept_over_lim','dinamic_saldo', ],  ascending=False)
def get_matrix_stat_2(df3_1,  e_d=None, tol_dept=1):
    if (e_d is None) :
        df3_1=df3_1.loc[df3_1['date']==df3_1['date'].max(),['client_name', 'dog_number', 'yur_hold',
         'dinamic_saldo', #'rating', 'garanty',
         ]]
    else:
        df3_1=df3_1.loc[df3_1['date']==e_d,['client_name', 'dog_number', 'yur_hold',
         'dinamic_saldo', #'rating', 'garanty',
         ]]
    df3_1['postpone_pay']=np.nan
    df3_1['prosrochka']=np.nan
    df3_1['percent']=np.nan
        
    # df3_1=df3_1[[ i for i in df3_1.columns if i not in ['rating', 'garanty']]]
    
    return df3_1.loc[ (df3_1['dinamic_saldo']>tol_dept)].sort_values(['dinamic_saldo', ],  ascending=False)

def get_matrix_stat_1_bseg(df3_1, s_d=None, e_d=None, tol_dept=1):
    if s_d is not None:
        df3_1=df3_1[df3_1['date']>=s_d]
    if e_d is not None:
        df3_1=df3_1[df3_1['date']<=e_d]
    if df3_1.shape[0]==0:
        return pd.DataFrame()
    df3_1=df3_1.sort_values([ 'id_rcm', 'client_name','date'])
    df6=pd.DataFrame()
    i0=0
    res=0
    dg_n=0
    for dg, dt, dp in df3_1[[ 'id_rcm', 'date','dept_over_lim']].values:
        if dg_n==0:
            # set_trace()
            dg_n=dg
            m=dp
        elif  dg_n!=dg:
            # set_trace()
            # print(dg)
            df6_1=pd.DataFrame({'id_rcm': [dg_n],
            'res': [res],
            'max': [m]})
            df6=pd.concat([df6, df6_1], ignore_index=True)
            if (dp>0):
                res=1
                i0=dp
            else:
                i0=0
            m=dp
            dg_n=dg
        else:
            if (i0==0) & (dp>0):
                res=res+1
                i0=dp
            elif (dp==0):
                i0=0
            if dp>m:
                m=dp
    df6_1=pd.DataFrame({'id_rcm': [dg_n],
            'res': [res],
            'max': [m]})
    df6=pd.concat([df6, df6_1], ignore_index=True)
    col0=[i  for i in 
       [ 'client_name','yur_hold','dog_number',  
    'rcm_categ', 
    # 'date', 
    'debitor_saldo_sum', 
      'days_off_cur_sum', 
     'dept_days_off_sum', 'dept_days_off_max',  'lim_sum', 
     'rating', #'garanty', 
     'lim_warr_garanty', 'lim_guar_garanty',
     'dept_over_lim','res','max']
       if (i in df3_1.columns) | (i in df6.columns )]
    
    # df3_1=df3_1[[ i for i in df3_1.columns if i not in ['rating', 'garanty']]]
    # df3_1=df3_1.loc[df3_1['date']==df3_1['date'].max(),].merge(df6, left_on='id_rcm', right_on='id_rcm')[col0].sort_values(['dept_over_lim','dinamic_saldo', ],  ascending=False)

    return df3_1.loc[(df3_1['date']==df3_1['date'].max()) & (df3_1['debitor_saldo_sum']>tol_dept),].merge(df6, left_on='id_rcm', right_on='id_rcm')[col0].sort_values(['dept_over_lim','debitor_saldo_sum', ],  ascending=False)
def get_matrix_stat_2_bseg(df3_1,  e_d=None, tol_dept=1):
    if (e_d is None) :
        df3_1=df3_1.loc[df3_1['date']==df3_1['date'].max(),['client_name', 'yur_hold','dog_number', 
         'debitor_saldo_sum', 
      'days_off_cur_sum', 
     'dept_days_off_sum', 'dept_days_off_max', 'rcm_categ', #'rating', 'garanty',
         'lim_warr_garanty', 'lim_guar_garanty',
         ]]
    else:
        df3_1=df3_1.loc[df3_1['date']==e_d,['client_name', 'dog_number', 
         'debitor_saldo_sum', 
      'days_off_cur_sum', 
     'dept_days_off_sum', 'dept_days_off_max', 'rcm_categ', #'rating', 'garanty',
         'lim_warr_garanty', 'lim_guar_garanty',
         ]]
    # df3_1['postpone_pay']=np.nan
    # df3_1['prosrochka']=np.nan
    df3_1['percent']=np.nan
        
    # df3_1=df3_1[[ i for i in df3_1.columns if i not in ['rating', 'garanty']]]
    
    return df3_1.loc[(df3_1['debitor_saldo_sum']>tol_dept)].sort_values(['debitor_saldo_sum', ],  ascending=False)


def get_dates_for_table():
    print('1. Загрузка данных')
    df = get_credit_data()
    
    print('2. Все контракты')
    df_dog_2=df.loc[(df['3_group']==2) , ['id_rcm','client_name','yur_hold', 'dog_number', 
       'date',  'dinamic_saldo', 'lim_sum', 'rating', 'garanty',
       'dept_over_lim']]
    df_dog_3=df.loc[(df['3_group']==3) , ['id_rcm','client_name','yur_hold', 'dog_number', 
       'date',  'dinamic_saldo', 'rating', 'garanty',
       ]]
    df_dog_1=df.loc[(df['3_group']==1) , ['id_rcm','client_name','yur_hold', 'dog_number', 
       'date',  'dinamic_saldo', 'rating', 'dept_over_lim'
       ]]
    # df_dog_2_1=get_matrix_stat_1(df_dog_2)
    # df_dog_3_1=get_matrix_stat_2(df_dog_3)
    # df_dog_1_1=get_matrix_stat_1(df_dog_1)
    return [df_dog_1,df_dog_2,df_dog_3]
def get_dates_for_table_bseg():
    print('1. Загрузка данных')
    df = get_credit_data_bseg()

    print('2. Все контракты')
    df_dog_2=df.loc[(df['3_group']==2) , ['id_rcm', 'client_name', 'yur_hold','dog_number',  
    'rcm_categ', 'date', 'debitor_saldo_sum', 
      'days_off_cur_sum', 
     'dept_days_off_sum', 'dept_days_off_max',  'lim_sum', 
     'rating', #'garanty', 
     'lim_warr_garanty', 'lim_guar_garanty',
     'dept_over_lim']]
    df_dog_3=df.loc[(df['3_group']==3) , ['id_rcm', 'client_name', 'yur_hold','dog_number', 
     'rcm_categ', 'date', 'debitor_saldo_sum', 
      'days_off_cur_sum', 
     'dept_days_off_sum', 'dept_days_off_max',  'rating', #'garanty', 
     'lim_warr_garanty', 'lim_guar_garanty',
       ]]
    df_dog_1=df.loc[(df['3_group']==1) , ['id_rcm', 'client_name', 'yur_hold',
    'dog_number',  'rcm_categ', 'date', 'debitor_saldo_sum', 
      'days_off_cur_sum', 
     'dept_days_off_sum', 'dept_days_off_max',  
     'rating', #'garanty', 
     'lim_warr_garanty', 'lim_guar_garanty', 'dept_over_lim'
       ]]
    # df_dog_2_1=get_matrix_stat_1(df_dog_2)
    # df_dog_3_1=get_matrix_stat_2(df_dog_3)
    # df_dog_1_1=get_matrix_stat_1(df_dog_1)
    return [df_dog_1,df_dog_2,df_dog_3]

@app.callback(
        [
        Output('datatable_clients_limit', 'data'),
        Output('datatable_clients_X', 'data'),
        Output('datatable_clients_prepaid', 'data'),
        ]
        ,
        Input('submit-val', 'n_clicks')
        ,
        State('risk_str_date', 'date'),
        State('risk_end_date', 'date'),
        background=True,
        # State('datatable_clients_limit', 'data'),  
        prevent_initial_call=True,
        running=[
        ( Output("submit-val", "disabled"), True, False),
        ]
)
def chose_period(n_c, s_d, e_d):
    df_dog_1,df_dog_2,df_dog_3=get_dates_for_table()
    df_dog_2_1=get_matrix_stat_1(df_dog_2, s_d=s_d, e_d= e_d)
    df_dog_3_1=get_matrix_stat_2(df_dog_3)
    df_dog_1_1=get_matrix_stat_1(df_dog_1)
    return [df_dog_2_1.to_dict('records'),df_dog_3_1.to_dict('records'),df_dog_1_1.to_dict('records'),]

    
@app.callback(
        [
        Output('datatable_clients_limit_bseg', 'data'),
        Output('datatable_clients_X_bseg', 'data'),
        Output('datatable_clients_prepaid_bseg', 'data'),
        ]
        ,
        Input('submit-val_bseg', 'n_clicks')
        ,
        State('risk_str_date_bseg', 'date'),
        State('risk_end_date_bseg', 'date'),
        background=True,
        # State('datatable_clients_limit', 'data'),  
        prevent_initial_call=True,
        running=[
        ( Output("submit-val_bseg", "disabled"), True, False),
        ]
)
def chose_period_bseg(n_c, s_d, e_d):
    df_dog_1,df_dog_2,df_dog_3=get_dates_for_table_bseg()
    df_dog_2_1=get_matrix_stat_1_bseg(df_dog_2, s_d=s_d, e_d= e_d)
    df_dog_3_1=get_matrix_stat_2_bseg(df_dog_3)
    df_dog_1_1=get_matrix_stat_1_bseg(df_dog_1)
    return [df_dog_2_1.to_dict('records'),df_dog_3_1.to_dict('records'),df_dog_1_1.to_dict('records'),]
    
@app.callback(
        [
        Output('dashboard13-dropdown-company', 'options'),
        Output('checklist-categ', 'options'),
        Output('dashboard13-dropdown-company', 'value'),
        Output('checklist-categ', 'value'),
        ]
        ,
        Input('checklist-DRO', 'value'),
        Input('checklist-categ', 'value'),
        # Input('RI-OS', 'value'),
        Input('RI-CH', 'value'),
        # State('dashboard13-dropdown-company', 'options'), 
        State('checklist-categ', 'options'),
        State('intermediate-value', 'data'), 
        background=True,
        prevent_initial_call=True,
        # running=[
        # ( Output("submit-val_bseg", "disabled"), True, False),
        # ]
)
def chose_filter(rcm_vid_v, rcm_categ_v, ch_v,  categ_op, df):
    # df=get_distinct_comp_bseg()
    df=pd.DataFrame.from_dict(df)
    ctx=dash.callback_context
    op1=categ_op
    v1=rcm_categ_v
    if ctx.triggered[0]['prop_id']=='checklist-DRO.value':
        op1=[ {'label': i, 'value': i} for i in df[df['rcm_vid'].isin(rcm_vid_v)]['rcm_categ'].unique()]
        v1=[i  for i in df[df['rcm_vid'].isin(rcm_vid_v)]['rcm_categ'].unique() if i in rcm_categ_v]
    if ch_v=='C':
            op3=[ {'label': i, 'value': i} for i in df[df['rcm_categ'].isin(rcm_categ_v)]['name1'].unique()]
            if 'ПАО "НЛМК"' in df[df['rcm_categ'].isin(rcm_categ_v)]['name1'].unique():
                v3='ПАО "НЛМК"'
            else:
                v3=[]
    else:
            op3=[ {'label': i, 'value': i} for i in df[df['rcm_categ'].isin(rcm_categ_v)]['yur_hold'].unique()]
            if 'ГК НЛМК' in df[df['rcm_categ'].isin(rcm_categ_v)]['yur_hold'].unique():
                v3='ГК НЛМК'
            else:
                v3=[]
   
    return [op3, op1, v3, v1 ]
    
@app.callback(
        [
        Output('nlmk_severstal', 'data'),
        ],
        State('checklist-DRO', 'value'),
        State('checklist-categ', 'value'),
        Input('RI-OS', 'value'),
        State('RI-CH', 'value'),
        State('dashboard13-dropdown-company', 'value'),
        Output('nlmk_severstal', 'figure'),
        background=True,
        prevent_initial_call=True,
        # running=[
        # ( Output("submit-val_bseg", "disabled"), True, False),
        # ]
)
def make_graph(rcm_vid_v, rcm_categ_v, os_v,ch_v, drop_v, categ_op,f):
    ctx=dash.callback_context
    df_result_t_m=get_saldo_bseg(rcm_vid=rcm_vid_v, rcm_categ=rcm_categ_v, name1=None, yur_hold=None)
    df_result_t_m=df_result_t_m.set_index('date')
    data=[go.Bar(
                                x=df_result_t_m[df_result_t_m['zuonr']==i].index,
                                y=df_result_t_m[df_result_t_m['zuonr']==i]['dmbtr'],
                                name=df_result_t_m[df_result_t_m['zuonr']==i][ 'rcm_dognum_reg'].values[0],
                            #     xperiod="M3",
                            #     xperiodalignment="middle",
                            #     xhoverformat="Q%q",
                                customdata=df_result_t_m[df_result_t_m['zuonr']==i][['rcm_vid', 'rcm_categ', 'rcm_dognum_reg']],
                                hovertemplate='<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
                                                        '<br><b>Дата</b>: %{x}'+
                                '<br><b>Тип договора</b>: %{customdata[0]}'+
                                '<br><b>Категория договора</b>: %{customdata[1]}'+
                                '<br><b>Номер договора</b>: %{customdata[2]}'+'<br><extra></extra>'
                            ) for i  in df_result_t_m['zuonr'].unique()
                                                    ]
    return [data]
    

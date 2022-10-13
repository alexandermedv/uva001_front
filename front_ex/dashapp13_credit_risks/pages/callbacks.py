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

from sqlalchemy import create_engine
from . import dash_app as app
from ..utils import  get_credit_data, get_credit_data_all, get_credit_data_clients#get_credit_data_filials,
# from .utils import get_limit_oper_client_zuonr_data, get_limit1, get_limit
def sum_nonlimit(s , n=0.13):
    if n in s.values:
        return n
    else:
        return s.sum()
def get_matrix_stat_1(df3_1, s_d=None, e_d=None):
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
        'dog_number',
       # 'date',  
        'dinamic_saldo', 'lim_sum',
       'dept_over_lim', 'rating', 'garanty','res','max'] if (i in df3_1.columns) | (i in df6.columns )]
    return df3_1.loc[df3_1['date']==df3_1['date'].max(),].merge(df6, left_on='id_rcm', right_on='id_rcm')[col0].sort_values(['dept_over_lim','dinamic_saldo', ],  ascending=False)
def get_matrix_stat_2(df3_1,  e_d=None):
    if (e_d is None) :
        df3_1=df3_1.loc[df3_1['date']==df3_1['date'].max(),['client_name', 'dog_number', 
         'dinamic_saldo', 'rating', 'garanty',]]
    else:
        df3_1=df3_1.loc[df3_1['date']==e_d,['client_name', 'dog_number', 
         'dinamic_saldo', 'rating', 'garanty',]]
    df3_1['postpone_pay']=np.nan
    df3_1['prosrochka']=np.nan
    df3_1['percent']=np.nan
    return df3_1.sort_values(['dinamic_saldo', ],  ascending=False)

def get_dates_for_table():
    print('1. Загрузка данных')
    df = get_credit_data()
    
    print('2. Все контракты')
    df_dog_2=df.loc[(df['3_group']==2) , ['id_rcm','client_name', 'dog_number', 
       'date',  'dinamic_saldo', 'lim_sum', 'rating', 'garanty',
       'dept_over_lim']]
    df_dog_3=df.loc[(df['3_group']==3) , ['id_rcm','client_name', 'dog_number', 
       'date',  'dinamic_saldo', 'rating', 'garanty',
       ]]
    df_dog_1=df.loc[(df['3_group']==1) , ['id_rcm','client_name', 'dog_number', 
       'date',  'dinamic_saldo', 'rating', 'dept_over_lim'
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

    

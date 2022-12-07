import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Output, Input, State
# from dash.dash_table.Format import Format, Group
import dash_bootstrap_components as dbc
import dash_table
from dash_table import  FormatTemplate
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
from ..utils import  get_saldo_bseg_uniq, get_saldo_bseg,get_saldo_bseg_group, get_credit_data, get_credit_data_all, get_credit_data_clients, get_credit_data_all_bseg, get_credit_data_bseg#get_credit_data_filials,
# from .utils import get_limit_oper_client_zuonr_data, get_limit1, get_limit
factoring=10500000000
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
    # df3_1['postpone_pay']=np.nan
    # df3_1['prosrochka']=np.nan
    # df3_1['percent']=np.nan
        
    # df3_1=df3_1[[ i for i in df3_1.columns if i not in ['rating', 'garanty']]]
    
    return df3_1.loc[ (df3_1['dinamic_saldo']>tol_dept)].sort_values(['dinamic_saldo', ],  ascending=False)

def get_matrix_stat_1_bseg(df3_1,sum_fact, s_d=None, e_d=None, tol_dept=1):
    if s_d is not None:
        df3_1=df3_1[df3_1['date']>=s_d]
        sum_fact=sum_fact[sum_fact['date']>=s_d]
    if e_d is not None:
        df3_1=df3_1[df3_1['date']<=e_d]
        sum_fact=sum_fact[sum_fact['date']<=e_d]
    if df3_1.shape[0]==0:
        return pd.DataFrame(),0
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
    df3_1['percent']=df3_1['dept_days_off_sum']/np.array([i if i>0 else 0.1 for i in df3_1['debitor_saldo_sum'].values])
    col0=[i  for i in 
       [ 'client_name','yur_hold','dog_number',  
    'rcm_categ', 
    # 'date', 
    'debitor_saldo_sum', 
      'days_off_cur_sum', 
     'dept_days_off_sum', 'dept_days_off_max',  'lim_sum', 
     'rating', 'percent', 
     'lim_warr_garanty', 'lim_guar_garanty',
     'dept_over_lim','res','max']
       if (i in df3_1.columns) | (i in df6.columns )]
    # df3_1=df3_1[[ i for i in df3_1.columns if i not in ['rating', 'garanty']]]
    # df3_1=df3_1.loc[df3_1['date']==df3_1['date'].max(),].merge(df6, left_on='id_rcm', right_on='id_rcm')[col0].sort_values(['dept_over_lim','dinamic_saldo', ],  ascending=False)

    return df3_1.loc[(df3_1['date']==df3_1['date'].max()) & (df3_1['debitor_saldo_sum']>tol_dept),].merge(df6, left_on='id_rcm', right_on='id_rcm')[col0].sort_values(['dept_over_lim','debitor_saldo_sum', ],  ascending=False), sum_fact.loc[(sum_fact['date']==sum_fact['date'].max())]['debitor_saldo_sum'].values[0]
def get_matrix_stat_2_bseg(df3_1,sum_fact,  e_d=None, tol_dept=1):
    if (e_d is None) :
        df3_1=df3_1.loc[df3_1['date']==df3_1['date'].max(),['client_name', 'yur_hold','dog_number', 
         'debitor_saldo_sum', 
      'days_off_cur_sum', 
     'dept_days_off_sum', 'dept_days_off_max', 'rcm_categ', #'rating', 'garanty',
        #  'lim_warr_garanty', 'lim_guar_garanty',
         ]]
        sum_fact=sum_fact.loc[(sum_fact['date']==sum_fact['date'].max())]['debitor_saldo_sum'].values[0]
    else:
        df3_1=df3_1.loc[df3_1['date']==e_d,['client_name', 'dog_number', 
         'debitor_saldo_sum', 
      'days_off_cur_sum', 
     'dept_days_off_sum', 'dept_days_off_max', 'rcm_categ', #'rating', 'garanty',
        #  'lim_warr_garanty', 'lim_guar_garanty',
         ]]
        sum_fact=sum_fact[sum_fact['date']<=e_d]
    # df3_1['postpone_pay']=np.nan
    # df3_1['prosrochka']=np.nan
    df3_1['percent']=df3_1['dept_days_off_sum']/np.array([i if i>0 else 0.1 for i in df3_1['debitor_saldo_sum'].values])

        
    # df3_1=df3_1[[ i for i in df3_1.columns if i not in ['rating', 'garanty']]]
    
    return df3_1.loc[(df3_1['debitor_saldo_sum']>tol_dept)].sort_values(['debitor_saldo_sum', ],  ascending=False), sum_fact


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
    return [df_dog_1,df_dog_2,df_dog_3]
def get_dates_for_table_bseg():
    print('1. Загрузка данных')
    df = get_credit_data_bseg()
    factoring_dogs=df[df['id_rcm'].isin([1968, 1855, 1867, 6508, 1949, 10300])]
    sum_fact=factoring_dogs.groupby('date')['debitor_saldo_sum'].sum().reset_index()
    factoring_dogs=factoring_dogs['dog_number'].unique()
    print('2. Все контракты')
    df_dog_2=df.loc[(df['3_group']==2) , ['id_rcm', 'client_name', 'yur_hold','dog_number',  
    'rcm_categ', 'date', 'debitor_saldo_sum', 
      'days_off_cur_sum', 
     'dept_days_off_sum', 'dept_days_off_max',  'lim_sum', 
     #'rating',  
     'lim_warr_garanty', 'lim_guar_garanty',
     'dept_over_lim']]
    df_dog_3=df.loc[(df['3_group']==3) , ['id_rcm', 'client_name', 'yur_hold','dog_number', 
     'rcm_categ', 'date', 'debitor_saldo_sum', 
      'days_off_cur_sum', 
     'dept_days_off_sum', 'dept_days_off_max',  #'rating',  
     'lim_warr_garanty', 'lim_guar_garanty',
       ]]
    df_dog_1=df.loc[(df['3_group']==1) , ['id_rcm', 'client_name', 'yur_hold',
    'dog_number',  'rcm_categ', 'date', 'debitor_saldo_sum', 
      'days_off_cur_sum', 
     'dept_days_off_sum', 'dept_days_off_max',  
     #'rating', 
    #  'lim_warr_garanty', 'lim_guar_garanty',
     'dept_over_lim'
       ]]
    # df_dog_2_1=get_matrix_stat_1(df_dog_2)
    # df_dog_3_1=get_matrix_stat_2(df_dog_3)
    # df_dog_1_1=get_matrix_stat_1(df_dog_1)
    return [df_dog_1,df_dog_2,df_dog_3,factoring_dogs, sum_fact]
def create_layout(): 
#     df_dog_1,df_dog_2,df_dog_3=get_dates_for_table()
#     df_dog_2_1=get_matrix_stat_1(df_dog_2)
#     df_dog_3_1=get_matrix_stat_2(df_dog_3)
#     df_dog_1_1=get_matrix_stat_1(df_dog_1)
#     df_dog_1_1=df_dog_1_1[[i for i in df_dog_1_1.columns if i not in ['res','max', 'percent','days_off_cur_sum', 
#      'dept_days_off_sum', 'dept_days_off_max','dept_over_lim']]]
#     is_need_bseg=True
#     if is_need_bseg:
#         df_dog_1_bseg,df_dog_2_bseg,df_dog_3_bseg,factoring_dogs, sum_fact=get_dates_for_table_bseg()
#         df_dog_2_1_bseg, sum_fact0=get_matrix_stat_1_bseg(df_dog_2_bseg,sum_fact)
#         df_dog_3_1_bseg, sum_fact0=get_matrix_stat_2_bseg(df_dog_3_bseg, sum_fact)
#         df_dog_1_1_bseg, sum_fact0=get_matrix_stat_1_bseg(df_dog_1_bseg, sum_fact)
#         df_dog_1_1_bseg=df_dog_1_1_bseg[[i for i in df_dog_1_1_bseg.columns if i not in ['res','max', 'percent','days_off_cur_sum', 
#      'dept_days_off_sum', 'dept_days_off_max','dept_over_lim']]]
#     else:
#         df_dog_1_bseg,df_dog_2_bseg,df_dog_3_bseg=(df_dog_1,df_dog_2,df_dog_3)
#         df_dog_2_1_bseg=df_dog_2_1
#         df_dog_3_1_bseg=df_dog_3_1
#         df_dog_1_1_bseg=df_dog_1_1
#         df_dog_1_1_bseg=df_dog_1_1_bseg[[i for i in df_dog_1_1_bseg.columns if i not in ['res','max', 'percent','days_off_cur_sum', 
#      'dept_days_off_sum', 'dept_days_off_max','dept_over_lim']]]
   
#     col_name_rus={
#         'yur_hold':['Холдинг','str', 0],
#         'rcm_categ':['Вид договора','str', 0],
#         'clients_count':['Кол-во превышений лимита','numeric', 1],
#         'postpone_pay':['Кол-во дней отсрочки платежа','numeric', 1],
#         'prosrochka':['Просроченная задолжность','numeric', 1],
#         'percent':['Доля долга','numeric', 1],
#         'res':['Кол-во превышений лимита','numeric', 1], 
#         'max':['Максимальное превышение лимита','numeric', 1],
#         'rating':['Рейтинг','numeric', 1],
#         'garanty':['Гарантии','numeric', 1],
#         'date':['Дата','str', 0],
#         'client':['id клиента','numeric', 0], 
#         'client_name':['Клиента','str', 0],
#         'id_rcm':['id договора','numeric', 0], 
#         'filial':['Филиал','str', 0],
#         'dog_number':['Договор','str', 0],
#         'dinamic_saldo':['Сальдо','numeric', 1],
#         'lim_sum':['Лимит','numeric', 1], 
#         'lim_warr_garanty' :['Обеспечение','numeric', 1],
#         'lim_guar_garanty' :['Гарантии','numeric', 1],
#         'dept_over_lim':['Превышение лимита','numeric', 1], 
#         'dinamic_saldo_X':['Сальдо безлимитных','numeric', 1],
#         'debitor':['debitor','numeric', 1],   
#         'debitor_X':['debitor_X','numeric', 1], 
#         'debitor_saldo_sum':['Дебиторское сальдо','numeric', 1], 
#         'days_off_cur_sum':['Дней просрочки на дату','numeric', 1], 
#         'dept_days_off_sum':['Долг просроченный на дату','numeric', 1], 
#         'dept_days_off_max':['Максимальный просроченный долг за период','numeric', 1],


#         'dinamic_saldo_min':['Минимальное сальдо','numeric', 1], 
#         'dinamic_saldo_mean_below_zero':['Средняя задолженность','numeric', 1], 
#         'dept_over_lim_min':['Максимальное превышение лимита','numeric', 1], 
#         'dept_over_lim_mean':['Среднее превышение лимита','numeric', 1],
#         'days_over_limit_max':['Максимум дней выше лимита','numeric', 1], 
#         'days_over_limit_mean':['Среднее число дней выше лимита','numeric', 1], 
#         'days_over_limit_count_days_over':['Число превышений лимита','numeric', 1], 
#         'days_over_limit':['Текущее число дней выше лимита','numeric', 1], 
#         'debitor_min':['debitor_min','numeric', 1], 
#         'debitor_mean_below_zero':['debitor_mean_below_zero','numeric', 1], 
#         'dept_over_lim_min_y':['dept_over_lim_min_y','numeric', 1],
#         'dept_over_lim_mean_y':['dept_over_lim_mean_y','numeric', 1], 
#         'days_over_limit_max_y':['days_over_limit_max_y','numeric', 1], 
#         'days_over_limit_mean_y':['days_over_limit_mean_y','numeric', 1], 
#         'days_over_limit_count_days_over_y':['days_over_limit_count_days_over_y','numeric', 1],
#         'dept_over_lim_y':['dept_over_lim_y','numeric', 1], 
#         'days_over_limit_y':['days_over_limit_y','numeric', 1]
	
#     }
    
#     print('5. Все и безлимитные')
#     df_all0=get_credit_data_all()
#     max_date=df_all0['date'].max()
#     min_date=df_all0['date'].min()
#     df_all0=df_all0.set_index('date')
    
#     dates=df_all0.index.date

#     df_all0_M=df_all0.groupby([pd.Grouper( freq="1M"),'3_group']).mean().reset_index(1)
#     df_all0_M_1=df_all0_M[df_all0_M['3_group']==1]
#     df_all0_M_2=df_all0_M[df_all0_M['3_group']==2]
#     df_all0_M_3=df_all0_M[df_all0_M['3_group']==3]
#     dates1_1=df_all0_M_1.index.date
#     dates1_2=df_all0_M_2.index.date
#     dates1_3=df_all0_M_3.index.date
#     df_all0_M_1=df_all0_M_1.reset_index()
#     df_all0_M_2=df_all0_M_2.reset_index()
#     df_all0_M_3=df_all0_M_3.reset_index()

#     points_1=df_all0_M_3['dinamic_saldo'].values
#     points_1_c=df_all0_M_1['clients_count'].values
#     points_2=df_all0_M_2['dinamic_saldo'].values
#     points_3=df_all0_M_3['dinamic_saldo'].values
    
#     points_1_0=[0 for i in dates1_1]
#     points_2_0=[0 for i in dates1_2]
#     points_3_0=[0 for i in dates1_3]
    
#     print('5. Все и безлимитные bseg')
#     if is_need_bseg:
#         df_all0_bseg=get_credit_data_all_bseg()
#     else:
#         df_all0_bseg=get_credit_data_all()
#         df_all0_bseg=df_all0_bseg.rename(columns={'dinamic_saldo':'debitor_saldo_sum'})

#     max_date_bseg=df_all0_bseg['date'].max()
#     min_date_bseg=df_all0_bseg['date'].min()
#     df_all0_bseg=df_all0_bseg.set_index('date')
    
#     dates_bseg=df_all0_bseg.index.date

#     df_all0_M_bseg=df_all0_bseg.groupby([pd.Grouper( freq="1M"),'3_group']).mean().reset_index(1)
#     df_all0_M_1_bseg=df_all0_M_bseg[df_all0_M_bseg['3_group']==1]
#     df_all0_M_2_bseg=df_all0_M_bseg[df_all0_M_bseg['3_group']==2]
#     df_all0_M_3_bseg=df_all0_M_bseg[df_all0_M_bseg['3_group']==3]
#     dates1_1_bseg=df_all0_M_1_bseg.index.date
#     dates1_2_bseg=df_all0_M_2_bseg.index.date
#     dates1_3_bseg=df_all0_M_3_bseg.index.date
#     df_all0_M_1_bseg=df_all0_M_1_bseg.reset_index()
#     df_all0_M_2_bseg=df_all0_M_2_bseg.reset_index()
#     df_all0_M_3_bseg=df_all0_M_3_bseg.reset_index()

#     points_1_bseg=df_all0_M_3_bseg['debitor_saldo_sum'].values
#     points_1_c_bseg=df_all0_M_1_bseg['clients_count'].values
#     points_2_bseg=df_all0_M_2_bseg['debitor_saldo_sum'].values
#     points_3_bseg=df_all0_M_3_bseg['debitor_saldo_sum'].values
#     points_3_p_bseg=df_all0_M_3_bseg['percent'].values

#     points_1_0_bseg=[0 for i in dates1_1_bseg]
#     points_2_0_bseg=[0 for i in dates1_2_bseg]
#     points_3_0_bseg=[0 for i in dates1_3_bseg]
#     print("saldo")
#     global df_saldo
#     df_result_t=get_saldo_bseg( name1='ПАО "НЛМК"')
    df_dog_uniq=get_saldo_bseg_uniq()
    # df_result_t_m=get_saldo_bseg_group( name1='ПАО "НЛМК"')
    # df_result_t_m=df_result_t_m.set_index('date')
    
    print("5. Старт загрузки layout")

    layout = html.Div(
        [   dcc.Store(id='intermediate-value', data=df_dog_uniq.to_dict('records')),
            html.Div(
                html.H5("Отчет кредитных рисков", className='row' ,
                style={'font-size': '3rem', 'padding-top':'30px'}
                ),
                className='product'
            ),
            html.Div([
                dcc.Tabs(id='dashboard13-tabs', value='tab-1', children=[
                    dcc.Tab(label='Управленческая ДЗ', value='tab-1', className="tab",),
                    dcc.Tab(label='Бухгалтерская ДЗ', value='tab-2', className="tab",),
                    dcc.Tab(label='Бухгалтерское сальдо', value='tab-3', className="tab",),
                ], className="row all-tabs"),
                #html.Div(id='tabs-example-content')
            ]),

            # Row 5 - Содержимое закладки
            html.Div(id='tab-content13'),
#             dcc.Graph(
#                 id="all_bar",
#                 figure=go.Figure(
#                     data=[
#                         go.Bar(name='Отсрочка платежа без потолка лимита', x=dates1_1, y=df_all0_M_1['dinamic_saldo'].values,
#                         hovertemplate =
#                                 '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>', xaxis='x1', marker_color="#97151c"),
#                         go.Bar(name='Кредитный лимит с отсрочкой платежа', x=dates1_2,hovertemplate =
#                                 '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>', y=points_2, xaxis='x1', marker_color='rgb(193, 122, 117)'),#'#006B19'
#                         go.Bar(name='Предоплата', x=dates1_3, y=points_3,hovertemplate =
#                                 '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>', xaxis='x1', marker_color='rgb(206, 205, 181)')
#                     ],
                    
#                     layout=go.Layout(
#                         title= 'Помесячная динамика дебиторской задолженности (в млрд руб., по данным отчета «Дин. сальдо»).',
#                         barmode='stack',
#                         plot_bgcolor='white',
#                         paper_bgcolor='white',
#                         # xaxis=dict(
#                         #     showticklabels=False,
#                         #     overlaying='x2',
#                         #     showdividers=False),
#                         margin={'l': 30, 'b': 30, 't': 80, 'r': 0},
#                         # legend={'x': 0, 'y': 1},
#                         showlegend=True
#                     )
#                 ), style={'width': '80%'},
#                 config={'displayModeBar': False}
#             ),
#             dcc.Graph(
#                 id="all_limit",
#                 figure=go.Figure(
#                     data=[
#                         go.Scatter(x=dates1_2, y=points_2, mode='lines',
#                         hovertemplate =
#                                 '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>',
#                           name= 'Динамическое сальдо долг', #line_color='rgb(40,80,0)', 
#                         fill='tonexty',line_shape='spline', xaxis='x1', line=dict(color="#006B19")),
#                         # go.Bar(name='Динамическое сальдо долг', x=dates1_2, y=points_2, xaxis='x1'),
#                         go.Scatter(x=dates1_2, y=df_all0_M_2['lim_sum'].values, mode='lines',
#                         hovertemplate =
#                                 '<i><b>Лимит</b></i>: \u20bd %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>',
#                          name= 'Кредитный лимит из SAP', line_color='#97151c', xaxis='x1'),
#                         go.Scatter(x=dates1_2, y=points_2_0, mode='lines',hoverinfo='none', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2'),
#                         # go.Scatter(x=dates1_2, y=[4800000000 for i in dates1_2], hoverinfo='none',mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.1, xaxis='x2')

#                         ],
#                     layout=go.Layout(
#                         title= 'Динамика задолженности клиентов с кредитным лимитом с отсрочкой платежа (в млрд руб., по данным отчета «Дин. сальдо»)',
#                         plot_bgcolor='white',
#                         paper_bgcolor='white',
#                         xaxis=dict(
#                             showticklabels=False,
#                             overlaying='x2',
#                             showdividers=False),
#                         margin={'l': 30, 'b': 30, 't': 80, 'r': 0},
#                         # legend={'x': 0, 'y': 1},
#                         showlegend=True
#                     )
#                 ), style={'width': '80%'},
#                 config={'displayModeBar': False}
#             ),
#             html.Div(    
#                 dbc.Navbar(
#                 [
#                     html.Div('Выберите начальную дату:', 
#                         style={'width': '15%', 
#                         'display': 'inline-block', 'marginBottom': 15, 'margin-left': 30,'marginTop': 25,
#                         'color': 'white'}
#                     ),
#                     dcc.DatePickerSingle(
#                         # calendar_orientation='vertical',
#                         clearable=True,
#                         id='risk_str_date',
#                         date=min_date,
#                         min_date_allowed=min_date,
#                         max_date_allowed=max_date,
#                         initial_visible_month=min_date,
#                         number_of_months_shown = 3,
#                         display_format='DD.MM.YYYY',
#                         style={'width': '20%', 'display': 'inline-block', 'color': 'white'}
#                     ),
#                     html.Div('Выберите последнюю дату:', 
#                         style={'width': '15%', 'display': 'inline-block', 'color': 'white'}
#                     ),
#                     dcc.DatePickerSingle(
#                         calendar_orientation='vertical',
#                         clearable=True,
#                         id='risk_end_date',
#                         date=max_date,
#                         min_date_allowed=min_date,
#                         max_date_allowed=max_date,
#                         initial_visible_month=min_date,
#                         number_of_months_shown = 3,
#                         display_format='DD.MM.YYYY',
#                         style={'width': '20%', 'display': 'inline-block', 'color': 'white'}
#                     ),
#                     html.Button('Submit', id='submit-val', n_clicks=0,
#                         style={'width': '15%', 'display': 'inline-block', 'background-color': 'white', }),
#                 ],dark=True, color='rgb(71, 71, 71)'
#                 )
#             ),

#             html.Div([
#                 html.H6('Детальная информация по задолженности клиентов с кредитным лимитом с отсрочкой платежа (по данным отчета «Дин. сальдо»)',
#                 className='row'),
#                 dbc.Col(dash_table.DataTable(
#                     id='datatable_clients_limit',
#                     columns=[{"name": col_name_rus[i][0], "id": i,
#                     #  "deletable": True, 
#                      'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
#                     {"name": col_name_rus[i][0], "id": i,
#                     #  "deletable": True, 
#                      'type': col_name_rus[i][1], 'format': dict(specifier=',.0f')}
#                      for i in    df_dog_2_1.columns if i not in ['rating', 'garanty']],
#                     data=(df_dog_2_1).to_dict('records'),
#                     # editable=True,
#                     filter_action="native",
#                     sort_action="native",
#                     sort_mode="multi",
#                     # column_selectable="single",
#                     # row_selectable="multi",
#                     # row_deletable=True,
#                     selected_columns=[],
#                     selected_rows=[],
#                     # page_action="native",
#                     # page_current= 0,
#                     page_size= 10, 
#                     # style_cell = {'textAlign': 'center'},
#                     style_cell={
#                             'minWidth': 10, 'maxWidth': 95, 'width': 10,'textAlign': 'left'
#                         },
#                     style_as_list_view=True,
#                     style_table={#'height': 530, 
#                             # 'width':800,
#                             'overflowY': 'auto',
#                             'lineHeight': '30px'},
#                     style_header={
#                                 # 'backgroundColor': 'rgb(138,36,50)',
#                                 # 'color': 'white',
#                                 'whiteSpace':'normal',
#                                 # 'fontWeight': 'bold',
#                                 # 'font_size': '16px'
#                                 'overflowY': 'auto',
#                                 'height': 'auto',
#                     },
#                     style_data={
#                             'whiteSpace': 'normal',
#                             'height': 'auto',
#                             'font_size': '12px',
#                             'line-height': 0.9
#                             # 'width': '100px',
#                             # 'maxWidth': '100px',
#                             # 'minWidth': '100px',
#                         },
#                     # style_data_conditional=[
#                     #     {'if': {'column_id': 'Лимит в SAP'},
#                     #     'width': '35px'},
#                     # ]
#                 ), width=12),
#                 dcc.Graph(
#                 id="all_x",
#                 figure=go.Figure(
#                     data=[
#                         go.Scatter(x=dates1_3, y=points_3, mode='lines', hovertemplate =
#                                 '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>',
#                         name= 'Динамическое сальдо долг', line=dict(color="#006B19"), line_shape='spline', xaxis='x1'),
#                         go.Scatter(x=dates1_3, y=points_3_0, mode='lines',hoverinfo='none', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')
#                     ],
#                     layout=go.Layout(
#                         title= 'Динамика задолженности клиентов с отсрочкой платежа без потолка лимита (в млрд руб., по данным отчета «Дин. сальдо»)',
#                         plot_bgcolor='white',
#                         paper_bgcolor='white',
#                         xaxis=dict(
#                             showticklabels=False,
#                             overlaying='x2',
#                             showdividers=False),
#                         margin={'l': 30, 'b': 30, 't': 80, 'r': 0},
#                         # legend={'x': 0, 'y': 1},
#                         showlegend=True
#                     )
#                 ), style={'width': '80%'},
#                 config={'displayModeBar': False}
#             ),
#                 html.H6('Детальная информация по задолженности клиентов с отсрочкой платежа без потолка лимита (по данным отчета «Дин. сальдо»)', className='row'),
#                 dbc.Col(dash_table.DataTable(
#                     id='datatable_clients_X',
#                     columns=[{"name": col_name_rus[i][0], "id": i,
#                      "deletable": True, 'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
#                     {"name": col_name_rus[i][0], "id": i,
#                      "deletable": True, 'type': col_name_rus[i][1], 'format': dict(specifier=',.0f')}
#                      for i in    df_dog_3_1.columns],
#                     data=(df_dog_3_1).to_dict('records'),
#                     # editable=True,
#                     filter_action="native",
#                     sort_action="native",
#                     sort_mode="multi",
#                     # column_selectable="single",
#                     # row_selectable="multi",
#                     # row_deletable=True,
#                     selected_columns=[],
#                     selected_rows=[],
#                     page_action="native",
#                     page_current= 0,
#                     page_size= 10, 
#                    # style_cell = {'textAlign': 'center'},
#                     style_cell={
#                             'minWidth': 10, 'maxWidth': 95, 'width': 10,'textAlign': 'left'
#                         },
#                     style_as_list_view=True,
#                     style_table={#'height': 530, 
#                             # 'width':800,
#                             'overflowY': 'auto',
#                             'lineHeight': '30px'},
#                     style_header={
#                                 # 'backgroundColor': 'rgb(138,36,50)',
#                                 # 'color': 'white',
#                                 'whiteSpace':'normal',
#                                 # 'fontWeight': 'bold',
#                                 # 'font_size': '16px'
#                                 'overflowY': 'auto',
#                                 'height': 'auto',
#                     },
#                     style_data={
#                             'whiteSpace': 'normal',
#                             'height': 'auto',
#                             'font_size': '12px',
#                             'line-height': 0.9
#                             # 'width': '100px',
#                             # 'maxWidth': '100px',
#                             # 'minWidth': '100px',
#                         }, 
#                     # style_data_conditional=[
#                     #     {'if': {'column_id': 'Лимит в SAP'},
#                     #     'width': '35px'},
#                     # ]
#                 ), width=12),
#                 dcc.Graph(
#                     id="all_prepaid",
#                     figure=go.Figure(
#                         data=[
#                             go.Bar(x=dates1_1, y=points_1_c,  yaxis='y1',
#                             hovertemplate =
#                                 '<i><b>Кол-во клиентов</b></i>:  %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>',  width=500000000, name= 'Кол-во клиентов', xaxis='x1', opacity=0.5),
#                             go.Scatter(x=dates1_1, y=points_1, mode='lines', name= 'Динамическое сальдо долг',
#                             hovertemplate =
#                                 '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>',
#                                    yaxis='y2', line=dict(color="#006B19"), 
#                             line_shape='spline'),
#                             # go.Scatter(x=dates1_1, y=[12000000000 for i in dates1_1],
#                             #     hoverinfo='none', mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.1, yaxis='y2', xaxis='x2'),
#                             # go.Scatter(x=dates1_1, y=[200 for i in dates1_1]
#                             # , hoverinfo='none', mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.1, yaxis='y1', xaxis='x2'),
#                             # go.Scatter(x=dates1_1, y=points_1_c, mode='bar', secondary_y=True,name= 'Кредитный лимит из SAP', line_color='rgb(207,0,15)', xaxis='x1'),
#                             go.Scatter(x=dates1_1, y=points_1_0, mode='lines',
#                                 hoverinfo='none', name= '', line_color='rgb(217,217,217)', line_width=0.5, yaxis='y1',xaxis='x2')
#                         ],
#                         layout=go.Layout(
#                             title= 'Динамика задолженности предоплатных клиентов в разрезе кол-ва клиентов и суммы задолженности в млрд руб. (по данным отчета «Дин. сальдо»)',
#                             plot_bgcolor='white',
#                             paper_bgcolor='white',
#                             xaxis=dict(
#                                 showticklabels=False,
#                                 overlaying='x2',
#                                 showdividers=False),
#                             yaxis=dict(title='Кол-во клиентов', side='right'),
#                             yaxis2=dict(title='Долг',
#                                     overlaying='y',
#                                     side='left'),
#                             margin={'l': 30, 'b': 30, 't': 40, 'r': 0},
#                             # legend={'x': 0, 'y': 1},
#                             showlegend=True
#                         )
#                     ), style={'width': '80%'},
#                     config={'displayModeBar': False}
#                 ),
#                 html.H6('Детальная информация по задолженности предоплатных клиентов (по данным отчета «Дин. сальдо»)', className='row'),
#                 dbc.Col(dash_table.DataTable(
#                     id='datatable_clients_prepaid',
#                     columns=[{"name": col_name_rus[i][0], "id": i,
#                      "deletable": True, 'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
#                     {"name": col_name_rus[i][0], "id": i,
#                      "deletable": True, 'type': col_name_rus[i][1], 'format': dict(specifier=',.0f')}
#                      for i in    df_dog_1_1.columns],
#                     data=(df_dog_1_1).to_dict('records'),
#                     # editable=True,
#                     filter_action="native",
#                     sort_action="native",
#                     sort_mode="multi",
#                     # column_selectable="single",
#                     # row_selectable="multi",
#                     # row_deletable=True,
#                     selected_columns=[],
#                     selected_rows=[],
#                     page_action="native",
#                     page_current= 0,
#                     page_size= 10, 
#                     # style_cell = {'textAlign': 'center'},
#                     style_cell={
#                             'minWidth': 10, 'maxWidth': 95, 'width': 10,'textAlign': 'left'
#                         },
#                     style_as_list_view=True,
#                     style_table={#'height': 530, 
#                             # 'width':800,
#                             'overflowY': 'auto',
#                             'lineHeight': '30px'},
#                     style_header={
#                                 # 'backgroundColor': 'rgb(138,36,50)',
#                                 # 'color': 'white',
#                                 'whiteSpace':'normal',
#                                 # 'fontWeight': 'bold',
#                                 # 'font_size': '16px'
#                                 'overflowY': 'auto',
#                                 'height': 'auto',
#                     },
#                     style_data={
#                             'whiteSpace': 'normal',
#                             'height': 'auto',
#                             'font_size': '12px',
#                             'line-height': 0.9
#                             # 'width': '100px',
#                             # 'maxWidth': '100px',
#                             # 'minWidth': '100px',
#                         },
#                     # style_data_conditional=[
#                     #     {'if': {'column_id': 'Лимит в SAP'},
#                     #     'width': '35px'},
#                     # ]
#                 ), width=12),

#                 dcc.Graph(
#                     id="all_bar_bseg",
#                     figure=go.Figure(
#                         data=[
#                             go.Bar(name='Отсрочка платежа без потолка лимита', x=dates1_1_bseg, y=df_all0_M_1_bseg['debitor_saldo_sum'].values,
#                             hovertemplate =
#                                     '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                     '<br><b>Дата</b>: %{x}<br><extra></extra>', xaxis='x1', marker_color="#97151c"),
#                             go.Bar(name='Кредитный лимит с отсрочкой платежа', x=dates1_2_bseg,hovertemplate =
#                                     '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                     '<br><b>Дата</b>: %{x}<br><extra></extra>', y=points_2_bseg, xaxis='x1', marker_color='rgb(193, 122, 117)'),#'#006B19'
#                             go.Bar(name='Предоплата', x=dates1_3_bseg, y=points_3_bseg,hovertemplate =
#                                     '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                     '<br><b>Дата</b>: %{x}<br><extra></extra>', xaxis='x1', marker_color='rgb(206, 205, 181)')
#                         ],
                        
#                         layout=go.Layout(
#                             title= 'Помесячная динамика дебиторской задолженности (в млрд руб., по данным бухгалтерского учета)',
#                             barmode='stack',
#                             plot_bgcolor='white',
#                             paper_bgcolor='white',
#                             # xaxis=dict(
#                             #     showticklabels=False,
#                             #     overlaying='x2',
#                             #     showdividers=False),
#                             margin={'l': 30, 'b': 30, 't': 80, 'r': 0},
#                             # legend={'x': 0, 'y': 1},
#                             showlegend=True
#                         )
#                     ), style={'width': '80%'},
#                     config={'displayModeBar': False}
#                 ),
#                 dcc.Graph(
#                     id="all_limit_bseg",
#                     figure=go.Figure(
#                         data=[
#                             go.Scatter(x=dates1_2_bseg, y=points_2_bseg, mode='lines',
#                             hovertemplate =
#                                     '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                     '<br><b>Дата</b>: %{x}<br><extra></extra>',
#                             name= 'Динамическое сальдо долг', #line_color='rgb(40,80,0)', 
#                             fill='tonexty',line_shape='spline', xaxis='x1', line=dict(color="#006B19")),
#                             # go.Bar(name='Динамическое сальдо долг', x=dates1_2, y=points_2, xaxis='x1'),
#                             go.Scatter(x=dates1_2_bseg, y=df_all0_M_2_bseg['lim_sum'].values, mode='lines',
#                             hovertemplate =
#                                     '<i><b>Лимит</b></i>: \u20bd %{y:,.0f}'+
#                                     '<br><b>Дата</b>: %{x}<br><extra></extra>',
#                             name= 'Кредитный лимит из SAP', line_color='#97151c', xaxis='x1'),
#                             go.Scatter(x=dates1_2_bseg, y=points_2_0_bseg, mode='lines',hoverinfo='none', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2'),
#                             # go.Scatter(x=dates1_2_bseg, y=[4800000000 for i in dates1_2_bseg], hoverinfo='none',mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.1, xaxis='x2')

#                             ],
#                         layout=go.Layout(
#                             title= 'Динамика задолженности клиентов с кредитным лимитом с отсрочкой платежа (в млрд руб., по данным бухгалтерского учета)',
#                             plot_bgcolor='white',
#                             paper_bgcolor='white',
#                             xaxis=dict(
#                                 showticklabels=False,
#                                 overlaying='x2',
#                                 showdividers=False),
#                             margin={'l': 30, 'b': 30, 't': 80, 'r': 0},
#                             # legend={'x': 0, 'y': 1},
#                             showlegend=True
#                         )
#                     ), style={'width': '80%'},
#                     config={'displayModeBar': False}
#                 ),
#                 dbc.Navbar(
#                 [
#                     html.Div('Выберите начальную дату_bseg:', 
#                         style={'width': '15%', 
#                         'display': 'inline-block', 'marginBottom': 15, 'margin-left': 30,'marginTop': 25,
#                         'color': 'white'}
#                     ),
#                     dcc.DatePickerSingle(
#                         # calendar_orientation='vertical',
#                         clearable=True,
#                         id='risk_str_date_bseg',
#                         date=min_date_bseg,
#                         min_date_allowed=min_date_bseg,
#                         max_date_allowed=max_date_bseg,
#                         initial_visible_month=min_date_bseg,
#                         number_of_months_shown = 3,
#                         display_format='DD.MM.YYYY',
#                         style={'width': '20%', 'display': 'inline-block', 'color': 'white'}
#                     ),
#                     html.Div('Выберите последнюю дату_bseg:', 
#                         style={'width': '15%', 'display': 'inline-block', 'color': 'white'}
#                     ),
#                     dcc.DatePickerSingle(
#                         calendar_orientation='vertical',
#                         clearable=True,
#                         id='risk_end_date_bseg',
#                         date=max_date_bseg,
#                         min_date_allowed=min_date_bseg,
#                         max_date_allowed=max_date_bseg,
#                         initial_visible_month=min_date_bseg,
#                         number_of_months_shown = 3,
#                         display_format='DD.MM.YYYY',
#                         style={'width': '20%', 'display': 'inline-block', 'color': 'white'}
#                     ),
#                     html.Button('Submit', id='submit-val_bseg', n_clicks=0,
#                         style={'width': '15%', 'display': 'inline-block', 'background-color': 'white', }),
#                 ],dark=True, color='rgb(71, 71, 71)'
#                 ),
#                 html.H6('Детальная информация по задолженности клиентов с кредитным лимитом с отсрочкой платежа (по данным бухгалтерского учета)', className='row'),
#                 dbc.Col(dash_table.DataTable(
#                     id='datatable_clients_limit_bseg',
#                     columns=[{"name": col_name_rus[i][0], "id": i,
#                     #  "deletable": True, 
#                      'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
#                     {"name": col_name_rus[i][0], "id": i,
#                     #  "deletable": True, 
#                      'type': col_name_rus[i][1], 'format': dict(specifier=',.0f') if i!= 'percent' else FormatTemplate.percentage(2)}
#                      for i in    df_dog_2_1_bseg.columns if i not in ['rating', 'garanty']],
#                     data=(df_dog_2_1_bseg).to_dict('records'),
#                     # editable=True,
#                     filter_action="native",
#                     sort_action="native",
#                     sort_mode="multi",
#                     # column_selectable="single",
#                     # row_selectable="multi",
#                     # row_deletable=True,
#                     selected_columns=[],
#                     selected_rows=[],
#                     tooltip_conditional=
#                     [
#                         {
#                             'if': {
#                                 'filter_query': "{{dog_number}} = '{}'".format(i),
#                                 'column_id': 'debitor_saldo_sum',
#                             },
#                             'backgroundColor': '#7FDBFF',
#                             'color': 'white',
#                             'type': 'markdown',
#                             'value': 'Факторинг 10,5 млрд.'
#                         }
#                         for i in factoring_dogs
#                     ],

#                     style_data_conditional=[
#                                     {
#                                         'if': {
#                                             'filter_query': "{{dog_number}} = '{}'".format(i),
#                                             'column_id': 'debitor_saldo_sum',
#                                         },
#                                         'backgroundColor': ('#0074D9' if sum_fact0 < factoring else '#97151c'),
#                                         'color': 'white',
#                                         'textDecoration': 'underline',
#                                         'textDecorationStyle': 'dotted',
#                                     }
#                                     for i in factoring_dogs
#                                 ],
#                     tooltip_delay=0,
#                     tooltip_duration=None,
#                     # page_action="native",
#                     # page_current= 0,
#                     page_size= 10, 
#                     # style_cell = {'textAlign': 'center'},
#                     style_cell={
#                             'minWidth': 10, 'maxWidth': 95, 'width': 10,'textAlign': 'left'
#                         },
#                     style_as_list_view=True,
#                     style_table={#'height': 530, 
#                             # 'width':800,
#                             'overflowY': 'auto',
#                             'lineHeight': '30px'},
#                     style_header={
#                                 # 'backgroundColor': 'rgb(138,36,50)',
#                                 # 'color': 'white',
#                                 'whiteSpace':'normal',
#                                 # 'fontWeight': 'bold',
#                                 # 'font_size': '16px'
#                                 'overflowY': 'auto',
#                                 'height': 'auto',
#                     },
#                     style_data={
#                             'whiteSpace': 'normal',
#                             'height': 'auto',
#                             'font_size': '12px',
#                             'line-height': 0.9
#                             # 'width': '100px',
#                             # 'maxWidth': '100px',
#                             # 'minWidth': '100px',
#                         },
#                     # style_data_conditional=[
#                     #     {'if': {'column_id': 'Лимит в SAP'},
#                     #     'width': '35px'},
#                     # ]
#                 ), width=12),
#                 dcc.Graph(
#                 id="all_x_bseg",
#                 figure=go.Figure(
#                     data=[
#                         go.Bar(x=dates1_3_bseg, y=points_3_p_bseg,  yaxis='y1',
#                             hovertemplate =
#                                 '<i><b>Доля просроченной задолжности</b></i>:  %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>',  width=500000000, name= 'Доля просроченной задолжности', xaxis='x1', opacity=0.5),

#                         go.Scatter(x=dates1_3_bseg, y=points_3_bseg, mode='lines', hovertemplate =
#                                 '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>',
#                         name= 'Динамическое сальдо долг', line=dict(color="#006B19"), line_shape='spline', yaxis='y2',xaxis='x1'),
#                         go.Scatter(x=dates1_3_bseg, y=points_3_0_bseg, mode='lines',hoverinfo='none', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')
#                     ],
#                     layout=go.Layout(
#                         title= 'Динамика задолженности клиентов с отсрочкой платежа без потолка лимита (по данным бухгалтерского учета)',
#                         plot_bgcolor='white',
#                         paper_bgcolor='white',
#                         xaxis=dict(
#                             showticklabels=False,
#                             overlaying='x2',
#                             showdividers=False),
#                         yaxis=dict(title='Доля просроченной задолжности', side='right',
#                         tickformat= ',.0%'),
#                         yaxis2=dict(title='Долг',
#                                     overlaying='y',
#                                     side='left'),
#                         margin={'l': 30, 'b': 30, 't': 80, 'r': 0},
#                         # legend={'x': 0, 'y': 1},
#                         showlegend=True
#                     )
#                 ), style={'width': '80%'},
#                 config={'displayModeBar': False}
#             ),
#                 html.H6('Детальная информация по задолженности клиентов с отсрочкой платежа без потолка лимита (по данным бухгалтерского учета)', className='row'),
#                 dbc.Col(dash_table.DataTable(
#                     id='datatable_clients_X_bseg',
#                     columns=[{"name": col_name_rus[i][0], "id": i,
#                      "deletable": True, 'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
#                     {"name": col_name_rus[i][0], "id": i,
#                      "deletable": True, 'type': col_name_rus[i][1], 'format': dict(specifier=',.0f') if i!= 'percent' else FormatTemplate.percentage(2)}
#                      for i in    df_dog_3_1_bseg.columns],
#                     data=(df_dog_3_1_bseg).to_dict('records'),
#                     # editable=True,
#                     filter_action="native",
#                     sort_action="native",
#                     sort_mode="multi",
#                     # column_selectable="single",
#                     # row_selectable="multi",
#                     # row_deletable=True,
#                     selected_columns=[],
#                     selected_rows=[],
#                     tooltip_conditional=
#                     [
#                         {
#                             'if': {
#                                 'filter_query': "{{dog_number}} = '{}'".format(i),
#                                 'column_id': 'debitor_saldo_sum',
#                             },
#                             'backgroundColor': '#7FDBFF',
#                             'color': 'white',
#                             'type': 'markdown',
#                             'value': 'Факторинг 10,5 млрд.'
#                         }
#                         for i in factoring_dogs
#                     ],

#                     style_data_conditional=[
#                                     {
#                                         'if': {
#                                             'filter_query': "{{dog_number}} = '{}'".format(i),
#                                             'column_id': 'debitor_saldo_sum',
#                                         },
#                                         'backgroundColor': ('#0074D9' if sum_fact0 < factoring else '#97151c'),
#                                         'color': 'white',
#                                         'textDecoration': 'underline',
#                                         'textDecorationStyle': 'dotted',
#                                     }
#                                     for i in factoring_dogs
#                                 ],
#                     tooltip_delay=0,
#                     tooltip_duration=None,
#                     page_action="native",
#                     page_current= 0,
#                     page_size= 10, 
#                    # style_cell = {'textAlign': 'center'},
#                     style_cell={
#                             'minWidth': 10, 'maxWidth': 95, 'width': 10,'textAlign': 'left'
#                         },
#                     style_as_list_view=True,
#                     style_table={#'height': 530, 
#                             # 'width':800,
#                             'overflowY': 'auto',
#                             'lineHeight': '30px'},
#                     style_header={
#                                 # 'backgroundColor': 'rgb(138,36,50)',
#                                 # 'color': 'white',
#                                 'whiteSpace':'normal',
#                                 # 'fontWeight': 'bold',
#                                 # 'font_size': '16px'
#                                 'overflowY': 'auto',
#                                 'height': 'auto',
#                     },
#                     style_data={
#                             'whiteSpace': 'normal',
#                             'height': 'auto',
#                             'font_size': '12px',
#                             'line-height': 0.9
#                             # 'width': '100px',
#                             # 'maxWidth': '100px',
#                             # 'minWidth': '100px',
#                         }, 
#                     # style_data_conditional=[
#                     #     {'if': {'column_id': 'Лимит в SAP'},
#                     #     'width': '35px'},
#                     # ]
#                 ), width=12),
#                 dcc.Graph(
#                     id="all_prepaid_bseg",
#                     figure=go.Figure(
#                         data=[
#                             go.Bar(x=dates1_1_bseg, y=points_1_c_bseg,  yaxis='y1',
#                             hovertemplate =
#                                 '<i><b>Кол-во клиентов</b></i>:  %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>',  width=500000000, name= 'Кол-во клиентов', xaxis='x1', opacity=0.5),
#                             go.Scatter(x=dates1_1_bseg, y=points_1_bseg, mode='lines', name= 'Динамическое сальдо долг',
#                             hovertemplate =
#                                 '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>',
#                                    yaxis='y2', line=dict(color="#006B19"), 
#                             line_shape='spline'),
#                             # go.Scatter(x=dates1_1_bseg, y=[12000000000 for i in dates1_1_bseg],
#                             #     hoverinfo='none', mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.1, yaxis='y2', xaxis='x2'),
#                             # go.Scatter(x=dates1_1_bseg, y=[200 for i in dates1_1_bseg]
#                             # , hoverinfo='none', mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.1, yaxis='y1', xaxis='x2'),
#                             # go.Scatter(x=dates1_1, y=points_1_c, mode='bar', secondary_y=True,name= 'Кредитный лимит из SAP', line_color='rgb(207,0,15)', xaxis='x1'),
#                             go.Scatter(x=dates1_1_bseg, y=points_1_0_bseg, mode='lines',
#                                 hoverinfo='none', name= '', line_color='rgb(217,217,217)', line_width=0.5, yaxis='y1',xaxis='x2')
#                         ],
#                         layout=go.Layout(
#                             title= 'Динамика задолженности предоплатных клиентов в разрезе кол-ва клиентов и суммы задолженности в млрд руб. (по данным бухгалтерского учета)',
#                             plot_bgcolor='white',
#                             paper_bgcolor='white',
#                             xaxis=dict(
#                                 showticklabels=False,
#                                 overlaying='x2',
#                                 showdividers=False),
#                             yaxis=dict(title='Кол-во клиентов', side='right'),
#                             yaxis2=dict(title='Долг',
#                                     overlaying='y',
#                                     side='left'),
#                             margin={'l': 30, 'b': 30, 't': 40, 'r': 0},
#                             # legend={'x': 0, 'y': 1},
#                             showlegend=True
#                         )
#                     ), style={'width': '80%'},
#                     config={'displayModeBar': False}
#                 ),
#                 html.H6('Детальная информация по задолженности предоплатных клиентов (по данным бухгалтерского учета)', className='row'),
#                 dbc.Col(dash_table.DataTable(
#                     id='datatable_clients_prepaid_bseg',
#                     columns=[{"name": col_name_rus[i][0], "id": i,
#                      "deletable": True, 'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
#                     {"name": col_name_rus[i][0], "id": i,
#                      "deletable": True, 'type': col_name_rus[i][1], 'format': dict(specifier=',.0f')}
#                      for i in    df_dog_1_1_bseg.columns],
#                     data=(df_dog_1_1_bseg).to_dict('records'),
#                     # editable=True,
#                     filter_action="native",
#                     sort_action="native",
#                     sort_mode="multi",
#                     # column_selectable="single",
#                     # row_selectable="multi",
#                     # row_deletable=True,
#                     selected_columns=[],
#                     selected_rows=[],
#                     tooltip_conditional=
#                     [
#                         {
#                             'if': {
#                                 'filter_query': "{{dog_number}} = '{}'".format(i),
#                                 'column_id': 'debitor_saldo_sum',
#                             },
#                             'backgroundColor': '#7FDBFF',
#                             'color': 'white',
#                             'type': 'markdown',
#                             'value': 'Факторинг 10,5 млрд.'
#                         }
#                         for i in factoring_dogs
#                     ],

#                     style_data_conditional=[
#                                     {
#                                         'if': {
#                                             'filter_query': "{{dog_number}} = '{}'".format(i),
#                                             'column_id': 'debitor_saldo_sum',
#                                         },
#                                         'backgroundColor': ('#0074D9' if sum_fact0 < factoring else '#97151c'),
#                                         'color': 'white',
#                                         'textDecoration': 'underline',
#                                         'textDecorationStyle': 'dotted',
#                                     }
#                                     for i in factoring_dogs
#                                 ],
#                     tooltip_delay=0,
#                     tooltip_duration=None,
#                     page_action="native",
#                     page_current= 0,
#                     page_size= 10, 
#                     # style_cell = {'textAlign': 'center'},
#                     style_cell={
#                             'minWidth': 10, 'maxWidth': 95, 'width': 10,'textAlign': 'left'
#                         },
#                     style_as_list_view=True,
#                     style_table={#'height': 530, 
#                             # 'width':800,
#                             'overflowY': 'auto',
#                             'lineHeight': '30px'},
#                     style_header={
#                                 # 'backgroundColor': 'rgb(138,36,50)',
#                                 # 'color': 'white',
#                                 'whiteSpace':'normal',
#                                 # 'fontWeight': 'bold',
#                                 # 'font_size': '16px'
#                                 'overflowY': 'auto',
#                                 'height': 'auto',
#                     },
#                     style_data={
#                             'whiteSpace': 'normal',
#                             'height': 'auto',
#                             'font_size': '12px',
#                             'line-height': 0.9
#                             # 'width': '100px',
#                             # 'maxWidth': '100px',
#                             # 'minWidth': '100px',
#                         },
#                     # style_data_conditional=[
#                     #     {'if': {'column_id': 'Лимит в SAP'},
#                     #     'width': '35px'},
#                     # ]
#                 ), width=12),
#                 dbc.Navbar(
#                 [
#                     dbc.Container(
#                             children=[
#                                 html.Details([
#                                     html.Summary('Тип договоров...',
#                                         style={'font-size': '1.3rem'}),
#                                     html.Br(),
#                                     dbc.Col([
#                                         dcc.Checklist(
#                                             id='checklist-DRO',
#                                             options=[
#                                             {'label': 'Доходный', 'value': 'D'},
#                                             {'label': 'Расходный', 'value': 'R'},
#                                             {'label': 'Доходнорасходный', 'value': 'O'},
#                                             ],
#                                             value=['D', 'R', 'O'],
#                                             labelStyle = {'display': 'block'}
#                                         )   
#                                     ])
#                                 ])
#                             ],
#                         style={'width': '13%', 
#                         'display': 'inline-block', #'marginBottom': 15,
#                         'margin-left': 30,
#                         'marginTop': 25,
#                         'color': 'white',
#                         'vertical-align':'top'}
#                         ),
#                     dbc.Container(
#                             children=[
#                                 html.Details([
#                                     html.Summary('Категория договоров...',
#                                         style={'font-size': '1.3rem'}
#                                     ),
#                                     html.Br(),
#                                     dbc.Col([
#                                         dcc.Checklist(
#                                             id='checklist-categ',
#                                             options=[ {'label': i, 'value': i} for i in df_dog_uniq['rcm_categ'].unique()],
#                                             value=df_dog_uniq['rcm_categ'].unique(),
#                                             # labelStyle = {'display': 'block'},
#                                             # style={'column-count': '2', 'white-space': 'pre-line'  ,  'overflow':'auto'}
#                                         )   
#                                     ])
#                                 ])
#                             ],
#                         style={'width': '15%', 
#                         'display': 'inline-block', 'marginBottom': 15,
#                          'margin-left': 10,
#                          'marginTop': 25,
#                         'color': 'white',
#                         'vertical-align':'top'}
#                         ),
#                     dbc.Col([
#                         html.H6('Детализация'),
#                         dcc.RadioItems(
#                             id='RI-OS',
#                             options=[
#                                 {'label': 'Суммарно по клиенту', 'value': 'S'},
#                                 {'label': 'Отдельные договоры', 'value': 'O'},
                                
#                             ],
#                             value='S'
#                         ),
#                         ],
#                         style={'width': '13%', 
#                             'display': 'inline-block', 'marginBottom': 15, 'margin-left': 20,'marginTop': 25,
#                             'color': 'white',
#                         'vertical-align':'top'}
#                     ),
#                     dbc.Col(
#                         [
#                         html.H6('Холдинг\компания'),
#                         dcc.RadioItems(
#                             id='RI-CH',
#                             options=[
#                                 {'label': 'Компании', 'value': 'C'},
#                                 {'label': 'Холдинги', 'value': 'H'},
#                             ],
#                             value='C'
#                         ),
#                         ],
#                         style={'width': '15%', 
#                             'display': 'inline-block', 'marginBottom': 15, 'margin-left': 10,'marginTop': 25,
#                             'color': 'white',
#                         'vertical-align':'top'}
#                     ),
#                     dcc.Dropdown(
#                         id="dashboard13-dropdown-company",
#                         options=[ {'label': i, 'value': i} for i in df_dog_uniq[ 'name1'].unique()],
#                         value='ПАО "НЛМК"',
#                         clearable=False,
#                         style={"display": "flex",
#                             "justify-content": "center",
#                             # 'width': '20%', 
#                             'display': 'inline-block', #'marginBottom': 15, 'margin-left': 10,
#                             'marginTop': 25,
#                         'vertical-align':'top',
#                         'text-align': 'left',
#                         # 'padding': '0 10px',
#                         # 'margin-bottom': '5px',
#                             },
#                         # className='three-columns'
                        
#                         ),
#                 ],dark=True, color='rgb(71, 71, 71)',
#                 style={'marginBottom': 15, 'margin-left': 15,'marginTop': 40}
#                 ),
#                 html.Button('Submit', id='submit-val_f', n_clicks=0,
#                     style={'width': '15%', 
#                     'marginBottom': 15, 'margin-left': 15,'marginTop': 40
#                      },
#                     className='Button_mine'),


#                 dcc.Graph(
#                     id="nlmk_severstal",
#                     figure=go.Figure(
#                         data=[#go.Bar(
#                             #     x=df_result_t_m[df_result_t_m['zuonr']==i].index,
#                             #     y=df_result_t_m[df_result_t_m['zuonr']==i]['dmbtr'],
#                             #     name=df_result_t_m[df_result_t_m['zuonr']==i][ 'rcm_dognum_reg'].values[0],
#                             # #     xperiod="M3",
#                             # #     xperiodalignment="middle",
#                             # #     xhoverformat="Q%q",
#                             #     customdata=df_result_t_m[df_result_t_m['zuonr']==i][['rcm_vid', 'rcm_categ', 'rcm_dognum_reg']],
#                             #     hovertemplate='<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                             #                             '<br><b>Дата</b>: %{x}'+
#                             #     '<br><b>Тип договора</b>: %{customdata[0]}'+
#                             #     '<br><b>Категория договора</b>: %{customdata[1]}'+
#                             #     '<br><b>Номер договора</b>: %{customdata[2]}'+'<br><extra></extra>'
#                             # ) for i  in df_result_t_m['zuonr'].unique()
#                             go.Bar(
#                                     x=df_result_t_m.index,
#                                     y=df_result_t_m['dmbtr'],
#                                     name='ПАО "НЛМК"',
#                                     hovertemplate='<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                                             '<br><b>Дата</b>: %{x}'+
#                                                             '<br><extra></extra>'
#                                 ) 
#                                                     ],
#                         layout=go.Layout(
#                             title= 'Сальдо ПАО "НЛМК"',
#                             # title={
#                             #         'text': 'Сальдо по договорам ПАО "НЛМК"',
#                             #         'style':{'font-weight': 'bold'}},
#                             plot_bgcolor='white',
#                             paper_bgcolor='white',
#                             # xaxis=dict(
#                             #     showticklabels=False,
#                             #     overlaying='x2',
#                             #     showdividers=False),
#                             # yaxis=dict(title='Кол-во клиентов', side='right'),
#                             # yaxis2=dict(title='Долг',
#                             #         overlaying='y',
#                             #         side='left'),
#                             margin={'l': 30, 'b': 30, 't': 40, 'r': 0},
#                             # legend={
#                             #     'itemwidth':'10'
#                             #     # 'x': 0, 'y': 1
#                             #     },
#                             barmode='relative',
#                             showlegend=True
#                         )
#                     ), style={'width': '100%'},
#                     config={'displayModeBar': False}
#                 ),



                

#  ], className='eleven columns', style={'marginBottom': 15, 'margin-left': 30,'marginTop': 25,
#                         }),
        
        
       
        ], 
        className='twelve columns', 
        style={'fontSize': 12})
    return layout


# def create_layout(): 
#     df_dog_1,df_dog_2,df_dog_3=get_dates_for_table()
#     df_dog_2_1=get_matrix_stat_1(df_dog_2)
#     df_dog_3_1=get_matrix_stat_2(df_dog_3)
#     df_dog_1_1=get_matrix_stat_1(df_dog_1)
#     df_dog_1_1=df_dog_1_1[[i for i in df_dog_1_1.columns if i not in ['res','max', 'percent','days_off_cur_sum', 
#      'dept_days_off_sum', 'dept_days_off_max','dept_over_lim']]]
#     is_need_bseg=True
#     if is_need_bseg:
#         df_dog_1_bseg,df_dog_2_bseg,df_dog_3_bseg,factoring_dogs, sum_fact=get_dates_for_table_bseg()
#         df_dog_2_1_bseg, sum_fact0=get_matrix_stat_1_bseg(df_dog_2_bseg,sum_fact)
#         df_dog_3_1_bseg, sum_fact0=get_matrix_stat_2_bseg(df_dog_3_bseg, sum_fact)
#         df_dog_1_1_bseg, sum_fact0=get_matrix_stat_1_bseg(df_dog_1_bseg, sum_fact)
#         df_dog_1_1_bseg=df_dog_1_1_bseg[[i for i in df_dog_1_1_bseg.columns if i not in ['res','max', 'percent','days_off_cur_sum', 
#      'dept_days_off_sum', 'dept_days_off_max','dept_over_lim']]]
#     else:
#         df_dog_1_bseg,df_dog_2_bseg,df_dog_3_bseg=(df_dog_1,df_dog_2,df_dog_3)
#         df_dog_2_1_bseg=df_dog_2_1
#         df_dog_3_1_bseg=df_dog_3_1
#         df_dog_1_1_bseg=df_dog_1_1
#         df_dog_1_1_bseg=df_dog_1_1_bseg[[i for i in df_dog_1_1_bseg.columns if i not in ['res','max', 'percent','days_off_cur_sum', 
#      'dept_days_off_sum', 'dept_days_off_max','dept_over_lim']]]
   
#     col_name_rus={
#         'yur_hold':['Холдинг','str', 0],
#         'rcm_categ':['Вид договора','str', 0],
#         'clients_count':['Кол-во превышений лимита','numeric', 1],
#         'postpone_pay':['Кол-во дней отсрочки платежа','numeric', 1],
#         'prosrochka':['Просроченная задолжность','numeric', 1],
#         'percent':['Доля долга','numeric', 1],
#         'res':['Кол-во превышений лимита','numeric', 1], 
#         'max':['Максимальное превышение лимита','numeric', 1],
#         'rating':['Рейтинг','numeric', 1],
#         'garanty':['Гарантии','numeric', 1],
#         'date':['Дата','str', 0],
#         'client':['id клиента','numeric', 0], 
#         'client_name':['Клиента','str', 0],
#         'id_rcm':['id договора','numeric', 0], 
#         'filial':['Филиал','str', 0],
#         'dog_number':['Договор','str', 0],
#         'dinamic_saldo':['Сальдо','numeric', 1],
#         'lim_sum':['Лимит','numeric', 1], 
#         'lim_warr_garanty' :['Обеспечение','numeric', 1],
#         'lim_guar_garanty' :['Гарантии','numeric', 1],
#         'dept_over_lim':['Превышение лимита','numeric', 1], 
#         'dinamic_saldo_X':['Сальдо безлимитных','numeric', 1],
#         'debitor':['debitor','numeric', 1],   
#         'debitor_X':['debitor_X','numeric', 1], 
#         'debitor_saldo_sum':['Дебиторское сальдо','numeric', 1], 
#         'days_off_cur_sum':['Дней просрочки на дату','numeric', 1], 
#         'dept_days_off_sum':['Долг просроченный на дату','numeric', 1], 
#         'dept_days_off_max':['Максимальный просроченный долг за период','numeric', 1],


#         'dinamic_saldo_min':['Минимальное сальдо','numeric', 1], 
#         'dinamic_saldo_mean_below_zero':['Средняя задолженность','numeric', 1], 
#         'dept_over_lim_min':['Максимальное превышение лимита','numeric', 1], 
#         'dept_over_lim_mean':['Среднее превышение лимита','numeric', 1],
#         'days_over_limit_max':['Максимум дней выше лимита','numeric', 1], 
#         'days_over_limit_mean':['Среднее число дней выше лимита','numeric', 1], 
#         'days_over_limit_count_days_over':['Число превышений лимита','numeric', 1], 
#         'days_over_limit':['Текущее число дней выше лимита','numeric', 1], 
#         'debitor_min':['debitor_min','numeric', 1], 
#         'debitor_mean_below_zero':['debitor_mean_below_zero','numeric', 1], 
#         'dept_over_lim_min_y':['dept_over_lim_min_y','numeric', 1],
#         'dept_over_lim_mean_y':['dept_over_lim_mean_y','numeric', 1], 
#         'days_over_limit_max_y':['days_over_limit_max_y','numeric', 1], 
#         'days_over_limit_mean_y':['days_over_limit_mean_y','numeric', 1], 
#         'days_over_limit_count_days_over_y':['days_over_limit_count_days_over_y','numeric', 1],
#         'dept_over_lim_y':['dept_over_lim_y','numeric', 1], 
#         'days_over_limit_y':['days_over_limit_y','numeric', 1]
	
#     }
    
#     print('5. Все и безлимитные')
#     df_all0=get_credit_data_all()
#     max_date=df_all0['date'].max()
#     min_date=df_all0['date'].min()
#     df_all0=df_all0.set_index('date')
    
#     dates=df_all0.index.date

#     df_all0_M=df_all0.groupby([pd.Grouper( freq="1M"),'3_group']).mean().reset_index(1)
#     df_all0_M_1=df_all0_M[df_all0_M['3_group']==1]
#     df_all0_M_2=df_all0_M[df_all0_M['3_group']==2]
#     df_all0_M_3=df_all0_M[df_all0_M['3_group']==3]
#     dates1_1=df_all0_M_1.index.date
#     dates1_2=df_all0_M_2.index.date
#     dates1_3=df_all0_M_3.index.date
#     df_all0_M_1=df_all0_M_1.reset_index()
#     df_all0_M_2=df_all0_M_2.reset_index()
#     df_all0_M_3=df_all0_M_3.reset_index()
#     # df_all0_M['date'] = df_all0_M['date'].dt.strftime('%m-%Y')
    
#     # df_filial['date'] = df_filial['date'].dt.strftime('%d/%m/%Y')
#     # df_clients['date'] = df_clients['date'].dt.strftime('%d/%m/%Y')
#     # points1=df_all0['lim_sum'].values
#     points_1=df_all0_M_3['dinamic_saldo'].values
#     points_1_c=df_all0_M_1['clients_count'].values
#     points_2=df_all0_M_2['dinamic_saldo'].values
#     points_3=df_all0_M_3['dinamic_saldo'].values
    
#     # points3=df_all0['dinamic_saldo_X'].values
#     # points4=df_all0['dept_over_lim'].values
#     points_1_0=[0 for i in dates1_1]
#     points_2_0=[0 for i in dates1_2]
#     points_3_0=[0 for i in dates1_3]
    
#     print('5. Все и безлимитные bseg')
#     if is_need_bseg:
#         df_all0_bseg=get_credit_data_all_bseg()
#     else:
#         df_all0_bseg=get_credit_data_all()
#         df_all0_bseg=df_all0_bseg.rename(columns={'dinamic_saldo':'debitor_saldo_sum'})

#     max_date_bseg=df_all0_bseg['date'].max()
#     min_date_bseg=df_all0_bseg['date'].min()
#     df_all0_bseg=df_all0_bseg.set_index('date')
    
#     dates_bseg=df_all0_bseg.index.date

#     df_all0_M_bseg=df_all0_bseg.groupby([pd.Grouper( freq="1M"),'3_group']).mean().reset_index(1)
#     df_all0_M_1_bseg=df_all0_M_bseg[df_all0_M_bseg['3_group']==1]
#     df_all0_M_2_bseg=df_all0_M_bseg[df_all0_M_bseg['3_group']==2]
#     df_all0_M_3_bseg=df_all0_M_bseg[df_all0_M_bseg['3_group']==3]
#     dates1_1_bseg=df_all0_M_1_bseg.index.date
#     dates1_2_bseg=df_all0_M_2_bseg.index.date
#     dates1_3_bseg=df_all0_M_3_bseg.index.date
#     df_all0_M_1_bseg=df_all0_M_1_bseg.reset_index()
#     df_all0_M_2_bseg=df_all0_M_2_bseg.reset_index()
#     df_all0_M_3_bseg=df_all0_M_3_bseg.reset_index()
#     # df_all0_M['date'] = df_all0_M['date'].dt.strftime('%m-%Y')
    
#     # df_filial['date'] = df_filial['date'].dt.strftime('%d/%m/%Y')
#     # df_clients['date'] = df_clients['date'].dt.strftime('%d/%m/%Y')
#     # points1=df_all0['lim_sum'].values
#     # if is_need_bseg:
#     points_1_bseg=df_all0_M_3_bseg['debitor_saldo_sum'].values
#     points_1_c_bseg=df_all0_M_1_bseg['clients_count'].values
#     points_2_bseg=df_all0_M_2_bseg['debitor_saldo_sum'].values
#     points_3_bseg=df_all0_M_3_bseg['debitor_saldo_sum'].values
#     points_3_p_bseg=df_all0_M_3_bseg['percent'].values
#     # else:
#     #     points_1_bseg=points_1
#     #     points_1_c_bseg=points_1_c
#     #     points_2_bseg=points_2
#     #     points_3_bseg=points_3


#     # points3=df_all0['dinamic_saldo_X'].values
#     # points4=df_all0['dept_over_lim'].values
#     points_1_0_bseg=[0 for i in dates1_1_bseg]
#     points_2_0_bseg=[0 for i in dates1_2_bseg]
#     points_3_0_bseg=[0 for i in dates1_3_bseg]
#     print("saldo")
#     global df_saldo
#     df_result_t=get_saldo_bseg( name1='ПАО "НЛМК"')
#     df_dog_uniq=get_saldo_bseg_uniq()
#     df_result_t_m=get_saldo_bseg_group( name1='ПАО "НЛМК"')
#     df_result_t_m=df_result_t_m.set_index('date')
    
#     # df_result_t_m=df_result_t.groupby([pd.Grouper( freq="1M"),#'zuonr', 
#     # #'kunnr', 'rcm_vid', 'rcm_categ', 
#     # 'name1', 'yur_hold',# 'rcm_dognum_reg'
#     # ]).mean().reset_index(1)
#     # df_result_t_m=df_result_t_m.reset_index([1,2,3,4,#5,6
#     # ])

#     print("5. Старт загрузки layout")

#     layout = html.Div(
#         [   dcc.Store(id='intermediate-value', data=df_dog_uniq.to_dict('records')),
#             html.Div(
#                 html.H5("Отчет кредитных рисков", className='row' ,
#                 style={'font-size': '3rem', 'padding-top':'30px'}
#                 ),
#                 className='product'
#             ),
#             html.Div([
#                 dcc.Tabs(id='dashboard13-tabs', value='tab-1', children=[
#                     dcc.Tab(label='Динсальдо', value='tab-1', className="tab",),
#                     dcc.Tab(label='Bseg', value='tab-2', className="tab",),
#                     dcc.Tab(label='Сальдо по бухучету', value='tab-3', className="tab",),
#                 ], className="row all-tabs"),
#                 #html.Div(id='tabs-example-content')
#             ]),

#             # Row 5 - Содержимое закладки
#             html.Div(id='tab-content13'),
#             dcc.Graph(
#                 id="all_bar",
#                 figure=go.Figure(
#                     data=[
#                         go.Bar(name='Отсрочка платежа без потолка лимита', x=dates1_1, y=df_all0_M_1['dinamic_saldo'].values,
#                         hovertemplate =
#                                 '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>', xaxis='x1', marker_color="#97151c"),
#                         go.Bar(name='Кредитный лимит с отсрочкой платежа', x=dates1_2,hovertemplate =
#                                 '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>', y=points_2, xaxis='x1', marker_color='rgb(193, 122, 117)'),#'#006B19'
#                         go.Bar(name='Предоплата', x=dates1_3, y=points_3,hovertemplate =
#                                 '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>', xaxis='x1', marker_color='rgb(206, 205, 181)')
#                     ],
                    
#                     layout=go.Layout(
#                         title= 'Помесячная динамика дебиторской задолженности (в млрд руб., по данным отчета «Дин. сальдо»).',
#                         barmode='stack',
#                         plot_bgcolor='white',
#                         paper_bgcolor='white',
#                         # xaxis=dict(
#                         #     showticklabels=False,
#                         #     overlaying='x2',
#                         #     showdividers=False),
#                         margin={'l': 30, 'b': 30, 't': 80, 'r': 0},
#                         # legend={'x': 0, 'y': 1},
#                         showlegend=True
#                     )
#                 ), style={'width': '80%'},
#                 config={'displayModeBar': False}
#             ),
#             dcc.Graph(
#                 id="all_limit",
#                 figure=go.Figure(
#                     data=[
#                         go.Scatter(x=dates1_2, y=points_2, mode='lines',
#                         hovertemplate =
#                                 '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>',
#                           name= 'Динамическое сальдо долг', #line_color='rgb(40,80,0)', 
#                         fill='tonexty',line_shape='spline', xaxis='x1', line=dict(color="#006B19")),
#                         # go.Bar(name='Динамическое сальдо долг', x=dates1_2, y=points_2, xaxis='x1'),
#                         go.Scatter(x=dates1_2, y=df_all0_M_2['lim_sum'].values, mode='lines',
#                         hovertemplate =
#                                 '<i><b>Лимит</b></i>: \u20bd %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>',
#                          name= 'Кредитный лимит из SAP', line_color='#97151c', xaxis='x1'),
#                         go.Scatter(x=dates1_2, y=points_2_0, mode='lines',hoverinfo='none', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2'),
#                         # go.Scatter(x=dates1_2, y=[4800000000 for i in dates1_2], hoverinfo='none',mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.1, xaxis='x2')

#                         ],
#                     layout=go.Layout(
#                         title= 'Динамика задолженности клиентов с кредитным лимитом с отсрочкой платежа (в млрд руб., по данным отчета «Дин. сальдо»)',
#                         plot_bgcolor='white',
#                         paper_bgcolor='white',
#                         xaxis=dict(
#                             showticklabels=False,
#                             overlaying='x2',
#                             showdividers=False),
#                         margin={'l': 30, 'b': 30, 't': 80, 'r': 0},
#                         # legend={'x': 0, 'y': 1},
#                         showlegend=True
#                     )
#                 ), style={'width': '80%'},
#                 config={'displayModeBar': False}
#             ),
#             html.Div(    
#                 dbc.Navbar(
#                 [
#                     html.Div('Выберите начальную дату:', 
#                         style={'width': '15%', 
#                         'display': 'inline-block', 'marginBottom': 15, 'margin-left': 30,'marginTop': 25,
#                         'color': 'white'}
#                     ),
#                     dcc.DatePickerSingle(
#                         # calendar_orientation='vertical',
#                         clearable=True,
#                         id='risk_str_date',
#                         date=min_date,
#                         min_date_allowed=min_date,
#                         max_date_allowed=max_date,
#                         initial_visible_month=min_date,
#                         number_of_months_shown = 3,
#                         display_format='DD.MM.YYYY',
#                         style={'width': '20%', 'display': 'inline-block', 'color': 'white'}
#                     ),
#                     html.Div('Выберите последнюю дату:', 
#                         style={'width': '15%', 'display': 'inline-block', 'color': 'white'}
#                     ),
#                     dcc.DatePickerSingle(
#                         calendar_orientation='vertical',
#                         clearable=True,
#                         id='risk_end_date',
#                         date=max_date,
#                         min_date_allowed=min_date,
#                         max_date_allowed=max_date,
#                         initial_visible_month=min_date,
#                         number_of_months_shown = 3,
#                         display_format='DD.MM.YYYY',
#                         style={'width': '20%', 'display': 'inline-block', 'color': 'white'}
#                     ),
#                     html.Button('Submit', id='submit-val', n_clicks=0,
#                         style={'width': '15%', 'display': 'inline-block', 'background-color': 'white', }),
#                 ],dark=True, color='rgb(71, 71, 71)'
#                 )
#             ),

#             html.Div([
#                 html.H6('Детальная информация по задолженности клиентов с кредитным лимитом с отсрочкой платежа (по данным отчета «Дин. сальдо»)',
#                 className='row'),
#                 dbc.Col(dash_table.DataTable(
#                     id='datatable_clients_limit',
#                     columns=[{"name": col_name_rus[i][0], "id": i,
#                     #  "deletable": True, 
#                      'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
#                     {"name": col_name_rus[i][0], "id": i,
#                     #  "deletable": True, 
#                      'type': col_name_rus[i][1], 'format': dict(specifier=',.0f')}
#                      for i in    df_dog_2_1.columns if i not in ['rating', 'garanty']],
#                     data=(df_dog_2_1).to_dict('records'),
#                     # editable=True,
#                     filter_action="native",
#                     sort_action="native",
#                     sort_mode="multi",
#                     # column_selectable="single",
#                     # row_selectable="multi",
#                     # row_deletable=True,
#                     selected_columns=[],
#                     selected_rows=[],
#                     # page_action="native",
#                     # page_current= 0,
#                     page_size= 10, 
#                     # style_cell = {'textAlign': 'center'},
#                     style_cell={
#                             'minWidth': 10, 'maxWidth': 95, 'width': 10,'textAlign': 'left'
#                         },
#                     style_as_list_view=True,
#                     style_table={#'height': 530, 
#                             # 'width':800,
#                             'overflowY': 'auto',
#                             'lineHeight': '30px'},
#                     style_header={
#                                 # 'backgroundColor': 'rgb(138,36,50)',
#                                 # 'color': 'white',
#                                 'whiteSpace':'normal',
#                                 # 'fontWeight': 'bold',
#                                 # 'font_size': '16px'
#                                 'overflowY': 'auto',
#                                 'height': 'auto',
#                     },
#                     style_data={
#                             'whiteSpace': 'normal',
#                             'height': 'auto',
#                             'font_size': '12px',
#                             'line-height': 0.9
#                             # 'width': '100px',
#                             # 'maxWidth': '100px',
#                             # 'minWidth': '100px',
#                         },
#                     # style_data_conditional=[
#                     #     {'if': {'column_id': 'Лимит в SAP'},
#                     #     'width': '35px'},
#                     # ]
#                 ), width=12),
#                 dcc.Graph(
#                 id="all_x",
#                 figure=go.Figure(
#                     data=[
#                         go.Scatter(x=dates1_3, y=points_3, mode='lines', hovertemplate =
#                                 '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>',
#                         name= 'Динамическое сальдо долг', line=dict(color="#006B19"), line_shape='spline', xaxis='x1'),
#                         go.Scatter(x=dates1_3, y=points_3_0, mode='lines',hoverinfo='none', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')
#                     ],
#                     layout=go.Layout(
#                         title= 'Динамика задолженности клиентов с отсрочкой платежа без потолка лимита (в млрд руб., по данным отчета «Дин. сальдо»)',
#                         plot_bgcolor='white',
#                         paper_bgcolor='white',
#                         xaxis=dict(
#                             showticklabels=False,
#                             overlaying='x2',
#                             showdividers=False),
#                         margin={'l': 30, 'b': 30, 't': 80, 'r': 0},
#                         # legend={'x': 0, 'y': 1},
#                         showlegend=True
#                     )
#                 ), style={'width': '80%'},
#                 config={'displayModeBar': False}
#             ),
#                 html.H6('Детальная информация по задолженности клиентов с отсрочкой платежа без потолка лимита (по данным отчета «Дин. сальдо»)', className='row'),
#                 dbc.Col(dash_table.DataTable(
#                     id='datatable_clients_X',
#                     columns=[{"name": col_name_rus[i][0], "id": i,
#                      "deletable": True, 'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
#                     {"name": col_name_rus[i][0], "id": i,
#                      "deletable": True, 'type': col_name_rus[i][1], 'format': dict(specifier=',.0f')}
#                      for i in    df_dog_3_1.columns],
#                     data=(df_dog_3_1).to_dict('records'),
#                     # editable=True,
#                     filter_action="native",
#                     sort_action="native",
#                     sort_mode="multi",
#                     # column_selectable="single",
#                     # row_selectable="multi",
#                     # row_deletable=True,
#                     selected_columns=[],
#                     selected_rows=[],
#                     page_action="native",
#                     page_current= 0,
#                     page_size= 10, 
#                    # style_cell = {'textAlign': 'center'},
#                     style_cell={
#                             'minWidth': 10, 'maxWidth': 95, 'width': 10,'textAlign': 'left'
#                         },
#                     style_as_list_view=True,
#                     style_table={#'height': 530, 
#                             # 'width':800,
#                             'overflowY': 'auto',
#                             'lineHeight': '30px'},
#                     style_header={
#                                 # 'backgroundColor': 'rgb(138,36,50)',
#                                 # 'color': 'white',
#                                 'whiteSpace':'normal',
#                                 # 'fontWeight': 'bold',
#                                 # 'font_size': '16px'
#                                 'overflowY': 'auto',
#                                 'height': 'auto',
#                     },
#                     style_data={
#                             'whiteSpace': 'normal',
#                             'height': 'auto',
#                             'font_size': '12px',
#                             'line-height': 0.9
#                             # 'width': '100px',
#                             # 'maxWidth': '100px',
#                             # 'minWidth': '100px',
#                         }, 
#                     # style_data_conditional=[
#                     #     {'if': {'column_id': 'Лимит в SAP'},
#                     #     'width': '35px'},
#                     # ]
#                 ), width=12),
#                 dcc.Graph(
#                     id="all_prepaid",
#                     figure=go.Figure(
#                         data=[
#                             go.Bar(x=dates1_1, y=points_1_c,  yaxis='y1',
#                             hovertemplate =
#                                 '<i><b>Кол-во клиентов</b></i>:  %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>',  width=500000000, name= 'Кол-во клиентов', xaxis='x1', opacity=0.5),
#                             go.Scatter(x=dates1_1, y=points_1, mode='lines', name= 'Динамическое сальдо долг',
#                             hovertemplate =
#                                 '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>',
#                                    yaxis='y2', line=dict(color="#006B19"), 
#                             line_shape='spline'),
#                             # go.Scatter(x=dates1_1, y=[12000000000 for i in dates1_1],
#                             #     hoverinfo='none', mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.1, yaxis='y2', xaxis='x2'),
#                             # go.Scatter(x=dates1_1, y=[200 for i in dates1_1]
#                             # , hoverinfo='none', mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.1, yaxis='y1', xaxis='x2'),
#                             # go.Scatter(x=dates1_1, y=points_1_c, mode='bar', secondary_y=True,name= 'Кредитный лимит из SAP', line_color='rgb(207,0,15)', xaxis='x1'),
#                             go.Scatter(x=dates1_1, y=points_1_0, mode='lines',
#                                 hoverinfo='none', name= '', line_color='rgb(217,217,217)', line_width=0.5, yaxis='y1',xaxis='x2')
#                         ],
#                         layout=go.Layout(
#                             title= 'Динамика задолженности предоплатных клиентов в разрезе кол-ва клиентов и суммы задолженности в млрд руб. (по данным отчета «Дин. сальдо»)',
#                             plot_bgcolor='white',
#                             paper_bgcolor='white',
#                             xaxis=dict(
#                                 showticklabels=False,
#                                 overlaying='x2',
#                                 showdividers=False),
#                             yaxis=dict(title='Кол-во клиентов', side='right'),
#                             yaxis2=dict(title='Долг',
#                                     overlaying='y',
#                                     side='left'),
#                             margin={'l': 30, 'b': 30, 't': 40, 'r': 0},
#                             # legend={'x': 0, 'y': 1},
#                             showlegend=True
#                         )
#                     ), style={'width': '80%'},
#                     config={'displayModeBar': False}
#                 ),
#                 html.H6('Детальная информация по задолженности предоплатных клиентов (по данным отчета «Дин. сальдо»)', className='row'),
#                 dbc.Col(dash_table.DataTable(
#                     id='datatable_clients_prepaid',
#                     columns=[{"name": col_name_rus[i][0], "id": i,
#                      "deletable": True, 'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
#                     {"name": col_name_rus[i][0], "id": i,
#                      "deletable": True, 'type': col_name_rus[i][1], 'format': dict(specifier=',.0f')}
#                      for i in    df_dog_1_1.columns],
#                     data=(df_dog_1_1).to_dict('records'),
#                     # editable=True,
#                     filter_action="native",
#                     sort_action="native",
#                     sort_mode="multi",
#                     # column_selectable="single",
#                     # row_selectable="multi",
#                     # row_deletable=True,
#                     selected_columns=[],
#                     selected_rows=[],
#                     page_action="native",
#                     page_current= 0,
#                     page_size= 10, 
#                     # style_cell = {'textAlign': 'center'},
#                     style_cell={
#                             'minWidth': 10, 'maxWidth': 95, 'width': 10,'textAlign': 'left'
#                         },
#                     style_as_list_view=True,
#                     style_table={#'height': 530, 
#                             # 'width':800,
#                             'overflowY': 'auto',
#                             'lineHeight': '30px'},
#                     style_header={
#                                 # 'backgroundColor': 'rgb(138,36,50)',
#                                 # 'color': 'white',
#                                 'whiteSpace':'normal',
#                                 # 'fontWeight': 'bold',
#                                 # 'font_size': '16px'
#                                 'overflowY': 'auto',
#                                 'height': 'auto',
#                     },
#                     style_data={
#                             'whiteSpace': 'normal',
#                             'height': 'auto',
#                             'font_size': '12px',
#                             'line-height': 0.9
#                             # 'width': '100px',
#                             # 'maxWidth': '100px',
#                             # 'minWidth': '100px',
#                         },
#                     # style_data_conditional=[
#                     #     {'if': {'column_id': 'Лимит в SAP'},
#                     #     'width': '35px'},
#                     # ]
#                 ), width=12),

#                 dcc.Graph(
#                     id="all_bar_bseg",
#                     figure=go.Figure(
#                         data=[
#                             go.Bar(name='Отсрочка платежа без потолка лимита', x=dates1_1_bseg, y=df_all0_M_1_bseg['debitor_saldo_sum'].values,
#                             hovertemplate =
#                                     '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                     '<br><b>Дата</b>: %{x}<br><extra></extra>', xaxis='x1', marker_color="#97151c"),
#                             go.Bar(name='Кредитный лимит с отсрочкой платежа', x=dates1_2_bseg,hovertemplate =
#                                     '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                     '<br><b>Дата</b>: %{x}<br><extra></extra>', y=points_2_bseg, xaxis='x1', marker_color='rgb(193, 122, 117)'),#'#006B19'
#                             go.Bar(name='Предоплата', x=dates1_3_bseg, y=points_3_bseg,hovertemplate =
#                                     '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                     '<br><b>Дата</b>: %{x}<br><extra></extra>', xaxis='x1', marker_color='rgb(206, 205, 181)')
#                         ],
                        
#                         layout=go.Layout(
#                             title= 'Помесячная динамика дебиторской задолженности (в млрд руб., по данным бухгалтерского учета)',
#                             barmode='stack',
#                             plot_bgcolor='white',
#                             paper_bgcolor='white',
#                             # xaxis=dict(
#                             #     showticklabels=False,
#                             #     overlaying='x2',
#                             #     showdividers=False),
#                             margin={'l': 30, 'b': 30, 't': 80, 'r': 0},
#                             # legend={'x': 0, 'y': 1},
#                             showlegend=True
#                         )
#                     ), style={'width': '80%'},
#                     config={'displayModeBar': False}
#                 ),
#                 dcc.Graph(
#                     id="all_limit_bseg",
#                     figure=go.Figure(
#                         data=[
#                             go.Scatter(x=dates1_2_bseg, y=points_2_bseg, mode='lines',
#                             hovertemplate =
#                                     '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                     '<br><b>Дата</b>: %{x}<br><extra></extra>',
#                             name= 'Динамическое сальдо долг', #line_color='rgb(40,80,0)', 
#                             fill='tonexty',line_shape='spline', xaxis='x1', line=dict(color="#006B19")),
#                             # go.Bar(name='Динамическое сальдо долг', x=dates1_2, y=points_2, xaxis='x1'),
#                             go.Scatter(x=dates1_2_bseg, y=df_all0_M_2_bseg['lim_sum'].values, mode='lines',
#                             hovertemplate =
#                                     '<i><b>Лимит</b></i>: \u20bd %{y:,.0f}'+
#                                     '<br><b>Дата</b>: %{x}<br><extra></extra>',
#                             name= 'Кредитный лимит из SAP', line_color='#97151c', xaxis='x1'),
#                             go.Scatter(x=dates1_2_bseg, y=points_2_0_bseg, mode='lines',hoverinfo='none', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2'),
#                             # go.Scatter(x=dates1_2_bseg, y=[4800000000 for i in dates1_2_bseg], hoverinfo='none',mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.1, xaxis='x2')

#                             ],
#                         layout=go.Layout(
#                             title= 'Динамика задолженности клиентов с кредитным лимитом с отсрочкой платежа (в млрд руб., по данным бухгалтерского учета)',
#                             plot_bgcolor='white',
#                             paper_bgcolor='white',
#                             xaxis=dict(
#                                 showticklabels=False,
#                                 overlaying='x2',
#                                 showdividers=False),
#                             margin={'l': 30, 'b': 30, 't': 80, 'r': 0},
#                             # legend={'x': 0, 'y': 1},
#                             showlegend=True
#                         )
#                     ), style={'width': '80%'},
#                     config={'displayModeBar': False}
#                 ),
#                 dbc.Navbar(
#                 [
#                     html.Div('Выберите начальную дату_bseg:', 
#                         style={'width': '15%', 
#                         'display': 'inline-block', 'marginBottom': 15, 'margin-left': 30,'marginTop': 25,
#                         'color': 'white'}
#                     ),
#                     dcc.DatePickerSingle(
#                         # calendar_orientation='vertical',
#                         clearable=True,
#                         id='risk_str_date_bseg',
#                         date=min_date_bseg,
#                         min_date_allowed=min_date_bseg,
#                         max_date_allowed=max_date_bseg,
#                         initial_visible_month=min_date_bseg,
#                         number_of_months_shown = 3,
#                         display_format='DD.MM.YYYY',
#                         style={'width': '20%', 'display': 'inline-block', 'color': 'white'}
#                     ),
#                     html.Div('Выберите последнюю дату_bseg:', 
#                         style={'width': '15%', 'display': 'inline-block', 'color': 'white'}
#                     ),
#                     dcc.DatePickerSingle(
#                         calendar_orientation='vertical',
#                         clearable=True,
#                         id='risk_end_date_bseg',
#                         date=max_date_bseg,
#                         min_date_allowed=min_date_bseg,
#                         max_date_allowed=max_date_bseg,
#                         initial_visible_month=min_date_bseg,
#                         number_of_months_shown = 3,
#                         display_format='DD.MM.YYYY',
#                         style={'width': '20%', 'display': 'inline-block', 'color': 'white'}
#                     ),
#                     html.Button('Submit', id='submit-val_bseg', n_clicks=0,
#                         style={'width': '15%', 'display': 'inline-block', 'background-color': 'white', }),
#                 ],dark=True, color='rgb(71, 71, 71)'
#                 ),
#                 html.H6('Детальная информация по задолженности клиентов с кредитным лимитом с отсрочкой платежа (по данным бухгалтерского учета)', className='row'),
#                 dbc.Col(dash_table.DataTable(
#                     id='datatable_clients_limit_bseg',
#                     columns=[{"name": col_name_rus[i][0], "id": i,
#                     #  "deletable": True, 
#                      'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
#                     {"name": col_name_rus[i][0], "id": i,
#                     #  "deletable": True, 
#                      'type': col_name_rus[i][1], 'format': dict(specifier=',.0f') if i!= 'percent' else FormatTemplate.percentage(2)}
#                      for i in    df_dog_2_1_bseg.columns if i not in ['rating', 'garanty']],
#                     data=(df_dog_2_1_bseg).to_dict('records'),
#                     # editable=True,
#                     filter_action="native",
#                     sort_action="native",
#                     sort_mode="multi",
#                     # column_selectable="single",
#                     # row_selectable="multi",
#                     # row_deletable=True,
#                     selected_columns=[],
#                     selected_rows=[],
#                     tooltip_conditional=
#                     [
#                         {
#                             'if': {
#                                 'filter_query': "{{dog_number}} = '{}'".format(i),
#                                 'column_id': 'debitor_saldo_sum',
#                             },
#                             'backgroundColor': '#7FDBFF',
#                             'color': 'white',
#                             'type': 'markdown',
#                             'value': 'Факторинг 10,5 млрд.'
#                         }
#                         for i in factoring_dogs
#                     ],

#                     style_data_conditional=[
#                                     {
#                                         'if': {
#                                             'filter_query': "{{dog_number}} = '{}'".format(i),
#                                             'column_id': 'debitor_saldo_sum',
#                                         },
#                                         'backgroundColor': ('#0074D9' if sum_fact0 < factoring else '#97151c'),
#                                         'color': 'white',
#                                         'textDecoration': 'underline',
#                                         'textDecorationStyle': 'dotted',
#                                     }
#                                     for i in factoring_dogs
#                                 ],
#                     tooltip_delay=0,
#                     tooltip_duration=None,
#                     # page_action="native",
#                     # page_current= 0,
#                     page_size= 10, 
#                     # style_cell = {'textAlign': 'center'},
#                     style_cell={
#                             'minWidth': 10, 'maxWidth': 95, 'width': 10,'textAlign': 'left'
#                         },
#                     style_as_list_view=True,
#                     style_table={#'height': 530, 
#                             # 'width':800,
#                             'overflowY': 'auto',
#                             'lineHeight': '30px'},
#                     style_header={
#                                 # 'backgroundColor': 'rgb(138,36,50)',
#                                 # 'color': 'white',
#                                 'whiteSpace':'normal',
#                                 # 'fontWeight': 'bold',
#                                 # 'font_size': '16px'
#                                 'overflowY': 'auto',
#                                 'height': 'auto',
#                     },
#                     style_data={
#                             'whiteSpace': 'normal',
#                             'height': 'auto',
#                             'font_size': '12px',
#                             'line-height': 0.9
#                             # 'width': '100px',
#                             # 'maxWidth': '100px',
#                             # 'minWidth': '100px',
#                         },
#                     # style_data_conditional=[
#                     #     {'if': {'column_id': 'Лимит в SAP'},
#                     #     'width': '35px'},
#                     # ]
#                 ), width=12),
#                 dcc.Graph(
#                 id="all_x_bseg",
#                 figure=go.Figure(
#                     data=[
#                         go.Bar(x=dates1_3_bseg, y=points_3_p_bseg,  yaxis='y1',
#                             hovertemplate =
#                                 '<i><b>Доля просроченной задолжности</b></i>:  %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>',  width=500000000, name= 'Доля просроченной задолжности', xaxis='x1', opacity=0.5),

#                         go.Scatter(x=dates1_3_bseg, y=points_3_bseg, mode='lines', hovertemplate =
#                                 '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>',
#                         name= 'Динамическое сальдо долг', line=dict(color="#006B19"), line_shape='spline', yaxis='y2',xaxis='x1'),
#                         go.Scatter(x=dates1_3_bseg, y=points_3_0_bseg, mode='lines',hoverinfo='none', name= '', line_color='rgb(217,217,217)', line_width=0.5, xaxis='x2')
#                     ],
#                     layout=go.Layout(
#                         title= 'Динамика задолженности клиентов с отсрочкой платежа без потолка лимита (по данным бухгалтерского учета)',
#                         plot_bgcolor='white',
#                         paper_bgcolor='white',
#                         xaxis=dict(
#                             showticklabels=False,
#                             overlaying='x2',
#                             showdividers=False),
#                         yaxis=dict(title='Доля просроченной задолжности', side='right',
#                         tickformat= ',.0%'),
#                         yaxis2=dict(title='Долг',
#                                     overlaying='y',
#                                     side='left'),
#                         margin={'l': 30, 'b': 30, 't': 80, 'r': 0},
#                         # legend={'x': 0, 'y': 1},
#                         showlegend=True
#                     )
#                 ), style={'width': '80%'},
#                 config={'displayModeBar': False}
#             ),
#                 html.H6('Детальная информация по задолженности клиентов с отсрочкой платежа без потолка лимита (по данным бухгалтерского учета)', className='row'),
#                 dbc.Col(dash_table.DataTable(
#                     id='datatable_clients_X_bseg',
#                     columns=[{"name": col_name_rus[i][0], "id": i,
#                      "deletable": True, 'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
#                     {"name": col_name_rus[i][0], "id": i,
#                      "deletable": True, 'type': col_name_rus[i][1], 'format': dict(specifier=',.0f') if i!= 'percent' else FormatTemplate.percentage(2)}
#                      for i in    df_dog_3_1_bseg.columns],
#                     data=(df_dog_3_1_bseg).to_dict('records'),
#                     # editable=True,
#                     filter_action="native",
#                     sort_action="native",
#                     sort_mode="multi",
#                     # column_selectable="single",
#                     # row_selectable="multi",
#                     # row_deletable=True,
#                     selected_columns=[],
#                     selected_rows=[],
#                     tooltip_conditional=
#                     [
#                         {
#                             'if': {
#                                 'filter_query': "{{dog_number}} = '{}'".format(i),
#                                 'column_id': 'debitor_saldo_sum',
#                             },
#                             'backgroundColor': '#7FDBFF',
#                             'color': 'white',
#                             'type': 'markdown',
#                             'value': 'Факторинг 10,5 млрд.'
#                         }
#                         for i in factoring_dogs
#                     ],

#                     style_data_conditional=[
#                                     {
#                                         'if': {
#                                             'filter_query': "{{dog_number}} = '{}'".format(i),
#                                             'column_id': 'debitor_saldo_sum',
#                                         },
#                                         'backgroundColor': ('#0074D9' if sum_fact0 < factoring else '#97151c'),
#                                         'color': 'white',
#                                         'textDecoration': 'underline',
#                                         'textDecorationStyle': 'dotted',
#                                     }
#                                     for i in factoring_dogs
#                                 ],
#                     tooltip_delay=0,
#                     tooltip_duration=None,
#                     page_action="native",
#                     page_current= 0,
#                     page_size= 10, 
#                    # style_cell = {'textAlign': 'center'},
#                     style_cell={
#                             'minWidth': 10, 'maxWidth': 95, 'width': 10,'textAlign': 'left'
#                         },
#                     style_as_list_view=True,
#                     style_table={#'height': 530, 
#                             # 'width':800,
#                             'overflowY': 'auto',
#                             'lineHeight': '30px'},
#                     style_header={
#                                 # 'backgroundColor': 'rgb(138,36,50)',
#                                 # 'color': 'white',
#                                 'whiteSpace':'normal',
#                                 # 'fontWeight': 'bold',
#                                 # 'font_size': '16px'
#                                 'overflowY': 'auto',
#                                 'height': 'auto',
#                     },
#                     style_data={
#                             'whiteSpace': 'normal',
#                             'height': 'auto',
#                             'font_size': '12px',
#                             'line-height': 0.9
#                             # 'width': '100px',
#                             # 'maxWidth': '100px',
#                             # 'minWidth': '100px',
#                         }, 
#                     # style_data_conditional=[
#                     #     {'if': {'column_id': 'Лимит в SAP'},
#                     #     'width': '35px'},
#                     # ]
#                 ), width=12),
#                 dcc.Graph(
#                     id="all_prepaid_bseg",
#                     figure=go.Figure(
#                         data=[
#                             go.Bar(x=dates1_1_bseg, y=points_1_c_bseg,  yaxis='y1',
#                             hovertemplate =
#                                 '<i><b>Кол-во клиентов</b></i>:  %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>',  width=500000000, name= 'Кол-во клиентов', xaxis='x1', opacity=0.5),
#                             go.Scatter(x=dates1_1_bseg, y=points_1_bseg, mode='lines', name= 'Динамическое сальдо долг',
#                             hovertemplate =
#                                 '<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                 '<br><b>Дата</b>: %{x}<br><extra></extra>',
#                                    yaxis='y2', line=dict(color="#006B19"), 
#                             line_shape='spline'),
#                             # go.Scatter(x=dates1_1_bseg, y=[12000000000 for i in dates1_1_bseg],
#                             #     hoverinfo='none', mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.1, yaxis='y2', xaxis='x2'),
#                             # go.Scatter(x=dates1_1_bseg, y=[200 for i in dates1_1_bseg]
#                             # , hoverinfo='none', mode='lines', name= '', line_color='rgb(217,217,217)', line_width=0.1, yaxis='y1', xaxis='x2'),
#                             # go.Scatter(x=dates1_1, y=points_1_c, mode='bar', secondary_y=True,name= 'Кредитный лимит из SAP', line_color='rgb(207,0,15)', xaxis='x1'),
#                             go.Scatter(x=dates1_1_bseg, y=points_1_0_bseg, mode='lines',
#                                 hoverinfo='none', name= '', line_color='rgb(217,217,217)', line_width=0.5, yaxis='y1',xaxis='x2')
#                         ],
#                         layout=go.Layout(
#                             title= 'Динамика задолженности предоплатных клиентов в разрезе кол-ва клиентов и суммы задолженности в млрд руб. (по данным бухгалтерского учета)',
#                             plot_bgcolor='white',
#                             paper_bgcolor='white',
#                             xaxis=dict(
#                                 showticklabels=False,
#                                 overlaying='x2',
#                                 showdividers=False),
#                             yaxis=dict(title='Кол-во клиентов', side='right'),
#                             yaxis2=dict(title='Долг',
#                                     overlaying='y',
#                                     side='left'),
#                             margin={'l': 30, 'b': 30, 't': 40, 'r': 0},
#                             # legend={'x': 0, 'y': 1},
#                             showlegend=True
#                         )
#                     ), style={'width': '80%'},
#                     config={'displayModeBar': False}
#                 ),
#                 html.H6('Детальная информация по задолженности предоплатных клиентов (по данным бухгалтерского учета)', className='row'),
#                 dbc.Col(dash_table.DataTable(
#                     id='datatable_clients_prepaid_bseg',
#                     columns=[{"name": col_name_rus[i][0], "id": i,
#                      "deletable": True, 'type': col_name_rus[i][1]} if  col_name_rus[i][2]==0 else 
#                     {"name": col_name_rus[i][0], "id": i,
#                      "deletable": True, 'type': col_name_rus[i][1], 'format': dict(specifier=',.0f')}
#                      for i in    df_dog_1_1_bseg.columns],
#                     data=(df_dog_1_1_bseg).to_dict('records'),
#                     # editable=True,
#                     filter_action="native",
#                     sort_action="native",
#                     sort_mode="multi",
#                     # column_selectable="single",
#                     # row_selectable="multi",
#                     # row_deletable=True,
#                     selected_columns=[],
#                     selected_rows=[],
#                     tooltip_conditional=
#                     [
#                         {
#                             'if': {
#                                 'filter_query': "{{dog_number}} = '{}'".format(i),
#                                 'column_id': 'debitor_saldo_sum',
#                             },
#                             'backgroundColor': '#7FDBFF',
#                             'color': 'white',
#                             'type': 'markdown',
#                             'value': 'Факторинг 10,5 млрд.'
#                         }
#                         for i in factoring_dogs
#                     ],

#                     style_data_conditional=[
#                                     {
#                                         'if': {
#                                             'filter_query': "{{dog_number}} = '{}'".format(i),
#                                             'column_id': 'debitor_saldo_sum',
#                                         },
#                                         'backgroundColor': ('#0074D9' if sum_fact0 < factoring else '#97151c'),
#                                         'color': 'white',
#                                         'textDecoration': 'underline',
#                                         'textDecorationStyle': 'dotted',
#                                     }
#                                     for i in factoring_dogs
#                                 ],
#                     tooltip_delay=0,
#                     tooltip_duration=None,
#                     page_action="native",
#                     page_current= 0,
#                     page_size= 10, 
#                     # style_cell = {'textAlign': 'center'},
#                     style_cell={
#                             'minWidth': 10, 'maxWidth': 95, 'width': 10,'textAlign': 'left'
#                         },
#                     style_as_list_view=True,
#                     style_table={#'height': 530, 
#                             # 'width':800,
#                             'overflowY': 'auto',
#                             'lineHeight': '30px'},
#                     style_header={
#                                 # 'backgroundColor': 'rgb(138,36,50)',
#                                 # 'color': 'white',
#                                 'whiteSpace':'normal',
#                                 # 'fontWeight': 'bold',
#                                 # 'font_size': '16px'
#                                 'overflowY': 'auto',
#                                 'height': 'auto',
#                     },
#                     style_data={
#                             'whiteSpace': 'normal',
#                             'height': 'auto',
#                             'font_size': '12px',
#                             'line-height': 0.9
#                             # 'width': '100px',
#                             # 'maxWidth': '100px',
#                             # 'minWidth': '100px',
#                         },
#                     # style_data_conditional=[
#                     #     {'if': {'column_id': 'Лимит в SAP'},
#                     #     'width': '35px'},
#                     # ]
#                 ), width=12),
#                 dbc.Navbar(
#                 [
#                     dbc.Container(
#                             children=[
#                                 html.Details([
#                                     html.Summary('Тип договоров...',
#                                         style={'font-size': '1.3rem'}),
#                                     html.Br(),
#                                     dbc.Col([
#                                         dcc.Checklist(
#                                             id='checklist-DRO',
#                                             options=[
#                                             {'label': 'Доходный', 'value': 'D'},
#                                             {'label': 'Расходный', 'value': 'R'},
#                                             {'label': 'Доходнорасходный', 'value': 'O'},
#                                             ],
#                                             value=['D', 'R', 'O'],
#                                             labelStyle = {'display': 'block'}
#                                         )   
#                                     ])
#                                 ])
#                             ],
#                         style={'width': '13%', 
#                         'display': 'inline-block', #'marginBottom': 15,
#                         'margin-left': 30,
#                         'marginTop': 25,
#                         'color': 'white',
#                         'vertical-align':'top'}
#                         ),
#                     dbc.Container(
#                             children=[
#                                 html.Details([
#                                     html.Summary('Категория договоров...',
#                                         style={'font-size': '1.3rem'}
#                                     ),
#                                     html.Br(),
#                                     dbc.Col([
#                                         dcc.Checklist(
#                                             id='checklist-categ',
#                                             options=[ {'label': i, 'value': i} for i in df_dog_uniq['rcm_categ'].unique()],
#                                             value=df_dog_uniq['rcm_categ'].unique(),
#                                             # labelStyle = {'display': 'block'},
#                                             # style={'column-count': '2', 'white-space': 'pre-line'  ,  'overflow':'auto'}
#                                         )   
#                                     ])
#                                 ])
#                             ],
#                         style={'width': '15%', 
#                         'display': 'inline-block', 'marginBottom': 15,
#                          'margin-left': 10,
#                          'marginTop': 25,
#                         'color': 'white',
#                         'vertical-align':'top'}
#                         ),
#                     dbc.Col([
#                         html.H6('Детализация'),
#                         dcc.RadioItems(
#                             id='RI-OS',
#                             options=[
#                                 {'label': 'Суммарно по клиенту', 'value': 'S'},
#                                 {'label': 'Отдельные договоры', 'value': 'O'},
                                
#                             ],
#                             value='S'
#                         ),
#                         ],
#                         style={'width': '13%', 
#                             'display': 'inline-block', 'marginBottom': 15, 'margin-left': 20,'marginTop': 25,
#                             'color': 'white',
#                         'vertical-align':'top'}
#                     ),
#                     dbc.Col(
#                         [
#                         html.H6('Холдинг\компания'),
#                         dcc.RadioItems(
#                             id='RI-CH',
#                             options=[
#                                 {'label': 'Компании', 'value': 'C'},
#                                 {'label': 'Холдинги', 'value': 'H'},
#                             ],
#                             value='C'
#                         ),
#                         ],
#                         style={'width': '15%', 
#                             'display': 'inline-block', 'marginBottom': 15, 'margin-left': 10,'marginTop': 25,
#                             'color': 'white',
#                         'vertical-align':'top'}
#                     ),
#                     dcc.Dropdown(
#                         id="dashboard13-dropdown-company",
#                         options=[ {'label': i, 'value': i} for i in df_dog_uniq[ 'name1'].unique()],
#                         value='ПАО "НЛМК"',
#                         clearable=False,
#                         style={"display": "flex",
#                             "justify-content": "center",
#                             # 'width': '20%', 
#                             'display': 'inline-block', #'marginBottom': 15, 'margin-left': 10,
#                             'marginTop': 25,
#                         'vertical-align':'top',
#                         'text-align': 'left',
#                         # 'padding': '0 10px',
#                         # 'margin-bottom': '5px',
#                             },
#                         # className='three-columns'
                        
#                         ),
#                 ],dark=True, color='rgb(71, 71, 71)',
#                 style={'marginBottom': 15, 'margin-left': 15,'marginTop': 40}
#                 ),
#                 html.Button('Submit', id='submit-val_f', n_clicks=0,
#                     style={'width': '15%', 
#                     'marginBottom': 15, 'margin-left': 15,'marginTop': 40
#                      },
#                     className='Button_mine'),


#                 dcc.Graph(
#                     id="nlmk_severstal",
#                     figure=go.Figure(
#                         data=[#go.Bar(
#                             #     x=df_result_t_m[df_result_t_m['zuonr']==i].index,
#                             #     y=df_result_t_m[df_result_t_m['zuonr']==i]['dmbtr'],
#                             #     name=df_result_t_m[df_result_t_m['zuonr']==i][ 'rcm_dognum_reg'].values[0],
#                             # #     xperiod="M3",
#                             # #     xperiodalignment="middle",
#                             # #     xhoverformat="Q%q",
#                             #     customdata=df_result_t_m[df_result_t_m['zuonr']==i][['rcm_vid', 'rcm_categ', 'rcm_dognum_reg']],
#                             #     hovertemplate='<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                             #                             '<br><b>Дата</b>: %{x}'+
#                             #     '<br><b>Тип договора</b>: %{customdata[0]}'+
#                             #     '<br><b>Категория договора</b>: %{customdata[1]}'+
#                             #     '<br><b>Номер договора</b>: %{customdata[2]}'+'<br><extra></extra>'
#                             # ) for i  in df_result_t_m['zuonr'].unique()
#                             go.Bar(
#                                     x=df_result_t_m.index,
#                                     y=df_result_t_m['dmbtr'],
#                                     name='ПАО "НЛМК"',
#                                     hovertemplate='<i><b>Сальдо</b></i>: \u20bd %{y:,.0f}'+
#                                                             '<br><b>Дата</b>: %{x}'+
#                                                             '<br><extra></extra>'
#                                 ) 
#                                                     ],
#                         layout=go.Layout(
#                             title= 'Сальдо ПАО "НЛМК"',
#                             # title={
#                             #         'text': 'Сальдо по договорам ПАО "НЛМК"',
#                             #         'style':{'font-weight': 'bold'}},
#                             plot_bgcolor='white',
#                             paper_bgcolor='white',
#                             # xaxis=dict(
#                             #     showticklabels=False,
#                             #     overlaying='x2',
#                             #     showdividers=False),
#                             # yaxis=dict(title='Кол-во клиентов', side='right'),
#                             # yaxis2=dict(title='Долг',
#                             #         overlaying='y',
#                             #         side='left'),
#                             margin={'l': 30, 'b': 30, 't': 40, 'r': 0},
#                             # legend={
#                             #     'itemwidth':'10'
#                             #     # 'x': 0, 'y': 1
#                             #     },
#                             barmode='relative',
#                             showlegend=True
#                         )
#                     ), style={'width': '100%'},
#                     config={'displayModeBar': False}
#                 ),



                

#  ], className='eleven columns', style={'marginBottom': 15, 'margin-left': 30,'marginTop': 25,
#                         }),
        
        
       
#         ], 
#         className='twelve columns', 
#         style={'fontSize': 12})
#     return layout


"""Выгрузка данных и вспомогательные функции"""
import os
import pandas as pd
from pandas.io import sql
# import front_ex.config as config
from sqlalchemy import create_engine
import datetime as dt

# Подневная загрузка 
def dag_load_daily():
    sql = '''
        select 
            date, 
            dag_id, 
            owners,
            state,
            sum(duration_mins) as duration_mins, 
            sum(duration_mins)/60 as duration_hours
            from (
                select 
                    --start_date::date as date,
                    start_date as date,
                    dr.dag_id, 
                    extract(days from end_date - start_date)*60*24  
                        + extract(hours from end_date - start_date)*60 
                        + extract(minutes from end_date - start_date) as duration_mins, 
                    state, 
                    run_type, 
                    owners
                    from airflow.dag_run dr
                        left join airflow.dag d on dr.dag_id = d.dag_id 
                        where start_date is not null and end_date is not null 
                            --and start_date::date = '2023-10-01'
            ) t group by date, dag_id, owners, state 
                order by date
    '''
    con=create_engine(os.environ['POSTGRE_URL_DASH_LOG'], max_identifier_length=128, encoding='utf-8')
    df = pd.read_sql(sql, con)
    return df
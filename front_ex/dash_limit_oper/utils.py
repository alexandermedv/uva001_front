import os
import pyhdb
import datetime as dt
from datetime import datetime
import numpy as np 
import pandas as pd
from sqlalchemy import create_engine

from ..utils import get_sap_s4_con_str

def get_connection_sap():
    connection_hana = pyhdb.connect(get_sap_s4_con_str)
    return connection_hana

def get_connection_postgre_string():
    """Строка подключения к postgre тест"""
    return os.environ['POSTGRE_URL_DASH']

def get_limit1():
        sql = "select * from analytics.limit1"
        con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')
        data = pd.read_sql(sql, con=con)
        return data

def get_limit():
        sql = """select * 
            from sap_s4.limit a
            left join sap_s4.kna1 b
            on a.lim_partner = b.kunnr
            """
        con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')
        data = pd.read_sql(sql, con=con)
        return data

def get_limit_oper_data(debug=False):
        """Получение первичных данных"""
        sql = "select * from sap_s4.limit_oper"
        con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')
        data = pd.read_sql(sql, con=con)
        if debug: print(data.head(3))
        return data   

def get_limit_oper_client_data():
        """Выгрузка данных по клиенту"""
        sql = "SELECT distinct(kunnr) as kunnr, name1 from sap_s4.limit_oper_kna"
        data = pd.read_sql(sql, con=create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8'))
        # print(data.head(3))
        return data
           
def get_limit_oper_zuonr_data(client):
        """Выгрузка данных по контрактам"""
        sql = "SELECT kunnr, zuonr from sap_s4.limit_oper_kna where kunnr = '%s'" % client
        data = pd.read_sql(sql, con=create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8'))
        # print(data.head(3))
        return data
def get_limit_oper_ttl_data(debug=False):
        """Выгрузка агрегированных данных"""

        # sql = """
        #         select ZUONR,
        #                         KUNNR,
        #                         BUDAT,
        #                         max(total) as max_dz,
        #                         min(total) as min_dz,
        #                         avg(total) as avg_dz
        #                                 FROM (SELECT *,
        #                                         (SELECT SUM(DMBTR_sign) 
        #                                         FROM sap_s4.limit_oper
        #                                         WHERE BUDAT <= a.BUDAT
        #                                         AND ZUONR = a.ZUONR) as total
        #                                 FROM sap_s4.limit_oper a
        #                                 ORDER BY BUDAT 
        #                                 ) b
        #                                 GROUP BY BUDAT,
        #                                         KUNNR, ZUONR
        #                                         ORDER BY BUDAT
        #         """
        sql = """
                select ZUONR, KUNNR, BUDAT,
                max(total) as max_dz,
                min(total) as min_dz,
                avg(total) as avg_dz
	from (
		select BUDAT, KUNNR, ZUONR, sum(a.dmbtr_sign) 
                        over (partition by zuonr order by a.budat rows between unbounded preceding and current row) as total
			        from (select BUDAT, KUNNR, ZUONR, sum(a.dmbtr_sign) as dmbtr_sign 
                                        from sap_s4.limit_oper a group by BUDAT, KUNNR, ZUONR) a
	) a  GROUP BY BUDAT, KUNNR, ZUONR ORDER BY BUDAT 
        """
        data = pd.read_sql(sql, con=create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8'))
        if debug: print(data.head(3))
        return data      

def get_limit_oper_client_zuonr_data(client, zuonr, debug=False):
        """Выгрузка проводок по клиентам и контрактам"""
        sql = """
                SELECT kunnr, zuonr, ind, shkzg, hkont, h_blart, dmbtr, cpudt, cputm, budat, belnr, bldat, dmbtr_sign, timestamp, stblg 
                        from sap_s4.limit_oper where kunnr = '%s' and zuonr = '%s'
        """ % (client, zuonr)
        data = pd.read_sql(sql, con=create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8'))
        if debug: print(data.head(3))
        return data 

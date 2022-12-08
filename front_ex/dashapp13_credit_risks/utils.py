"""Выгрузка данных и вспомогательные функции"""
import os
import datetime as dt
import pandas as pd
from sqlalchemy import create_engine
#from app import engine_analysis, engine_cons

# from . import engine_cons

# engine_cons = create_engine("""postgresql://locadm:Temp001@msc199-
# sdb04.domain.local:8031/uva_cons""", max_identifier_length=128, encoding='utf-8')
def make_str_from_list(col0, s=''):
    return (s+', '+s).join(str(x) for x in col0)
def makestr_if_exist(col0, s1, s2,s=''):
	return s1+make_str_from_list(col0,s=s)+s2 if col0 is not None else ''

# Выгрузка таблицы по рискам
def get_credit_data():
	schema='analysis'
	Name_table='debitor_saldo_anlis_contracts'
	chunksize=100000
	sql = '''
		SELECT *
		FROM '''+schema+'''.'''+Name_table +''' where
	date>='2020-11-01'
	--and  date='2021-08-31' 
	'''
	con=create_engine(os.environ['POSTGRE_URL_DASH'] , max_identifier_length=128, encoding='utf-8') 
	df2=con.execute(sql).fetchall()
	df2=pd.DataFrame()
	for chunk in pd.read_sql_query(sql , con, chunksize=chunksize):
		df2=df2.append(chunk)
	return df2
def get_credit_data_bseg():
	schema='analysis'
	Name_table='saldo_bseg_contracts'
	chunksize=100000
	sql = '''
		SELECT *
		FROM '''+schema+'''.'''+Name_table +''' where
	date>='2020-08-01' and date<'2022-10-01' 
	--and date='2021-08-31' 
	'''
	con=create_engine(os.environ['POSTGRE_URL_DASH'] , max_identifier_length=128, encoding='utf-8') 
	df2=con.execute(sql).fetchall()
	df2=pd.DataFrame()
	for chunk in pd.read_sql_query(sql , con, chunksize=chunksize):
		df2=df2.append(chunk)
	return df2
def get_credit_data_clients():
	schema='analysis'
	Name_table='debitor_saldo_anlis_clients'
	chunksize=100000
	sql = '''
		SELECT *
		FROM '''+schema+'''.'''+Name_table+''' where
	date>='2020-11-01' '''
	con=create_engine(os.environ['POSTGRE_URL_DASH'] , max_identifier_length=128, encoding='utf-8') 	
	df2=con.execute(sql).fetchall()
	df2=pd.DataFrame()
	for chunk in pd.read_sql_query(sql , con, chunksize=chunksize):
		df2=df2.append(chunk)
	return df2

def get_credit_data_all():
	schema='analysis'
	Name_table='debitor_saldo_anlis_all'
	chunksize=100000
	sql = '''
		SELECT *
		FROM '''+schema+'''.'''+Name_table +''' where
	date>='2020-11-01'  '''
	con=create_engine(os.environ['POSTGRE_URL_DASH'] , max_identifier_length=128, encoding='utf-8') 
	df2=con.execute(sql).fetchall()
	df2=pd.DataFrame()
	for chunk in pd.read_sql_query(sql , con, chunksize=chunksize):
		df2=df2.append(chunk)
	return df2

def get_credit_data_all_bseg():
	schema='analysis'
	Name_table='saldo_bseg_all'
	chunksize=100000
	sql = '''
		SELECT *
		FROM '''+schema+'''.'''+Name_table +''' where
	date>='2020-11-01'  --and date<'2022-10-01' '''
	con=create_engine(os.environ['POSTGRE_URL_DASH'] , max_identifier_length=128, encoding='utf-8') 
	df2=con.execute(sql).fetchall()
	df2=pd.DataFrame()
	for chunk in pd.read_sql_query(sql , con, chunksize=chunksize):
		df2=df2.append(chunk)
	return df2

def get_saldo_bseg(rcm_vid=None, rcm_categ=None, name1=None, yur_hold=None):
	
	schema='analysis'
	Name_table='saldo_bsegall_all_h_bldatmonth'
	chunksize=100000
	sql = '''
		SELECT date, zuonr, kunnr, rcm_vid, rcm_categ, name1, yur_hold, rcm_dognum_reg, dmbtr
	FROM  '''+schema+'''.'''+Name_table +''' where
	''' +makestr_if_exist(rcm_vid, " rcm_vid in ( '", "') and",s="'")+	makestr_if_exist(rcm_categ, " rcm_categ in ( '", "') and",s="'")+ ((""" name1='"""+name1 +"""' and""") if name1 is not None else '' )+	((""" yur_hold='"""+yur_hold +"""' and""") if yur_hold is not None else '') +'''
	date>='2020-08-01'  and date<'2022-11-01' '''
	con=create_engine(os.environ['POSTGRE_URL_DASH'] , max_identifier_length=128, encoding='utf-8') 
	df2=con.execute(sql).fetchall()
	df2=pd.DataFrame()
	for chunk in pd.read_sql_query(sql , con, chunksize=chunksize):
		df2=df2.append(chunk)
	return df2
def get_saldo_bseg_uniq():
	
	schema='analysis'
	Name_table='saldo_bsegall_all_h_bldatmonth'
	chunksize=100000
	sql = '''
		SELECT  distinct  rcm_vid, rcm_categ, name1, yur_hold
	FROM  '''+schema+'''.'''+Name_table +''' where
	date>='2020-08-01'  and date<'2022-11-01' '''
	con=create_engine(os.environ['POSTGRE_URL_DASH'] , max_identifier_length=128, encoding='utf-8') 
	df2=con.execute(sql).fetchall()
	df2=pd.DataFrame()
	for chunk in pd.read_sql_query(sql , con, chunksize=chunksize):
		df2=df2.append(chunk)
	return df2
def get_saldo_bseg_group(rcm_vid=None, rcm_categ=None, name1=None, yur_hold=None):
	
	schema='analysis'
	Name_table='saldo_bsegall_all_h_bldatmonth'
	chunksize=100000
	sql = '''
		SELECT date '''+((', name1') if name1 is not None else '')+''', yur_hold, sum(dmbtr) as dmbtr
	FROM  '''+schema+'''.'''+Name_table +''' where
	''' +makestr_if_exist(rcm_vid, " rcm_vid in ( '", "') and",s="'")+	makestr_if_exist(rcm_categ, " rcm_categ in ( '", "') and",s="'")+ ((""" name1='"""+name1 +"""' and""") if name1 is not None else '' )+	((""" yur_hold='"""+yur_hold +"""' and""") if yur_hold is not None else '') +'''
	date>='2020-08-01'  and date<'2022-11-01' 
	group by date,yur_hold'''+((', name1') if name1 is not None else '')
	con=create_engine(os.environ['POSTGRE_URL_DASH'] , max_identifier_length=128, encoding='utf-8') 
	df2=con.execute(sql).fetchall()
	df2=pd.DataFrame()
	for chunk in pd.read_sql_query(sql , con, chunksize=chunksize):
		df2=df2.append(chunk)
	return df2

# def get_distinct_comp_bseg():
# 	schema='analysis'
# 	Name_table='saldo_bsegall_all_h_budat'
# 	chunksize=100000
# 	sql = '''
# 		SELECT distinct rcm_vid, rcm_categ, name1, yur_hold
# 	FROM  '''+schema+'''.'''+Name_table 
# 	con=create_engine(os.environ['POSTGRE_URL_DASH'] , max_identifier_length=128, encoding='utf-8') 
# 	df2=con.execute(sql).fetchall()
# 	df2=pd.DataFrame()
# 	for chunk in pd.read_sql_query(sql , con, chunksize=chunksize):
# 		df2=df2.append(chunk)
# 	return df2







# def get_credit_data():
# 	schema='analysis'
# 	Name_table='debitor_saldo_anlis_for_dash'
# 	login='svc_fs_uva'
# 	passwors='Temp001'
# 	ip_server='172.17.0.136:5432'
# 	chunksize=100000
# 	sql = '''
# 		SELECT *
# 		FROM '''+schema+'''.'''+Name_table +''' where
# 	date='2022-08-31' limit 100'''
# 	con = create_engine('postgresql://'+login+':'+passwors+'@'+ip_server+'/uva_cons' , max_identifier_length=128, encoding='utf-8')
# 	df2=con.execute(sql).fetchall()
# 	df2=pd.DataFrame()
# 	for chunk in pd.read_sql_query(sql , con, chunksize=chunksize):
# 		df2=df2.append(chunk)
# 	return df2
# def get_credit_data_clients():
# 	schema='analysis'
# 	Name_table='debitor_saldo_anlis_clients'
# 	login='svc_fs_uva'
# 	passwors='Temp001'
# 	ip_server='172.17.0.136:5432'
# 	chunksize=100000
# 	sql = '''
# 		SELECT *
# 		FROM '''+schema+'''.'''+Name_table+''' where
# 	date='2022-08-31' limit 100'''
# 	con = create_engine('postgresql://'+login+':'+passwors+'@'+ip_server+'/uva_cons' , max_identifier_length=128, encoding='utf-8')
# 	df2=con.execute(sql).fetchall()
# 	df2=pd.DataFrame()
# 	for chunk in pd.read_sql_query(sql , con, chunksize=chunksize):
# 		df2=df2.append(chunk)
# 	return df2
# def get_credit_data_filials():
# 	schema='analysis'
# 	Name_table='debitor_saldo_anlis_filials'
# 	login='svc_fs_uva'
# 	passwors='Temp001'
# 	ip_server='172.17.0.136:5432'
# 	chunksize=100000
# 	sql = '''
# 		SELECT *
# 		FROM '''+schema+'''.'''+Name_table
# 	con = create_engine('postgresql://'+login+':'+passwors+'@'+ip_server+'/uva_cons' , max_identifier_length=128, encoding='utf-8')
# 	df2=con.execute(sql).fetchall()
# 	df2=pd.DataFrame()
# 	for chunk in pd.read_sql_query(sql , con, chunksize=chunksize):
# 		df2=df2.append(chunk)
# 	return df2
# def get_credit_data_all():
# 	schema='analysis'
# 	Name_table='debitor_saldo_anlis_all'
# 	login='svc_fs_uva'
# 	passwors='Temp001'
# 	ip_server='172.17.0.136:5432'
# 	chunksize=100000
# 	sql = '''
# 		SELECT *
# 		FROM '''+schema+'''.'''+Name_table
# 	con = create_engine('postgresql://'+login+':'+passwors+'@'+ip_server+'/uva_cons' , max_identifier_length=128, encoding='utf-8')
# 	df2=con.execute(sql).fetchall()
# 	df2=pd.DataFrame()
# 	for chunk in pd.read_sql_query(sql , con, chunksize=chunksize):
# 		df2=df2.append(chunk)
# 	return df2




# import os
# import pyhdb
# import datetime as dt
# from datetime import datetime
# import numpy as np 
# import pandas as pd
# from sqlalchemy import create_engine

# from ..utils import get_sap_s4_con_str

# def get_connection_sap():
#     connection_hana = pyhdb.connect(get_sap_s4_con_str)
#     return connection_hana

# def get_connection_postgre_string():
#     """Строка подключения к postgre тест"""
#     return os.environ['POSTGRE_URL_DASH']

# def get_limit1():
#         sql = "select * from analytics.limit1"
#         con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')
#         data = pd.read_sql(sql, con=con)
#         return data

# def get_limit():
#         sql = """select * 
#             from sap_s4.limit a
#             left join sap_s4.kna1 b
#             on a.lim_partner = b.kunnr
#             """
#         con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')
#         data = pd.read_sql(sql, con=con)
#         return data

# def get_limit_oper_data(debug=False):
#         """Получение первичных данных"""
#         sql = "select * from sap_s4.limit_oper"
#         con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')
#         data = pd.read_sql(sql, con=con)
#         if debug: print(data.head(3))
#         return data   

# def get_limit_oper_client_data():
#         """Выгрузка данных по клиенту"""
#         sql = "SELECT distinct(kunnr) as kunnr, name1 from sap_s4.limit_oper_kna"
#         data = pd.read_sql(sql, con=create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8'))
#         # print(data.head(3))
#         return data
           
# def get_limit_oper_zuonr_data(client):
#         """Выгрузка данных по контрактам"""
#         sql = "SELECT kunnr, zuonr from sap_s4.limit_oper_kna where kunnr = '%s'" % client
#         data = pd.read_sql(sql, con=create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8'))
#         # print(data.head(3))
#         return data
# def get_limit_oper_ttl_data(debug=False):
#         """Выгрузка агрегированных данных"""

#         # sql = """
#         #         select ZUONR,
#         #                         KUNNR,
#         #                         BUDAT,
#         #                         max(total) as max_dz,
#         #                         min(total) as min_dz,
#         #                         avg(total) as avg_dz
#         #                                 FROM (SELECT *,
#         #                                         (SELECT SUM(DMBTR_sign) 
#         #                                         FROM sap_s4.limit_oper
#         #                                         WHERE BUDAT <= a.BUDAT
#         #                                         AND ZUONR = a.ZUONR) as total
#         #                                 FROM sap_s4.limit_oper a
#         #                                 ORDER BY BUDAT 
#         #                                 ) b
#         #                                 GROUP BY BUDAT,
#         #                                         KUNNR, ZUONR
#         #                                         ORDER BY BUDAT
#         #         """
#         sql = """
#                 select ZUONR, KUNNR, BUDAT,
#                 max(total) as max_dz,
#                 min(total) as min_dz,
#                 avg(total) as avg_dz
# 	from (
# 		select BUDAT, KUNNR, ZUONR, sum(a.dmbtr_sign) 
#                         over (partition by zuonr order by a.budat rows between unbounded preceding and current row) as total
# 			        from (select BUDAT, KUNNR, ZUONR, sum(a.dmbtr_sign) as dmbtr_sign 
#                                         from sap_s4.limit_oper a group by BUDAT, KUNNR, ZUONR) a
# 	) a  GROUP BY BUDAT, KUNNR, ZUONR ORDER BY BUDAT 
#         """
#         data = pd.read_sql(sql, con=create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8'))
#         if debug: print(data.head(3))
#         return data      

# def get_limit_oper_client_zuonr_data(client, zuonr, debug=False):
#         """Выгрузка проводок по клиентам и контрактам"""
#         sql = """
#                 SELECT kunnr, zuonr, ind, shkzg, hkont, h_blart, dmbtr, cpudt, cputm, budat, belnr, bldat, dmbtr_sign, timestamp, stblg 
#                         from sap_s4.limit_oper where kunnr = '%s' and zuonr = '%s'
#         """ % (client, zuonr)
#         data = pd.read_sql(sql, con=create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8'))
#         if debug: print(data.head(3))
#         return data 

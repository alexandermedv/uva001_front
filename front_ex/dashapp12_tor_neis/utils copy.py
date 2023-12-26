"""Выгрузка данных и вспомогательные функции"""
import os
import pandas as pd
# import front_ex.config as config
from sqlalchemy import create_engine

#Выгрузка полного списка ремонтов
def get_tors(start_date, end_date):
    """ Выгрузка списка ремонтов"""
    sql = '''
        SELECT
        a.yeardata "Год"
        ,count(a.zakaz) "Общее количество"
        ,c.nekach "Некачественные"
        ,case when c.nekach <> '0' then (count(a.zakaz)-c.nekach) else count(a.zakaz) end  "Качественные"
        FROM sap_s4.tor_all_ik a
        left join 
        (select
            a.yeardatadk
            ,count(a.zakazdk) as nekach
            from sap_s4.tor_neis_ik a group by a.yeardatadk) c on c.yeardatadk = a.yeardata
            WHERE a.data1353 between '%s' AND '%s'
            group by a.yeardata, c.nekach
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

#Выгрузка ремонтов по Контрагентам
def get_tors_by_contr(start_date, end_date):
    """ Выгрузка списка ремонтов по контрагентам"""
    sql = '''
        SELECT
        k.yeardata "Год"
        ,k.lifnr_gr "Контрагент"
        ,k.total "Общее количество"
        ,k.nekach "Некачественный"
        ,k.kach "Качественные"
        ,round(k.nekach*100/k.total, 2) "Процент"
        from
        (
        select
		a.yeardata
		--,a.lifnr
		--,a.name1
		,m.lifnr_gr
		,count(a.zakaz) as total
		,c.nekach
		,count(a.zakaz)-c.nekach as kach
		from sap_s4.tor_all_ik a 
		left join sap_s4.mapping m on m.lifnr = a.lifnr 
		left join (select
                a.yeardatadk
                ,m.lifnr_gr
                ,count(a.zakazdk) as nekach
                from sap_s4.tor_neis_ik a 
				left join sap_s4.mapping m on m.lifnr = a.lifnrdk 
				group by a.yeardatadk,m.lifnr_gr) c on c.yeardatadk = a.yeardata and c.lifnr_gr = m.lifnr_gr
        where a.data1353 between '%s' AND '%s'
        group by a.yeardata,m.lifnr_gr, c.nekach) k
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

#Выгрузка ремонтов по Клиентам
def get_tors_by_client(start_date, end_date):
    """ Выгрузка списка ремонтов по клиентам"""
    sql = '''
        SELECT
        k.yeardata "Год"
        ,k.naim_depo "Наименование Депо"
        ,k.total "Общее количество"
        ,k.nekach "Некачественный"
        ,k.kach "Качественные"
        ,round(k.nekach*100/k.total, 2) "Процент"
        from
        (
            select
            a.yeardata
            ,a.naim_depo
            ,count(a.zakaz) as total
            ,c.nekach
            ,count(a.zakaz)-c.nekach as kach
            from sap_s4.tor_all_ik a
            left join 
                (select
                a.yeardatadk
                ,a.naim_depo
                ,count(a.zakazdk) as nekach
                from sap_s4.tor_neis_ik a group by a.yeardatadk,a.naim_depo) c on c.yeardatadk = a.yeardata and c.naim_depo = a.naim_depo
        where a.data1353 between '%s' AND '%s'
        group by a.yeardata, c.nekach, a.naim_depo) k
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

#Выгрузка количество ремонтов
def get_tors_count(start_date, end_date):
     """Выгрузка количества"""
     sql = '''
         SELECT 
         count(a.ZAKAZ) AS "Количество ремонтов"
         FROM sap_s4.tor_all_ik a
         WHERE a.data1353 BETWEEN '%s' AND '%s'
     ''' % (start_date, end_date)

     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


#Выгрузка количество ремонтов для спидометра
def get_tors_count_speed(start_date, end_date):
     """Выгрузка количества для спидометра"""
     sql = '''
         SELECT
		 count(a.ZAKAZ) "Общее количество"
		,count(c.ZAKAZDK) "Некачественные"
		,count(a.ZAKAZ) - count(c.ZAKAZDK) "Качественные"
		FROM sap_s4.tor_all_ik a
		left join sap_s4.tor_neis_ik c on c.zakazdk = a.zakaz and c.data1353dk = a.data1353
		WHERE a.data1353 BETWEEN '%s' AND '%s'
     ''' % (start_date, end_date)

     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


#Выгрузка количество некачественных ремонтов
def get_tors_count_nk(start_date, end_date):
     """Выгрузка количества некачественных"""
     sql = '''
         SELECT 
         count(a.zakazdk) AS "Количество некач ремонтов"
         FROM sap_s4.tor_neis_ik a
         WHERE a.data1353dk BETWEEN '%s' AND '%s'
     ''' % (start_date, end_date)

     return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

#Выгрузка TOP-10 ремонтов по Контрагентам
def get_top_tors_by_contr(start_date, end_date):
    """ Выгрузка ТОП-10 ремонтов по контрагентам"""
    sql = '''
select m.                                                                                                                                                                                                                               * from (        		
select
k.lifnr_gr "Контрагент"
,k.total "Общее количество"
,k.nekach "Некачественный"
,k.kach "Качественные"
,k.perc "Процент"
from (
select
d.lifnr_gr
,sum(d.total) as total
,sum(d.nekach) as nekach
,sum(d.kach) as kach
,case when sum(d.nekach) > '0' then round(sum(d.nekach)*100/sum(d.total), 2) else '0' end perc
from (
select
c.lifnr_gr
,c.data1353
,c.total
,c.nekach
,c.total - c.nekach as kach
from (
select
		m.lifnr_gr
		,a.data1353
		,count(a.zakaz) as total
		,case when b.nekach is null then '0' else b.nekach end nekach
		from sap_s4.tor_all_ik a 
		left join sap_s4.mapping m on m.lifnr = a.lifnr 
		left join (
				select
				m.lifnr_gr
				,a.data1353dk
				,count(zakazdk) as nekach
				from sap_s4.tor_neis_ik a 
				left join sap_s4.mapping m on m.lifnr = a.lifnrdk
				--where m.lifnr_gr = 'ВРК-1'
				group by m.lifnr_gr, a.data1353dk) b on b.lifnr_gr = m.lifnr_gr and b.data1353dk = a.data1353
		
		where a.data1353 between '%s' AND '%s'
		--and m.lifnr_gr = 'ВРК-1'
		group by m.lifnr_gr, a.data1353, b.nekach) c) d group by d.lifnr_gr) k order by k.perc desc limit 10) m
        order by "Общее количество" desc
				
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


#Выгрузка TOP-10 ремонтов по Клиентам
def get_tors_by_contr_bubl(start_date, end_date):
    """ Выгрузка ТОП-10 ремонтов по клиентам"""
    sql = '''
        select sum(nekach) "Некачественные"
,sum(kach) "Качественные" from (
select
case when s.qtynk = '1' then count(qtynk) else 0 end nekach
,case when s.qtynk = '0' then count(qtynk) else 0 end kach
from (
select
k.lifnr_gr 
,k.total 
,k.nekach 
,k.kach 
,k.perc f
,case when k.perc >= '10' then 1 else 0 end qtynk
from (
select
d.lifnr_gr
,sum(d.total) as total
,sum(d.nekach) as nekach
,sum(d.kach) as kach
,case when sum(d.nekach) > '0' then round(sum(d.nekach)*100/sum(d.total), 2) else '0' end perc
from (
select
c.lifnr_gr
,c.data1353
,c.total
,c.nekach
,c.total - c.nekach as kach
from (
select
		m.lifnr_gr
		,a.data1353
		,count(a.zakaz) as total
		,case when b.nekach is null then '0' else b.nekach end nekach
		from sap_s4.tor_all_ik a 
		left join sap_s4.mapping m on m.lifnr = a.lifnr 
		left join (
				select
				m.lifnr_gr
				,a.data1353dk
				,count(zakazdk) as nekach
				from sap_s4.tor_neis_ik a 
				left join sap_s4.mapping m on m.lifnr = a.lifnrdk
				--where m.lifnr_gr = 'ВРК-1'
				group by m.lifnr_gr, a.data1353dk) b on b.lifnr_gr = m.lifnr_gr and b.data1353dk = a.data1353
		
		where a.data1353 between '%s' AND '%s'
		--and m.lifnr_gr = 'ВРК-1'
		group by m.lifnr_gr, a.data1353, b.nekach) c) d group by d.lifnr_gr) k order by k.perc desc --limit 10
			) s	group by s.qtynk) n
            order by sum(kach) desc
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

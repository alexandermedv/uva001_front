"""Выгрузка данных и вспомогательные функции"""
import os
import pandas as pd
# import front_ex.config as config
from sqlalchemy import create_engine


# Значения списка РПС
def get_rps(start_date, end_date):
    """Выгрузка списка РПС"""
    sql = '''
        SELECT DISTINCT rod_id_text
        FROM dashboard.tor_ik
        WHERE DATNRP BETWEEN '%s' AND '%s'
        ORDER BY rod_id_text ASC
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Значения полного списка РПС
def get_all_rps(start_date, end_date):
    """Выгрузка списка РПС"""
    sql = '''
        SELECT DISTINCT rod_id_text
        FROM dashboard.tor_ik
        WHERE DATNRP BETWEEN '%s' AND '%s'
        ORDER BY rod_id_text ASC
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


# Максимальная дата в выгрузке
def get_max_date():
    """Максимальная дата в выгрузке"""
    sql = '''
    SELECT MAX(t.DATNRP)
    FROM dashboard.tor_ik t
    '''
    # return engine_cons.execute(sql).fetchone()[0]
    con = create_engine(config.POSTGRE_DB, max_identifier_length=128, encoding='utf-8')
    return con.execute(sql).fetchone()[0]

    
def get_tors_count(start_date, end_date):
    """Выгрузка количества"""
    sql = '''
        SELECT 
        count(a.AUFNR) AS "Количество ремонтов"
        FROM dashboard.tor_ik a
        WHERE a.DATNRP BETWEEN '%s' AND '%s'
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

def get_tors_by_rps(start_date, end_date):
    """Выгрузка ремонтов в разрезе РПС"""
    sql = '''
        SELECT 
        a.ROD_ID_GROUP AS "РПС", 
        a.ILATX AS "Вид ремонта",
        count(a.AUFNR) AS "Количество ремонтов"
        FROM dashboard.tor_ik a
        WHERE a.DATNRP BETWEEN '%s' AND '%s'
        GROUP BY a.ROD_ID_GROUP, a.ILATX
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


def get_tors_by_rps_pr(start_date, end_date):
    """Выгрузка ремонтов в разрезе РПС"""
    sql = '''
        SELECT 
        a.ROD_ID_TEXT AS "РПС", 
        a.ILATX AS "Вид ремонта",
        count(a.AUFNR) AS "Количество ремонтов"
        FROM dashboard.tor_ik a
        WHERE a.ROD_ID_GROUP = 'Прочие' and a.DATNRP BETWEEN '%s' AND '%s'
        GROUP BY a.ROD_ID_TEXT, a.ILATX
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))




def get_tors_by_type(start_date, end_date):
    """Выгрузка ремонтов в разрезе видов ТОР"""
    sql = '''
        SELECT 
        a.ILATX AS "Вид ремонта",
        count(a.AUFNR) AS "Количество ремонтов"
        FROM dashboard.tor_ik a
        WHERE a.DATNRP BETWEEN '%s' AND '%s'
        GROUP BY a.ILATX
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

def get_top_tors_by_rps(start_date, end_date):
    """Выгрузка топ3 кодов неисправности в разрезе РПС"""
    sql = '''
      SELECT
      a.ROD_ID_GROUP "РПС"
      ,a.NEIS1_KOD as "Код неисправности_id"
	  ,k."Полное наименование"
      ,concat_ws(' - ',a.ROD_ID_GROUP, a.NEIS1_KOD, a.KURZTEXT1) AS "Код неисправности"
      ,concat_ws(' - ', a.NEIS1_KOD, a.KURZTEXT1) AS "Код неисправности2"
      ,concat_ws(' - ', a.ROD_ID_GROUP, a.NEIS1_KOD) AS "Код неисправности3"
      ,a.KOLVO "Количество"
      FROM (
          SELECT t.ROD_ID_GROUP, t.NEIS1_KOD, t.KURZTEXT1, count(AUFNR) as KOLVO,
          ROW_NUMBER() OVER (PARTITION BY ROD_ID_GROUP ORDER BY count(AUFNR) DESC) AS r
          FROM dashboard.tor_ik t 
          WHERE t.DATNRP BETWEEN '%s' AND '%s' GROUP BY t.ROD_ID_GROUP, t.NEIS1_KOD,t.KURZTEXT1) a
          LEFT JOIN dashboard.kn_info_ik k on k."Код неисправности"::text = a.NEIS1_KOD
          WHERE a.r <= 3
          ORDER BY a.ROD_ID_GROUP,a.KOLVO asc;
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


def get_top_tors_by_rps_pr(start_date, end_date):
    """Выгрузка топ3 кодов неисправности в разрезе РПС"""
    sql = '''
      SELECT
      a.ROD_ID_TEXT "РПС" 
      ,a.NEIS1_KOD as "Код неисправности_id"
	  ,k."Полное наименование"
      ,concat_ws(' - ', a.ROD_ID_TEXT, a.NEIS1_KOD, a.KURZTEXT1) AS "Код неисправности"
      ,concat_ws(' - ', a.NEIS1_KOD, a.KURZTEXT1) AS "Код неисправности2"
      ,concat_ws(' - ', a.ROD_ID_TEXT, a.NEIS1_KOD) AS "Код неисправности3"
      ,a.KOLVO "Количество"
      FROM (
          SELECT t.ROD_ID_TEXT,t.ROD_ID_GROUP, t.NEIS1_KOD, t.KURZTEXT1, count(AUFNR) as KOLVO,
          ROW_NUMBER() OVER (PARTITION BY ROD_ID_TEXT ORDER BY count(AUFNR) DESC) AS r
          FROM dashboard.tor_ik t 
          WHERE t.DATNRP BETWEEN '%s' AND '%s' AND t.ROD_ID_GROUP = 'Прочие' GROUP BY t.ROD_ID_TEXT,t.ROD_ID_GROUP, t.NEIS1_KOD,t.KURZTEXT1) a
          LEFT JOIN dashboard.kn_info_ik k on k."Код неисправности"::text = a.NEIS1_KOD
          WHERE a.r <= 3
          ORDER BY a.ROD_ID_TEXT,a.KOLVO desc;
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

def get_top_tors_by_type(start_date, end_date):
    """Выгрузка топ кодов неисправности в разрезе видов ТОР"""
    sql = '''
      SELECT
      a.ILATX AS "Вид ремонта"
      ,case when a.ILATX = 'ТР-1' then 1
	  when a.ILATX = 'ТР-2' then 2
	  when a.ILATX = 'ДР' then 3
	  else 4 end as "Сортировка"
      ,a.NEIS1_KOD as "Код неисправности_id"
	  ,k."Полное наименование"
	  ,concat_ws(' - ', a.ILATX, a.NEIS1_KOD, a.KURZTEXT1) AS "Код неисправности"
      ,concat_ws(' - ', a.NEIS1_KOD, a.KURZTEXT1) AS "Код неисправности2"
      ,concat_ws(' - ', a.ILATX, a.NEIS1_KOD) AS "Код неисправности3"
      ,a.KOLVO AS "Количество"
      FROM (
          SELECT t.ILATX,t.NEIS1_KOD, t.KURZTEXT1, count(AUFNR) as KOLVO,
          ROW_NUMBER() OVER (PARTITION BY ILATX ORDER BY count(AUFNR) DESC) AS r
          FROM dashboard.tor_ik t 
          WHERE t.DATNRP BETWEEN '%s' AND '%s' GROUP BY t.ILATX, t.NEIS1_KOD,t.KURZTEXT1) a
          LEFT JOIN dashboard.kn_info_ik k on k."Код неисправности"::text = a.NEIS1_KOD
          WHERE a.r <= 3 
          ORDER BY "Сортировка",a.KOLVO asc;
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


def get_avg_tors(start_date, end_date):
    """Выгрузка средняя длительность ремонтов"""
    sql = '''
      SELECT
      a.ILATX "Вид ремонта"
      ,ROUND(a.DIFF) "Средняя длительность"
      ,t.AVGTIME "Плановая длительность"
      ,case when a.ILATX = 'ТР-1' then 1
	  when a.ILATX = 'ТР-2' then 2
	  when a.ILATX = 'ДР' then 3
	  else 4 end as "Сортировка"
      from (			   
          select
          a.ILATX
          ,avg(a.DIFF) as DIFF
          from (
              select
              t.ILATX
              ,t.AUFNR
              ,t.DATNRP
              ,t.DATRP
              ,t.DATRP-t.DATNRP as DIFF
              from dashboard.tor_ik t
              where t.TSTAT is null and t.DATNRP BETWEEN '%s' AND '%s') a
              GROUP BY a.ILATX) a left join dashboard.avgttor t on t.ILATX = a.ILATX order by "Сортировка" desc
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))



def get_bad_tors_912(start_date, end_date):
    """Выгрузка некачественных 912 ремонтов"""
    sql = '''
      select
        q.KOD_NEIS AS "Код неисправности"
        ,q.ROD_ID_TEXT AS "РПС"
        ,sum(q.COUNTAUFNR) AS "Количество"
        from (
            select
            a.eqktx
            ,a.rod_id_text
            ,a.kod_neis
            ,count(aufnr) as countaufnr
            from (
                select
                a.aufnr
                ,a.ilatx
                ,a.rod_id_text
                ,a.eqktx
                ,a.onrp
                ,a.pnrp
                ,a.kod_neis
                ,b.aufnr as baufnr
                ,b.ilatx as bilatx
                ,b.datnrp as datnrp
                from (
                    select
                     t.aufnr
                     ,t.ilatx
                     ,t.rod_id_text
                     ,t.eqktx
                     ,t.datnrp as onrp
                     ,k.datnrp as pnrp
                     ,case when (t.neis1_kod = '912' or t.neis2_kod = '912' or t.neis3_kod = '912') then 912
                     when (t.neis1_kod = '913' or t.neis2_kod = '913' or t.neis3_kod = '913') then 913 end as kod_neis
                    from dashboard.tor_ik t
                    left join (select
                                f.aufnr,f.rod_id_text, max(f.ddatnrp) as datnrp from (
                                select
                                t.aufnr, t.ilatx, t.rod_id_text, t.eqktx, t.datnrp, d.aufnr as daufnr, d.ilatx, d.datnrp as ddatnrp
                                from dashboard.tor_ik t 
                                left join dashboard.tor_ik d on d.eqktx = t.eqktx and d.ilatx in ('КР','ДР') and d.datnrp < t.datnrp
                                where t.ilatx in ('ТР-1','ТР-2') and (t.neis1_kod in ('912','913') or t.neis2_kod in ('912','913') or t.neis3_kod in ('912','913'))) f group by f.aufnr, f.rod_id_text
                                ) k on k.aufnr = t.aufnr
                    where t.datnrp between '%s' AND '%s' and t.ilatx in ('ТР-1','ТР-2') and (t.neis1_kod in ('912','913') or t.neis2_kod in ('912','913') or t.neis3_kod in ('912','913'))
                    ) a 
                    left join dashboard.tor_ik b on b.eqktx = a.eqktx and b.ilatx in ('ТР-1','ТР-2') and (a.pnrp < b.datnrp and  b.datnrp < a.onrp)
                    ) a where a.bilatx is null group by a.eqktx, a.rod_id_text,a.kod_neis) q where q.kod_neis = '912' group by q.kod_neis, q.rod_id_text order by q.kod_neis desc

    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

def get_bad_tors_913(start_date, end_date):
    """Выгрузка некачественных 913 ремонтов"""
    sql = '''
      select
        q.KOD_NEIS AS "Код неисправности"
        ,q.ROD_ID_TEXT AS "РПС"
        ,sum(q.COUNTAUFNR) AS "Количество"
        from (
            select
            a.eqktx
            ,a.rod_id_text
            ,a.kod_neis
            ,count(aufnr) as countaufnr
            from (
                select
                a.aufnr
                ,a.ilatx
                ,a.rod_id_text
                ,a.eqktx
                ,a.onrp
                ,a.pnrp
                ,a.kod_neis
                ,b.aufnr as baufnr
                ,b.ilatx as bilatx
                ,b.datnrp as datnrp
                from (
                    select
                     t.aufnr
                     ,t.ilatx
                     ,t.rod_id_text
                     ,t.eqktx
                     ,t.datnrp as onrp
                     ,k.datnrp as pnrp
                     ,case when (t.neis1_kod = '912' or t.neis2_kod = '912' or t.neis3_kod = '912') then 912
                     when (t.neis1_kod = '913' or t.neis2_kod = '913' or t.neis3_kod = '913') then 913 end as kod_neis
                    from dashboard.tor_ik t
                    left join (select
                                f.aufnr,f.rod_id_text, max(f.ddatnrp) as datnrp from (
                                select
                                t.aufnr, t.ilatx, t.rod_id_text, t.eqktx, t.datnrp, d.aufnr as daufnr, d.ilatx, d.datnrp as ddatnrp
                                from dashboard.tor_ik t 
                                left join dashboard.tor_ik d on d.eqktx = t.eqktx and d.ilatx in ('КР','ДР') and d.datnrp < t.datnrp
                                where t.ilatx in ('ТР-1','ТР-2') and (t.neis1_kod in ('912','913') or t.neis2_kod in ('912','913') or t.neis3_kod in ('912','913'))) f group by f.aufnr, f.rod_id_text
                                ) k on k.aufnr = t.aufnr
                    where t.datnrp between '%s' AND '%s' and t.ilatx in ('ТР-1','ТР-2') and (t.neis1_kod in ('912','913') or t.neis2_kod in ('912','913') or t.neis3_kod in ('912','913'))
                    ) a 
                    left join dashboard.tor_ik b on b.eqktx = a.eqktx and b.ilatx in ('ТР-1','ТР-2') and (a.pnrp < b.datnrp and  b.datnrp < a.onrp)
                    ) a where a.bilatx is null group by a.eqktx, a.rod_id_text,a.kod_neis) q where q.kod_neis = '913' group by q.kod_neis, q.rod_id_text order by q.kod_neis desc

    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


def get_kodneis_info():
    """Выгрузка ремонтов в разрезе РПС"""
    sql = '''
			  select
			  a."Код неисправности", a."Полное наименование", a."Наименование", a."Код причины", a."Расшифровка причины"
			  from dashboard.kn_info_ik a
    ''' 

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))

"""Выгрузка данных и вспомогательные функции"""
import os
import pandas as pd
import front_ex.config as config
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
    SELECT MAX(DATNRP)
    FROM dashboard.tor_ik
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
        a.ROD_ID_TEXT AS "РПС", 
        a.ILATX AS "Вид ремонта",
        count(a.AUFNR) AS "Количество ремонтов"
        FROM dashboard.tor_ik a
        WHERE a."DATNRP" BETWEEN '%s' AND '%s'
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
      a.ROD_ID_TEXT, a.NEIS1_KOD, a.KURZTEXT1, a.KOLVO
      FROM (
          SELECT t.ROD_ID_TEXT,t.NEIS1_KOD, t.KURZTEXT1, count(AUFNR) as KOLVO,
          ROW_NUMBER() OVER (PARTITION BY ROD_ID_TEXT ORDER BY count(AUFNR) DESC) AS r
          FROM dashboard.tor_ik t 
          WHERE t."DATNRP" BETWEEN '%s' AND '%s' GROUP BY t.ROD_ID_TEXT, t.NEIS1_KOD,t.KURZTEXT1) a
          WHERE a.r <= 3;
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))




def get_top_tors_by_type(start_date, end_date):
    """Выгрузка топ кодов неисправности в разрезе видов ТОР"""
    sql = '''
      SELECT
      a.ILATX, a.NEIS1_KOD, a.KURZTEXT1, a.KOLVO
      FROM (
          SELECT t.ILATX,t.NEIS1_KOD, t.KURZTEXT1, count(AUFNR) as KOLVO,
          ROW_NUMBER() OVER (PARTITION BY ILATX ORDER BY count(AUFNR) DESC) AS r
          FROM dashboard.tor_ik t 
          WHERE t."DATNRP" BETWEEN '%s' AND '%s' GROUP BY t.ILATX, t.NEIS1_KOD,t.KURZTEXT1) a
          WHERE a.r <= 3;
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


def get_avg_tors(start_date, end_date):
    """Выгрузка средняя длительность ремонтов"""
    sql = '''
      SELECT
      a.*, t.AVGTIME
      from (			   
          select
          a.ILATX
          ,avg(a.DIFF)
          from (
              select
              t.ILATX
              ,t.AUFNR
              ,t."DATNRP"
              ,t."DATRP"
              ,t."DATRP"-t."DATNRP" as DIFF
              from dashboard.tor_ik t
              where t.TSTAT is null and t."DATNRP" BETWEEN '%s' AND '%s') a
              GROUP BY a.ILATX) a left join dashboard.avgttor t on t.ILATX = a.ILATX
    ''' % (start_date, end_date)

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128, encoding='utf-8'))


import datetime as dt
import pandas as pd
import os
#from .. import engine_cons
from sqlalchemy import create_engine
import front_ex.config as config

def get_connection_sap():
    connection_hana = pyhdb.connect(
            host = config.SAP_HOST ,
            port = config.SAP_HOST_PORT,
            user = config.SAP_HOST_USER,
            password = config.SAP_HOST_PASSWORD
            )
    return connection_hana

def get_connection_postgre_string():
    """Строка подключения к postgre тест"""
    return config.POSTGRE_DB

def get_conflict1_data():
    """Выгрузка данных по конфликту 1"""
    sql = '''
        SELECT * FROM analysis.conflict1
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_conflict2_data():
    """Выгрузка данных по конфликту 2"""
    sql = '''
        SELECT * FROM analysis.conflict2
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_conflict3_data():
    """Выгрузка данных по конфликту 3"""
    sql = '''
        SELECT * FROM analysis.conflict3
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_conflict4_data():
    """Выгрузка данных по конфликту 4"""
    sql = '''
        SELECT * FROM analysis.conflict4
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_conflict5_data():
    """Выгрузка данных по конфликту 5"""
    sql = '''
        SELECT * FROM analysis.conflict5
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_conflict6_data():
    """Выгрузка данных по конфликту 6"""
    sql = '''
        SELECT * FROM analysis.conflict6
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_conflict7_data():
    """Выгрузка данных по конфликту 7"""
    sql = '''
        SELECT * FROM analysis.conflict7
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_conflict8_data():
    """Выгрузка данных по конфликту 8"""
    sql = '''
        SELECT * FROM analysis.conflict8
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_conflict9_data():
    """Выгрузка данных по конфликту 9"""
    sql = '''
        SELECT * FROM analysis.conflict9
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_conflict10_data():
    """Выгрузка данных по конфликту 10"""
    sql = '''
        SELECT * FROM analysis.conflict10
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_conflict11_data():
    """Выгрузка данных по конфликту 11"""
    sql = '''
        SELECT * FROM analysis.conflict11
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_conflict12_data():
    """Выгрузка данных по конфликту 12"""
    sql = '''
        SELECT * FROM analysis.conflict12
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_conflict13_data():
    """Выгрузка данных по конфликту 13"""
    sql = '''
        SELECT * FROM analysis.conflict13
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_conflict14_data():
    """Выгрузка данных по конфликту 14"""
    sql = '''
        SELECT * FROM analysis.conflict14
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_conflict15_data():
    """Выгрузка данных по конфликту 15"""
    sql = '''
        SELECT * FROM analysis.conflict15
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_conflict16_data():
    """Выгрузка данных по конфликту 16"""
    sql = '''
        SELECT * FROM analysis.conflict16
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_conflict17_data():
    """Выгрузка данных по конфликту 17"""
    sql = '''
        SELECT * FROM analysis.conflict17
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_conflict18_data():
    """Выгрузка данных по конфликту 18"""
    sql = '''
        SELECT * FROM analysis.conflict18
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_summary_data():
    """Выгрузка сводных данных по конфликтам"""
    sql = '''
        SELECT * FROM analysis.sap_sod_conflicts
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_inactive_data():
    """Выгрузка данных по неактивным УЗ"""
    sql = '''
        SELECT * FROM analysis.inactive
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_unlimited_time_data():
    """Выгрузка данных по УЗ внешних сотрудников, не ограниченным по сроку действия"""
    sql = '''
        SELECT * FROM analysis.unlimited_time
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_profiles_data():
    """Выгрузка данных по стандартным привилегированным профилям"""
    sql = '''
        SELECT * FROM analysis.profiles
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_conf_users_data(trans):
    """Выгрузка списка пользователей с выбранной конфликтующей транзакцией"""
    sql = """
            SELECT *
            FROM sap_s4.agr_users
            WHERE agr_name IN (

            SELECT agr_name
            FROM sap_s4.agr_1251
            WHERE object = 'S_TCODE'
            AND field = 'TCD'
            AND low = %(trans)s
            )
            """
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con, params={"trans":trans})

def get_usr02_data():
    """Выгрузка данных по УЗ пользователей в SAP"""
    sql = '''
        SELECT * FROM sap_s4.usr02
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_user_addrs_data():
    """Выгрузка департамента и должности пользователей в SAP"""
    sql = '''
        SELECT * FROM sap_s4.user_addrs
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)

def get_agr_texts_data():
    """Выгрузка описания ролей"""
    sql = '''
        SELECT * FROM sap_s4.agr_texts
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)
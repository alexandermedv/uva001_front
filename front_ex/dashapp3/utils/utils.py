import datetime as dt
import pandas as pd
import os
from .. import engine_cons

def get_conflict1_data():
    """Выгрузка данных по конфликту 1"""
    sql = '''
        SELECT * FROM analysis.conflict1
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_conflict2_data():
    """Выгрузка данных по конфликту 2"""
    sql = '''
        SELECT * FROM analysis.conflict2
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_conflict3_data():
    """Выгрузка данных по конфликту 3"""
    sql = '''
        SELECT * FROM analysis.conflict3
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_conflict4_data():
    """Выгрузка данных по конфликту 4"""
    sql = '''
        SELECT * FROM analysis.conflict4
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_conflict5_data():
    """Выгрузка данных по конфликту 5"""
    sql = '''
        SELECT * FROM analysis.conflict5
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_conflict6_data():
    """Выгрузка данных по конфликту 6"""
    sql = '''
        SELECT * FROM analysis.conflict6
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_conflict7_data():
    """Выгрузка данных по конфликту 7"""
    sql = '''
        SELECT * FROM analysis.conflict7
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_conflict8_data():
    """Выгрузка данных по конфликту 8"""
    sql = '''
        SELECT * FROM analysis.conflict8
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_conflict9_data():
    """Выгрузка данных по конфликту 9"""
    sql = '''
        SELECT * FROM analysis.conflict9
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_conflict10_data():
    """Выгрузка данных по конфликту 10"""
    sql = '''
        SELECT * FROM analysis.conflict10
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_conflict11_data():
    """Выгрузка данных по конфликту 11"""
    sql = '''
        SELECT * FROM analysis.conflict11
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_conflict12_data():
    """Выгрузка данных по конфликту 12"""
    sql = '''
        SELECT * FROM analysis.conflict12
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_conflict13_data():
    """Выгрузка данных по конфликту 13"""
    sql = '''
        SELECT * FROM analysis.conflict13
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_conflict14_data():
    """Выгрузка данных по конфликту 14"""
    sql = '''
        SELECT * FROM analysis.conflict14
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_conflict15_data():
    """Выгрузка данных по конфликту 15"""
    sql = '''
        SELECT * FROM analysis.conflict15
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_conflict16_data():
    """Выгрузка данных по конфликту 16"""
    sql = '''
        SELECT * FROM analysis.conflict16
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_conflict17_data():
    """Выгрузка данных по конфликту 17"""
    sql = '''
        SELECT * FROM analysis.conflict17
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_conflict18_data():
    """Выгрузка данных по конфликту 18"""
    sql = '''
        SELECT * FROM analysis.conflict18
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_summary_data():
    """Выгрузка сводных данных по конфликтам"""
    sql = '''
        SELECT * FROM analysis.sap_sod_conflicts
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_inactive_data():
    """Выгрузка данных по неактивным УЗ"""
    sql = '''
        SELECT * FROM analysis.inactive
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_unlimited_time_data():
    """Выгрузка данных по УЗ внешних сотрудников, не ограниченным по сроку действия"""
    sql = '''
        SELECT * FROM analysis.unlimited_time
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_profiles_data():
    """Выгрузка данных по стандартным привилегированным профилям"""
    sql = '''
        SELECT * FROM analysis.profiles
            '''

    return pd.read_sql(sql, con=engine_cons)

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

    return pd.read_sql(sql, con=engine_cons, params={"trans":trans})

def get_usr02_data():
    """Выгрузка данных по УЗ пользователей в SAP"""
    sql = '''
        SELECT * FROM sap_s4.usr02
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_user_addrs_data():
    """Выгрузка департамента и должности пользователей в SAP"""
    sql = '''
        SELECT * FROM sap_s4.user_addrs
            '''

    return pd.read_sql(sql, con=engine_cons)

def get_agr_texts_data():
    """Выгрузка описания ролей"""
    sql = '''
        SELECT * FROM sap_s4.agr_texts
            '''

    return pd.read_sql(sql, con=engine_cons)
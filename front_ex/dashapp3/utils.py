import pyhdb
import datetime as dt
import pandas as pd
import os
from .. import engine_cons
from sqlalchemy import create_engine


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
    """Выгрузка сводных данных по концликтам"""
    sql = '''
        SELECT * FROM analysis.sap_sod_conflicts
            '''
    con = create_engine(get_connection_postgre_string(), max_identifier_length=128, encoding='utf-8')

    return pd.read_sql(sql, con=con)
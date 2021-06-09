import front_ex.config as config
from sqlalchemy import create_engine
import pandas as pd


def get_details_dost():
    """Выгрузка деталей в статусе ДОСТ"""
    sql = """
        SELECT *
        FROM dashboard.equipment
        LIMIT 100
        """

    return pd.read_sql(sql, con=create_engine(config.POSTGRE_DB, max_identifier_length=128, encoding='utf-8'))

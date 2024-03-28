import os
from sqlalchemy import create_engine
import pandas as pd


def get_details_dost():
    """Выгрузка деталей в статусе ДОСТ"""
    sql = """
        SELECT *
        FROM dashboard.equipment
        LIMIT 100
        """

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))

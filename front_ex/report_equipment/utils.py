import os
from sqlalchemy import create_engine
import pandas as pd


def get_equipment():
    """Выгрузка справочника номерных деталей"""
    sql = """
        SELECT *
        FROM dashboard.equipment
        LIMIT 10000
        """

    return pd.read_sql(sql, con=create_engine(os.environ['POSTGRE_URL_DASH'], max_identifier_length=128))

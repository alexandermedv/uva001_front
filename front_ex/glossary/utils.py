from sqlalchemy import create_engine
import pandas as pd
import json
from pprint import pprint


def get_glossary():
    """Открытие файла со словарем"""
    with open('./front_ex/glossary/data.json') as json_file:
        data = json.load(json_file)

    return data

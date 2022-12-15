"""Выгрузка данных и вспомогательные функции"""
import os
from contextlib import contextmanager
from typing import Optional
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from .settings import login_prod, password_prod, ENDPOINT_prod, locate_schema_file
import json
from datetime import datetime
import xmlschema  # type: ignore
from zeep import Client  # type: ignore


@contextmanager
def get_client(login, password, wdsl_url=ENDPOINT_prod) -> Client:
    """Клиент для использования в конструкции with"""
    client = Client(wdsl_url)
    # client.transport.session.proxies = {
    #     'https': 'http://msc01-cfw01.pgk.rzd:9090',
    #     'http': 'http://msc01-cfw01.pgk.rzd:9090'
    # }
    result = client.service.Authmethod(login, password)
    #print('login =, password=, wdsl_url=, result=', login, password, wdsl_url, result, flush=True)
    try:
        # передаем в with
        yield client
    finally:
        # закрываем сессию
        client.service.End()


def get_schema(filename: str) -> xmlschema.XMLSchema10:
    return xmlschema.XMLSchema(locate_schema_file(filename))


# def create_getter(method_name, schema_filename, finalise_with):
#     def getter(client, *arg, **kwarg):
#         xml = client.service[method_name](*arg, **kwarg).xmlData
#         print('xml =', xml)
#         data = get_schema(schema_filename).to_dict(xml)
#         print('data =', data)
#         return finalise_with(data)
#     return getter

engine_postgre = create_engine('postgresql://uruevav:Squirrel14@172.17.0.134:5432/interfax', max_identifier_length=128)

class Reporter:
    """Класс Reporter позволяет воспользоваться методами API Spark-Interfax.
       На входе нужно предоставить свой логин и пароль.
       Названия методов соотвествуют документации http://sparkgatetest.interfax.ru/iFaxWebService/.
       В академической версии API доступна ограниченная часть методов 
       (см. https://github.com/finec-mgimo/interfax-client/issues/2)
    """

    wdsl_url = ENDPOINT_prod
    """
    Класс для логина и получения данных:
       - иницализируется парой логин-пароль
       - одноименные методы с SOAP API Spark-Interfax
    """

    def __init__(self, login: Optional[str], password: Optional[str]):
        self.client = Client(self.wdsl_url)
        self.enter = lambda: self.client.service.Authmethod(login, password)

    def __enter__(self):
        self.enter()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.client.service.End()

    def Lets_connect(self, *arg, **kwarg):
        method = kwarg.get('method')
        print('В Lets_connect подано значение ', method)
        xml = self.client.service[method]()
        #xml = self.client.service[kwarg.pop('method')](*arg, **kwarg)
        return xml

def spark_GetStateAccount(**kwarg):
    with Reporter(login_prod, password_prod) as reporter:
        try:
            xml = reporter.Lets_connect(**kwarg).xmlData
            #print('xml = ', xml)
            #print('login_prod =, password_prod=, ENDPOINT_prod=', login_prod, password_prod, ENDPOINT_prod, flush=True)
        except:
            print('Подключение не сработало')
            xml = 'Ошибка при вызове метода'
        return xml
        
    # try:
    #     json_data = json.dumps(get_schema("CompanyAccountingReport.xsd").to_dict(xml)) # тут нужно будет сделать автоматическое подтягивание правильного xsd-файла
    # except:
    #     json_data = 'Не получилось распарсить данные с помощью xsd-файла'
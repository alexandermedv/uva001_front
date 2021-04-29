import os

class DefaultConfig():
    # Установка временной зоны для приложения и Docker
    USE_TZ = True
    TIMEZONE = 'Europe/Moscow' 
class DevelopConfig(DefaultConfig):
    FLASK_ENV = 'development'
    # Настройки WSGI - run_simple
    USE_DEBUGGER = True
    USE_RELOADER = True
    # General
    DEBUG = True
    # Настройки Postgre
    POSTGRE_DB = os.environ.get('POSTGRE_URL_DEV')
    # Настройки SAP
    SAP_HOST =  os.environ.get('SAP_HOST_DEV')
    SAP_HOST_PORT = os.environ.get('SAP_HOST_PORT_DEV')
    SAP_HOST_USER = os.environ.get('SAP_HOST_USER_DEV')
    SAP_HOST_PASSWORD = os.environ.get('SAP_HOST_PASSWORD_DEV') 
    # Настройки FLASK
    FLASK_PORT = os.environ.get('FLASK_PORT_DEV')
class ProdConfig(DefaultConfig):
    FLASK_ENV = 'production'
    # Настройки WSGI - run_simple
    USE_DEBUGGER = False
    USE_RELOADER = False
     # General
    DEBUG = False
    # Настройки Postgre
    POSTGRE_DB = os.environ.get('POSTGRE_URL_PROD')
    # Настройки SAP
    SAP_HOST = os.environ.get('SAP_HOST_PROD')
    SAP_HOST_PORT = os.environ.get('SAP_HOST_PORT_PROD')
    SAP_HOST_USER = os.environ.get('SAP_HOST_USER_PROD')
    SAP_HOST_PASSWORD = os.environ.get('SAP_HOST_PASSWORD_PROD') 
    # Настройки FLASK
    FLASK_PORT = os.environ.get('FLASK_PORT_PROD')
class TestConfig(DefaultConfig):
    FLASK_ENV = 'development'
    # Настройки WSGI - run_simple
    USE_DEBUGGER = False
    USE_RELOADER = False
    # General
    DEBUG = False
    # Настройки Postgre
    POSTGRE_DB = os.environ.get('POSTGRE_URL_PROD')
    # Настройки SAP
    SAP_HOST = os.environ.get('SAP_HOST_PROD')
    SAP_HOST_PORT = os.environ.get('SAP_HOST_PORT_PROD')
    SAP_HOST_USER = os.environ.get('SAP_HOST_USER_PROD')
    SAP_HOST_PASSWORD = os.environ.get('SAP_HOST_PASSWORD_PROD') 
    # Настройки FLASK
    FLASK_PORT = os.environ.get('FLASK_PORT_TEST')

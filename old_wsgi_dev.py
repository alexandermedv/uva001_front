import os
from dotenv import load_dotenv

# Переменные окружения
load_dotenv(os.path.abspath(os.path.dirname(__file__))+'/.dev.env')
print('База данных приложения', os.environ['SQLALCHEMY_DATABASE_URI'])
print('База данных для отчетов и дэшбордов', os.environ['POSTGRE_URL_DASH'])
print('База SAP S4', os.environ['SAP_HOST_S4'])

# Обязательно добавить app иначе flask db его не видит 
from front_ex import dispatch_app, app

if(__name__ == '__main__'):
    app.wsgi_app = dispatch_app
    app.run('0.0.0.0', int(os.environ['FLASK_PORT']), debug=os.environ['FLASK_DEBUG'])
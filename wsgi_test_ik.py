import os
from dotenv import load_dotenv

# Переменные окружения
load_dotenv(os.path.abspath(os.path.dirname(__file__))+'/.test.env')

# Обязательно добавить app иначе flask db его не видит 
from front_ex import dispatch_app, app

if (__name__ == '__main__'):
    app.wsgi_app = dispatch_app
    app.run('172.17.0.133', '7113', debug=True)

from werkzeug.serving import run_simple
import os
from dotenv import load_dotenv

# Переменные окружения
load_dotenv(os.path.abspath(os.path.dirname(__file__))+'/.env')
import front_ex.config as config

# запуск Flask и встроенных Дэшбордов
from front_ex import dispatch_app, app  

if(__name__ == '__main__'):
        run_simple('0.0.0.0', int(config.FLASK_PORT), dispatch_app, use_debugger=config.USE_DEBUGGER, use_reloader=config.USE_RELOADER)

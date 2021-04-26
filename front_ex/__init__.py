# Инициализация Celery
import flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

import config

flask_app = flask.Flask(__name__)
flask_app.config.update(
    USE_TZ = True,
    TIMEZONE = 'Europe/Moscow',   
    # USE_TZ = True,
    # TIMEZONE = 'Europe/Moscow',   
)

# Сборка Dashboard 
from .dash_limit_oper import dash_app as dash_limit_oper
# from .dash_osv_dev import dash_app as dash_osv_dev

# Добавляем руты 
import front_ex.views #import app

# Сборка в Middleware
dispatch_app = DispatcherMiddleware(flask_app, {
    'limit_oper': dash_limit_oper.server
    # '/dash_osv_dev': dash_osv_dev.server  
    })
    
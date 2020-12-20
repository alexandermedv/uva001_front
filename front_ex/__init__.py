# Инициализация Celery
import flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

flask_app = flask.Flask(__name__)
flask_app.config.update(
    USE_TZ = True,
    TIMEZONE = 'Europe/Moscow',   
)

# Добавляем руты 
import front_ex.views #import app

# Сборка Dashboard 
from .dash_osv import dash_app as dash_osv
from .dash_osv_dev import dash_app as dash_osv_dev

# Сборка в Middleware
dispatch_app = DispatcherMiddleware(flask_app, {
    '/dash_osv': dash_osv.server,
    '/dash_osv_dev': dash_osv_dev.server  
    }) 

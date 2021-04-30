# Инициализация Celery
import flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import front_ex.config as config

# Добавляем логирование пользователей и роли
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

flask_app = flask.Flask(__name__)
flask_app.config.update(
    USE_TZ = config.USE_TZ,
    TIMEZONE = config.TIMEZONE,   
)

# Добавляем базы данных и логин-менеджер
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
db = SQLAlchemy(app)
manager = LoginManager(app)

# Сборка Dashboards
from .dash_limit_oper import dash_app as dash_limit_oper
from .dashapp1 import dash_app as dashapp1
# from .dash_osv_dev import dash_app as dash_osv_dev

# Добавляем руты 
import front_ex.views #import app

# Сборка в Middleware
dispatch_app = DispatcherMiddleware(flask_app, {
    'limit_oper': dash_limit_oper.server,
    'dashapp1': dashapp1.server
    # '/dash_osv_dev': dash_osv_dev.server  
    })
    
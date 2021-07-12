# Инициализация Celery
import os
from os import path as op
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import front_ex.config as config


# Добавляем логирование пользователей и роли
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.update(
    USE_TZ = config.USE_TZ,
    TIMEZONE = config.TIMEZONE,   
)

# Добавляем базы данных и логин-менеджер
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config.SECRET_KEY or os.randov
db = SQLAlchemy(app)
db.create_all()


login = LoginManager()
login.init_app(app)

migrate = Migrate(app, db, compare_type=True)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Сборка Dashboards
from .dash_limit_oper import dash_app as dash_limit_oper
from .dashapp1 import dash_app as dashapp1
from .dashapp3 import dash_app as dashapp3
# from .dash_osv_dev import dash_app as dash_osv_dev

# Добавляем руты 
import front_ex.routes

# # Сборка в Middleware
# dispatch_app = DispatcherMiddleware(flask_app, {
#     'limit_oper': dash_limit_oper.server,
#     'dashapp1': dashapp1.server,
#     'dashboard3': dashapp3.server
#     # '/dash_osv_dev': dash_osv_dev.server  
#     })

# Сборка в Middleware
dispatch_app = DispatcherMiddleware(app.wsgi_app, {
    'limit_oper': dash_limit_oper.server,
    'dashapp1': dashapp1.server,
    'dashboard3': dashapp3.server
    })

# Инициализация Celery
import flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

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
flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.config['SECRET_KEY'] = config.SECRET_KEY or os.randov
db = SQLAlchemy(flask_app)
db.create_all()


login = LoginManager()
login.init_app(flask_app)

migrate = Migrate(flask_app, db, compare_type=True)

manager = Manager(flask_app)
manager.add_command('db', MigrateCommand)

# Сборка Dashboards
from .dash_limit_oper import dash_app as dash_limit_oper
from .dashapp1 import dash_app as dashapp1

# Добавляем руты 
import front_ex.routes

# Сборка в Middleware
dispatch_app = DispatcherMiddleware(flask_app, {
    'limit_oper': dash_limit_oper.server,
    'dashapp1': dashapp1.server
    # '/dash_osv_dev': dash_osv_dev.server  
    })
    
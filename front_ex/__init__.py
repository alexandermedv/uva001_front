# Инициализация Celery
import os
from os import path as op
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware


from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import UserMixin, LoginManager
from flask_admin import Admin 

from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user
from flask_admin.contrib import fileadmin

# Добавление русской локали
from flask_babelex import Babel

# Встроенные API
from flask_restful import Api 

from . import config
from .forms import LoginForm

# Добавляем логирование пользователей и роли
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.update(
    USE_TZ = config.USE_TZ,
    TIMEZONE = config.TIMEZONE,   
)

#### Добавляет шаблон Bootstrap
Bootstrap(app)

# Добавляем локаль
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'Europe/Moscow'
babel = Babel(app)

# Добавляем базы данных и логин-менеджер
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config.SECRET_KEY or os.randov
db = SQLAlchemy(app)
db.create_all()

# Миграция - создание и обновление структуры баз данных
migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Логирование 
login = LoginManager()
login.init_app(app)

from .models import User,Role,HomeIndexView,UserModelView,RoleModelView,ReportModelView,RedirectTaskView,Report 

# Добавляем админку
# Добавление ролевой модели из Flask_Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, login_form=LoginForm)

# декоратор под первого пользователя
@app.before_first_request
def create_user():
    db.create_all()
    user = User.query.first()
    if not user:
        user_datastore.create_user(ldap_account='svc_fs-uva', email='svc_fs-uva@pgkweb.ru', active=True)
        # user_datastore.create_user(email='admin@admin', password='admin')
        db.session.commit()

# Create directory
path = op.join(op.dirname(__file__), 'files')
try:
    os.mkdir(path)
except OSError:
    pass

# добавление административной формы
admin = Admin(app, name = 'Администрирование', template_mode='bootstrap3', \
    index_view=HomeIndexView(name='Обзор', endpoint='admin.user', url='/admin'))
admin.add_view(UserModelView(User, db.session, name='Пользователи'))
admin.add_view(RoleModelView(Role, db.session, name='Роли'))
admin.add_view(ReportModelView(Report, db.session, name='Отчеты'))
admin.add_view(fileadmin.FileAdmin(path , '/files/', name='Файлы'))
admin.add_view(RedirectTaskView(name='На сайт'))

# Встроенный API
api = Api(app)
migrate = Migrate(app, db, compare_type=True)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Сборка Dashboards
from .dash_limit_oper import dash_app as dash_limit_oper
from .dashapp1 import dash_app as dashapp1
from .dashapp3 import dash_app as dashapp3

import front_ex.reports
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

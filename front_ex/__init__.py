# Инициализация Celery
import os
from os import path as op
from flask import Flask, redirect, url_for, request
from healthcheck import HealthCheck
from werkzeug.middleware.dispatcher import DispatcherMiddleware


from flask import Flask, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
# from flask_script import Manager
from flask_migrate import Migrate
# from flask_migrate import MigrateCommand
# from flask_login import UserMixin, LoginManager
from flask_admin import Admin

from flask_security import Security, SQLAlchemyUserDatastore, current_user, login_required
from flask_admin.contrib import fileadmin

# Добавление русской локали
from flask_babel import Babel
from sqlalchemy import func
from datetime import timedelta

# Встроенные API
# from flask_restful import Api

# from .forms import LoginForm
# Добавляем логирование пользователей и роли
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)

# app.config.update(
#     USE_TZ = os.environ['USE_TZ'],
#     TIMEZONE = os.environ['TIMEZONE'],   
# )
CORS(app)

#### Добавляет шаблон Bootstrap
Bootstrap(app)

# Добавляем локаль
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'Europe/Moscow'
babel = Babel(app)

# Добавляем базы данных и логин-менеджер
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
print(os.environ['SQLALCHEMY_DATABASE_URI'])
app.config['SQLALCHEMY_BINDS'] = {'log': os.environ['SQLALCHEMY_DATABASE_LOG']}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 25.12.23 AT - Ошибка входа, Илья
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True} 
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
db.create_all(bind=None)
db.create_all(bind=['log'])

# Миграция - создание и обновление структуры баз данных
migrate = Migrate(app, db, compare_type=True)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

# Логирование
login = LoginManager()
login.init_app(app)

from .models import User,Role,Dash,HomeIndexView,UserModelView,RoleModelView,ReportModelView,RedirectTaskView,Report,DashModelView 

# Добавляем админку
# Добавление ролевой модели из Flask_Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# print(user_datastore)

from .forms import UserLoginForm 

# security = Security()
# app.config['SECURITY_REGISTERABLE']=True
# app.config['SECURITY_PASSWORD_SALT'] = 'salt'

# AT
# security = Security(login_form=UserLoginForm)
# app.config['SECURITY_MSG_LOGIN'] = ('Для просмотра сайта требуется авторизоваться', 'info')
# security.init_app(app=app, datastore = user_datastore)

# AT
# app.config['SECURITY_USER_INDENTITY_ATTRIBUTES'] = [
#     {'ldap_account':{'case_intensitive': False}}
# ]
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=15)

# декоратор под первого пользователя
# @app.before_first_request
def create_user():
    with app.app_context():
        db.create_all(bind=None)
        db.create_all(bind=['log'])
        user = User.query.first()
        if not user:
            user_to_create = User(ldap_account='svc_fs_uva', email='svc_fs_uva@pgkweb.ru', active=True)
            user_datastore.create_user(ldap_account='svc_fs_uva', email='svc_fs_uva@pgkweb.ru', active=True)
            db.session.commit()
            
            user = User.query.first()

            # user_to_create.fs_uniquifier = '000'
            
            role = Role.query.first()
            if not role:
                user_datastore.create_role(name='admin', description='Администратор, полные полномочия')
                role = Role.query.first()
            user_datastore.add_role_to_user(user, 'admin')
            # print('user =', security.datastore.find_user(email="svc_fs_uva@pgkweb.ru"))
            # user_datastore.create_user(email='admin@admin', password='admin')
            db.session.commit()
create_user()


# @app.login_manager.unauthorized_handler
# def unauth_handler():
#     return jsonify(success=False, data={'login_required': True}, message='Authorize please to access this page'), 401

# Create directory
path = op.join(op.dirname(__file__), 'files')
try:
    os.mkdir(path)
except OSError:
    pass

# добавление административной формы
# adminuser=admin.user
admin = Admin(app, name = 'Администрирование', template_mode='bootstrap3', \
    index_view=HomeIndexView(name='Обзор', endpoint='adminuser', url='/admin'))
admin.add_view(UserModelView(User, db.session, name='Пользователи'))
admin.add_view(RoleModelView(Role, db.session, name='Роли'))
admin.add_view(DashModelView(Dash, db.session, name='Дэшборды'))
admin.add_view(ReportModelView(Report, db.session, name='Отчеты'))
admin.add_view(fileadmin.FileAdmin(path , '/files/', name='Файлы'))
admin.add_view(RedirectTaskView(name='На сайт'))

# Встроенный API
# api = Api(app)
migrate = Migrate(app, db, compare_type=True)

# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

# Сборка Dashboards
from .dash_limit_oper import dash_app as dash_limit_oper
from .dashapp1 import dash_app as dashapp1
from .dashapp3 import dash_app as dashapp3
from .dashapp5 import dash_app as dashapp5
from .dashapp6_monitoring import dash_app as dashapp6_monitoring
from .dashapp7_repairs import dash_app as dashapp7_repairs
from .dashapp8_empty_transportations import dash_app as dashapp8_empty_transportations
from .dashapp9_resellers_commerce import dash_app as dashapp9_resellers_commerce
from .dashapp10_nagon import dash_app as dashapp10_nagon
# from .dashapp11_risks import dash_app as dashapp11_risks
from .dashapp12_tor_neis import dash_app as dashapp12_tor_neis
# from .dashapp13_credit_risks import dash_app as dashapp13_credit_risks
# from .dashapp14_spark_api_count_request import dash_app as dashapp14_spark_api_count_request
from .dashapp15_airflow import dash_app as dashapp15_airflow
from .dashapp_credibility_rating import dash_app as dashapp_credibility_rating
from .dashapp_resellers_uru import dash_app as dashapp_resellers_uru

# Добавляем руты и таски
import front_ex.routes
import front_ex.reports
# from .dash_osv_dev import dash_app as dash_osv_dev

# Сборка в Middleware
dispatch_app = DispatcherMiddleware(app.wsgi_app, {
    'limit_oper': dash_limit_oper.server,
    'dashapp1': dashapp1.server,
    'dashboard3': dashapp3.server,
    'dashapp5': dashapp5.server,
    'dashapp6': dashapp6_monitoring.server,
    'dashapp7': dashapp7_repairs.server,
    'dashapp8': dashapp8_empty_transportations.server,
    'dashapp9': dashapp9_resellers_commerce.server,
    'dashapp10': dashapp10_nagon.server,
    # 'dashapp11': dashapp11_risks.server,
    'dashapp12': dashapp12_tor_neis.server,  
    # 'dashapp13': dashapp13_credit_risks.server,
    # 'dashapp14': dashapp14_spark_api_count_request.server,
    'dashapp15': dashapp15_airflow.server, 
    'credibility_rating': dashapp_credibility_rating.server, 
    'resellers_uru': dashapp_resellers_uru.server, 
    })


# Healthcheck
health = HealthCheck()
from .utils import get_postgre_con_str, get_log_con_str

# Проверка доступности баз данных
def front_db_available():
    front_db_engine = get_postgre_con_str()
    if front_db_engine:
        result = True
    else:
        result = False
    return result, "front_db_checked"

def log_db_available():
    sap_s4p_engine = get_log_con_str()
    if sap_s4p_engine:
        result = True
    else:
        result = False
    return result, "log_db_checked"

# def get_sap_s4_con_str():
#     """Строка подключения к S4 прод"""
#     return os.environ['SAP_HOST_S4']

# def get_udv_con_str():
#     """Строка подключения к УДВ прод"""
#     return os.environ['UDV']


health.add_check(front_db_available)
health.add_check(log_db_available)

app.add_url_rule('/healthcheck', 'healthcheck', view_func=lambda: health.run())

# AT
@login.user_loader
def user_loader(user):
    print('@login.user_loader', int(user))
    return User.query.filter(User.id==int(user)).first()
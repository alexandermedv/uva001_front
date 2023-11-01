# Инициализация Celery
import os
from os import path as op
from flask import Flask, redirect, url_for, request
from werkzeug.middleware.dispatcher import DispatcherMiddleware


from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate
# from flask_migrate import MigrateCommand
from flask_login import UserMixin, LoginManager
from flask_admin import Admin

from flask_security import Security, SQLAlchemyUserDatastore, current_user, login_required
from flask_admin.contrib import fileadmin

# Добавление русской локали
from flask_babelex import Babel

# Встроенные API
from flask_restful import Api

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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
db.create_all()

# Миграция - создание и обновление структуры баз данных
migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)
# manager.add_command('db', MigrateCommand)

# Логирование
# login = LoginManager()
# login.init_app(app)

from .models import User,Role,Dash,HomeIndexView,UserModelView,RoleModelView,ReportModelView,RedirectTaskView,Report,DashModelView 

# Добавляем админку
# Добавление ролевой модели из Flask_Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()
app.config['SECURITY_MSG_LOGIN'] = ('Для просмотра сайта требуется авторизоваться', 'info')
security.init_app(app=app, datastore = user_datastore)

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
admin.add_view(DashModelView(Dash, db.session, name='Дэшборды'))
admin.add_view(ReportModelView(Report, db.session, name='Отчеты'))
admin.add_view(fileadmin.FileAdmin(path , '/files/', name='Файлы'))
admin.add_view(RedirectTaskView(name='На сайт'))

# Встроенный API
api = Api(app)
migrate = Migrate(app, db, compare_type=True)

manager = Manager(app)
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
from .dashapp11_risks import dash_app as dashapp11_risks
from .dashapp13_credit_risks import dash_app as dashapp13_credit_risks
from .dashapp14_spark_api_count_request import dash_app as dashapp14_spark_api_count_request
from .dashapp15_credibility_rating import dash_app as dashapp15_credibility_rating

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
    'dashapp11': dashapp11_risks.server, 
    'dashapp13': dashapp13_credit_risks.server,
    'dashapp14': dashapp14_spark_api_count_request.server,
    'dashapp15': dashapp15_credibility_rating.server,
    })

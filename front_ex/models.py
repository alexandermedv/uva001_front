from datetime import datetime
from flask_wtf import FlaskForm
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user
from flask import url_for, redirect, render_template, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, BooleanField
from wtforms import SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, InputRequired, Email, NumberRange, EqualTo
from wtforms.fields.html5 import DateField, EmailField
from functools import wraps
from flask_admin import BaseView, AdminIndexView, expose

from . import db, login
from .config.html_roles import html_access_roles

# Связь роли с пользователем
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    # __table_args = {'schema':'ver1'}

    id = db.Column(db.Integer, primary_key=True)
    # Сюда надо заводить Аккаунт Windows
    ldap_account = db.Column(db.Unicode(250), nullable=False)
    last_name = db.Column(db.Unicode(250))
    first_name = db.Column(db.Unicode(250))
    second_name = db.Column(db.Unicode(250))
    dept_id = db.Column(db.Unicode(1000))
    position = db.Column(db.Unicode(1000))
    email = db.Column('email', db.Unicode(250), nullable=False)
    active = db.Column(db.Boolean())
    # Пароль не требуется, поскольку он проверяется по LDAP
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.last_name)
    
    # Модель подразумевает одну роль на один логин и много ролей на один роут
    def get_roles(self, *args):
        return self.roles
    
    def get_role_by_html_element(*args):
        print('args', args[1])
        if args:
            return html_access_roles.get(args[1])
        return []

    def to_json(self):
        return { 
            "last_name": self.last_name,
            "first_name": self.first_name,
            "second_name": self.second_name,
            "dept_id": self.dept_id,
            "position": self.position,
            "email": self.email,
            # "type": self.type,
            "active": self.active, 
            "role": self.roles}

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
	    self.password = generate_password_hash(password)

    def check_password(self,  password):
	    return check_password_hash(self.password, password)

    # Проверка пересечения по ролям
    def get_roles(self, *args):
        return self.roles
    
    def check_roles(self, object_roles):
        print('set', set(self.get_roles()).intersection(object_roles))
        return set(self.get_roles()).intersection(object_roles)    

# def requires_roles(*roles):
#     """Проверка роли"""
#     def wrapper(f):
#         @wraps(f)
#         def wrapped(*args, **kwargs):
#             if current_user.get_role(*args) not in roles:
#                 # Redirect the user to an unauthorized notice!
#                 return "Ваш аккаунт не имеет доступа к данной странице."
#             return f(*args, **kwargs)
#         return wrapped
#     return wrapper

def requires_roles(*roles):
    """Проверка роли"""
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Если надется хоть одна роль на пересечении
            if not set(current_user.get_roles(*args)).intersection(roles):
                # Redirect the user to an unauthorized notice!
                print(set(current_user.get_roles(*args)).intersection(roles))
                return "Ваш аккаунт не имеет доступа к данной странице."
            return f(*args, **kwargs)
        return wrapped
    return wrapper

# Роли
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

#### Встраивание Flask Admin
class UserModelView(ModelView):
    '''
        Закладка Пользователи
    '''
    def is_accessible(self):
        return (current_user.is_active , current_user.is_authenticated)
    
    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('signin'))

    column_list = ['id', 'ldap_account', 'last_name','first_name', 'second_name', 'email', 'active', 'roles', 'confirmed_at']
    form_columns = ('ldap_account','last_name','first_name','second_name','email', 'active', 'roles')

    column_labels = dict(id="#", ldap_account='Учетная запись', last_name='Фамилия',first_name='Имя', second_name='Отчество', active='Активно', \
        roles = 'Роли', confirmed_at='Дата с') 

    column_searchable_list = ['last_name', 'ldap_account', 'email']

    can_export = True

    def on_model_change(self, form, model, is_created):

        if is_created:
            model.confirmed_at = datetime.now()
            model.active = True

class HomeIndexView(AdminIndexView):
    """
        Убрать закладку Home
    """
    def is_visible(self):
        # This view won't appear in the menu structure
        return False

    @expose('/')
    def index(self):
        return self.render(
            'admin/base.html',
        )

class RedirectTaskView(BaseView):
    '''
        Закладка задачи - переход на страницу задач
    '''
    @expose('/')
    def index(self):
        return self.render(
            'index.html'
        )

class RoleModelView(ModelView):
    '''
        Закладка Роль
    '''
    def is_accessible(self):
        return (current_user.is_active , current_user.is_authenticated)
    
    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('signin'))
            # return redirect(url_for('security.login'))
    column_list = ['id','name','description']
    column_labels = dict(id="#", name='Роль', description='Описание') 

# Реестр отчетов
# Пользователи
roles_reports = db.Table(
    'roles_reports',
    db.Column('report_id', db.Integer(), db.ForeignKey('report.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Report(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    instance = db.Column(db.String(255))
    name = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    description = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=roles_reports,
                            backref=db.backref('reports', lazy='dynamic'))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.id
    
    # Роли доступа к отчету
    def get_access_roles(self):
        return self.roles

class ReportModelView(ModelView):
    '''
        Закладка Отчеты
    '''
    def is_accessible(self):
        return (current_user.is_active , current_user.is_authenticated)
    
    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('signin'))
            # return redirect(url_for('security.login'))
        
    column_list = ['id','instance','name','active','description','roles']
    form_columns = ['instance', 'name','active','description', 'roles']
    
    column_labels = dict(id="#",instance='Код',name='Наименование',active='Активно',description='Описание') 
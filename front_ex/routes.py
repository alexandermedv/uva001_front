from flask_login import current_user, login_required, login_user, logout_user
from flask import url_for, redirect, render_template, flash, request
import pandas as pd

from . import flask_app, db, login
from .forms import LoginForm, CreateUserForm, ProfileForm, EditUserForm, PasswordUserForm
from .models import User, requires_roles
from sqlalchemy import create_engine
import os
import front_ex.config as config
from .report1 import utils as report1

# Доступы по текущей сессии
@login.user_loader
def load_user(id):
    """Инициализация пользователя"""
    user = User.query.filter_by(id=id).first()
    return user

# Руты к дэшбордам
@flask_app.route('/limit_oper/')
@login_required
def render_limit_oper():
    return render_template('/limit_oper/overview.html')

@flask_app.route('/dashapp1/')
@login_required
def render_dashapp1():
    return render_template('/dashapp1/overview.html')    

@flask_app.route('/dashboard3/')
@login_required
def render_dashapp3():
    return render_template('/dashapp3/overview.html')   

@flask_app.route('/report1/')
@login_required
def render_report1():
    # con = create_engine(config.POSTGRE_DB, max_identifier_length=128, encoding='utf-8')
    # sql = '''SELECT *
    # FROM dashboard.equipment
    # LIMIT 100
    # '''
    df1 = report1.get_details_dost()
    print(df1)
    return render_template('/report1/report1.html', title='report1', items=df1[['equnr', 'eartx', 'status', 'erdat', 'hequi', 'typtx', 'last_oper_date']].to_dict(orient='records')) 

# Общий роутинг
@flask_app.route('/', methods=['GET', 'POST'])
def signin():
    """Вход в систему"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        # print('email', form.email.data, 'password', form.password.data, 'remeber_me',form.remember_me.data)
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        else:
            flash('Invalid username')
            return redirect(url_for('signin'))
    else: print('errors', form.errors)
    return render_template('/user/signin.html', title='Sign In', form=form)

# Общие вводные
@flask_app.route('/index')
@login_required
def index():
    """Первичная страница"""
    return render_template('index.html')

#### Действия пользователя
@flask_app.route('/user/create_user', methods=['get', 'post'])
@login_required
@requires_roles('Администратор')
def create_user():
    """Создание пользователя"""
    form = CreateUserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            usr = User(personnel_number=form.personnel_number.data,
                            email= form.email.data,
                            full_name=form.family_name.data + " " + form.first_name.data + " " + form.second_name.data,
                            family_name=form.family_name.data,
                            first_name=form.first_name.data,
                            second_name=form.second_name.data,
                            dept_id=form.dept_id.data,
                            position=form.position.data,
                            role=form.role.data,
                            status=form.status.data
                            )
            usr.set_password(form.password.data)
            db.session.add(usr)
            db.session.commit()

            # return 'Данные сохранены'
            users = User.query.all()
            return render_template('/user/users.html', users = users, user=usr)
        else:
            message = 'Поля заполнены некорректно. Пожалуйста, проверьте введенные данные.'
            flash(message)

            return render_template('/user/create_user.html', form=form)

    return render_template('/user/create_user.html', title='create user', form=form)

@flask_app.route('/user/edit_user/<user>', methods=['get', 'post'])
@login_required
@requires_roles('Администратор')
def edit_user(user):
    """Редактирование пользователя"""
    if current_user.is_authenticated:
        
        user = User.query.filter_by(id=user).first()
        form = EditUserForm()
        
        if request.method == 'GET':
            form.personnel_number.data = user.personnel_number
            form.email.data = user.email
            form.family_name.data = user.family_name 
            form.first_name.data = user.first_name
            form.second_name.data = user.second_name
            form.dept_id.data = user.dept_id
            form.position.data = user.position
            form.role.data = user.role
            form.status.data = user.status

        if request.method == 'POST':
            if form.validate_on_submit():
                user.personnel_number = form.personnel_number.data 
                user.email = form.email.data
                user.family_name = form.family_name.data 
                user.first_name = form.first_name.data
                user.second_name = form.second_name.data
                user.dept_id = form.dept_id.data
                user.position = form.position.data
                user.role = form.role.data
                user.status = form.status.data
                db.session.commit()

            # return 'Данные сохранены'
            users = User.query.all()
            return redirect(url_for('users', user=user.id))

    return render_template('/user/edit_user.html', title='edit user', form = form, user = user.id)

@flask_app.route('/user/edit_password_user/<user>', methods=['GET', 'POST'])
@login_required
@requires_roles('Администратор')
def edit_password_user(user):
    """Изменение пароля пользователя"""
    if current_user.is_authenticated:
        
        user = User.query.filter_by(id=user).first()
        form = PasswordUserForm()

        if request.method == 'POST':    
            if form.cancel.data:  # if cancel button is clicked, the form.cancel.data will be True
                return redirect(url_for('users', user=user.id)) 
                # redirect(url_for('previous_page_view_name'))
            if form.validate_on_submit():
                if user:
                    user.set_password(form.password.data)
                    db.session.commit()
            return redirect(url_for('users', user=user.id))

    return render_template('/user/edit_password_user.html', title='edit password user', form=form, user=user.id)

@flask_app.route('/user/delete_user/<user>', methods=['GET', 'POST'])
@login_required
@requires_roles('Администратор')
def delete_user(user):
    """Удаление пользователя"""
    if current_user.is_authenticated:
        
        user = User.query.filter_by(id=user).delete()
        db.session.commit()
        return redirect(url_for('users', user=current_user.id))

    return redirect(url_for('users', user=current_user.id))

@flask_app.route('/user/users/<user>', methods=['GET', 'POST'])
@login_required
@requires_roles('Администратор')
def users(user=current_user):
    """Управление пользователями"""
    # if current_user.is_authenticated:
    users = User.query.order_by(User.id.asc()).all()
    cur_user = User.query.filter_by(id=user).first()
    return render_template('/user/users.html', users=users, user=cur_user)
    
@flask_app.route('/user/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Профиль пользователя"""
    if current_user.is_authenticated:
        form = ProfileForm()
        form.full_name.data = current_user.full_name
        form.email.data = current_user.email
        if request.method == 'POST':
            if form.validate_on_submit():
                user = User.query.filter_by(email=current_user.email).first()
                if user:
                    user.set_password(form.password.data)
                    db.session.commit()
                    flash('Пароль изменен')
    return render_template('/user/profile.html', title='profile', form=form)

@flask_app.route('/logout')
def logout():
    """Выход из системы"""  
    logout_user()
    return redirect(url_for('signin'))

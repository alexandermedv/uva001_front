from flask_login import current_user, login_required, login_user, logout_user
from flask import url_for, redirect, render_template, flash, request
import pandas as pd

from . import flask_app, db, login
from .forms import LoginForm, CreateUserForm, ProfileForm
from .models import User, requires_roles

# Доступы по текущей сессии
@login.user_loader
def load_user(id):
    """Инициализация пользователя"""
    user = User.query.filter_by(id=id).first()
    print(user.get_role())
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

# Общий роутинг
@flask_app.route('/', methods=['GET', 'POST'])
def signin():
    """Вход в систему"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # print('email', form.email.data, 'password', form.password.data, 'remeber_me',form.remember_me.data)
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Invalid username')
            return redirect(url_for('signin'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    else: print('errors', form.errors)
    return render_template('/user/signin.html', title='Sign In', form=form)

# Общие вводные
@flask_app.route('/index')
@login_required
def index():
    """Первичная страница"""
    return render_template('index.html')

# Действия пользователя
@flask_app.route('/user/create_user', methods=['get', 'post'])
@login_required
@requires_roles('Администратор')
def create_user():
    """Создание пользователя"""
    form = CreateUserForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            #password_hash = User.set_password(password)

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
            usr.set_password(password)
            db.session.add(usr)
            db.session.commit()

            return 'Данные сохранены'
        else:
            message = 'Поля заполнены некорректно. Пожалуйста, проверьте введенные данные.'
            flash(message)
            return render_template('/user/create_user.html', form=form)

    return render_template('/user/create_user.html', title='create user', form=form)
    
@flask_app.route('/user/profile', methods=['GET', 'POST'])
@login_required
@requires_roles('Администратор')
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
                    user.set_password(form.email.data)
                    db.session.commit()
                    flash('Пароль изменен.')
    return render_template('/user/profile.html', title='profile', form=form)

@flask_app.route('/user/users', methods=['GET', 'POST'])
@login_required
def users():
    """Управление пользователями"""
    # if current_user.is_authenticated:
    users = User.query.all()
    print(users)
    return render_template('/user/users.html', users = users)

@flask_app.route('/logout')
def logout():
    """Выход из системы"""  
    logout_user()
    return redirect(url_for('signin'))

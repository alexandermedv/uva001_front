from flask_login import current_user, login_required, login_user, logout_user
from flask import url_for, redirect, render_template, flash, request

from . import flask_app, db, login
from .forms import LoginForm, CreateUserForm
from .models import User

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
        print('email', form.email.data, 'password', form.password.data, 'remeber_me',form.remember_me.data)
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

@flask_app.route('/signup')
def signup():
    return render_template('/signup.html')

# Действия пользователя
@flask_app.route('/user/create_user', methods=['get', 'post'])
def create_user():
    """Создание пользователя"""
    form = CreateUserForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            email = form.email.data
            personnel_number = form.personnel_number.data
            family_name = form.family_name.data
            first_name = form.first_name.data
            second_name = form.second_name.data
            full_name = family_name + " " + first_name + " " + second_name
            dept_id = form.dept_id.data
            position = form.position.data
            role = form.role.data
            status = form.status.data
            password = form.password.data

            #password_hash = User.set_password(password)

            usr = User(personnel_number=personnel_number,
                            email= email,
                            full_name=full_name,
                            family_name=family_name,
                            first_name=first_name,
                            second_name=second_name,
                            dept_id=dept_id,
                            position=position,
                            role=role,
                            status=status
                            )
            usr.set_password(password)
            db.session.add(usr)

            # usr_set = User_settings(
            #     selected_audit=None
            # )
            # db.session.add(usr_set)
            db.session.commit()

            return 'Данные сохранены'
        else:
            message = 'Поля заполнены некорректно. Пожалуйста, проверьте введенные данные.'
            flash(message)
            return render_template('/user/create_user.html', form=form)

    return render_template('/user/create_user.html', title='create user', form=form)
    
@flask_app.route('/user')
@login_required
def account():
    """Личный кабинет"""
    if current_user.is_authenticated:
        user = { 'name': current_user.full_name,
                 'email': current_user.email,
                 'position': current_user.position}
    return render_template('account.html', title='account', user=user)

@flask_app.route('/logout')
def logout():
    """Выход из системы"""  
    logout_user()
    return redirect(url_for('signin'))

# Доступы по текущей сессии
@login.user_loader
def load_user(id):
    """Инициализация пользователя"""
    print(id)
    user = User.query.filter_by(email=id).first()
    print('user', user)
    return user
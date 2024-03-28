from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, InputRequired, Email, NumberRange, EqualTo
from wtforms.fields import DateField, EmailField
from wtforms.widgets import TextInput
from flask_security.forms import LoginForm

class LoginForm(FlaskForm):
    """Форма авторизации пользователя"""

    ldap_account = StringField('Аккаунт windows')
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
    
    # Неиспользуемые объекты
    email = StringField('E-mail')
    remember = BooleanField('Запомнить меня')
    next = StringField('Next')

class ProfileForm(FlaskForm):
    """Форма профиля пользователя"""
    login = StringField('Учетная запись', render_kw={'readonly': True})
    full_name = StringField('Полное имя', render_kw={'readonly': True})
    email = EmailField('Email', render_kw={'readonly': True})

    

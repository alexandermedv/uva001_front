from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, InputRequired, Email, NumberRange, EqualTo
from wtforms.fields.html5 import DateField, EmailField
from wtforms.widgets import TextInput

class LoginForm(FlaskForm):
    """Форма авторизации пользователя"""
    # email = StringField('E-mail', validators=[DataRequired()])
    ldap_account = StringField('Аккаунт windows')
    password = PasswordField('Пароль', validators=[DataRequired()])
    # Запоминать пароль не требуется
    # remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
class ProfileForm(FlaskForm):
    """Форма профиля пользователя"""
    login = StringField('Учетная запись', render_kw={'readonly': True})
    full_name = StringField('Полное имя', render_kw={'readonly': True})
    email = EmailField('Email', render_kw={'readonly': True})

    

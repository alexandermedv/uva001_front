from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, InputRequired, Email, NumberRange, EqualTo
from wtforms.fields.html5 import DateField, EmailField
from wtforms.widgets import TextInput

import front_ex.config as config 

class LoginForm(FlaskForm):
    """Форма авторизации пользователя"""
    # email = StringField('E-mail', validators=[DataRequired()])
    ldap_account = StringField('Аккаунт windows')
    password = PasswordField('Пароль', validators=[DataRequired()])
    # Запоминать пароль не требуется
    # remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class CreateUserForm(FlaskForm):
    """Форма создания пользователя"""
    email = EmailField('E-mail', validators=[DataRequired(), Email()], description="E-mail")
    family_name = StringField("Фамилия: ",
        validators=[InputRequired(message='Введите фамилию'),
        Length(min=1, max=100, message='Длина фамилии должна быть от 1 до 100.')], description="Фамилия")
    first_name = StringField("Имя: ",
        validators=[InputRequired(message='Введите имя'),
        Length(min=1, max=100, message='Длина имени должна быть от 1 до 100.')], description="Имя")
    second_name = StringField("Отчество: ",
        validators=[InputRequired(message='Введите отчество'),
        Length(min=1, max=100, message='Длина отчества должна быть от 1 до 100.')], description="Отчество")
    dept_id = StringField("Название подразделения: ",
        validators=[InputRequired(message='Введите название подразделения'),
        Length(min=1, max=100, message='''Название подразделения должно содержать от 1 до 100 символов.''')], description="Название подразделения")
    position = StringField("Позиция: ",
        validators=[InputRequired(message='Введите позицию'),
        Length(min=1, max=1000, message='Длина позиции должна быть от 1 до 1000.')], description="Должность")
    status = SelectField("Статус пользователя: ", choices = config.USER_STATUS,
        validators=[InputRequired(message='Выберите статус пользователя.')], description="Статус")
    password = PasswordField('Пароль',
        validators=[InputRequired(message='Введите пароль.'),
        Length(min=8, message='Длина пароля должна быть не менее 8 символов.'),
                            EqualTo('password_confirmation', message='Пароли не совпадают.')], description="Пароль")
    password_confirmation = PasswordField('Подтверждение пароля', validators=[DataRequired()], description="Подтверждение пароля")
    role = SelectField("Роль: ", choices = config.USER_ROLES,
        validators=[InputRequired(message='Выберите тип пользователя.')], description='Роль')
    submit = SubmitField("Создать")

class EditUserForm(FlaskForm):
    """Форма создания пользователя"""
    email = EmailField('E-mail', validators=[DataRequired(), Email()], description="E-mail")
    personnel_number = IntegerField("Табельный номер: ",
        validators=[InputRequired(message='Введите табельный номер.')], description="Табельный номер")
    family_name = StringField("Фамилия: ",
        validators=[InputRequired(message='Введите фамилию'),
        Length(min=1, max=100, message='Длина фамилии должна быть от 1 до 100.')], description="Фамилия")
    first_name = StringField("Имя: ",
        validators=[InputRequired(message='Введите имя'),
        Length(min=1, max=100, message='Длина имени должна быть от 1 до 100.')], description="Имя")
    second_name = StringField("Отчество: ",
        validators=[InputRequired(message='Введите отчество'),
        Length(min=1, max=100, message='Длина отчества должна быть от 1 до 100.')], description="Отчество")
    dept_id = StringField("Название подразделения: ",
        validators=[InputRequired(message='Введите название подразделения'),
        Length(min=1, max=100, message='''Название подразделения должно содержать от 1 до 100 символов.''')], description="Название подразделения")
    position = StringField("Позиция: ",
        validators=[InputRequired(message='Введите позицию'),
        Length(min=1, max=1000, message='Длина позиции должна быть от 1 до 1000.')], description="Должность")
    status = SelectField("Статус пользователя: ", choices = config.USER_STATUS,
        validators=[InputRequired(message='Выберите статус пользователя.')], description="Статус")
    role = SelectField("Роль: ", choices = config.USER_ROLES,
        validators=[InputRequired(message='Выберите тип пользователя.')], description='Роль')
    submit = SubmitField("Изменить")

class PasswordUserForm(FlaskForm):
    """Изменение пароля пользователя"""
    password = PasswordField('Пароль',
        validators=[InputRequired(message='Введите пароль'),
        Length(min=8, message='Длина пароля должна быть не менее 8 символов'),
                            EqualTo('password_confirmation', message='Пароли не совпадают.')], description="Пароль")
    password_confirmation = PasswordField('Подтверждение пароля', validators=[DataRequired()], description="Подтверждение пароля")
    submit = SubmitField("Изменить")
    cancel = SubmitField("Отмена", render_kw={'formnovalidate': True})

class ProfileForm(FlaskForm):
    """Форма профиля пользователя"""
    full_name = StringField('Полное имя', render_kw={'readonly': True})
    email = EmailField('Email', render_kw={'readonly': True})
    password = PasswordField('Пароль',
        validators=[InputRequired(message='Введите пароль.'),
        Length(min=8, message='Длина пароля должна быть не менее 8 символов.'),
                            EqualTo('password_confirmation', message='Пароли не совпадают.')], description="Пароль")
    password_confirmation = PasswordField('Подтверждение пароля', validators=[DataRequired()], description="Подтверждение пароля")
    change_password = SubmitField('Изменить пароль')

    

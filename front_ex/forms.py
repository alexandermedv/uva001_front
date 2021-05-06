from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, InputRequired, Email, NumberRange, EqualTo
from wtforms.fields.html5 import DateField, EmailField

"""Словари типов"""
USER_TYPE = ['Аудитор', 'Запчасти', 'ПКУ']
USER_STATUS = ['Активен', 'Неактивен']

class LoginForm(FlaskForm):
    """Форма авторизации пользователя"""
    # email = StringField('E-mail', validators=[DataRequired()])
    # password = PasswordField('Пароль', validators=[DataRequired()])
    email = StringField('E-mail')
    password = PasswordField('Пароль')
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class CreateUserForm(FlaskForm):
    """Форма создания пользователя"""
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    personnel_number = TextAreaField("Табельный номер: ",
        validators=[InputRequired(message='Введите табельный номер.')])
    family_name = StringField("Фамилия: ",
        validators=[InputRequired(message='Введите фамилию'),
        Length(min=1, max=100, message='Длина фамилии должна быть от 1 до 100.')])
    first_name = StringField("Имя: ",
        validators=[InputRequired(message='Введите имя'),
        Length(min=1, max=100, message='Длина имени должна быть от 1 до 100.')])
    second_name = StringField("Отчество: ",
        validators=[InputRequired(message='Введите отчество'),
        Length(min=1, max=100, message='Длина отчества должна быть от 1 до 100.')])
    dept_id = IntegerField("Код подразделения: ",
        validators=[InputRequired(message='Введите код подразделения'),
        NumberRange(min=1, max=1000, message='''Код подразделения должен быть в диапазоне от
             1 до 1000.''')])
    position = StringField("Позиция: ",
        validators=[InputRequired(message='Введите позицию'),
        Length(min=1, max=1000, message='Длина позиции должна быть от 1 до 1000.')])
    # type = SelectField("Тип пользователя: ", choices = USER_TYPE,
    #     validators=[InputRequired(message='Выберите тип пользователя.')])
    status = SelectField("Статус пользователя: ", choices = USER_STATUS,
        validators=[InputRequired(message='Выберите статус пользователя.')])
    password = PasswordField('Пароль',
        validators=[InputRequired(message='Введите пароль.'),
        Length(min=8, message='Длина пароля должна быть не менее 8 символов.'),
                            EqualTo('password_confirmation', message='Пароли не совпадают.')])
    password_confirmation = PasswordField('Подтверждение пароля', validators=[DataRequired()])
    submit = SubmitField("Создать")
    type = SelectField("Роль: ", choices = USER_STATUS,
         validators=[InputRequired(message='Выберите тип пользователя.')])
    

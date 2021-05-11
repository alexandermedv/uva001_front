from flask_wtf import FlaskForm
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, BooleanField
from wtforms import SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, InputRequired, Email, NumberRange, EqualTo
from wtforms.fields.html5 import DateField, EmailField
from functools import wraps

from . import db, login
from .config.html_roles import html_access_roles

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    # __table_args = {'schema':'ver1'}

    id = db.Column(db.Integer, primary_key=True)
    personnel_number = db.Column(db.Integer)
    full_name = db.Column(db.Unicode(1000))
    family_name = db.Column(db.Unicode(100))
    first_name = db.Column(db.Unicode(100))
    second_name = db.Column(db.Unicode(100))
    dept_id = db.Column(db.Integer)
    position = db.Column(db.Unicode(1000))
    email = db.Column('email', db.Unicode(100), nullable=False)
    status = db.Column(db.Unicode(100))
    password_hash = db.Column(db.Unicode(200))
    role = db.Column(db.String(100), default='guest')
    
    def __repr__(self):
        return '<User {}>'.format(self.full_name)
    
    # Модель подразумевает одну роль на один логин и много ролей на один роут
    def get_role(self, *args):
        return self.role
    
    def get_role_by_html_element(*args):
        print('args', args[1])
        if args:
            return html_access_roles.get(args[1])
        return []

    def to_json(self):
        return { "personnel_number": self.personnel_number,
            "full_name": self.full_name,
            "family_name": self.family_name,
            "first_name": self.first_name,
            "second_name": self.second_name,
            "dept_id": self.dept_id,
            "position": self.position,
            "email": self.email,
            # "type": self.type,
            "status": self.status, 
            "role": self.role}

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
	    self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
	    return check_password_hash(self.password_hash, password)

def requires_roles(*roles):
    """Проверка роли"""
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            print('get_role')
            if current_user.get_role(*args) not in roles:
                # Redirect the user to an unauthorized notice!
                return "Ваш аккаунт не имеет доступа к данной странице."
            return f(*args, **kwargs)
        return wrapped
    return wrapper
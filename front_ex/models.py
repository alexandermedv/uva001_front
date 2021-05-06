from flask_login import UserMixin, current_user
from . import db, login
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args = {'schema':'ver1'}

    id = db.Column(db.Integer, primary_key=True)
    personnel_number = db.Column(db.Integer)
    full_name = db.Column(db.Unicode(1000))
    family_name = db.Column(db.Unicode(100))
    first_name = db.Column(db.Unicode(100))
    second_name = db.Column(db.Unicode(100))
    dept_id = db.Column(db.Integer)
    position = db.Column(db.Unicode(1000))
    email = db.Column('email', db.Unicode(100), nullable=False)
    # type = db.Column(db.Unicode(100))
    status = db.Column(db.Unicode(100))
    password_hash = db.Column(db.Unicode(200))
    role = db.Column(db.String(100), default='guest')

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
        return str(self.email)

    def set_password(self, password):
	    self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
	    return check_password_hash(self.password_hash, password)

def requires_roles(*roles):
    """Проверка роли"""
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                # Redirect the user to an unauthorized notice!
                return "You are not authorized to access this page"
            return f(*args, **kwargs)
        return wrapped
    return wrapper
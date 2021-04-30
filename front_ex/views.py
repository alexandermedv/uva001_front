import flask
from . import flask_app

# Роутинг
@flask_app.route('/')
def main():
    return flask.render_template('index.html')

@flask_app.route('/limit_oper/')
# @login_required
def render_limit_oper():
    return flask.render_template('/limit_oper/overview.html')

@flask_app.route('/dashapp1/')
# @login_required
def render_dashapp1():
    return flask.render_template('/dashapp1/overview.html')

# Логирование пользователей и авторизация
@flask_app.route('/login')
def login():
    print('login')
    return flask.render_template('/login.html')

@flask_app.route('/signup')
def signup():
    return flask.render_template('/signup.html')

@flask_app.route('/logout')
def logout():
    return flask.render_template('/logout.html')

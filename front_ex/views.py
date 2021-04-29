import flask
from . import flask_app

# Роутинг
@flask_app.route('/')
def main():
    return flask.render_template('index.html')

@flask_app.route('/limit_oper/')
def render_limit_oper():
    return flask.render_template('/limit_oper/overview.html')

@flask_app.route('/dashapp1/')
def render_dashapp1():
    return flask.render_template('/dashapp1/overview.html')
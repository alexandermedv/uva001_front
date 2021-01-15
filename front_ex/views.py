import flask
from . import flask_app

# Роутинг
@flask_app.route('/')
def hello():
    return flask.render_template('index.html')

@flask_app.route('/limit_oper/')
def render_dashboard():
    return flask.render_template('/limit_oper/overview.html')

# @flask_app.route('/reports')
# def render_reports():
#     return flask.redirect('/dash2')